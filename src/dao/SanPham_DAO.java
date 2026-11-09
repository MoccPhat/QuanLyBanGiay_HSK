package dao;

import connectDB.ConnectDB;
import entity.NhanVien;
import entity.SanPham;

import java.sql.*;
import java.util.ArrayList;

/**
 * Lớp truy xuất và thao tác dữ liệu (tầng DAO) cho Sản phẩm trong CSDL SQL Server,
 * quản lý danh mục sản phẩm, ràng buộc giá bán/giá nhập, xóa mềm và tìm kiếm nâng cao.
 */
public class SanPham_DAO {

    private String lastError = "";

    /**
     * Lấy thông báo lỗi gần nhất phát sinh khi thực thi các thao tác cơ sở dữ liệu.
     *
     * @return chuỗi mô tả lỗi gần nhất
     */
    public String getLastError() {
        return lastError;
    }

    /**
     * Phân tích mã lỗi SQLException từ SQL Server để chuyển thành thông báo lỗi tiếng Việt thân thiện với người dùng.
     *
     * @param e ngoại lệ SQLException phát sinh từ hệ quản trị CSDL
     */
    private void handleSQLException(SQLException e) {
        int code = e.getErrorCode();
        String msg = e.getMessage();
        if (code == 2627 || code == 2601) {
            lastError = "Mã sản phẩm đã tồn tại trong hệ thống!";
        } else if (code == 547) {
            if (msg != null && msg.contains("CK_SanPham_ma")) {
                lastError = "Mã sản phẩm không đúng định dạng (SPxxxx)!";
            } else if (msg != null && msg.contains("CK_SanPham_giaNhap")) {
                lastError = "Giá nhập phải lớn hơn 0!";
            } else if (msg != null && msg.contains("CK_SanPham_giaBan")) {
                lastError = "Giá bán niêm yết phải lớn hơn hoặc bằng giá nhập!";
            } else if (msg != null && msg.contains("CK_SanPham_ten")) {
                lastError = "Tên sản phẩm không được để trống!";
            } else {
                lastError = "Dữ liệu không thỏa mãn ràng buộc CSDL: " + msg;
            }
        } else {
            lastError = "Không kết nối được CSDL (" + code + "): " + msg;
        }
    }

    /**
     * Mở hoặc tái sử dụng kết nối CSDL từ ConnectDB Singleton.
     *
     * @return đối tượng Connection đang kết nối
     * @throws SQLException khi không thể thiết lập kết nối cơ sở dữ liệu
     */
    private Connection getConnection() throws SQLException {
        ConnectDB.getInstance();
        Connection con = ConnectDB.getConnection();
        if (con == null || con.isClosed()) {
            ConnectDB.getInstance().connect();
            con = ConnectDB.getConnection();
        }
        return con;
    }

    /**
     * Lấy danh sách toàn bộ sản phẩm đang kinh doanh (trangThai = 1), sắp xếp tăng dần theo mã sản phẩm.
     *
     * @return danh sách các đối tượng SanPham
     */
    public ArrayList<SanPham> getAllSanPham() {
        ArrayList<SanPham> ds = new ArrayList<>();
        try {
            Connection con = getConnection();
            String sql = "SELECT * FROM SanPham WHERE trangThai = 1 ORDER BY maSanPham ASC";
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    String maSP = rs.getString("maSanPham");
                    String tenSP = rs.getString("tenSanPham");
                    String loai = rs.getString("loaiGiay");
                    String hang = rs.getString("thuongHieu");
                    double giaNhap = rs.getDouble("giaNhap");
                    double giaBan = rs.getDouble("giaBan");
                    String chatLieu = rs.getString("chatLieu");
                    boolean trangThai = rs.getBoolean("trangThai");

                    SanPham sp = new SanPham(maSP, tenSP, loai, hang, giaNhap, giaBan, chatLieu, trangThai);
                    ds.add(sp);
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Tìm kiếm và lấy thông tin chi tiết của một sản phẩm theo mã định danh.
     *
     * @param maSP mã sản phẩm cần tìm kiếm
     * @return đối tượng SanPham nếu tìm thấy, null nếu không tồn tại
     */
    public SanPham getSanPhamTheoMa(String maSP) {
        SanPham sp = null;
        try {
            Connection con = getConnection();
            String sql = "SELECT * FROM SanPham WHERE maSanPham = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maSP);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        String tenSP = rs.getString("tenSanPham");
                        String loai = rs.getString("loaiGiay");
                        String hang = rs.getString("thuongHieu");
                        double giaNhap = rs.getDouble("giaNhap");
                        double giaBan = rs.getDouble("giaBan");
                        String chatLieu = rs.getString("chatLieu");
                        boolean trangThai = rs.getBoolean("trangThai");

                        sp = new SanPham(maSP, tenSP, loai, hang, giaNhap, giaBan, chatLieu, trangThai);
                    }
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return sp;
    }

    /**
     * Kiểm tra mã sản phẩm đã tồn tại trong CSDL hay chưa để chống trùng khóa chính.
     *
     * @param maSP mã sản phẩm cần kiểm tra
     * @return true nếu mã đã tồn tại, ngược lại false
     */
    public boolean kiemTraTrungMa(String maSP) {
        String sql = "SELECT 1 FROM SanPham WHERE maSanPham = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maSP);
                try (ResultSet rs = pstmt.executeQuery()) {
                    return rs.next();
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return false;
    }

    /**
     * Thêm mới một sản phẩm vào CSDL có kiểm tra quyền Quản lý của người gọi.
     *
     * @param sp đối tượng SanPham chứa thông tin cần thêm mới
     * @param caller đối tượng NhanVien đại diện cho người gọi thao tác (phải là Quản lý)
     * @return true nếu thêm thành công, ngược lại false
     */
    public boolean themSanPham(SanPham sp, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền thêm sản phẩm!";
            return false;
        }
        int n = 0;
        try {
            Connection con = getConnection();
            String sql = "INSERT INTO SanPham (maSanPham, tenSanPham, loaiGiay, thuongHieu, giaNhap, giaBan, chatLieu, trangThai) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, sp.getMaSanPham());
                pstmt.setString(2, sp.getTenSanPham());
                pstmt.setString(3, sp.getLoaiGiay());
                pstmt.setString(4, sp.getThuongHieu());
                pstmt.setDouble(5, sp.getGiaNhap());
                pstmt.setDouble(6, sp.getGiaBan());

                if (sp.getChatLieu() == null || sp.getChatLieu().trim().isEmpty()) {
                    pstmt.setNull(7, Types.NVARCHAR);
                } else {
                    pstmt.setString(7, sp.getChatLieu().trim());
                }

                pstmt.setBoolean(8, sp.isTrangThai());
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Thêm mới một sản phẩm vào CSDL (phiên bản không truyền người gọi thao tác).
     *
     * @param sp đối tượng SanPham chứa thông tin cần thêm mới
     * @return true nếu thêm thành công, ngược lại false
     */
    public boolean themSanPham(SanPham sp) {
        return themSanPham(sp, null);
    }

    /**
     * Cập nhật thông tin chi tiết của sản phẩm có kiểm tra quyền Quản lý của người gọi.
     *
     * @param sp đối tượng SanPham chứa thông tin cập nhật mới
     * @param caller đối tượng NhanVien đại diện cho người gọi thao tác (phải là Quản lý)
     * @return true nếu cập nhật thành công, ngược lại false
     */
    public boolean capNhatSanPham(SanPham sp, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền cập nhật sản phẩm!";
            return false;
        }
        int n = 0;
        try {
            Connection con = getConnection();
            String sql = "UPDATE SanPham SET tenSanPham = ?, loaiGiay = ?, thuongHieu = ?, giaNhap = ?, giaBan = ?, chatLieu = ? WHERE maSanPham = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, sp.getTenSanPham());
                pstmt.setString(2, sp.getLoaiGiay());
                pstmt.setString(3, sp.getThuongHieu());
                pstmt.setDouble(4, sp.getGiaNhap());
                pstmt.setDouble(5, sp.getGiaBan());

                if (sp.getChatLieu() == null || sp.getChatLieu().trim().isEmpty()) {
                    pstmt.setNull(6, Types.NVARCHAR);
                } else {
                    pstmt.setString(6, sp.getChatLieu().trim());
                }

                pstmt.setString(7, sp.getMaSanPham());
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Cập nhật thông tin chi tiết của sản phẩm (phiên bản không truyền người gọi thao tác).
     *
     * @param sp đối tượng SanPham chứa thông tin cập nhật mới
     * @return true nếu cập nhật thành công, ngược lại false
     */
    public boolean capNhatSanPham(SanPham sp) {
        return capNhatSanPham(sp, null);
    }

    /**
     * Xóa mềm sản phẩm bằng cách chuyển trangThai = 0 có kiểm tra quyền Quản lý.
     *
     * @param maSP mã sản phẩm cần xóa mềm
     * @param caller đối tượng NhanVien đại diện cho người gọi thao tác (phải là Quản lý)
     * @return true nếu xóa mềm thành công, ngược lại false
     */
    public boolean xoaSanPham(String maSP, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền xóa sản phẩm!";
            return false;
        }
        int n = 0;
        try {
            Connection con = getConnection();
            // Xóa mềm: Chuyển trangThai = 0
            String sql = "UPDATE SanPham SET trangThai = 0 WHERE maSanPham = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maSP);
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Xóa mềm sản phẩm bằng cách chuyển trangThai = 0 (phiên bản không truyền người gọi thao tác).
     *
     * @param maSP mã sản phẩm cần xóa mềm
     * @return true nếu xóa mềm thành công, ngược lại false
     */
    public boolean xoaSanPham(String maSP) {
        return xoaSanPham(maSP, null);
    }

    /**
     * Lấy danh sách tất cả các thương hiệu giày hiện có trong CSDL (phục vụ lọc nâng cao).
     *
     * @return danh sách các chuỗi tên thương hiệu
     */
    public ArrayList<String> getAllThuongHieu() {
        ArrayList<String> ds = new ArrayList<>();
        String sql = "SELECT DISTINCT thuongHieu FROM SanPham WHERE thuongHieu IS NOT NULL AND thuongHieu <> '' ORDER BY thuongHieu ASC";
        try {
            Connection con = getConnection();
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    ds.add(rs.getString("thuongHieu"));
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Lấy danh sách tất cả các phân loại giày hiện có trong CSDL (phục vụ lọc nâng cao).
     *
     * @return danh sách các chuỗi phân loại giày
     */
    public ArrayList<String> getAllLoaiGiay() {
        ArrayList<String> ds = new ArrayList<>();
        String sql = "SELECT DISTINCT loaiGiay FROM SanPham WHERE loaiGiay IS NOT NULL AND loaiGiay <> '' ORDER BY loaiGiay ASC";
        try {
            Connection con = getConnection();
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    ds.add(rs.getString("loaiGiay"));
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Tìm kiếm nâng cao sản phẩm theo nhiều tiêu chí kết hợp:
     * Thương hiệu, khoảng giá bán (từ - đến), loại giày, tình trạng còn hàng/ngừng bán.
     *
     * @param thuongHieu thương hiệu giày cần lọc (hoặc 'Tất cả')
     * @param giaTu mức giá bán tối thiểu (hoặc null nếu không giới hạn)
     * @param giaDen mức giá bán tối đa (hoặc null nếu không giới hạn)
     * @param loaiGiay loại giày cần lọc (hoặc 'Tất cả')
     * @param conHang tình trạng còn hàng (true: chỉ lấy sản phẩm còn hàng tồn kho, false: hết hàng hoặc ngừng bán, null: Tất cả)
     * @return danh sách các đối tượng SanPham thỏa mãn điều kiện lọc
     */
    public ArrayList<SanPham> timKiemNangCao(String thuongHieu, Double giaTu, Double giaDen, String loaiGiay, Boolean conHang) {
        ArrayList<SanPham> ds = new ArrayList<>();
        StringBuilder sql = new StringBuilder("SELECT sp.* FROM SanPham sp WHERE 1=1 ");
        ArrayList<Object> params = new ArrayList<>();

        if (thuongHieu != null && !thuongHieu.trim().isEmpty() && !thuongHieu.equalsIgnoreCase("Tất cả")) {
            sql.append("AND sp.thuongHieu = ? ");
            params.add(thuongHieu.trim());
        }

        if (giaTu != null && giaTu >= 0) {
            sql.append("AND sp.giaBan >= ? ");
            params.add(giaTu);
        }

        if (giaDen != null && giaDen >= 0) {
            sql.append("AND sp.giaBan <= ? ");
            params.add(giaDen);
        }

        if (loaiGiay != null && !loaiGiay.trim().isEmpty() && !loaiGiay.equalsIgnoreCase("Tất cả")) {
            sql.append("AND sp.loaiGiay = ? ");
            params.add(loaiGiay.trim());
        }

        if (conHang != null) {
            if (conHang) {
                sql.append("AND sp.trangThai = 1 AND EXISTS (SELECT 1 FROM ChiTietGiay ctg WHERE ctg.maSanPham = sp.maSanPham AND ctg.soLuongTon > 0) ");
            } else {
                sql.append("AND (sp.trangThai = 0 OR NOT EXISTS (SELECT 1 FROM ChiTietGiay ctg WHERE ctg.maSanPham = sp.maSanPham AND ctg.soLuongTon > 0)) ");
            }
        }

        sql.append("ORDER BY sp.maSanPham ASC");

        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql.toString())) {
                for (int i = 0; i < params.size(); i++) {
                    Object p = params.get(i);
                    if (p instanceof String) {
                        pstmt.setString(i + 1, (String) p);
                    } else if (p instanceof Double) {
                        pstmt.setDouble(i + 1, (Double) p);
                    }
                }

                try (ResultSet rs = pstmt.executeQuery()) {
                    while (rs.next()) {
                        String maSP = rs.getString("maSanPham");
                        String tenSP = rs.getString("tenSanPham");
                        String loai = rs.getString("loaiGiay");
                        String hang = rs.getString("thuongHieu");
                        double giaNhap = rs.getDouble("giaNhap");
                        double giaBan = rs.getDouble("giaBan");
                        String chatLieu = rs.getString("chatLieu");
                        boolean trangThai = rs.getBoolean("trangThai");

                        ds.add(new SanPham(maSP, tenSP, loai, hang, giaNhap, giaBan, chatLieu, trangThai));
                    }
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return ds;
    }
}

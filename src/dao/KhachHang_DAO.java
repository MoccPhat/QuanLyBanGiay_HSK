package dao;

import connectDB.ConnectDB;
import entity.KhachHang;
import entity.NhanVien;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;

/**
 * Lớp truy xuất và thao tác dữ liệu (tầng DAO) cho Khách hàng trong CSDL SQL Server,
 * quản lý thông tin khách hàng, tích điểm, phân hạng thành viên và tìm kiếm nâng cao.
 */
public class KhachHang_DAO {
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
     * Lấy danh sách toàn bộ khách hàng trong hệ thống, sắp xếp tăng dần theo mã khách hàng.
     *
     * @return danh sách các đối tượng KhachHang
     */
    public ArrayList<KhachHang> getAllKhachHang() {
        ArrayList<KhachHang> ds = new ArrayList<>();
        String sql = "SELECT * FROM KhachHang ORDER BY maKhachHang ASC";
        try {
            Connection con = getConnection();
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    String maKH = rs.getString("maKhachHang");
                    String hoTen = rs.getString("hoTen");
                    String sdt = rs.getString("soDienThoai");
                    Date ns = rs.getDate("ngaySinh");
                    LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : null;
                    boolean gioiTinh = rs.getBoolean("gioiTinh");
                    String diaChi = rs.getString("diaChi");
                    String email = rs.getString("email");
                    int diem = rs.getInt("diemTichLuy");
                    String hang = rs.getString("hangThanhVien");

                    KhachHang kh = new KhachHang(maKH, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, diem, hang);
                    ds.add(kh);
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Tìm kiếm khách hàng theo số điện thoại chính xác.
     *
     * @param sdt số điện thoại của khách hàng cần tìm
     * @return đối tượng KhachHang tương ứng hoặc null nếu không tìm thấy
     */
    public KhachHang timTheoSoDienThoai(String sdt) {
        KhachHang kh = null;
        String sql = "SELECT * FROM KhachHang WHERE soDienThoai = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, sdt);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        String maKH = rs.getString("maKhachHang");
                        String hoTen = rs.getString("hoTen");
                        Date ns = rs.getDate("ngaySinh");
                        LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : null;
                        boolean gioiTinh = rs.getBoolean("gioiTinh");
                        String diaChi = rs.getString("diaChi");
                        String email = rs.getString("email");
                        int diem = rs.getInt("diemTichLuy");
                        String hang = rs.getString("hangThanhVien");

                        kh = new KhachHang(maKH, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, diem, hang);
                    }
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return kh;
    }

    /**
     * Tìm kiếm khách hàng theo mã định danh duy nhất.
     *
     * @param maKH mã khách hàng cần tìm kiếm
     * @return đối tượng KhachHang tương ứng hoặc null nếu không tìm thấy
     */
    public KhachHang getKhachHangTheoMa(String maKH) {
        KhachHang kh = null;
        String sql = "SELECT * FROM KhachHang WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maKH);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        String hoTen = rs.getString("hoTen");
                        String sdt = rs.getString("soDienThoai");
                        Date ns = rs.getDate("ngaySinh");
                        LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : null;
                        boolean gioiTinh = rs.getBoolean("gioiTinh");
                        String diaChi = rs.getString("diaChi");
                        String email = rs.getString("email");
                        int diem = rs.getInt("diemTichLuy");
                        String hang = rs.getString("hangThanhVien");

                        kh = new KhachHang(maKH, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, diem, hang);
                    }
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return kh;
    }

    /**
     * Kiểm tra mã khách hàng đã tồn tại trong CSDL hay chưa để chống trùng khóa chính.
     *
     * @param maKH mã khách hàng cần kiểm tra
     * @return true nếu mã đã tồn tại, ngược lại false
     */
    public boolean kiemTraTrungMa(String maKH) {
        String sql = "SELECT 1 FROM KhachHang WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maKH);
                try (ResultSet rs = pstmt.executeQuery()) {
                    return rs.next();
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return false;
    }

    /**
     * Kiểm tra số điện thoại khách hàng đã tồn tại trong CSDL hay chưa.
     *
     * @param sdt số điện thoại cần kiểm tra
     * @return true nếu số điện thoại đã tồn tại, ngược lại false
     */
    public boolean kiemTraTrungSDT(String sdt) {
        return kiemTraTrungSDT(sdt, null);
    }

    /**
     * Kiểm tra số điện thoại khách hàng đã tồn tại hay chưa (loại trừ mã khách hàng đang cập nhật).
     *
     * @param sdt số điện thoại cần kiểm tra
     * @param maKHExclude mã khách hàng cần loại trừ khỏi phạm vi kiểm tra trùng
     * @return true nếu số điện thoại bị trùng lặp, ngược lại false
     */
    public boolean kiemTraTrungSDT(String sdt, String maKHExclude) {
        boolean coExclude = (maKHExclude != null && !maKHExclude.trim().isEmpty());
        String sql = "SELECT 1 FROM KhachHang WHERE soDienThoai = ?" + (coExclude ? " AND maKhachHang <> ?" : "");
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, sdt);
                if (coExclude) {
                    pstmt.setString(2, maKHExclude.trim());
                }
                try (ResultSet rs = pstmt.executeQuery()) {
                    return rs.next();
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return false;
    }

    /**
     * Thêm mới một khách hàng vào CSDL.
     *
     * @param kh đối tượng KhachHang chứa thông tin cần thêm mới
     * @return true nếu thêm thành công, ngược lại false
     */
    public boolean themKhachHang(KhachHang kh) {
        lastError = "";
        int n = 0;
        String sql = "INSERT INTO KhachHang (maKhachHang, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, diemTichLuy, hangThanhVien) " +
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, kh.getMaKhachHang());
                pstmt.setString(2, kh.getHoTen());
                pstmt.setString(3, kh.getSoDienThoai());
                pstmt.setDate(4, (kh.getNgaySinh() != null) ? Date.valueOf(kh.getNgaySinh()) : null);
                pstmt.setBoolean(5, kh.isGioiTinh());
                
                if (kh.getDiaChi() != null && !kh.getDiaChi().trim().isEmpty()) {
                    pstmt.setString(6, kh.getDiaChi().trim());
                } else {
                    pstmt.setNull(6, Types.NVARCHAR);
                }

                if (kh.getEmail() != null && !kh.getEmail().trim().isEmpty()) {
                    pstmt.setString(7, kh.getEmail().trim());
                } else {
                    pstmt.setNull(7, Types.VARCHAR);
                }

                pstmt.setInt(8, kh.getDiemTichLuy());
                pstmt.setString(9, kh.getHangThanhVien());

                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Cập nhật thông tin cá nhân của khách hàng (họ tên, sđt, ngày sinh, giới tính, địa chỉ, email).
     *
     * @param kh đối tượng KhachHang chứa thông tin cập nhật mới
     * @return true nếu cập nhật thành công, ngược lại false
     */
    public boolean capNhatKhachHang(KhachHang kh) {
        lastError = "";
        int n = 0;
        String sql = "UPDATE KhachHang SET hoTen = ?, soDienThoai = ?, ngaySinh = ?, gioiTinh = ?, diaChi = ?, email = ? WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, kh.getHoTen());
                pstmt.setString(2, kh.getSoDienThoai());
                pstmt.setDate(3, (kh.getNgaySinh() != null) ? Date.valueOf(kh.getNgaySinh()) : null);
                pstmt.setBoolean(4, kh.isGioiTinh());
                if (kh.getDiaChi() != null && !kh.getDiaChi().trim().isEmpty()) {
                    pstmt.setString(5, kh.getDiaChi().trim());
                } else {
                    pstmt.setNull(5, Types.NVARCHAR);
                }
                if (kh.getEmail() != null && !kh.getEmail().trim().isEmpty()) {
                    pstmt.setString(6, kh.getEmail().trim());
                } else {
                    pstmt.setNull(6, Types.VARCHAR);
                }
                pstmt.setString(7, kh.getMaKhachHang());
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Xóa khách hàng khỏi hệ thống có kiểm tra quyền Quản lý và chặn xóa nếu khách đã có lịch sử hóa đơn.
     *
     * @param maKH mã khách hàng cần xóa
     * @param caller đối tượng NhanVien đại diện cho người gọi thao tác (phải là Quản lý)
     * @return true nếu xóa thành công, ngược lại false
     */
    public boolean xoaKhachHang(String maKH, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền xóa khách hàng!";
            return false;
        }
        try {
            Connection con = getConnection();
            String checkSql = "SELECT COUNT(*) FROM HoaDon WHERE maKhachHang = ?";
            try (PreparedStatement checkStmt = con.prepareStatement(checkSql)) {
                checkStmt.setString(1, maKH);
                try (ResultSet rs = checkStmt.executeQuery()) {
                    if (rs.next() && rs.getInt(1) > 0) {
                        lastError = "Khách đã có lịch sử hóa đơn, không thể xóa";
                        return false;
                    }
                }
            }
            String sql = "DELETE FROM KhachHang WHERE maKhachHang = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maKH);
                return pstmt.executeUpdate() > 0;
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Xóa khách hàng khỏi hệ thống (phiên bản không truyền người gọi thao tác).
     *
     * @param maKH mã khách hàng cần xóa
     * @return true nếu xóa thành công, ngược lại false
     */
    public boolean xoaKhachHang(String maKH) {
        return xoaKhachHang(maKH, null);
    }

    /**
     * Tự động sinh mã khách hàng mới có dạng KHxxxx tăng dần liên tục và an toàn khi đồng thời truy cập.
     *
     * @return chuỗi mã khách hàng mới được sinh ra
     */
    public String sinhMaKhachHangMoi() {
        try {
            Connection con = getConnection();
            String sql = "SELECT ISNULL(MAX(CAST(SUBSTRING(maKhachHang, 3, 4) AS INT)), 0) + 1 AS nextId FROM KhachHang WITH (UPDLOCK, HOLDLOCK) WHERE maKhachHang LIKE 'KH[0-9][0-9][0-9][0-9]'";
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery(sql)) {
                if (rs.next()) {
                    return String.format("KH%04d", rs.getInt("nextId"));
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return String.format("KH%04d", Math.abs(System.currentTimeMillis() % 10000));
    }

    /**
     * Tìm kiếm nâng cao khách hàng theo nhiều tiêu chí kết hợp:
     * Hạng thành viên, khoảng điểm tích lũy (từ - đến), giới tính.
     *
     * @param hangThanhVien tên hạng thành viên cần lọc (hoặc 'Tất cả')
     * @param diemTu mức điểm tích lũy tối thiểu (hoặc null nếu không giới hạn)
     * @param diemDen mức điểm tích lũy tối đa (hoặc null nếu không giới hạn)
     * @param gioiTinh giới tính cần lọc (true: Nam, false: Nữ, null: Tất cả)
     * @return danh sách các đối tượng KhachHang thỏa mãn tiêu chuẩn lọc
     */
    public ArrayList<KhachHang> timKiemNangCao(String hangThanhVien, Integer diemTu, Integer diemDen, Boolean gioiTinh) {
        ArrayList<KhachHang> ds = new ArrayList<>();
        StringBuilder sql = new StringBuilder("SELECT * FROM KhachHang WHERE 1=1 ");
        ArrayList<Object> params = new ArrayList<>();

        if (hangThanhVien != null && !hangThanhVien.trim().isEmpty() && !hangThanhVien.equalsIgnoreCase("Tất cả")) {
            sql.append("AND hangThanhVien = ? ");
            params.add(hangThanhVien.trim());
        }

        if (diemTu != null && diemTu >= 0) {
            sql.append("AND diemTichLuy >= ? ");
            params.add(diemTu);
        }

        if (diemDen != null && diemDen >= 0) {
            sql.append("AND diemTichLuy <= ? ");
            params.add(diemDen);
        }

        if (gioiTinh != null) {
            sql.append("AND gioiTinh = ? ");
            params.add(gioiTinh);
        }

        sql.append("ORDER BY diemTichLuy DESC, maKhachHang ASC");

        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql.toString())) {
                for (int i = 0; i < params.size(); i++) {
                    Object p = params.get(i);
                    if (p instanceof String) {
                        pstmt.setString(i + 1, (String) p);
                    } else if (p instanceof Integer) {
                        pstmt.setInt(i + 1, (Integer) p);
                    } else if (p instanceof Boolean) {
                        pstmt.setBoolean(i + 1, (Boolean) p);
                    }
                }

                try (ResultSet rs = pstmt.executeQuery()) {
                    while (rs.next()) {
                        String maKH = rs.getString("maKhachHang");
                        String hoTen = rs.getString("hoTen");
                        String sdt = rs.getString("soDienThoai");
                        Date ns = rs.getDate("ngaySinh");
                        LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : null;
                        boolean gt = rs.getBoolean("gioiTinh");
                        String diaChi = rs.getString("diaChi");
                        String email = rs.getString("email");
                        int diem = rs.getInt("diemTichLuy");
                        String hang = rs.getString("hangThanhVien");

                        ds.add(new KhachHang(maKH, hoTen, sdt, ngaySinh, gt, diaChi, email, diem, hang));
                    }
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }
}

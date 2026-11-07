package dao;

import connectDB.ConnectDB;
import entity.KhachHang;
import entity.NhanVien;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;

public class KhachHang_DAO {
    private String lastError = "";

    public String getLastError() {
        return lastError;
    }

    private Connection getConnection() throws SQLException {
        ConnectDB.getInstance();
        Connection con = ConnectDB.getConnection();
        if (con == null || con.isClosed()) {
            ConnectDB.getInstance().connect();
            con = ConnectDB.getConnection();
        }
        return con;
    }

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

    public boolean kiemTraTrungSDT(String sdt) {
        return kiemTraTrungSDT(sdt, null);
    }

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

    public boolean capNhatDiem(String maKH, int diemMoi, String hangMoi) {
        lastError = "";
        int n = 0;
        String sql = "UPDATE KhachHang SET diemTichLuy = ?, hangThanhVien = ? WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setInt(1, diemMoi);
                pstmt.setString(2, hangMoi);
                pstmt.setString(3, maKH);
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Cập nhật thông tin khách hàng (L12):
     * Bổ sung ngaySinh, gioiTinh, email vào câu UPDATE để không bị mất dữ liệu.
     * Bỏ cập nhật hangThanhVien từ form (hạng thành viên tự tính theo điểm tích lũy).
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
     * Xóa khách hàng (L13 & L14):
     * - Kiểm tra quyền Quản lý ở tầng DAO (L14).
     * - Kiểm tra lịch sử hóa đơn: nếu đã có hóa đơn -> chặn xóa và trả về thông báo thân thiện (L13).
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

    public boolean xoaKhachHang(String maKH) {
        return xoaKhachHang(maKH, null);
    }

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

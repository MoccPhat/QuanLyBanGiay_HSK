package dao;

import connectDB.ConnectDB;
import entity.NhanVien;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;

public class NhanVien_DAO {

    private String lastError = "";

    public String getLastError() {
        return lastError;
    }

    private void handleSQLException(SQLException e) {
        int code = e.getErrorCode();
        String msg = e.getMessage();
        if (code == 2627 || code == 2601) {
            if (msg != null && msg.contains("UQ_NhanVien_soDienThoai")) {
                lastError = "Số điện thoại này đã được sử dụng bởi nhân viên khác!";
            } else if (msg != null && msg.contains("PK_NhanVien")) {
                lastError = "Mã nhân viên đã tồn tại trong hệ thống!";
            } else {
                lastError = "Dữ liệu bị trùng lặp khóa chính hoặc duy nhất!";
            }
        } else if (code == 547) {
            if (msg != null && msg.contains("CK_NhanVien_ma")) {
                lastError = "Mã nhân viên không đúng định dạng (NVxxxx)!";
            } else if (msg != null && msg.contains("CK_NhanVien_sdt")) {
                lastError = "Số điện thoại không hợp lệ (10 số, bắt đầu bằng 03, 05, 07, 08, 09)!";
            } else if (msg != null && msg.contains("CK_NhanVien_email")) {
                lastError = "Email không đúng định dạng!";
            } else if (msg != null && msg.contains("CK_NhanVien_tuoi")) {
                lastError = "Nhân viên phải từ 18 tuổi trở lên";
            } else if (msg != null && msg.contains("CK_NhanVien_chucVu")) {
                lastError = "Chức vụ không hợp lệ (Quản lý hoặc Nhân viên bán hàng)!";
            } else if (msg != null && msg.contains("CK_NhanVien_ca")) {
                lastError = "Ca làm việc không hợp lệ (Ca sáng, Ca chiều, Ca tối, Toàn thời gian)!";
            } else if (msg != null && msg.contains("CK_NhanVien_luong")) {
                lastError = "Lương cơ bản phải lớn hơn 0!";
            } else if (msg != null && msg.contains("CK_NhanVien_matKhau")) {
                lastError = "Mật khẩu chưa được băm chuẩn SHA-256 (64 ký tự)!";
            } else {
                lastError = "Dữ liệu không thỏa mãn ràng buộc CSDL: " + msg;
            }
        } else {
            lastError = "Không kết nối được CSDL (" + code + "): " + msg;
        }
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

    public ArrayList<NhanVien> getAllNhanVien() {
        ArrayList<NhanVien> ds = new ArrayList<>();
        try {
            Connection con = getConnection();
            String sql = "SELECT * FROM NhanVien WHERE trangThai = 1 ORDER BY maNhanVien ASC";
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    String maNV = rs.getString("maNhanVien");
                    String hoTen = rs.getString("hoTen");
                    String sdt = rs.getString("soDienThoai");
                    Date ns = rs.getDate("ngaySinh");
                    LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : LocalDate.of(2000, 1, 1);
                    boolean gioiTinh = rs.getBoolean("gioiTinh");
                    String diaChi = rs.getString("diaChi");
                    String email = rs.getString("email");
                    String chucVu = rs.getString("chucVu");
                    double luong = rs.getDouble("luongCoBan");
                    String ca = rs.getString("caLamViec");
                    String matKhau = rs.getString("matKhau");
                    boolean trangThai = rs.getBoolean("trangThai");

                    NhanVien nv = new NhanVien(maNV, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, chucVu, luong, ca, matKhau, trangThai);
                    ds.add(nv);
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return ds;
    }

    public String hashSHA256(String input) {
        try {
            java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(input.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Xác thực đăng nhập (L10):
     * Phân biệt rõ ràng 3 trường hợp khi thất bại:
     * 1. Không tìm thấy mã nhân viên (hoặc tài khoản bị ngừng hoạt động).
     * 2. Mật khẩu không chính xác.
     * 3. Lỗi kết nối CSDL hoặc ngoại lệ hệ thống.
     */
    public NhanVien dangNhap(String maNV, String matKhau) {
        lastError = "";
        NhanVien nv = null;
        try {
            Connection con = getConnection();
            String sql = "SELECT * FROM NhanVien WHERE maNhanVien = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maNV);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        boolean trangThai = rs.getBoolean("trangThai");
                        if (!trangThai) {
                            lastError = "Tài khoản nhân viên '" + maNV + "' đã bị vô hiệu hóa hoặc ngừng hoạt động!";
                            return null;
                        }
                        String dbHash = rs.getString("matKhau");
                        String inputHash = hashSHA256(matKhau);

                        if (inputHash.equalsIgnoreCase(dbHash)) {
                            String hoTen = rs.getString("hoTen");
                            String sdt = rs.getString("soDienThoai");
                            Date ns = rs.getDate("ngaySinh");
                            LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : LocalDate.of(2000, 1, 1);
                            boolean gioiTinh = rs.getBoolean("gioiTinh");
                            String diaChi = rs.getString("diaChi");
                            String email = rs.getString("email");
                            String chucVu = rs.getString("chucVu");
                            double luong = rs.getDouble("luongCoBan");
                            String ca = rs.getString("caLamViec");

                            nv = new NhanVien(maNV, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, chucVu, luong, ca, dbHash, trangThai);
                        } else {
                            lastError = "Mật khẩu không chính xác!";
                            return null;
                        }
                    } else {
                        lastError = "Không tìm thấy tài khoản nhân viên '" + maNV + "'!";
                        return null;
                    }
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return nv;
    }

    public NhanVien getNhanVienTheoMa(String maNV) {
        NhanVien nv = null;
        try {
            Connection con = getConnection();
            String sql = "SELECT * FROM NhanVien WHERE maNhanVien = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maNV);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        String hoTen = rs.getString("hoTen");
                        String sdt = rs.getString("soDienThoai");
                        Date ns = rs.getDate("ngaySinh");
                        LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : LocalDate.of(2000, 1, 1);
                        boolean gioiTinh = rs.getBoolean("gioiTinh");
                        String diaChi = rs.getString("diaChi");
                        String email = rs.getString("email");
                        String chucVu = rs.getString("chucVu");
                        double luong = rs.getDouble("luongCoBan");
                        String ca = rs.getString("caLamViec");
                        String matKhau = rs.getString("matKhau");
                        boolean trangThai = rs.getBoolean("trangThai");

                        nv = new NhanVien(maNV, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, chucVu, luong, ca, matKhau, trangThai);
                    }
                }
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return nv;
    }

    public boolean kiemTraTrungMa(String maNV) {
        String sql = "SELECT 1 FROM NhanVien WHERE maNhanVien = ?";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maNV);
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

    public boolean kiemTraTrungSDT(String sdt, String maNVExclude) {
        boolean coExclude = (maNVExclude != null && !maNVExclude.trim().isEmpty());
        String sql = "SELECT 1 FROM NhanVien WHERE soDienThoai = ?" + (coExclude ? " AND maNhanVien <> ?" : "");
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, sdt);
                if (coExclude) {
                    pstmt.setString(2, maNVExclude.trim());
                }
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

    public boolean themNhanVien(NhanVien nv, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền thêm nhân viên!";
            return false;
        }
        if (nv.getNgaySinh() != null) {
            int age = java.time.Period.between(nv.getNgaySinh(), LocalDate.now()).getYears();
            if (age < 18) {
                lastError = "Nhân viên phải từ 18 tuổi trở lên";
                return false;
            }
        }
        int n = 0;
        try {
            Connection con = getConnection();
            String sql = "INSERT INTO NhanVien (maNhanVien, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, chucVu, luongCoBan, caLamViec, matKhau, trangThai) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, nv.getMaNhanVien());
                pstmt.setString(2, nv.getHoTen());
                pstmt.setString(3, nv.getSoDienThoai());
                pstmt.setDate(4, (nv.getNgaySinh() != null) ? Date.valueOf(nv.getNgaySinh()) : Date.valueOf(LocalDate.of(2000, 1, 1)));
                pstmt.setBoolean(5, nv.isGioiTinh());

                if (nv.getDiaChi() == null || nv.getDiaChi().trim().isEmpty()) {
                    pstmt.setNull(6, Types.NVARCHAR);
                } else {
                    pstmt.setString(6, nv.getDiaChi().trim());
                }

                if (nv.getEmail() == null || nv.getEmail().trim().isEmpty()) {
                    pstmt.setNull(7, Types.VARCHAR);
                } else {
                    pstmt.setString(7, nv.getEmail().trim());
                }

                pstmt.setString(8, nv.getChucVu());
                pstmt.setDouble(9, nv.getLuongCoBan());

                if (nv.getCaLamViec() == null || nv.getCaLamViec().trim().isEmpty()) {
                    pstmt.setNull(10, Types.NVARCHAR);
                } else {
                    pstmt.setString(10, nv.getCaLamViec().trim());
                }

                String pwd = nv.getMatKhau();
                if (pwd == null || pwd.length() != 64) {
                    pwd = hashSHA256(pwd != null ? pwd : "123456");
                }
                pstmt.setString(11, pwd);
                pstmt.setBoolean(12, nv.isTrangThai());

                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean themNhanVien(NhanVien nv) {
        return themNhanVien(nv, null);
    }

    public boolean capNhatNhanVien(NhanVien nv, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền cập nhật nhân viên!";
            return false;
        }
        if (nv.getNgaySinh() != null) {
            int age = java.time.Period.between(nv.getNgaySinh(), LocalDate.now()).getYears();
            if (age < 18) {
                lastError = "Nhân viên phải từ 18 tuổi trở lên";
                return false;
            }
        }
        int n = 0;
        try {
            Connection con = getConnection();
            String sql = "UPDATE NhanVien SET hoTen = ?, soDienThoai = ?, ngaySinh = ?, gioiTinh = ?, diaChi = ?, email = ?, chucVu = ?, luongCoBan = ?, caLamViec = ? WHERE maNhanVien = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, nv.getHoTen());
                pstmt.setString(2, nv.getSoDienThoai());
                pstmt.setDate(3, (nv.getNgaySinh() != null) ? Date.valueOf(nv.getNgaySinh()) : Date.valueOf(LocalDate.of(2000, 1, 1)));
                pstmt.setBoolean(4, nv.isGioiTinh());

                if (nv.getDiaChi() == null || nv.getDiaChi().trim().isEmpty()) {
                    pstmt.setNull(5, Types.NVARCHAR);
                } else {
                    pstmt.setString(5, nv.getDiaChi().trim());
                }

                if (nv.getEmail() == null || nv.getEmail().trim().isEmpty()) {
                    pstmt.setNull(6, Types.VARCHAR);
                } else {
                    pstmt.setString(6, nv.getEmail().trim());
                }

                pstmt.setString(7, nv.getChucVu());
                pstmt.setDouble(8, nv.getLuongCoBan());

                if (nv.getCaLamViec() == null || nv.getCaLamViec().trim().isEmpty()) {
                    pstmt.setNull(9, Types.NVARCHAR);
                } else {
                    pstmt.setString(9, nv.getCaLamViec().trim());
                }

                pstmt.setString(10, nv.getMaNhanVien());
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatNhanVien(NhanVien nv) {
        return capNhatNhanVien(nv, null);
    }

    public boolean xoaNhanVien(String maNV, NhanVien caller) {
        lastError = "";
        if (caller != null && !caller.isQuanLy()) {
            lastError = "Từ chối truy cập: Chỉ Quản lý mới có quyền xóa nhân viên!";
            return false;
        }
        int n = 0;
        try {
            Connection con = getConnection();
            String sql = "UPDATE NhanVien SET trangThai = 0 WHERE maNhanVien = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maNV);
                n = pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean xoaNhanVien(String maNV) {
        return xoaNhanVien(maNV, null);
    }
}

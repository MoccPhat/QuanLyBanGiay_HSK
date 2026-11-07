package dao;

import connectDB.ConnectDB;
import entity.NhanVien;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Base64;

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

    public static final int PBKDF2_ITERATIONS = 100000;
    public static final int PBKDF2_KEY_LENGTH = 256;
    public static final int SALT_BYTES = 16;

    /**
     * Băm mật khẩu bằng PBKDF2WithHmacSHA256 (L08).
     * Định dạng lưu trữ: pbkdf2$<iterations>$<saltBase64>$<hashBase64>
     */
    public static String hashPBKDF2(String password) {
        try {
            SecureRandom random = new SecureRandom();
            byte[] salt = new byte[SALT_BYTES];
            random.nextBytes(salt);

            PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, PBKDF2_ITERATIONS, PBKDF2_KEY_LENGTH);
            SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
            byte[] hash = skf.generateSecret(spec).getEncoded();

            String saltBase64 = Base64.getEncoder().encodeToString(salt);
            String hashBase64 = Base64.getEncoder().encodeToString(hash);
            return "pbkdf2$" + PBKDF2_ITERATIONS + "$" + saltBase64 + "$" + hashBase64;
        } catch (Exception e) {
            throw new RuntimeException("Lỗi khi băm mật khẩu PBKDF2: " + e.getMessage(), e);
        }
    }

    /**
     * Xác thực mật khẩu: Hỗ trợ cả chuẩn mới PBKDF2 và chuẩn cũ SHA-256 (64 hex) (L08).
     * Dùng MessageDigest.isEqual để chống tấn công Timing Attack.
     */
    public static boolean verifyPassword(String password, String storedHash) {
        if (password == null || storedHash == null) {
            return false;
        }
        storedHash = storedHash.trim();
        if (storedHash.startsWith("pbkdf2$")) {
            String[] parts = storedHash.split("\\$");
            if (parts.length != 4) {
                return false;
            }
            try {
                int iterations = Integer.parseInt(parts[1]);
                byte[] salt = Base64.getDecoder().decode(parts[2]);
                byte[] expectedHash = Base64.getDecoder().decode(parts[3]);

                PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, expectedHash.length * 8);
                SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
                byte[] testHash = skf.generateSecret(spec).getEncoded();

                return MessageDigest.isEqual(expectedHash, testHash);
            } catch (Exception e) {
                return false;
            }
        } else {
            // Tương thích ngược: Chuỗi băm SHA-256 cũ (64 ký tự hex)
            String sha256 = hashSHA256Static(password);
            return MessageDigest.isEqual(
                sha256.getBytes(StandardCharsets.UTF_8),
                storedHash.toLowerCase().getBytes(StandardCharsets.UTF_8)
            );
        }
    }

    public static String hashSHA256Static(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
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

    public String hashSHA256(String input) {
        return hashSHA256Static(input);
    }

    /**
     * Kiểm tra kích thước cột matKhau trong bảng NhanVien có đủ lưu chuỗi PBKDF2 (~83 ký tự) hay không.
     * Nếu CHAR(64), không thể nhồi 83 ký tự để tránh lỗi SQL Server 8152.
     */
    public boolean isColumnLargeEnoughForPBKDF2(Connection con) {
        try {
            String sql = "SELECT CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'NhanVien' AND COLUMN_NAME = 'matKhau'";
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int len = rs.getInt(1);
                    return len >= 83 || len == -1;
                }
            }
        } catch (Exception ignored) {}
        return false;
    }

    /**
     * Đổi mật khẩu nhân viên (L08):
     * Bắt buộc kiểm tra mật khẩu cũ. Băm mật khẩu mới bằng PBKDF2 (nếu cột hỗ trợ) hoặc SHA-256.
     */
    public boolean doiMatKhau(String maNV, String matKhauCu, String matKhauMoi) {
        lastError = "";
        if (maNV == null || maNV.trim().isEmpty()) {
            lastError = "Mã nhân viên không hợp lệ!";
            return false;
        }
        if (matKhauMoi == null || matKhauMoi.trim().length() < 6) {
            lastError = "Mật khẩu mới phải từ 6 ký tự trở lên!";
            return false;
        }
        try {
            Connection con = getConnection();
            String selectSql = "SELECT matKhau FROM NhanVien WHERE maNhanVien = ?";
            String storedHash = null;
            try (PreparedStatement pstmt = con.prepareStatement(selectSql)) {
                pstmt.setString(1, maNV);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
                        storedHash = rs.getString("matKhau");
                    } else {
                        lastError = "Không tìm thấy nhân viên có mã: " + maNV;
                        return false;
                    }
                }
            }

            if (!verifyPassword(matKhauCu, storedHash)) {
                lastError = "Mật khẩu cũ không chính xác!";
                return false;
            }

            boolean canUsePBKDF2 = isColumnLargeEnoughForPBKDF2(con);
            String newHash = canUsePBKDF2 ? hashPBKDF2(matKhauMoi) : hashSHA256(matKhauMoi);

            String updateSql = "UPDATE NhanVien SET matKhau = ? WHERE maNhanVien = ?";
            try (PreparedStatement pstmt = con.prepareStatement(updateSql)) {
                pstmt.setString(1, newHash);
                pstmt.setString(2, maNV);
                return pstmt.executeUpdate() > 0;
            }
        } catch (SQLException e) {
            handleSQLException(e);
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Xác thực đăng nhập (L08 & L10):
     * Phân biệt rõ ràng 3 trường hợp khi thất bại:
     * 1. Không tìm thấy mã nhân viên (hoặc tài khoản bị ngừng hoạt động).
     * 2. Mật khẩu không chính xác (hỗ trợ cả PBKDF2 và SHA-256).
     * 3. Lỗi kết nối CSDL hoặc ngoại lệ hệ thống.
     * Tự động nâng cấp hash SHA-256 lên PBKDF2 nếu đăng nhập đúng và kích thước cột cho phép (L08).
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

                        if (verifyPassword(matKhau, dbHash)) {
                            // Tự động nâng cấp từ SHA-256 lên PBKDF2 khi login thành công nếu cột DB đủ chứa (L08)
                            if (dbHash != null && !dbHash.trim().startsWith("pbkdf2$") && isColumnLargeEnoughForPBKDF2(con)) {
                                try (PreparedStatement upStmt = con.prepareStatement("UPDATE NhanVien SET matKhau = ? WHERE maNhanVien = ?")) {
                                    String pbkdf2Hash = hashPBKDF2(matKhau);
                                    upStmt.setString(1, pbkdf2Hash);
                                    upStmt.setString(2, maNV);
                                    upStmt.executeUpdate();
                                    dbHash = pbkdf2Hash;
                                } catch (Exception ignored) {}
                            }

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
                if (pwd == null || pwd.trim().isEmpty()) {
                    lastError = "Vui lòng nhập mật khẩu khởi tạo cho nhân viên mới!";
                    return false;
                }
                if (!pwd.startsWith("pbkdf2$") && pwd.length() != 64) {
                    if (pwd.length() < 6) {
                        lastError = "Mật khẩu khởi tạo phải từ 6 ký tự trở lên!";
                        return false;
                    }
                    boolean canUsePBKDF2 = isColumnLargeEnoughForPBKDF2(con);
                    pwd = canUsePBKDF2 ? hashPBKDF2(pwd) : hashSHA256(pwd);
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

    /**
     * Tìm kiếm nhân viên theo từ khóa (Mã NV, Họ tên hoặc Số điện thoại).
     */
    public ArrayList<NhanVien> timKiemNhanVien(String tuKhoa) {
        ArrayList<NhanVien> ds = new ArrayList<>();
        if (tuKhoa == null || tuKhoa.trim().isEmpty()) {
            return getAllNhanVien();
        }
        String pattern = "%" + tuKhoa.trim() + "%";
        String sql = "SELECT * FROM NhanVien WHERE trangThai = 1 AND (maNhanVien LIKE ? OR hoTen LIKE ? OR soDienThoai LIKE ? OR chucVu LIKE ?) ORDER BY maNhanVien ASC";
        try {
            Connection con = getConnection();
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, pattern);
                pstmt.setString(2, pattern);
                pstmt.setString(3, pattern);
                pstmt.setString(4, pattern);
                try (ResultSet rs = pstmt.executeQuery()) {
                    while (rs.next()) {
                        String maNV = rs.getString("maNhanVien");
                        String hoTen = rs.getString("hoTen");
                        String sdt = rs.getString("soDienThoai");
                        Date ns = rs.getDate("ngaySinh");
                        LocalDate ngaySinh = (ns != null) ? ns.toLocalDate() : null;
                        boolean gioiTinh = rs.getBoolean("gioiTinh");
                        String diaChi = rs.getString("diaChi");
                        String email = rs.getString("email");
                        String chucVu = rs.getString("chucVu");
                        double luong = rs.getDouble("luongCoBan");
                        String caLam = rs.getString("caLamViec");
                        String matKhau = rs.getString("matKhau");
                        boolean trangThai = rs.getBoolean("trangThai");

                        NhanVien nv = new NhanVien(maNV, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, chucVu, luong, caLam, matKhau, trangThai);
                        ds.add(nv);
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

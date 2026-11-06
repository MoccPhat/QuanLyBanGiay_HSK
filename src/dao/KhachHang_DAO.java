package dao;

import connectDB.ConnectDB;
import entity.KhachHang;

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
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
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
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }

    public KhachHang timTheoSoDienThoai(String sdt) {
        KhachHang kh = null;
        String sql = "SELECT * FROM KhachHang WHERE soDienThoai = ?";
        try {
            Connection con = getConnection();
            PreparedStatement pstmt = con.prepareStatement(sql);
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
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return kh;
    }

    public KhachHang getKhachHangTheoMa(String maKH) {
        KhachHang kh = null;
        String sql = "SELECT * FROM KhachHang WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            PreparedStatement pstmt = con.prepareStatement(sql);
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
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return kh;
    }

    public boolean kiemTraTrungMa(String maKH) {
        String sql = "SELECT 1 FROM KhachHang WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maKH);
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            lastError = e.getMessage();
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
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, sdt);
            if (coExclude) {
                pstmt.setString(2, maKHExclude.trim());
            }
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            lastError = e.getMessage();
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
            PreparedStatement pstmt = con.prepareStatement(sql);
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
        } catch (SQLException e) {
            lastError = e.getMessage();
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
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setInt(1, diemMoi);
            pstmt.setString(2, hangMoi);
            pstmt.setString(3, maKH);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatKhachHang(KhachHang kh) {
        lastError = "";
        int n = 0;
        String sql = "UPDATE KhachHang SET hoTen = ?, soDienThoai = ?, diaChi = ?, hangThanhVien = ? WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, kh.getHoTen());
            pstmt.setString(2, kh.getSoDienThoai());
            if (kh.getDiaChi() != null && !kh.getDiaChi().trim().isEmpty()) {
                pstmt.setString(3, kh.getDiaChi().trim());
            } else {
                pstmt.setNull(3, Types.NVARCHAR);
            }
            pstmt.setString(4, kh.getHangThanhVien());
            pstmt.setString(5, kh.getMaKhachHang());
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean xoaKhachHang(String maKH) {
        lastError = "";
        int n = 0;
        String sql = "DELETE FROM KhachHang WHERE maKhachHang = ?";
        try {
            Connection con = getConnection();
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maKH);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            lastError = e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    public String sinhMaKhachHangMoi() {
        try {
            Connection con = getConnection();
            String sql = "SELECT ISNULL(MAX(CAST(SUBSTRING(maKhachHang, 3, 4) AS INT)), 0) + 1 AS nextId FROM KhachHang WHERE maKhachHang LIKE 'KH[0-9][0-9][0-9][0-9]'";
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery(sql)) {
                if (rs.next()) {
                    return String.format("KH%04d", rs.getInt("nextId"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return String.format("KH%04d", Math.abs(System.currentTimeMillis() % 10000));
    }
}

package dao;

import connectDB.ConnectDB;
import entity.NhanVien;
import entity.SanPham;

import java.sql.*;
import java.util.ArrayList;

public class SanPham_DAO {

    private String lastError = "";

    public String getLastError() {
        return lastError;
    }

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

    private Connection getConnection() throws SQLException {
        ConnectDB.getInstance();
        Connection con = ConnectDB.getConnection();
        if (con == null || con.isClosed()) {
            ConnectDB.getInstance().connect();
            con = ConnectDB.getConnection();
        }
        return con;
    }

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

    public boolean themSanPham(SanPham sp) {
        return themSanPham(sp, null);
    }

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

    public boolean capNhatSanPham(SanPham sp) {
        return capNhatSanPham(sp, null);
    }

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

    public boolean xoaSanPham(String maSP) {
        return xoaSanPham(maSP, null);
    }
}

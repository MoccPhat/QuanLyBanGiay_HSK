package dao;

import connectDB.ConnectDB;
import entity.KhachHang;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;

public class KhachHang_DAO {

    public ArrayList<KhachHang> getAllKhachHang() {
        ArrayList<KhachHang> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT * FROM KhachHang";
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
            e.printStackTrace();
        }
        return ds;
    }

    public KhachHang timTheoSoDienThoai(String sdt) {
        KhachHang kh = null;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT * FROM KhachHang WHERE soDienThoai = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, sdt);
            ResultSet rs = pstmt.executeQuery();
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
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return kh;
    }

    public boolean themKhachHang(KhachHang kh) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "INSERT INTO KhachHang (maKhachHang, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, diemTichLuy, hangThanhVien) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, kh.getMaKhachHang());
            pstmt.setString(2, kh.getHoTen());
            pstmt.setString(3, kh.getSoDienThoai());
            pstmt.setDate(4, (kh.getNgaySinh() != null) ? Date.valueOf(kh.getNgaySinh()) : null);
            pstmt.setBoolean(5, kh.isGioiTinh());
            pstmt.setString(6, kh.getDiaChi());
            pstmt.setString(7, kh.getEmail());
            pstmt.setInt(8, kh.getDiemTichLuy());
            pstmt.setString(9, kh.getHangThanhVien());

            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatDiem(String maKH, int diemMoi, String hangMoi) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE KhachHang SET diemTichLuy = ?, hangThanhVien = ? WHERE maKhachHang = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setInt(1, diemMoi);
            pstmt.setString(2, hangMoi);
            pstmt.setString(3, maKH);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatKhachHang(KhachHang kh) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE KhachHang SET hoTen = ?, soDienThoai = ?, diaChi = ?, hangThanhVien = ? WHERE maKhachHang = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, kh.getHoTen());
            pstmt.setString(2, kh.getSoDienThoai());
            pstmt.setString(3, kh.getDiaChi());
            pstmt.setString(4, kh.getHangThanhVien());
            pstmt.setString(5, kh.getMaKhachHang());
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean xoaKhachHang(String maKH) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "DELETE FROM KhachHang WHERE maKhachHang = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maKH);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }
}

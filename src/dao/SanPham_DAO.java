package dao;

import connectDB.ConnectDB;
import entity.SanPham;

import java.sql.*;
import java.util.ArrayList;

public class SanPham_DAO {

    public ArrayList<SanPham> getAllSanPham() {
        ArrayList<SanPham> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT * FROM SanPham WHERE trangThai = 1";
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
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
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ds;
    }

    public SanPham getSanPhamTheoMa(String maSP) {
        SanPham sp = null;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "SELECT * FROM SanPham WHERE maSanPham = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maSP);
            ResultSet rs = pstmt.executeQuery();
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
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return sp;
    }

    public boolean themSanPham(SanPham sp) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "INSERT INTO SanPham (maSanPham, tenSanPham, loaiGiay, thuongHieu, giaNhap, giaBan, chatLieu, trangThai) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, sp.getMaSanPham());
            pstmt.setString(2, sp.getTenSanPham());
            pstmt.setString(3, sp.getLoaiGiay());
            pstmt.setString(4, sp.getThuongHieu());
            pstmt.setDouble(5, sp.getGiaNhap());
            pstmt.setDouble(6, sp.getGiaBan());
            pstmt.setString(7, sp.getChatLieu());
            pstmt.setBoolean(8, sp.isTrangThai());

            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatSanPham(SanPham sp) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE SanPham SET tenSanPham = ?, loaiGiay = ?, thuongHieu = ?, giaNhap = ?, giaBan = ?, chatLieu = ? WHERE maSanPham = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, sp.getTenSanPham());
            pstmt.setString(2, sp.getLoaiGiay());
            pstmt.setString(3, sp.getThuongHieu());
            pstmt.setDouble(4, sp.getGiaNhap());
            pstmt.setDouble(5, sp.getGiaBan());
            pstmt.setString(6, sp.getChatLieu());
            pstmt.setString(7, sp.getMaSanPham());

            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean xoaSanPham(String maSP) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            // Xóa mềm: Chuyển trangThai = 0
            String sql = "UPDATE SanPham SET trangThai = 0 WHERE maSanPham = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maSP);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }
}

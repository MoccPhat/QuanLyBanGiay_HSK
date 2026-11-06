package dao;

import connectDB.ConnectDB;
import entity.NhanVien;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class NhanVien_DAO {

    public ArrayList<NhanVien> getAllNhanVien() {
        ArrayList<NhanVien> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT * FROM NhanVien WHERE trangThai = 1";
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
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
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ds;
    }

    public NhanVien dangNhap(String maNV, String matKhau) {
        NhanVien nv = null;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT * FROM NhanVien WHERE maNhanVien = ? AND matKhau = ? AND trangThai = 1";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maNV);
            pstmt.setString(2, matKhau);
            ResultSet rs = pstmt.executeQuery();
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
                boolean trangThai = rs.getBoolean("trangThai");

                nv = new NhanVien(maNV, hoTen, sdt, ngaySinh, gioiTinh, diaChi, email, chucVu, luong, ca, matKhau, trangThai);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return nv;
    }

    public boolean themNhanVien(NhanVien nv) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "INSERT INTO NhanVien (maNhanVien, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, chucVu, luongCoBan, caLamViec, matKhau, trangThai) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, nv.getMaNhanVien());
            pstmt.setString(2, nv.getHoTen());
            pstmt.setString(3, nv.getSoDienThoai());
            pstmt.setDate(4, Date.valueOf(nv.getNgaySinh()));
            pstmt.setBoolean(5, nv.isGioiTinh());
            pstmt.setString(6, nv.getDiaChi());
            pstmt.setString(7, nv.getEmail());
            pstmt.setString(8, nv.getChucVu());
            pstmt.setDouble(9, nv.getLuongCoBan());
            pstmt.setString(10, nv.getCaLamViec());
            pstmt.setString(11, nv.getMatKhau());
            pstmt.setBoolean(12, nv.isTrangThai());

            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean capNhatNhanVien(NhanVien nv) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE NhanVien SET hoTen = ?, soDienThoai = ?, chucVu = ?, luongCoBan = ?, caLamViec = ?, diaChi = ? WHERE maNhanVien = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, nv.getHoTen());
            pstmt.setString(2, nv.getSoDienThoai());
            pstmt.setString(3, nv.getChucVu());
            pstmt.setDouble(4, nv.getLuongCoBan());
            pstmt.setString(5, nv.getCaLamViec());
            pstmt.setString(6, nv.getDiaChi());
            pstmt.setString(7, nv.getMaNhanVien());
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean xoaNhanVien(String maNV) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE NhanVien SET trangThai = 0 WHERE maNhanVien = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maNV);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }
}

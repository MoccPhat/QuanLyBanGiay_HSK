package dao;

import connectDB.ConnectDB;
import entity.ChiTietGiay;
import entity.SanPham;

import java.sql.*;
import java.util.ArrayList;

public class ChiTietGiay_DAO {
    private SanPham_DAO sp_dao = new SanPham_DAO();

    public ArrayList<ChiTietGiay> getAllChiTietGiay() {
        ArrayList<ChiTietGiay> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT c.*, s.tenSanPham, s.loaiGiay, s.thuongHieu, s.giaNhap, s.giaBan, s.chatLieu, s.trangThai AS spTrangThai " +
                         "FROM ChiTietGiay c JOIN SanPham s ON c.maSanPham = s.maSanPham " +
                         "WHERE s.trangThai = 1";
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                String maCTG = rs.getString("maChiTietGiay");
                String maSP = rs.getString("maSanPham");
                String tenSP = rs.getString("tenSanPham");
                String loai = rs.getString("loaiGiay");
                String hang = rs.getString("thuongHieu");
                double giaNhap = rs.getDouble("giaNhap");
                double giaBan = rs.getDouble("giaBan");
                String chatLieu = rs.getString("chatLieu");
                boolean spTrangThai = rs.getBoolean("spTrangThai");

                SanPham sp = new SanPham(maSP, tenSP, loai, hang, giaNhap, giaBan, chatLieu, spTrangThai);

                int size = rs.getInt("kichThuoc");
                String mau = rs.getString("mauSac");
                int ton = rs.getInt("soLuongTon");
                String hinh = rs.getString("hinhAnh");

                ChiTietGiay ctg = new ChiTietGiay(maCTG, sp, size, mau, ton, hinh);
                ds.add(ctg);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ds;
    }

    public ArrayList<ChiTietGiay> getChiTietTheoSanPham(String maSP) {
        ArrayList<ChiTietGiay> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "SELECT c.*, s.tenSanPham, s.loaiGiay, s.thuongHieu, s.giaNhap, s.giaBan, s.chatLieu, s.trangThai AS spTrangThai " +
                         "FROM ChiTietGiay c JOIN SanPham s ON c.maSanPham = s.maSanPham " +
                         "WHERE c.maSanPham = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, maSP);
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                String maCTG = rs.getString("maChiTietGiay");
                String tenSP = rs.getString("tenSanPham");
                String loai = rs.getString("loaiGiay");
                String hang = rs.getString("thuongHieu");
                double giaNhap = rs.getDouble("giaNhap");
                double giaBan = rs.getDouble("giaBan");
                String chatLieu = rs.getString("chatLieu");
                boolean spTrangThai = rs.getBoolean("spTrangThai");

                SanPham sp = new SanPham(maSP, tenSP, loai, hang, giaNhap, giaBan, chatLieu, spTrangThai);
                int size = rs.getInt("kichThuoc");
                String mau = rs.getString("mauSac");
                int ton = rs.getInt("soLuongTon");
                String hinh = rs.getString("hinhAnh");

                ChiTietGiay ctg = new ChiTietGiay(maCTG, sp, size, mau, ton, hinh);
                ds.add(ctg);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ds;
    }

    public boolean capNhatTonKho(String maCTG, int soLuongTru) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setInt(1, soLuongTru);
            pstmt.setString(2, maCTG);
            pstmt.setInt(3, soLuongTru);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public boolean themChiTietGiay(ChiTietGiay ctg) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh) " +
                         "VALUES (?, ?, ?, ?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, ctg.getMaChiTietGiay());
            pstmt.setString(2, ctg.getSanPham().getMaSanPham());
            pstmt.setInt(3, ctg.getKichThuoc());
            pstmt.setString(4, ctg.getMauSac());
            pstmt.setInt(5, ctg.getSoLuongTon());
            String hinh = ctg.getHinhAnh();
            if (hinh == null || hinh.trim().isEmpty()) {
                hinh = "default_shoe.png";
            }
            pstmt.setString(6, hinh);
            n = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return n > 0;
    }

    public String sinhMaChiTietGiayMoi() {
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            String sql = "SELECT ISNULL(MAX(CAST(SUBSTRING(maChiTietGiay, 4, 10) AS INT)), 0) + 1 AS nextId FROM ChiTietGiay WHERE maChiTietGiay LIKE 'CTG%'";
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery(sql)) {
                if (rs.next()) {
                    return String.format("CTG%04d", rs.getInt("nextId"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return String.format("CTG%04d", Math.abs(System.currentTimeMillis() % 10000));
    }

    public ArrayList<ChiTietGiay> layTatCaChiTietGiay() {
        return getAllChiTietGiay();
    }
}

package dao;

import connectDB.ConnectDB;
import entity.ChiTietGiay;
import entity.SanPham;

import java.sql.*;
import java.util.ArrayList;

/**
 * Lớp truy xuất và thao tác dữ liệu (tầng DAO) cho Biến thể giày (ChiTietGiay) trong CSDL SQL Server,
 * quản lý thông tin kích cỡ, màu sắc, tồn kho và hình ảnh của từng SKU sản phẩm.
 */
public class ChiTietGiay_DAO {
    private SanPham_DAO sp_dao = new SanPham_DAO();
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
     * Lấy danh sách toàn bộ các biến thể giày (SKU) của những sản phẩm đang hoạt động kinh doanh.
     *
     * @return danh sách các đối tượng ChiTietGiay
     */
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
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
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
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Lấy danh sách tất cả các biến thể kích cỡ và màu sắc thuộc về một sản phẩm cụ thể theo mã.
     *
     * @param maSP mã sản phẩm cần tra cứu các biến thể
     * @return danh sách các đối tượng ChiTietGiay tương ứng với mã sản phẩm
     */
    public ArrayList<ChiTietGiay> getChiTietTheoSanPham(String maSP) {
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
                         "WHERE c.maSanPham = ?";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maSP);
                try (ResultSet rs = pstmt.executeQuery()) {
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
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Thêm mới một bản ghi biến thể giày (size, màu sắc, tồn kho, ảnh) vào CSDL.
     *
     * @param ctg đối tượng ChiTietGiay chứa thông tin biến thể cần thêm mới
     * @return true nếu thêm thành công, ngược lại false
     */
    public boolean themChiTietGiay(ChiTietGiay ctg) {
        int n = 0;
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh) " +
                         "VALUES (?, ?, ?, ?, ?, ?)";
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
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
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return n > 0;
    }

    /**
     * Tự động sinh mã biến thể giày mới có dạng CTGxxxx tăng dần liên tục và chống trùng lặp.
     *
     * @return chuỗi mã biến thể giày mới được sinh ra
     */
    public String sinhMaChiTietGiayMoi() {
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT ISNULL(MAX(CAST(SUBSTRING(maChiTietGiay, 4, 10) AS INT)), 0) + 1 AS nextId FROM ChiTietGiay WITH (UPDLOCK, HOLDLOCK) WHERE maChiTietGiay LIKE 'CTG%'";
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery(sql)) {
                if (rs.next()) {
                    return String.format("CTG%04d", rs.getInt("nextId"));
                }
            }
        } catch (SQLException e) {
            lastError = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return String.format("CTG%04d", Math.abs(System.currentTimeMillis() % 10000));
    }

}

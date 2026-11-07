package dao;

import connectDB.ConnectDB;
import entity.*;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;

/**
 * Lớp DAO quản lý nghiệp vụ và thao tác CSDL cho Hóa đơn bán lẻ.
 * Áp dụng giao dịch toàn vẹn (Transaction ACID) tuân thủ đúng quy trình nghiệp vụ:
 * 1. Khóa bảng sinh mã hóa đơn tăng dần liên tục, chống trùng lặp giữa các máy POS.
 * 2. Lưu hóa đơn với đầy đủ tiền hàng, chiết khấu, điểm trừ, điểm cộng và tiền thanh toán thực.
 * 3. Lưu chi tiết hóa đơn và trừ tồn kho có điều kiện (rollback ngay nếu thiếu hàng).
 * 4. Khấu trừ điểm tích lũy đã dùng, cộng điểm thưởng mới và tự động cập nhật lại hạng thành viên.
 */
public class HoaDon_DAO {
    private String lastErrorMessage = "";

    public String getLastErrorMessage() {
        return lastErrorMessage;
    }

    public String getLastError() {
        return lastErrorMessage;
    }

    public ArrayList<HoaDon> getAllHoaDon() {
        ArrayList<HoaDon> ds = new ArrayList<>();
        String sql = "SELECT h.*, nv.hoTen AS tenNV, kh.hoTen AS tenKH " +
                     "FROM HoaDon h " +
                     "JOIN NhanVien nv ON h.maNhanVien = nv.maNhanVien " +
                     "LEFT JOIN KhachHang kh ON h.maKhachHang = kh.maKhachHang " +
                     "ORDER BY h.ngayLap DESC";

        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }

            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {

                while (rs.next()) {
                    String maHD = rs.getString("maHoaDon");
                    Timestamp ts = rs.getTimestamp("ngayLap");
                    LocalDateTime ngayLap = (ts != null) ? ts.toLocalDateTime() : LocalDateTime.now();

                    String maNV = rs.getString("maNhanVien");
                    String tenNV = rs.getString("tenNV");
                    NhanVien nv = new NhanVien(maNV);
                    nv.setHoTen(tenNV);

                    String maKH = rs.getString("maKhachHang");
                    String tenKH = rs.getString("tenKH");
                    KhachHang kh = null;
                    if (maKH != null) {
                        kh = new KhachHang(maKH);
                        kh.setHoTen(tenKH);
                    }

                    double tongTienHang = rs.getDouble("tongTienHang");
                    double chietKhau = rs.getDouble("chietKhau");
                    int diemSuDung = rs.getInt("diemSuDung");
                    double tienGiamDiem = rs.getDouble("tienGiamDiem");
                    double tongTien = rs.getDouble("tongTien");
                    String phuongThuc = rs.getString("phuongThucTT");
                    double tienKhachDua = rs.getDouble("tienKhachDua");
                    double tienThua = rs.getDouble("tienThua");
                    int diemCong = rs.getInt("diemCong");

                    HoaDon hd = new HoaDon(maHD, ngayLap, nv, kh, tongTien, phuongThuc, tienKhachDua, tienThua);
                    hd.setTongTienHang(tongTienHang);
                    hd.setChietKhau(chietKhau);
                    hd.setDiemSuDung(diemSuDung);
                    hd.setTienGiamDiem(tienGiamDiem);
                    hd.setDiemCong(diemCong);

                    ds.add(hd);
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }

    /**
     * Thực thi một giao dịch bán hàng an toàn trong duy nhất 1 Transaction CSDL.
     * @param hd Thông tin hóa đơn và các dòng sản phẩm trong giỏ hàng.
     * @return true nếu lưu thành công toàn bộ, false nếu có lỗi hoặc hết tồn kho.
     */
    public boolean themHoaDon(HoaDon hd) {
        Connection con = null;
        try {
            ConnectDB.getInstance();
            con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }

            // Bật chế độ quản lý Transaction thủ công
            con.setAutoCommit(false);

            // Bước 1: Sinh mã hóa đơn an toàn với UPDLOCK và HOLDLOCK
            String maHD = hd.getMaHoaDon();
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT ISNULL(MAX(CAST(SUBSTRING(maHoaDon, 3, 6) AS INT)), 0) + 1 AS nextId FROM HoaDon WITH (UPDLOCK, HOLDLOCK)")) {
                if (rs.next()) {
                    maHD = String.format("HD%06d", rs.getInt("nextId"));
                    hd.setMaHoaDon(maHD);
                }
            }

            // Bước 2: Chuẩn bị các giá trị số tiền và điểm
            double tienHang = hd.getTongTienHang();
            if (tienHang <= 0) {
                for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                    tienHang += ct.getThanhTien();
                }
                hd.setTongTienHang(tienHang);
            }
            double chietKhau = 0;
            int diemDung = 0;
            double tienGiamDiem = 0;
            int diemCong = 0;

            if (hd.getKhachHang() != null && hd.getKhachHang().getMaKhachHang() != null && !hd.getKhachHang().getMaKhachHang().trim().isEmpty()) {
                chietKhau = hd.getChietKhau();
                // Điểm dùng tối đa không được vượt quá số tiền còn lại sau chiết khấu thành viên
                double tienSauChietKhau = Math.max(0, tienHang - chietKhau);
                int diemToiDa = (int) Math.floor(tienSauChietKhau / 1000.0);
                diemDung = Math.min(hd.getDiemSuDung(), diemToiDa);
                tienGiamDiem = diemDung * 1000.0;
                hd.setDiemSuDung(diemDung);
                hd.setTienGiamDiem(tienGiamDiem);
            } else {
                // Khách vãng lai: bắt buộc = 0 theo ràng buộc CK_HoaDon_diemKhach của SQL Server
                chietKhau = 0;
                diemDung = 0;
                tienGiamDiem = 0;
                hd.setChietKhau(0);
                hd.setDiemSuDung(0);
                hd.setTienGiamDiem(0);
            }

            double tongPhaiTra = Math.max(0, tienHang - chietKhau - tienGiamDiem);
            hd.setTongTien(tongPhaiTra);

            if (hd.getKhachHang() != null && hd.getKhachHang().getMaKhachHang() != null && !hd.getKhachHang().getMaKhachHang().trim().isEmpty()) {
                diemCong = (int) Math.floor(tongPhaiTra / 100000.0);
            } else {
                diemCong = 0;
            }
            hd.setDiemCong(diemCong);

            double tienDua = hd.getTienKhachDua();
            if ("Chuyển khoản QR".equals(hd.getPhuongThucTT())) {
                tienDua = tongPhaiTra;
                hd.setTienKhachDua(tienDua);
                hd.setTienThua(0);
            } else {
                if (tienDua < tongPhaiTra) {
                    tienDua = tongPhaiTra;
                    hd.setTienKhachDua(tienDua);
                }
                hd.setTienThua(Math.max(0, tienDua - tongPhaiTra));
            }

            // Bước 3: INSERT bảng HoaDon với đầy đủ 13 cột của CSDL
            String sqlHD = "INSERT INTO HoaDon (maHoaDon, ngayLap, maNhanVien, maKhachHang, " +
                           "                    tongTienHang, chietKhau, diemSuDung, tienGiamDiem, " +
                           "                    tongTien, phuongThucTT, tienKhachDua, tienThua, diemCong) " +
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            try (PreparedStatement pstmtHD = con.prepareStatement(sqlHD)) {
                pstmtHD.setString(1, maHD);
                pstmtHD.setTimestamp(2, Timestamp.valueOf(hd.getNgayLap()));
                pstmtHD.setString(3, hd.getNhanVien().getMaNhanVien());
                if (hd.getKhachHang() != null && hd.getKhachHang().getMaKhachHang() != null && !hd.getKhachHang().getMaKhachHang().trim().isEmpty()) {
                    pstmtHD.setString(4, hd.getKhachHang().getMaKhachHang().trim());
                } else {
                    pstmtHD.setNull(4, Types.VARCHAR);
                }
                pstmtHD.setBigDecimal(5, java.math.BigDecimal.valueOf(tienHang));
                pstmtHD.setBigDecimal(6, java.math.BigDecimal.valueOf(chietKhau));
                pstmtHD.setInt(7, diemDung);
                pstmtHD.setBigDecimal(8, java.math.BigDecimal.valueOf(tienGiamDiem));
                pstmtHD.setBigDecimal(9, java.math.BigDecimal.valueOf(tongPhaiTra));
                pstmtHD.setString(10, hd.getPhuongThucTT());
                pstmtHD.setBigDecimal(11, java.math.BigDecimal.valueOf(tienDua));
                pstmtHD.setBigDecimal(12, java.math.BigDecimal.valueOf(hd.getTienThua()));
                pstmtHD.setInt(13, diemCong);
                pstmtHD.executeUpdate();
            }

            // Bước 4: INSERT từng dòng vào ChiTietHoaDon và trừ tồn kho tương ứng
            String sqlCT = "INSERT INTO ChiTietHoaDon (maHoaDon, maChiTietGiay, soLuong, donGia, giamGia, thanhTien) " +
                           "VALUES (?, ?, ?, ?, ?, ?)";
            String sqlKho = "UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?";

            try (PreparedStatement pstmtCT = con.prepareStatement(sqlCT);
                 PreparedStatement pstmtKho = con.prepareStatement(sqlKho)) {

                for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                    pstmtCT.setString(1, maHD);
                    pstmtCT.setString(2, ct.getChiTietGiay().getMaChiTietGiay());
                    pstmtCT.setInt(3, ct.getSoLuong());
                    pstmtCT.setBigDecimal(4, java.math.BigDecimal.valueOf(ct.getDonGia()));
                    pstmtCT.setBigDecimal(5, java.math.BigDecimal.valueOf(ct.getGiamGia()));
                    pstmtCT.setBigDecimal(6, java.math.BigDecimal.valueOf(ct.getThanhTien()));
                    pstmtCT.executeUpdate();

                    pstmtKho.setInt(1, ct.getSoLuong());
                    pstmtKho.setString(2, ct.getChiTietGiay().getMaChiTietGiay());
                    pstmtKho.setInt(3, ct.getSoLuong());
                    int updated = pstmtKho.executeUpdate();
                    if (updated == 0) {
                        con.rollback();
                        lastErrorMessage = "Tồn kho không đủ đáp ứng cho biến thể SKU: " + ct.getChiTietGiay().getMaChiTietGiay();
                        System.err.println("Giao dịch bị hủy: " + lastErrorMessage);
                        return false;
                    }
                }
            }

            // Bước 5: Cập nhật điểm và hạng khách hàng nếu có mã khách
            if (hd.getKhachHang() != null && hd.getKhachHang().getMaKhachHang() != null && !hd.getKhachHang().getMaKhachHang().trim().isEmpty()) {
                String sqlDiem = "UPDATE KhachHang SET " +
                                 "  diemTichLuy = CASE WHEN diemTichLuy >= ? THEN diemTichLuy - ? ELSE 0 END + ?, " +
                                 "  hangThanhVien = CASE " +
                                 "    WHEN (CASE WHEN diemTichLuy >= ? THEN diemTichLuy - ? ELSE 0 END + ?) >= 200 THEN N'Kim Cương' " +
                                 "    WHEN (CASE WHEN diemTichLuy >= ? THEN diemTichLuy - ? ELSE 0 END + ?) >= 100 THEN N'Vàng' " +
                                 "    WHEN (CASE WHEN diemTichLuy >= ? THEN diemTichLuy - ? ELSE 0 END + ?) >= 30  THEN N'Bạc' " +
                                 "    ELSE N'Đồng' END " +
                                 "WHERE maKhachHang = ?";
                try (PreparedStatement pstmtDiem = con.prepareStatement(sqlDiem)) {
                    pstmtDiem.setInt(1, diemDung);
                    pstmtDiem.setInt(2, diemDung);
                    pstmtDiem.setInt(3, diemCong);
                    pstmtDiem.setInt(4, diemDung);
                    pstmtDiem.setInt(5, diemDung);
                    pstmtDiem.setInt(6, diemCong);
                    pstmtDiem.setInt(7, diemDung);
                    pstmtDiem.setInt(8, diemDung);
                    pstmtDiem.setInt(9, diemCong);
                    pstmtDiem.setInt(10, diemDung);
                    pstmtDiem.setInt(11, diemDung);
                    pstmtDiem.setInt(12, diemCong);
                    pstmtDiem.setString(13, hd.getKhachHang().getMaKhachHang().trim());
                    pstmtDiem.executeUpdate();
                }
            }

            // Cam kết toàn bộ giao dịch thành công (Commit)
            con.commit();
            return true;

        } catch (SQLException e) {
            lastErrorMessage = "Lỗi CSDL khi lưu hóa đơn: " + e.getMessage();
            e.printStackTrace();
            if (con != null) {
                try {
                    con.rollback();
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
            return false;
        } finally {
            if (con != null) {
                try {
                    con.setAutoCommit(true);
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public int getTongSoLuongBanRa() {
        String sql = "SELECT ISNULL(SUM(soLuong), 0) FROM ChiTietHoaDon";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    return rs.getInt(1);
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return 0;
    }

    public int getTongKhachHang() {
        String sql = "SELECT COUNT(*) FROM KhachHang";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    return rs.getInt(1);
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return 0;
    }

    public ArrayList<Object[]> getTopSanPhamBanChay(int top) {
        ArrayList<Object[]> list = new ArrayList<>();
        String sql = "SELECT TOP (?) sp.maSanPham, sp.tenSanPham, sp.thuongHieu, " +
                     "       ISNULL(SUM(ct.soLuong), 0) AS tongSL, " +
                     "       ISNULL(SUM(ct.thanhTien), 0) AS tongDT " +
                     "FROM ChiTietHoaDon ct " +
                     "JOIN ChiTietGiay ctg ON ct.maChiTietGiay = ctg.maChiTietGiay " +
                     "JOIN SanPham sp ON ctg.maSanPham = sp.maSanPham " +
                     "GROUP BY sp.maSanPham, sp.tenSanPham, sp.thuongHieu " +
                     "ORDER BY tongSL DESC, tongDT DESC";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setInt(1, top);
                try (ResultSet rs = pstmt.executeQuery()) {
                    int rank = 1;
                    while (rs.next()) {
                        String ma = rs.getString("maSanPham");
                        String ten = rs.getString("tenSanPham");
                        String hang = rs.getString("thuongHieu");
                        int sl = rs.getInt("tongSL");
                        double dt = rs.getDouble("tongDT");
                        list.add(new Object[]{"#" + (rank++), ma, ten, hang, sl, dt});
                    }
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return list;
    }
}

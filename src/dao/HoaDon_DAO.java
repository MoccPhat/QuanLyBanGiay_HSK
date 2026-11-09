package dao;

import connectDB.ConnectDB;
import entity.*;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;

/**
 * Lớp truy xuất và thao tác dữ liệu (tầng DAO) cho Hóa đơn bán lẻ trong CSDL SQL Server,
 * áp dụng giao dịch toàn vẹn ACID, quản lý thanh toán, trừ tồn kho, tích điểm và thống kê doanh thu.
 */
public class HoaDon_DAO {
    private String lastErrorMessage = "";

    /**
     * Lấy thông báo lỗi chi tiết gần nhất phát sinh khi thực thi thao tác CSDL.
     *
     * @return chuỗi mô tả lỗi chi tiết gần nhất
     */
    public String getLastErrorMessage() {
        return lastErrorMessage;
    }

    /**
     * Lấy thông báo lỗi gần nhất phát sinh khi thực thi thao tác CSDL (phương thức bí danh của getLastErrorMessage).
     *
     * @return chuỗi mô tả lỗi gần nhất
     */
    public String getLastError() {
        return lastErrorMessage;
    }

    /**
     * Lớp đóng gói kết quả tính toán chi tiết tiền hóa đơn bảo toàn độ chính xác số học.
     */
    public static class KetQuaTinhTien {
        private final double tongTienHang;
        private final double chietKhau;
        private final int diemSuDung;
        private final double tienGiamDiem;
        private final double tongPhaiTra;
        private final int diemCong;

        /**
         * Khởi tạo đối tượng đóng gói kết quả tính toán tiền hóa đơn.
         *
         * @param tongTienHang tổng tiền hàng gốc
         * @param chietKhau số tiền chiết khấu theo hạng thành viên
         * @param diemSuDung số điểm tích lũy sử dụng
         * @param tienGiamDiem số tiền giảm trừ tương ứng từ điểm
         * @param tongPhaiTra tổng tiền khách thực tế cần thanh toán
         * @param diemCong số điểm tích lũy được cộng mới
         */
        public KetQuaTinhTien(double tongTienHang, double chietKhau, int diemSuDung, double tienGiamDiem, double tongPhaiTra, int diemCong) {
            this.tongTienHang = tongTienHang;
            this.chietKhau = chietKhau;
            this.diemSuDung = diemSuDung;
            this.tienGiamDiem = tienGiamDiem;
            this.tongPhaiTra = tongPhaiTra;
            this.diemCong = diemCong;
        }

        /**
         * Lấy tổng tiền hàng gốc.
         *
         * @return số tiền hàng gốc (VNĐ)
         */
        public double getTongTienHang() { return tongTienHang; }

        /**
         * Lấy số tiền chiết khấu theo hạng thành viên.
         *
         * @return số tiền chiết khấu (VNĐ)
         */
        public double getChietKhau() { return chietKhau; }

        /**
         * Lấy số điểm tích lũy sử dụng.
         *
         * @return số điểm sử dụng
         */
        public int getDiemSuDung() { return diemSuDung; }

        /**
         * Lấy số tiền giảm trừ quy đổi từ điểm tích lũy.
         *
         * @return số tiền giảm từ điểm (VNĐ)
         */
        public double getTienGiamDiem() { return tienGiamDiem; }

        /**
         * Lấy tổng số tiền thực tế khách cần thanh toán sau giảm trừ.
         *
         * @return tổng tiền cần thanh toán (VNĐ)
         */
        public double getTongPhaiTra() { return tongPhaiTra; }

        /**
         * Lấy số điểm tích lũy được cộng mới từ đơn hàng.
         *
         * @return số điểm thưởng được cộng
         */
        public int getDiemCong() { return diemCong; }
    }

    /**
     * Tập trung tính chiết khấu và tiền thanh toán tại 1 điểm duy nhất dùng BigDecimal với quy tắc làm tròn HALF_UP.
     * Khách vãng lai: chiết khấu = 0, điểm = 0, điểm cộng = 0.
     *
     * @param tongTienHangVal tổng tiền hàng gốc trước giảm giá
     * @param kh thông tin khách hàng mua hàng (hoặc null nếu là khách vãng lai)
     * @param diemMuonDung số điểm tích lũy khách hàng mong muốn sử dụng
     * @return đối tượng KetQuaTinhTien chứa các khoản tiền và điểm tính toán chi tiết
     */
    public static KetQuaTinhTien tinhChiTietTien(double tongTienHangVal, KhachHang kh, int diemMuonDung) {
        java.math.BigDecimal tienHang = java.math.BigDecimal.valueOf(tongTienHangVal).setScale(0, java.math.RoundingMode.HALF_UP);
        if (tienHang.compareTo(java.math.BigDecimal.ZERO) < 0) {
            tienHang = java.math.BigDecimal.ZERO;
        }

        java.math.BigDecimal chietKhau = java.math.BigDecimal.ZERO;
        int diemDung = 0;
        java.math.BigDecimal tienGiamDiem = java.math.BigDecimal.ZERO;
        int diemCong = 0;

        if (kh != null && kh.getMaKhachHang() != null && !kh.getMaKhachHang().trim().isEmpty()) {
            double pt = kh.tinhChietKhau();
            if (pt > 0) {
                chietKhau = tienHang.multiply(java.math.BigDecimal.valueOf(pt)).setScale(0, java.math.RoundingMode.HALF_UP);
            }
            java.math.BigDecimal tienSauChietKhau = tienHang.subtract(chietKhau);
            if (tienSauChietKhau.compareTo(java.math.BigDecimal.ZERO) < 0) {
                tienSauChietKhau = java.math.BigDecimal.ZERO;
            }

            int diemCoTheDung = tienSauChietKhau.divide(java.math.BigDecimal.valueOf(1000), 0, java.math.RoundingMode.FLOOR).intValue();
            int diemCo = kh.getDiemTichLuy();
            int diemToiDa = Math.min(diemCo, diemCoTheDung);

            diemDung = Math.max(0, Math.min(diemMuonDung, diemToiDa));
            tienGiamDiem = java.math.BigDecimal.valueOf(diemDung).multiply(java.math.BigDecimal.valueOf(1000));
        }

        java.math.BigDecimal tongPhaiTra = tienHang.subtract(chietKhau).subtract(tienGiamDiem);
        if (tongPhaiTra.compareTo(java.math.BigDecimal.ZERO) < 0) {
            tongPhaiTra = java.math.BigDecimal.ZERO;
        }

        if (kh != null && kh.getMaKhachHang() != null && !kh.getMaKhachHang().trim().isEmpty()) {
            diemCong = tongPhaiTra.divide(java.math.BigDecimal.valueOf(100000), 0, java.math.RoundingMode.FLOOR).intValue();
        } else {
            diemCong = 0;
        }

        return new KetQuaTinhTien(
            tienHang.doubleValue(),
            chietKhau.doubleValue(),
            diemDung,
            tienGiamDiem.doubleValue(),
            tongPhaiTra.doubleValue(),
            diemCong
        );
    }

    /**
     * Lấy danh sách toàn bộ hóa đơn trong CSDL, sắp xếp giảm dần theo ngày lập.
     *
     * @return danh sách các đối tượng HoaDon
     */
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
     * Thực thi một giao dịch bán hàng an toàn trong duy nhất 1 Transaction CSDL:
     * khóa sinh mã hóa đơn, lưu hóa đơn 13 cột, lưu chi tiết hóa đơn, trừ kho và cập nhật tích điểm.
     *
     * @param hd Thông tin hóa đơn và các dòng sản phẩm trong giỏ hàng
     * @return true nếu lưu thành công toàn bộ, false nếu có lỗi hoặc hết tồn kho
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

            // Bước 2: Chuẩn bị các giá trị số tiền và điểm dùng logic tập trung BigDecimal (L09)
            double tienHang = hd.getTongTienHang();
            if (tienHang <= 0) {
                for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                    tienHang += ct.getThanhTien();
                }
            }

            KetQuaTinhTien kq = tinhChiTietTien(tienHang, hd.getKhachHang(), hd.getDiemSuDung());
            hd.setTongTienHang(kq.getTongTienHang());
            hd.setChietKhau(kq.getChietKhau());
            hd.setDiemSuDung(kq.getDiemSuDung());
            hd.setTienGiamDiem(kq.getTienGiamDiem());
            hd.setTongTien(kq.getTongPhaiTra());
            hd.setDiemCong(kq.getDiemCong());

            double chietKhau = kq.getChietKhau();
            int diemDung = kq.getDiemSuDung();
            double tienGiamDiem = kq.getTienGiamDiem();
            int diemCong = kq.getDiemCong();
            double tongPhaiTra = kq.getTongPhaiTra();
            double tienDua = hd.getTienKhachDua();

            // L33: DAO từ chối thanh toán nếu tiền khách đưa không đủ (không ghi đè tiềnDua = tongPhaiTra)
            if ("Chuyển khoản QR".equals(hd.getPhuongThucTT())) {
                tienDua = tongPhaiTra;
                hd.setTienKhachDua(tienDua);
                hd.setTienThua(0);
            } else {
                if (tienDua < tongPhaiTra) {
                    con.rollback();
                    lastErrorMessage = "Tiền khách đưa không đủ thanh toán đơn hàng (Thiếu: " + (tongPhaiTra - tienDua) + " VNĐ)!";
                    return false;
                }
                hd.setTienKhachDua(tienDua);
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

    /**
     * Tính tổng số lượng tất cả các sản phẩm giày dép đã bán ra từ các hóa đơn.
     *
     * @return tổng số lượng sản phẩm nguyên đã xuất bán
     */
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

    /**
     * Đếm tổng số lượng khách hàng đã đăng ký thông tin trong hệ thống.
     *
     * @return tổng số lượng khách hàng
     */
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

    /**
     * Lấy danh sách những sản phẩm bán chạy nhất theo số lượng xuất bán và tổng doanh thu.
     *
     * @param top số lượng sản phẩm đứng đầu cần lấy
     * @return danh sách các mảng Object[] chứa thông tin: thứ hạng, mã SP, tên SP, hãng, tổng SL, tổng doanh thu
     */
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

    /**
     * Lấy danh sách chi tiết các món hàng (sản phẩm, biến thể, số lượng, giá, thành tiền) của một hóa đơn theo mã.
     *
     * @param maHD mã hóa đơn cần tra cứu danh sách chi tiết
     * @return danh sách các đối tượng ChiTietHoaDon thuộc hóa đơn
     */
    public ArrayList<ChiTietHoaDon> getChiTietHoaDonTheoMa(String maHD) {
        ArrayList<ChiTietHoaDon> list = new ArrayList<>();
        String sql = "SELECT ct.*, ctg.kichThuoc, ctg.mauSac, ctg.soLuongTon, ctg.hinhAnh, " +
                     "       sp.maSanPham, sp.tenSanPham, sp.loaiGiay, sp.thuongHieu, sp.giaNhap, sp.giaBan, sp.chatLieu, sp.trangThai AS spTrangThai " +
                     "FROM ChiTietHoaDon ct " +
                     "JOIN ChiTietGiay ctg ON ct.maChiTietGiay = ctg.maChiTietGiay " +
                     "JOIN SanPham sp ON ctg.maSanPham = sp.maSanPham " +
                     "WHERE ct.maHoaDon = ? " +
                     "ORDER BY ct.maChiTietGiay ASC";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maHD);
                try (ResultSet rs = pstmt.executeQuery()) {
                    HoaDon hdRef = new HoaDon(maHD);
                    while (rs.next()) {
                        String maCTG = rs.getString("maChiTietGiay");
                        int sl = rs.getInt("soLuong");
                        double donGia = rs.getDouble("donGia");
                        double giamGia = rs.getDouble("giamGia");
                        double thanhTien = rs.getDouble("thanhTien");

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

                        ChiTietHoaDon cthd = new ChiTietHoaDon(hdRef, ctg, sl, donGia, giamGia, thanhTien);
                        list.add(cthd);
                    }
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return list;
    }

    /**
     * Lấy thông tin đầy đủ của một hóa đơn kèm toàn bộ danh sách chi tiết các món hàng theo mã định danh.
     *
     * @param maHD mã hóa đơn cần tìm kiếm
     * @return đối tượng HoaDon đầy đủ thông tin hoặc null nếu không tồn tại
     */
    public HoaDon getHoaDonTheoMa(String maHD) {
        String sql = "SELECT h.*, nv.hoTen AS tenNV, kh.hoTen AS tenKH " +
                     "FROM HoaDon h " +
                     "JOIN NhanVien nv ON h.maNhanVien = nv.maNhanVien " +
                     "LEFT JOIN KhachHang kh ON h.maKhachHang = kh.maKhachHang " +
                     "WHERE h.maHoaDon = ?";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, maHD);
                try (ResultSet rs = pstmt.executeQuery()) {
                    if (rs.next()) {
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

                        ArrayList<ChiTietHoaDon> dsCT = getChiTietHoaDonTheoMa(maHD);
                        for (ChiTietHoaDon ct : dsCT) {
                            hd.themChiTiet(ct);
                        }
                        return hd;
                    }
                }
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return null;
    }

    /**
     * Tìm kiếm hóa đơn theo từ khóa (khớp với Mã HĐ, Tên Thu ngân hoặc Tên Khách hàng).
     *
     * @param tuKhoa từ khóa cần tìm kiếm
     * @return danh sách các đối tượng HoaDon thỏa mãn từ khóa tìm kiếm
     */
    public ArrayList<HoaDon> timKiemHoaDon(String tuKhoa) {
        if (tuKhoa == null || tuKhoa.trim().isEmpty()) {
            return getAllHoaDon();
        }
        ArrayList<HoaDon> ds = new ArrayList<>();
        String pattern = "%" + tuKhoa.trim() + "%";
        String sql = "SELECT h.*, nv.hoTen AS tenNV, kh.hoTen AS tenKH " +
                     "FROM HoaDon h " +
                     "JOIN NhanVien nv ON h.maNhanVien = nv.maNhanVien " +
                     "LEFT JOIN KhachHang kh ON h.maKhachHang = kh.maKhachHang " +
                     "WHERE h.maHoaDon LIKE ? OR nv.hoTen LIKE ? OR kh.hoTen LIKE ? " +
                     "ORDER BY h.ngayLap DESC";
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            try (PreparedStatement pstmt = con.prepareStatement(sql)) {
                pstmt.setString(1, pattern);
                pstmt.setString(2, pattern);
                pstmt.setString(3, pattern);
                try (ResultSet rs = pstmt.executeQuery()) {
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
            }
        } catch (SQLException e) {
            lastErrorMessage = "Không kết nối được CSDL: " + e.getMessage();
            e.printStackTrace();
        }
        return ds;
    }
}

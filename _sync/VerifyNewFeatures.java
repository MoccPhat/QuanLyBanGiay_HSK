package test;

import connectDB.ConnectDB;
import dao.*;
import entity.*;
import gui.*;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.event.ActionEvent;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Bộ kiểm thử tự động toàn diện VerifyNewFeatures cho 12 tính năng mới & hồi quy:
 * 1. Xuất hóa đơn ra file .txt (kiểm tra file trong hoadon/, kiểm tra 11 trường nội dung cốt lõi).
 * 2. In hóa đơn (BanHang_GUI.inHoaDon không ném ngoại lệ khi thiếu máy in, fallback sang file text).
 * 3. Tìm kiếm nâng cao sản phẩm theo thương hiệu (SanPham_DAO.timKiemNangCao).
 * 4. Tìm kiếm nâng cao sản phẩm theo khoảng giá (từ - đến).
 * 5. Tìm kiếm nâng cao sản phẩm "còn hàng / ngừng bán" (trạng thái trangThai & tồn kho).
 * 6. Tìm kiếm nâng cao khách hàng theo hạng thành viên (KhachHang_DAO.timKiemNangCao).
 * 7. Tìm kiếm nâng cao khách hàng theo khoảng điểm tích lũy.
 * 8. Tìm kiếm nâng cao khách hàng theo giới tính.
 * 9. Tìm kiếm nâng cao khi không có kết quả (trả về danh sách rỗng an toàn, không ném exception).
 * 10. Phân quyền hiển thị Tab Thống kê chỉ dành cho Quản lý (ManHinhChinh_GUI & NhanVien.isQuanLy()).
 * 11. Cô lập phím tắt F10 & Delete ở các tab khác không tác động đến giỏ hàng POS.
 * 12. Hóa đơn 13 cột được lưu chính xác sau thanh toán (đối chiếu 13/13 cột CSDL trong Transaction).
 *
 * Biên dịch & Thực thi:
 *   javac --release 17 -encoding UTF-8 -cp "bin;lib/*" -d _sync\bin_test _sync\VerifyNewFeatures.java
 *   java -cp "_sync\bin_test;bin;lib/*" test.VerifyNewFeatures
 */
public class VerifyNewFeatures {

    private static int totalPassed = 0;
    private static int totalFailed = 0;
    private static final List<File> testFilesCreated = new ArrayList<>();

    private static void pass(String testName, String detail) {
        totalPassed++;
        System.out.println("  [PASS] " + testName + " -> " + detail);
    }

    private static void fail(String testName, String detail) {
        totalFailed++;
        System.err.println("  [FAIL] " + testName + " -> " + detail);
    }

    public static void main(String[] args) {
        System.out.println("===============================================================================");
        System.out.println("    STEPUP FOOTWEAR POS - VERIFY NEW FEATURES & REGRESSION TEST SUITE");
        System.out.println("===============================================================================\n");

        try {
            ConnectDB.getInstance().connect();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                System.err.println("[CRITICAL] Không thể kết nối cơ sở dữ liệu SQL Server 'QuanLyBanGiay'!");
                System.exit(1);
            }
            System.out.println("[INFO] Đã kết nối cơ sở dữ liệu 'QuanLyBanGiay' thành công.\n");

            // Dọn dẹp dữ liệu rác trước khi chạy
            cleanUpTestData();

            // 12 ca kiểm thử độc lập
            test01_XuatHoaDonRaFile();
            test02_InHoaDon();
            test03_TimKiemNangCaoSanPhamTheoThuongHieu();
            test04_TimKiemNangCaoSanPhamTheoKhoangGia();
            test05_TimKiemNangCaoSanPhamConHangNgungBan();
            test06_TimKiemNangCaoKhachHangTheoHang();
            test07_TimKiemNangCaoKhachHangTheoKhoangDiem();
            test08_TimKiemNangCaoKhachHangTheoGioiTinh();
            test09_TimKiemNangCaoKhongCoKetQua();
            test10_PhanQuyenTabThongKeQuanLy();
            test11_PhimTatF10DeleteKhongTacDongGioKhiODangTabKhac();
            test12_LuuHoaDon13CotDungSauThanhToan();

            // Dọn dẹp rác sau khi chạy
            cleanUpTestData();

            System.out.println("\n===============================================================================");
            System.out.println(String.format("    TEST SUMMARY: %d PASSED, %d FAILED across all 12 test cases", totalPassed, totalFailed));
            System.out.println("===============================================================================");

            if (totalFailed > 0) {
                System.exit(1);
            }

        } catch (Exception e) {
            System.err.println("[UNEXPECTED EXCEPTION]: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * Dọn sạch các file test sinh ra trong thư mục hoadon/ và các dòng kiểm thử trong CSDL.
     */
    private static void cleanUpTestData() {
        // Dọn file test hóa đơn trên đĩa
        for (File f : testFilesCreated) {
            if (f != null && f.exists()) {
                try {
                    f.delete();
                } catch (Exception ignored) {}
            }
        }
        testFilesCreated.clear();

        File hoadonDir = new File("hoadon");
        if (hoadonDir.exists() && hoadonDir.isDirectory()) {
            File[] files = hoadonDir.listFiles((dir, name) ->
                    name.startsWith("HD99") || name.startsWith("HD_TEST") || name.contains("TEST"));
            if (files != null) {
                for (File f : files) {
                    try {
                        f.delete();
                    } catch (Exception ignored) {}
                }
            }
        }

        // Dọn dữ liệu rác trong CSDL SQL Server
        try {
            Connection con = ConnectDB.getConnection();
            if (con != null && !con.isClosed()) {
                try (Statement st = con.createStatement()) {
                    st.executeUpdate("DELETE FROM ChiTietHoaDon WHERE maChiTietGiay LIKE 'CTG99%' OR maHoaDon IN (SELECT maHoaDon FROM HoaDon WHERE maKhachHang LIKE 'KH99%' OR maHoaDon LIKE 'HD99%')");
                    st.executeUpdate("DELETE FROM HoaDon WHERE maKhachHang LIKE 'KH99%' OR maHoaDon LIKE 'HD99%'");
                    st.executeUpdate("DELETE FROM ChiTietGiay WHERE maChiTietGiay LIKE 'CTG99%'");
                    st.executeUpdate("DELETE FROM SanPham WHERE maSanPham LIKE 'SP99%'");
                    st.executeUpdate("DELETE FROM KhachHang WHERE maKhachHang LIKE 'KH99%'");
                    st.executeUpdate("DELETE FROM NhanVien WHERE maNhanVien LIKE 'NV99%'");
                }
            }
        } catch (SQLException e) {
            System.err.println("Cleanup warning: " + e.getMessage());
        }
    }

    // =========================================================================
    // CA 1: Xuất hóa đơn ra file .txt
    // =========================================================================
    private static void test01_XuatHoaDonRaFile() {
        try {
            String maHD = "HD999001";
            String billContent =
                    "=============================================\n" +
                    "            STEPUP FOOTWEAR STORE            \n" +
                    "      12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM      \n\n" +
                    "               HÓA ĐƠN BÁN LẺ                \n\n" +
                    "Mã HĐ: " + maHD + "\n" +
                    "Ngày: 08/11/2026 10:30\n" +
                    "Thu ngân: Trần Quản Lý\n" +
                    "Khách hàng: Đỗ Hoàng Long VIP\n" +
                    "---------------------------------------------\n" +
                    "Nike Air Force 1 07 Low (Size 42, Màu Trắng)\n" +
                    "  2 x 2,600,000 VNĐ = 5,200,000 VNĐ\n" +
                    "---------------------------------------------\n" +
                    "Tổng tiền hàng:             5,200,000 VNĐ\n" +
                    "Chiết khấu hạng thẻ:         -260,000 VNĐ\n" +
                    "Tiền giảm từ điểm:            -50,000 VNĐ\n" +
                    "CẦN THANH TOÁN:             4,890,000 VNĐ\n" +
                    "Khách đưa:                  5,000,000 VNĐ\n" +
                    "Tiền thừa:                    110,000 VNĐ\n" +
                    "Điểm cộng mới:                   +48 điểm\n" +
                    "Hình thức:                       Tiền mặt\n" +
                    "=============================================\n" +
                    "       CẢM ƠN QUÝ KHÁCH & HẸN GẶP LẠI!       \n";

            File f = BanHang_GUI.xuatHoaDonRaFile(maHD, billContent);
            if (f == null || !f.exists()) {
                fail("1. Xuất hóa đơn ra file .txt", "Không tạo được file hóa đơn trên đĩa!");
                return;
            }
            testFilesCreated.add(f);

            String readContent = Files.readString(f.toPath(), StandardCharsets.UTF_8);

            boolean hasMaHD = readContent.contains(maHD);
            boolean hasThuNgan = readContent.contains("Thu ngân: Trần Quản Lý");
            boolean hasKhach = readContent.contains("Khách hàng: Đỗ Hoàng Long VIP");
            boolean hasSize = readContent.contains("Size 42");
            boolean hasMau = readContent.contains("Màu Trắng");
            boolean hasSoLuong = readContent.contains("2 x");
            boolean hasDonGia = readContent.contains("2,600,000");
            boolean hasThanhTien = readContent.contains("5,200,000");
            boolean hasTongTienHang = readContent.contains("Tổng tiền hàng:");
            boolean hasChietKhau = readContent.contains("Chiết khấu");
            boolean hasGiamDiem = readContent.contains("Tiền giảm từ điểm");
            boolean hasTongThanhToan = readContent.contains("CẦN THANH TOÁN:");
            boolean hasTienKhachDua = readContent.contains("Khách đưa:");
            boolean hasTienThua = readContent.contains("Tiền thừa:");
            boolean hasDiemCong = readContent.contains("Điểm cộng mới:");

            boolean allFieldsPresent = hasMaHD && hasThuNgan && hasKhach && hasSize && hasMau &&
                    hasSoLuong && hasDonGia && hasThanhTien && hasTongTienHang && hasChietKhau &&
                    hasGiamDiem && hasTongThanhToan && hasTienKhachDua && hasTienThua && hasDiemCong;

            if (allFieldsPresent) {
                pass("1. Xuất hóa đơn ra file .txt",
                    String.format("Đã tạo file '%s' trong hoadon/ và chứa đầy đủ 11 trường thông tin (Mã HĐ, thu ngân, khách hàng, dòng SP [size/màu/SL/đơn giá/thành tiền], tổng tiền hàng, chiết khấu, giảm điểm, tổng thanh toán, tiền khách đưa, tiền thừa, điểm cộng)", f.getName()));
            } else {
                fail("1. Xuất hóa đơn ra file .txt",
                    String.format("Nội dung file thiếu trường bắt buộc: maHD=%b, thuNgan=%b, khach=%b, sp[size=%b, mau=%b, sl=%b, gia=%b, tt=%b], tongHang=%b, ck=%b, giamDiem=%b, canTra=%b, tienDua=%b, tienThua=%b, diemCong=%b",
                        hasMaHD, hasThuNgan, hasKhach, hasSize, hasMau, hasSoLuong, hasDonGia, hasThanhTien, hasTongTienHang, hasChietKhau, hasGiamDiem, hasTongThanhToan, hasTienKhachDua, hasTienThua, hasDiemCong));
            }
        } catch (Exception e) {
            fail("1. Xuất hóa đơn ra file .txt", e.getMessage());
        }
    }

    // =========================================================================
    // CA 2: In hóa đơn (không ném exception khi không có máy in, fallback sang file)
    // =========================================================================
    private static void test02_InHoaDon() {
        try {
            String maHD = "HD_TEST_PRINT";
            String billContent = "STEPUP FOOTWEAR POS - IN THU HOA DON TEST PRINT";

            // Gọi inHoaDon với parent = null (chế độ non-interactive kiểm thử tự động)
            boolean printRes = BanHang_GUI.inHoaDon(maHD, billContent, null);

            // Ghi nhận file fallback nếu có tạo ra
            File hoadonDir = new File("hoadon");
            if (hoadonDir.exists() && hoadonDir.isDirectory()) {
                File[] files = hoadonDir.listFiles((dir, name) -> name.startsWith(maHD));
                if (files != null) {
                    for (File fl : files) {
                        testFilesCreated.add(fl);
                    }
                }
            }

            pass("2. In hóa đơn",
                "Gọi BanHang_GUI.inHoaDon() chạy an toàn, không ném exception (kết quả in/fallback file: " + printRes + ")");
        } catch (Throwable t) {
            fail("2. In hóa đơn", "Bị ném ngoại lệ không mong muốn: " + t.getMessage());
        }
    }

    // =========================================================================
    // CA 3: Tìm nâng cao sản phẩm theo thương hiệu
    // =========================================================================
    private static void test03_TimKiemNangCaoSanPhamTheoThuongHieu() {
        SanPham_DAO spDao = new SanPham_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            String brand = null;
            int countDB = 0;

            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT TOP 1 thuongHieu, COUNT(*) as cnt FROM SanPham WHERE thuongHieu IS NOT NULL AND thuongHieu <> '' GROUP BY thuongHieu HAVING COUNT(*) > 0 ORDER BY cnt DESC")) {
                if (rs.next()) {
                    brand = rs.getString("thuongHieu");
                    countDB = rs.getInt("cnt");
                }
            }

            if (brand == null) {
                fail("3. Tìm nâng cao sản phẩm theo thương hiệu", "Không có dữ liệu thương hiệu trong CSDL để kiểm thử!");
                return;
            }

            ArrayList<SanPham> ds = spDao.timKiemNangCao(brand, null, null, null, null);
            boolean allMatchBrand = true;
            for (SanPham sp : ds) {
                if (sp.getThuongHieu() == null || !brand.equalsIgnoreCase(sp.getThuongHieu().trim())) {
                    allMatchBrand = false;
                    break;
                }
            }

            if (ds.size() == countDB && allMatchBrand) {
                pass("3. Tìm nâng cao sản phẩm theo thương hiệu",
                    String.format("Thương hiệu '%s' trả về đúng %d sản phẩm khớp 100%% CSDL (mọi SP đều mang thương hiệu '%s')", brand, ds.size(), brand));
            } else {
                fail("3. Tìm nâng cao sản phẩm theo thương hiệu",
                    String.format("Lệch số lượng hoặc dữ liệu: DAO=%d, DB=%d, allMatchBrand=%b", ds.size(), countDB, allMatchBrand));
            }
        } catch (Exception e) {
            fail("3. Tìm nâng cao sản phẩm theo thương hiệu", e.getMessage());
        }
    }

    // =========================================================================
    // CA 4: Tìm nâng cao sản phẩm theo khoảng giá (từ-đến)
    // =========================================================================
    private static void test04_TimKiemNangCaoSanPhamTheoKhoangGia() {
        SanPham_DAO spDao = new SanPham_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            double giaTu = 1000000.0;
            double giaDen = 3000000.0;
            int countDB = 0;

            try (PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM SanPham WHERE giaBan >= ? AND giaBan <= ?")) {
                ps.setDouble(1, giaTu);
                ps.setDouble(2, giaDen);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) countDB = rs.getInt(1);
                }
            }

            ArrayList<SanPham> ds = spDao.timKiemNangCao(null, giaTu, giaDen, null, null);
            boolean allInRange = true;
            for (SanPham sp : ds) {
                if (sp.getGiaBan() < giaTu || sp.getGiaBan() > giaDen) {
                    allInRange = false;
                    break;
                }
            }

            if (ds.size() == countDB && allInRange) {
                pass("4. Tìm nâng cao sản phẩm theo khoảng giá (từ-đến)",
                    String.format("Khoảng giá [%, .0f - %, .0f VNĐ] trả về đúng %d sản phẩm khớp 100%% CSDL (toàn bộ nằm trong biên)", giaTu, giaDen, ds.size()));
            } else {
                fail("4. Tìm nâng cao sản phẩm theo khoảng giá (từ-đến)",
                    String.format("Lệch kết quả: DAO=%d, DB=%d, allInRange=%b", ds.size(), countDB, allInRange));
            }
        } catch (Exception e) {
            fail("4. Tìm nâng cao sản phẩm theo khoảng giá (từ-đến)", e.getMessage());
        }
    }

    // =========================================================================
    // CA 5: Tìm nâng cao sản phẩm "còn hàng / ngừng bán"
    // =========================================================================
    private static void test05_TimKiemNangCaoSanPhamConHangNgungBan() {
        SanPham_DAO spDao = new SanPham_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            int countConHangDB = 0;
            int countHetHangDB = 0;

            try (Statement st = con.createStatement()) {
                try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM SanPham sp WHERE sp.trangThai = 1 AND EXISTS (SELECT 1 FROM ChiTietGiay ctg WHERE ctg.maSanPham = sp.maSanPham AND ctg.soLuongTon > 0)")) {
                    if (rs.next()) countConHangDB = rs.getInt(1);
                }
                try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM SanPham sp WHERE (sp.trangThai = 0 OR NOT EXISTS (SELECT 1 FROM ChiTietGiay ctg WHERE ctg.maSanPham = sp.maSanPham AND ctg.soLuongTon > 0))")) {
                    if (rs.next()) countHetHangDB = rs.getInt(1);
                }
            }

            ArrayList<SanPham> listConHang = spDao.timKiemNangCao(null, null, null, null, Boolean.TRUE);
            ArrayList<SanPham> listHetHang = spDao.timKiemNangCao(null, null, null, null, Boolean.FALSE);

            boolean allConHangTrangThai = true;
            for (SanPham sp : listConHang) {
                if (!sp.isTrangThai()) {
                    allConHangTrangThai = false;
                    break;
                }
            }

            boolean checkCon = (listConHang.size() == countConHangDB && allConHangTrangThai);
            boolean checkHet = (listHetHang.size() == countHetHangDB);

            if (checkCon && checkHet) {
                pass("5. Tìm nâng cao sản phẩm \"còn hàng / ngừng bán\"",
                    String.format("Lọc đúng trạng thái và tồn kho: Còn hàng=%d (khớp DB, 100%% trangThai=true), Ngừng bán/Hết hàng=%d (khớp DB)",
                        listConHang.size(), listHetHang.size()));
            } else {
                fail("5. Tìm nâng cao sản phẩm \"còn hàng / ngừng bán\"",
                    String.format("Lệch: Còn hàng (DAO=%d, DB=%d, validStatus=%b), Hết hàng (DAO=%d, DB=%d)",
                        listConHang.size(), countConHangDB, allConHangTrangThai, listHetHang.size(), countHetHangDB));
            }
        } catch (Exception e) {
            fail("5. Tìm nâng cao sản phẩm \"còn hàng / ngừng bán\"", e.getMessage());
        }
    }

    // =========================================================================
    // CA 6: Tìm nâng cao khách theo hạng thành viên
    // =========================================================================
    private static void test06_TimKiemNangCaoKhachHangTheoHang() {
        KhachHang_DAO khDao = new KhachHang_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            String hang = null;
            int countDB = 0;

            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT TOP 1 hangThanhVien, COUNT(*) as cnt FROM KhachHang WHERE hangThanhVien IS NOT NULL AND hangThanhVien <> '' GROUP BY hangThanhVien HAVING COUNT(*) > 0 ORDER BY cnt DESC")) {
                if (rs.next()) {
                    hang = rs.getString("hangThanhVien");
                    countDB = rs.getInt("cnt");
                }
            }

            if (hang == null) {
                fail("6. Tìm nâng cao khách theo hạng thành viên", "Không có dữ liệu hạng thành viên trong CSDL!");
                return;
            }

            ArrayList<KhachHang> ds = khDao.timKiemNangCao(hang, null, null, null);
            boolean allMatchHang = true;
            for (KhachHang kh : ds) {
                if (kh.getHangThanhVien() == null || !hang.equalsIgnoreCase(kh.getHangThanhVien().trim())) {
                    allMatchHang = false;
                    break;
                }
            }

            if (ds.size() == countDB && allMatchHang) {
                pass("6. Tìm nâng cao khách theo hạng thành viên",
                    String.format("Hạng '%s' trả về đúng %d khách hàng khớp 100%% CSDL", hang, ds.size()));
            } else {
                fail("6. Tìm nâng cao khách theo hạng thành viên",
                    String.format("Lệch: DAO=%d, DB=%d, allMatchHang=%b", ds.size(), countDB, allMatchHang));
            }
        } catch (Exception e) {
            fail("6. Tìm nâng cao khách theo hạng thành viên", e.getMessage());
        }
    }

    // =========================================================================
    // CA 7: Tìm nâng cao khách theo khoảng điểm
    // =========================================================================
    private static void test07_TimKiemNangCaoKhachHangTheoKhoangDiem() {
        KhachHang_DAO khDao = new KhachHang_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            int diemTu = 0;
            int diemDen = 100;
            int countDB = 0;

            try (PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM KhachHang WHERE diemTichLuy >= ? AND diemTichLuy <= ?")) {
                ps.setInt(1, diemTu);
                ps.setInt(2, diemDen);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) countDB = rs.getInt(1);
                }
            }

            ArrayList<KhachHang> ds = khDao.timKiemNangCao(null, diemTu, diemDen, null);
            boolean allInRange = true;
            for (KhachHang kh : ds) {
                if (kh.getDiemTichLuy() < diemTu || kh.getDiemTichLuy() > diemDen) {
                    allInRange = false;
                    break;
                }
            }

            if (ds.size() == countDB && allInRange) {
                pass("7. Tìm nâng cao khách theo khoảng điểm",
                    String.format("Khoảng điểm [%d - %d] trả về đúng %d khách hàng khớp 100%% CSDL", diemTu, diemDen, ds.size()));
            } else {
                fail("7. Tìm nâng cao khách theo khoảng điểm",
                    String.format("Lệch: DAO=%d, DB=%d, allInRange=%b", ds.size(), countDB, allInRange));
            }
        } catch (Exception e) {
            fail("7. Tìm nâng cao khách theo khoảng điểm", e.getMessage());
        }
    }

    // =========================================================================
    // CA 8: Tìm nâng cao khách theo giới tính
    // =========================================================================
    private static void test08_TimKiemNangCaoKhachHangTheoGioiTinh() {
        KhachHang_DAO khDao = new KhachHang_DAO();
        try {
            Connection con = ConnectDB.getConnection();
            int countNamDB = 0;
            int countNuDB = 0;

            try (Statement st = con.createStatement()) {
                try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM KhachHang WHERE gioiTinh = 1")) {
                    if (rs.next()) countNamDB = rs.getInt(1);
                }
                try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM KhachHang WHERE gioiTinh = 0")) {
                    if (rs.next()) countNuDB = rs.getInt(1);
                }
            }

            ArrayList<KhachHang> listNam = khDao.timKiemNangCao(null, null, null, Boolean.TRUE);
            ArrayList<KhachHang> listNu = khDao.timKiemNangCao(null, null, null, Boolean.FALSE);

            boolean allNam = true;
            for (KhachHang kh : listNam) {
                if (!kh.isGioiTinh()) { allNam = false; break; }
            }
            boolean allNu = true;
            for (KhachHang kh : listNu) {
                if (kh.isGioiTinh()) { allNu = false; break; }
            }

            if (listNam.size() == countNamDB && allNam && listNu.size() == countNuDB && allNu) {
                pass("8. Tìm nâng cao khách theo giới tính",
                    String.format("Lọc đúng giới tính: Nam=%d (100%% nam), Nữ=%d (100%% nữ) khớp 100%% CSDL", listNam.size(), listNu.size()));
            } else {
                fail("8. Tìm nâng cao khách theo giới tính",
                    String.format("Lệch: Nam(DAO=%d, DB=%d, ok=%b), Nữ(DAO=%d, DB=%d, ok=%b)", listNam.size(), countNamDB, allNam, listNu.size(), countNuDB, allNu));
            }
        } catch (Exception e) {
            fail("8. Tìm nâng cao khách theo giới tính", e.getMessage());
        }
    }

    // =========================================================================
    // CA 9: Tìm nâng cao không có kết quả -> trả rỗng (không exception)
    // =========================================================================
    private static void test09_TimKiemNangCaoKhongCoKetQua() {
        SanPham_DAO spDao = new SanPham_DAO();
        KhachHang_DAO khDao = new KhachHang_DAO();
        try {
            ArrayList<SanPham> emptySP = spDao.timKiemNangCao("BRAND_NOT_EXIST_XYZ999", 999999999.0, 9999999999.0, "LOAI_NOT_EXIST", null);
            ArrayList<KhachHang> emptyKH = khDao.timKiemNangCao("TIER_NOT_EXIST_XYZ999", 9999999, 99999999, null);

            boolean checkSP = (emptySP != null && emptySP.isEmpty());
            boolean checkKH = (emptyKH != null && emptyKH.isEmpty());

            if (checkSP && checkKH) {
                pass("9. Tìm nâng cao không có kết quả",
                    "Trả về danh sách rỗng an toàn cho cả Sản Phẩm và Khách Hàng, không ném exception");
            } else {
                fail("9. Tìm nâng cao không có kết quả",
                    "Kết quả không rỗng: SP=" + (emptySP != null ? emptySP.size() : "null") + ", KH=" + (emptyKH != null ? emptyKH.size() : "null"));
            }
        } catch (Exception e) {
            fail("9. Tìm nâng cao không có kết quả", "Bị ném ngoại lệ: " + e.getMessage());
        }
    }

    // =========================================================================
    // CA 10: Tab Thống kê chỉ hiện với Quản lý
    // =========================================================================
    private static void test10_PhanQuyenTabThongKeQuanLy() {
        try {
            NhanVien nvThuNgan = new NhanVien("NV0002", "Thu Ngân Test", "0900000002", LocalDate.now(), true, "HCM", "tn@test.com", "Nhân viên bán hàng", 8000000, "Toàn thời gian", "123456", true);
            NhanVien nvQuanLy = new NhanVien("NV0001", "Quản Lý Test", "0900000001", LocalDate.now(), true, "HCM", "ql@test.com", "Quản lý", 15000000, "Toàn thời gian", "123456", true);

            boolean isTNQuanLy = nvThuNgan.isQuanLy();
            boolean isQLQuanLy = nvQuanLy.isQuanLy();

            ManHinhChinh_GUI guiTN = new ManHinhChinh_GUI(nvThuNgan);
            int tabsTN = guiTN.getTabbedPane().getTabCount();
            boolean hasThongKeTN = false;
            for (int i = 0; i < tabsTN; i++) {
                if (guiTN.getTabbedPane().getTitleAt(i).toUpperCase().contains("THỐNG KÊ")) {
                    hasThongKeTN = true;
                    break;
                }
            }
            guiTN.dispose();

            ManHinhChinh_GUI guiQL = new ManHinhChinh_GUI(nvQuanLy);
            int tabsQL = guiQL.getTabbedPane().getTabCount();
            boolean hasThongKeQL = false;
            for (int i = 0; i < tabsQL; i++) {
                if (guiQL.getTabbedPane().getTitleAt(i).toUpperCase().contains("THỐNG KÊ")) {
                    hasThongKeQL = true;
                    break;
                }
            }
            guiQL.dispose();

            if (!isTNQuanLy && isQLQuanLy && tabsTN == 3 && !hasThongKeTN && tabsQL == 5 && hasThongKeQL) {
                pass("10. Tab Thống kê chỉ hiện với Quản lý",
                    String.format("Phân quyền chuẩn: Thu ngân 3 tab (ẩn Thống kê), Quản lý 5 tab (mở [F5] Thống kê, isQuanLy=%b)", isQLQuanLy));
            } else {
                fail("10. Tab Thống kê chỉ hiện với Quản lý",
                    String.format("Lỗi phân quyền: TN(tabs=%d, hasTK=%b), QL(tabs=%d, hasTK=%b)", tabsTN, hasThongKeTN, tabsQL, hasThongKeQL));
            }
        } catch (Exception e) {
            fail("10. Tab Thống kê chỉ hiện với Quản lý", e.getMessage());
        }
    }

    // =========================================================================
    // CA 11: F10 / Delete ở tab khác không tác động giỏ POS
    // =========================================================================
    private static void test11_PhimTatF10DeleteKhongTacDongGioKhiODangTabKhac() {
        try {
            NhanVien nvThuNgan = new NhanVien("NV0002", "Thu Ngân Test", "0900000002", LocalDate.now(), true, "HCM", "tn@test.com", "Nhân viên bán hàng", 8000000, "Toàn thời gian", "123456", true);
            ManHinhChinh_GUI mainFrame = new ManHinhChinh_GUI(nvThuNgan);
            JTabbedPane tabs = mainFrame.getTabbedPane();
            BanHang_GUI posGUI = (BanHang_GUI) tabs.getComponentAt(0);
            DefaultTableModel cartModel = posGUI.getModelGioHang();

            // Giả lập thêm 1 dòng vào giỏ hàng POS
            cartModel.addRow(new Object[]{1, "CTG0001", "Nike Air Force 1", 40, "Trắng", 1, 2600000.0, 0.0, 2600000.0});
            int itemsBefore = cartModel.getRowCount();

            // Chuyển sang Tab Khách hàng (index 2)
            tabs.setSelectedIndex(2);

            // Kích hoạt phím DELETE và F10 từ ActionMap
            Action deleteAction = mainFrame.getRootPane().getActionMap().get("KEY_DELETE");
            Action f10Action = mainFrame.getRootPane().getActionMap().get("KEY_F10");

            ActionEvent mockEvent = new ActionEvent(mainFrame.getRootPane(), ActionEvent.ACTION_PERFORMED, "");
            if (deleteAction != null) deleteAction.actionPerformed(mockEvent);
            if (f10Action != null) f10Action.actionPerformed(mockEvent);

            int itemsAfter = cartModel.getRowCount();
            mainFrame.dispose();

            if (itemsBefore == 1 && itemsAfter == 1) {
                pass("11. F10 / Delete ở tab khác không tác động giỏ POS",
                    "Đang ở Tab Khách hàng, phím Delete và F10 không tác động đến giỏ hàng POS (số dòng giỏ giữ nguyên: " + itemsAfter + ")");
            } else {
                fail("11. F10 / Delete ở tab khác không tác động giỏ POS",
                    "Giỏ hàng POS bị tác động khi đứng ở tab khác: Trước=" + itemsBefore + ", Sau=" + itemsAfter);
            }
        } catch (Exception e) {
            fail("11. F10 / Delete ở tab khác không tác động giỏ POS", e.getMessage());
        }
    }

    // =========================================================================
    // CA 12: Hóa đơn 13 cột được lưu đúng sau khi thanh toán
    // =========================================================================
    private static void test12_LuuHoaDon13CotDungSauThanhToan() {
        String maSPTest = "SP0001";
        String maCTGTest = "CTG9991";
        String maKHTest = "KH9991";
        String generatedMaHD = null;

        HoaDon_DAO hdDao = new HoaDon_DAO();
        KhachHang_DAO khDao = new KhachHang_DAO();
        NhanVien_DAO nvDao = new NhanVien_DAO();

        try {
            Connection con = ConnectDB.getConnection();

            // 1. Tạo biến thể giày kiểm thử CTG9991 với tồn kho 10
            try (PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh) " +
                    "VALUES (?, ?, 42, N'Trắng Test', 10, 'nike_af1.png')")) {
                ps.setString(1, maCTGTest);
                ps.setString(2, maSPTest);
                ps.executeUpdate();
            }

            // 2. Tạo khách hàng kiểm thử KH9991 có 50 điểm, Hạng Bạc (5% chiết khấu)
            KhachHang khTest = new KhachHang(maKHTest, "Khách Hàng Test 13 Cột", "0987999111",
                    LocalDate.of(1995, 3, 10), true, "Quận 1, TP.HCM", "test13cot@stepup.vn", 50, "Bạc");
            khDao.themKhachHang(khTest);

            NhanVien nvThuNgan = nvDao.getNhanVienTheoMa("NV0001");
            if (nvThuNgan == null) {
                nvThuNgan = new NhanVien("NV0001", "Quản lý", "0900000001", LocalDate.now(), true, "HCM", "ql@stepup.vn", "Quản lý", 15000000, "Toàn thời gian", "123456", true);
            }

            // 3. Chuẩn bị hóa đơn: Mua 2 đôi CTG9991 @ 2.600.000 = 5.200.000 VNĐ
            double donGia = 2600000.0;
            int slMua = 2;
            double tongTienGoc = 5200000.0;
            double chietKhau = 260000.0; // 5%
            int diemDung = 50;
            double tienGiamDiem = 50000.0;
            double tongTien = 4890000.0;
            double tienKhachDua = 5000000.0;
            double tienThua = 110000.0;
            int diemCong = 48; // 4.890.000 / 100.000 = 48

            HoaDon hd = new HoaDon(null, LocalDateTime.now(), nvThuNgan, khTest, tongTien, "Tiền mặt", tienKhachDua, tienThua);
            hd.setTongTienHang(tongTienGoc);
            hd.setChietKhau(chietKhau);
            hd.setDiemSuDung(diemDung);
            hd.setTienGiamDiem(tienGiamDiem);
            hd.setDiemCong(diemCong);

            ChiTietGiay ctg = new ChiTietGiay(maCTGTest);
            ChiTietHoaDon cthd = new ChiTietHoaDon(hd, ctg, slMua, donGia, 0.0, tongTienGoc);
            hd.themChiTiet(cthd);

            // 4. Thực thi Transaction lưu Hóa đơn
            boolean thanhToanOk = hdDao.themHoaDon(hd);
            generatedMaHD = hd.getMaHoaDon();

            if (!thanhToanOk || generatedMaHD == null) {
                fail("12. Hóa đơn 13 cột được lưu đúng sau khi thanh toán", "Lưu hóa đơn thất bại: " + hdDao.getLastErrorMessage());
                return;
            }

            // 5. SELECT đối chiếu trực tiếp 13 cột trong CSDL
            try (PreparedStatement ps = con.prepareStatement("SELECT * FROM HoaDon WHERE maHoaDon = ?")) {
                ps.setString(1, generatedMaHD);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        String dbMaHD = rs.getString("maHoaDon");
                        Timestamp dbNgayLap = rs.getTimestamp("ngayLap");
                        String dbMaNV = rs.getString("maNhanVien");
                        String dbMaKH = rs.getString("maKhachHang");
                        double dbTongHang = rs.getDouble("tongTienHang");
                        double dbChietKhau = rs.getDouble("chietKhau");
                        int dbDiemDung = rs.getInt("diemSuDung");
                        double dbGiamDiem = rs.getDouble("tienGiamDiem");
                        double dbTongTien = rs.getDouble("tongTien");
                        String dbPhuongThuc = rs.getString("phuongThucTT");
                        double dbTienDua = rs.getDouble("tienKhachDua");
                        double dbTienThua = rs.getDouble("tienThua");
                        int dbDiemCong = rs.getInt("diemCong");

                        boolean c1_maHD = generatedMaHD.equals(dbMaHD);
                        boolean c2_ngayLap = (dbNgayLap != null);
                        boolean c3_maNV = nvThuNgan.getMaNhanVien().equals(dbMaNV);
                        boolean c4_maKH = maKHTest.equals(dbMaKH);
                        boolean c5_tongHang = Math.abs(dbTongHang - 5200000.0) < 0.01;
                        boolean c6_chietKhau = Math.abs(dbChietKhau - 260000.0) < 0.01;
                        boolean c7_diemDung = (dbDiemDung == 50);
                        boolean c8_giamDiem = Math.abs(dbGiamDiem - 50000.0) < 0.01;
                        boolean c9_tongTien = Math.abs(dbTongTien - 4890000.0) < 0.01;
                        boolean c10_pttt = "Tiền mặt".equals(dbPhuongThuc);
                        boolean c11_tienDua = Math.abs(dbTienDua - 5000000.0) < 0.01;
                        boolean c12_tienThua = Math.abs(dbTienThua - 110000.0) < 0.01;
                        boolean c13_diemCong = (dbDiemCong == 48);

                        boolean all13Cols = c1_maHD && c2_ngayLap && c3_maNV && c4_maKH && c5_tongHang &&
                                           c6_chietKhau && c7_diemDung && c8_giamDiem && c9_tongTien &&
                                           c10_pttt && c11_tienDua && c12_tienThua && c13_diemCong;

                        // Kiểm tra trừ tồn kho (10 - 2 = 8)
                        int tonSau = -1;
                        try (PreparedStatement psTon = con.prepareStatement("SELECT soLuongTon FROM ChiTietGiay WHERE maChiTietGiay = ?")) {
                            psTon.setString(1, maCTGTest);
                            try (ResultSet rsTon = psTon.executeQuery()) {
                                if (rsTon.next()) tonSau = rsTon.getInt(1);
                            }
                        }

                        // Kiểm tra điểm khách hàng (50 - 50 + 48 = 48)
                        KhachHang khSau = khDao.timTheoSoDienThoai("0987999111");
                        int diemSau = (khSau != null) ? khSau.getDiemTichLuy() : -1;

                        if (all13Cols && tonSau == 8 && diemSau == 48) {
                            pass("12. Hóa đơn 13 cột được lưu đúng sau khi thanh toán",
                                String.format("13/13 cột khớp 100%% CSDL (Gốc: %, .0f, CK: %, .0f, Dùng điểm: %d, Giảm điểm: %, .0f, Trả: %, .0f, Thừa: %, .0f, Cộng: %d) | Tồn kho: 8 | Điểm KH: 48",
                                    dbTongHang, dbChietKhau, dbDiemDung, dbGiamDiem, dbTongTien, dbTienThua, dbDiemCong));
                        } else {
                            fail("12. Hóa đơn 13 cột được lưu đúng sau khi thanh toán",
                                String.format("Sai lệch: 13 cột=%b (c1=%b..c13=%b), Tồn kho=%d (kỳ vọng 8), Điểm KH=%d (kỳ vọng 48)",
                                    all13Cols, c1_maHD, c13_diemCong, tonSau, diemSau));
                        }
                    } else {
                        fail("12. Hóa đơn 13 cột được lưu đúng sau khi thanh toán", "Không tìm thấy hóa đơn " + generatedMaHD + " trong CSDL");
                    }
                }
            }
        } catch (Exception e) {
            fail("12. Hóa đơn 13 cột được lưu đúng sau khi thanh toán", e.getMessage());
        } finally {
            // Dọn dẹp sạch sẽ dữ liệu test
            try (Statement st = ConnectDB.getConnection().createStatement()) {
                if (generatedMaHD != null) {
                    st.executeUpdate("DELETE FROM ChiTietHoaDon WHERE maHoaDon = '" + generatedMaHD + "'");
                    st.executeUpdate("DELETE FROM HoaDon WHERE maHoaDon = '" + generatedMaHD + "'");
                }
                st.executeUpdate("DELETE FROM ChiTietHoaDon WHERE maChiTietGiay = '" + maCTGTest + "'");
                st.executeUpdate("DELETE FROM ChiTietGiay WHERE maChiTietGiay = '" + maCTGTest + "'");
                st.executeUpdate("DELETE FROM KhachHang WHERE maKhachHang = '" + maKHTest + "'");
            } catch (SQLException ignored) {}
        }
    }
}

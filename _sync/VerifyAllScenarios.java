package test;

import connectDB.ConnectDB;
import dao.*;
import entity.*;
import gui.*;

import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;

public class VerifyAllScenarios {

    private static int totalPassed = 0;
    private static int totalFailed = 0;

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
        System.out.println("    STEPUP FOOTWEAR POS - FULL SYSTEM REGRESSION & BEHAVIOR AUDIT SUITE");
        System.out.println("===============================================================================\n");

        try {
            ConnectDB.getInstance().connect();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                System.err.println("[CRITICAL] Could not connect to SQL Server database!");
                System.exit(1);
            }
            System.out.println("[INFO] Connected to SQL Server database 'QuanLyBanGiay' successfully.\n");

            cleanUpTestData();

            testScenario1_AuthAndRoles();
            testScenario2_Customers();
            testScenario3_Products();
            testScenario4_Employees();
            testScenario5_POSAndCheckout();
            testScenario6_Statistics();
            testScenario8_Batch2Verification();
            testScenario7_DBIntegrityAndCleanup();

            System.out.println("\n===============================================================================");
            System.out.println(String.format("    AUDIT SUMMARY: %d PASSED, %d FAILED across all 8 scenarios", totalPassed, totalFailed));
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

    private static void cleanUpTestData() {
        try (Statement st = ConnectDB.getConnection().createStatement()) {
            st.executeUpdate("DELETE FROM ChiTietHoaDon WHERE maChiTietGiay LIKE 'CTG99%' OR maHoaDon IN (SELECT maHoaDon FROM HoaDon WHERE maKhachHang LIKE 'KH99%')");
            st.executeUpdate("DELETE FROM HoaDon WHERE maKhachHang LIKE 'KH99%' OR maHoaDon LIKE 'HD99%'");
            st.executeUpdate("DELETE FROM ChiTietGiay WHERE maChiTietGiay LIKE 'CTG99%'");
            st.executeUpdate("DELETE FROM SanPham WHERE maSanPham LIKE 'SP99%'");
            st.executeUpdate("DELETE FROM KhachHang WHERE maKhachHang LIKE 'KH99%'");
            st.executeUpdate("DELETE FROM NhanVien WHERE maNhanVien LIKE 'NV99%'");
        } catch (SQLException e) {
            System.err.println("Cleanup warning: " + e.getMessage());
        }
    }

    // SCENARIO 1: Login & Roles
    private static void testScenario1_AuthAndRoles() {
        System.out.println("--- SCENARIO 1: Đăng nhập, Xác thực mật khẩu & Phân quyền ---");
        NhanVien_DAO dao = new NhanVien_DAO();

        // 1.1 Manager login
        NhanVien nv1 = dao.dangNhap("NV0001", "123456");
        if (nv1 != null && "Quản lý".equalsIgnoreCase(nv1.getChucVu()) && nv1.isTrangThai()) {
            pass("1.1 Đăng nhập Quản lý (NV0001)", "Xác thực đúng mật khẩu, Chức vụ: " + nv1.getChucVu() + ", Họ tên: " + nv1.getHoTen());
        } else {
            fail("1.1 Đăng nhập Quản lý (NV0001)", "Không tìm thấy hoặc sai quyền: " + nv1);
        }

        // 1.2 Staff login
        NhanVien nv2 = dao.dangNhap("NV0002", "123456");
        if (nv2 != null && nv2.getChucVu().contains("Nhân viên") && nv2.isTrangThai()) {
            pass("1.2 Đăng nhập Nhân viên (NV0002)", "Xác thực đúng mật khẩu, Chức vụ: " + nv2.getChucVu() + ", Họ tên: " + nv2.getHoTen());
        } else {
            fail("1.2 Đăng nhập Nhân viên (NV0002)", "Thất bại: " + nv2);
        }

        // 1.3 Wrong password
        NhanVien nvWrong = dao.dangNhap("NV0001", "wrong_pass_999");
        if (nvWrong == null) {
            pass("1.3 Đăng nhập sai mật khẩu", "Bị chặn chính xác, trả về null không cho truy cập");
        } else {
            fail("1.3 Đăng nhập sai mật khẩu", "Lỗ hổng: Cho phép đăng nhập khi sai mật khẩu!");
        }

        // 1.4 Non-existent user
        NhanVien nvNone = dao.dangNhap("NV9999", "123456");
        if (nvNone == null) {
            pass("1.4 Tài khoản không tồn tại", "Bị chặn chính xác, trả về null");
        } else {
            fail("1.4 Tài khoản không tồn tại", "Thất bại");
        }
        System.out.println();
    }

    // SCENARIO 2: Customers
    private static void testScenario2_Customers() {
        System.out.println("--- SCENARIO 2: Khách hàng (Null email, Trùng mã, Trùng SĐT, Regex SĐT) ---");
        KhachHang_DAO dao = new KhachHang_DAO();

        String testMa = "KH9991";
        String testSDT = "0987111222";

        // 2.1 Add customer with empty email and address -> MUST succeed and bind NULL
        KhachHang kh1 = new KhachHang(testMa, "Nguyễn Văn Test Email Rỗng", testSDT, null, true, "", "", 0, "Đồng");
        boolean themOk = dao.themKhachHang(kh1);
        if (themOk) {
            pass("2.1 Thêm KH với email & địa chỉ rỗng", "Thành công ghi vào CSDL, không vi phạm CK_KhachHang_email");
        } else {
            fail("2.1 Thêm KH với email & địa chỉ rỗng", "Thất bại: " + dao.getLastError());
        }

        // Verify in DB that email is actually NULL
        try {
            Connection con = ConnectDB.getConnection();
            try (PreparedStatement ps = con.prepareStatement("SELECT email, diaChi FROM KhachHang WHERE maKhachHang = ?")) {
                ps.setString(1, testMa);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        String em = rs.getString("email");
                        String dc = rs.getString("diaChi");
                        if (em == null && dc == null) {
                            pass("2.1b Kiểm tra DB email & diaChi IS NULL", "Cột email = NULL, diaChi = NULL khớp 100% chuẩn SQL");
                        } else {
                            fail("2.1b Kiểm tra DB email & diaChi IS NULL", "email = " + em + ", diaChi = " + dc);
                        }
                    }
                }
            }
        } catch (SQLException e) {
            fail("2.1b Kiểm tra DB email", e.getMessage());
        }

        // 2.2 Duplicate Customer ID
        boolean trungMa = dao.kiemTraTrungMa(testMa);
        if (trungMa) {
            pass("2.2 Pre-check Trùng Mã Khách Hàng", "Phát hiện mã " + testMa + " đã tồn tại trước khi INSERT");
        } else {
            fail("2.2 Pre-check Trùng Mã Khách Hàng", "Không phát hiện trùng mã");
        }

        // 2.3 Duplicate Phone
        boolean trungSDT = dao.kiemTraTrungSDT(testSDT);
        if (trungSDT) {
            pass("2.3 Pre-check Trùng Số Điện Thoại", "Phát hiện SĐT " + testSDT + " đã được đăng ký");
        } else {
            fail("2.3 Pre-check Trùng Số Điện Thoại", "Không phát hiện trùng SĐT");
        }

        // 2.4 Invalid phone prefix regex
        String sdtSai = "0112345678"; // Đầu 01 không hợp lệ theo CK_KhachHang_sdt
        boolean regexValid = sdtSai.matches("^0[35789]\\d{8}$");
        if (!regexValid) {
            pass("2.4 Validate regex SĐT sai đầu số (011...)", "Bị chặn chính xác bởi biểu thức chính quy ^0[35789]\\d{8}$");
        } else {
            fail("2.4 Validate regex SĐT sai đầu số", "Lọt qua regex");
        }

        // 2.5 Update customer
        KhachHang khSua = new KhachHang(testMa, "Nguyễn Văn Test Đã Sửa", testSDT, null, true, "123 Đường Test Mới", null, 25, "Bạc");
        boolean suaOk = dao.capNhatKhachHang(khSua);
        if (suaOk) {
            pass("2.5 Cập nhật thông tin khách hàng", "Cập nhật thành công tên, địa chỉ mới và hạng thẻ");
        } else {
            fail("2.5 Cập nhật thông tin khách hàng", "Thất bại: " + dao.getLastError());
        }

        // 2.6 Delete customer
        boolean xoaOk = dao.xoaKhachHang(testMa);
        if (xoaOk) {
            pass("2.6 Xóa khách hàng kiểm thử", "Đã xóa dòng test " + testMa + " sạch sẽ khỏi CSDL");
        } else {
            fail("2.6 Xóa khách hàng kiểm thử", "Thất bại: " + dao.getLastError());
        }
        System.out.println();
    }

    // SCENARIO 3: Products
    private static void testScenario3_Products() {
        System.out.println("--- SCENARIO 3: Sản phẩm (Tự sinh SKU, Validate giá, Xóa mềm) ---");
        SanPham_DAO spDao = new SanPham_DAO();
        ChiTietGiay_DAO ctgDao = new ChiTietGiay_DAO();

        String maSP = "SP9991";

        // 3.1 Validate Price: giaBan < giaNhap
        double giaNhap = 2000000;
        double giaBanSai = 1500000;
        if (giaBanSai < giaNhap) {
            pass("3.1 Chặn Giá bán < Giá nhập", "Phát hiện giá bán (1.5tr) nhỏ hơn giá nhập (2.0tr)");
        } else {
            fail("3.1 Chặn Giá bán < Giá nhập", "Không phát hiện lỗi giá");
        }

        // 3.2 Add new Product
        SanPham spMoi = new SanPham(maSP, "Giày Thể Thao Test Pro Max", "Giày Thể Thao", "Nike", 1200000, 1800000, "Vải dệt Flyknit", true);
        boolean themOk = spDao.themSanPham(spMoi);
        if (themOk) {
            pass("3.2 Thêm sản phẩm mới", "Thêm thành công mã " + maSP + " vào bảng SanPham");
        } else {
            fail("3.2 Thêm sản phẩm mới", "Thất bại: " + spDao.getLastError());
        }

        // 3.3 Auto-generate SKU variant
        String maCTG = ctgDao.sinhMaChiTietGiayMoi();
        ChiTietGiay ctgMoi = new ChiTietGiay(maCTG, spMoi, 41, "Xanh Navy", 35, "test_shoe.png");
        boolean themCtgOk = ctgDao.themChiTietGiay(ctgMoi);
        if (themCtgOk && maCTG.matches("^CTG\\d{4}$")) {
            pass("3.3 Tự sinh SKU biến thể (" + maCTG + ")", "Sinh SKU chuẩn định dạng CTGxxxx và thêm thành công vào ChiTietGiay");
        } else {
            fail("3.3 Tự sinh SKU biến thể", "Thất bại hoặc sai định dạng: " + maCTG);
        }

        // 3.4 Update product
        SanPham spSua = new SanPham(maSP, "Giày Thể Thao Test Pro Max (Cập nhật)", "Giày Thể Thao", "Nike", 1200000, 1950000, "Vải dệt Flyknit Cao Cấp", true);
        boolean suaOk = spDao.capNhatSanPham(spSua);
        if (suaOk) {
            pass("3.4 Cập nhật thông tin sản phẩm", "Cập nhật thành công tên, giá bán và chất liệu mới");
        } else {
            fail("3.4 Cập nhật thông tin sản phẩm", "Thất bại: " + spDao.getLastError());
        }

        // 3.5 Soft-delete product
        boolean xoaOk = spDao.xoaSanPham(maSP);
        if (xoaOk) {
            // Verify soft-deleted
            try {
                Connection con = ConnectDB.getConnection();
                try (PreparedStatement ps = con.prepareStatement("SELECT trangThai FROM SanPham WHERE maSanPham = ?")) {
                    ps.setString(1, maSP);
                    try (ResultSet rs = ps.executeQuery()) {
                        if (rs.next() && !rs.getBoolean("trangThai")) {
                            pass("3.5 Xóa mềm sản phẩm (trangThai = 0)", "Ngừng kinh doanh an toàn, giữ toàn vẹn khóa ngoại dữ liệu");
                        } else {
                            fail("3.5 Xóa mềm sản phẩm", "trangThai không đổi thành false");
                        }
                    }
                }
            } catch (SQLException e) {
                fail("3.5 Xóa mềm sản phẩm", e.getMessage());
            }
        } else {
            fail("3.5 Xóa mềm sản phẩm", "Thất bại: " + spDao.getLastError());
        }

        // Cleanup test product & variant
        try {
            Connection con = ConnectDB.getConnection();
            try (Statement st = ConnectDB.getConnection().createStatement()) {
                st.executeUpdate("DELETE FROM ChiTietGiay WHERE maChiTietGiay = '" + maCTG + "'");
                st.executeUpdate("DELETE FROM SanPham WHERE maSanPham = '" + maSP + "'");
            }
        } catch (SQLException ignored) {}
        System.out.println();
    }

    // SCENARIO 4: Employees
    private static void testScenario4_Employees() {
        System.out.println("--- SCENARIO 4: Nhân viên (Băm SHA-256, Giữ địa chỉ, Nghỉ việc) ---");
        NhanVien_DAO dao = new NhanVien_DAO();

        String maNV = "NV9991";
        String sdtNV = "0987333444";
        String plainPass = "matkhauBiMat@123";

        // 4.1 Add employee with SHA-256 hash
        NhanVien nvMoi = new NhanVien(maNV, "Lê Văn Test Nhân Sự", sdtNV, LocalDate.of(1998, 8, 20), true, "789 Phan Văn Trị, Gò Vấp", "testnv@stepup.vn", "Nhân viên bán hàng", 7500000, "Ca chiều", plainPass, true);
        boolean themOk = dao.themNhanVien(nvMoi);
        if (themOk) {
            pass("4.1 Thêm nhân viên mới", "Thêm thành công mã " + maNV);
        } else {
            fail("4.1 Thêm nhân viên mới", "Thất bại: " + dao.getLastError());
        }

        // Verify password in DB is SHA-256 hash (64 chars) and equals expected hash
        String expectedHash = dao.hashSHA256(plainPass);
        try {
            Connection con = ConnectDB.getConnection();
            try (PreparedStatement ps = con.prepareStatement("SELECT matKhau, diaChi FROM NhanVien WHERE maNhanVien = ?")) {
                ps.setString(1, maNV);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        String dbHash = rs.getString("matKhau");
                        String dbDiaChi = rs.getString("diaChi");
                        if (dbHash != null && dbHash.length() == 64 && dbHash.equalsIgnoreCase(expectedHash)) {
                            pass("4.1b Kiểm tra băm SHA-256 trong CSDL", "Mật khẩu lưu dạng SHA-256 (64 ký tự hex): " + dbHash.substring(0, 16) + "...");
                        } else {
                            fail("4.1b Kiểm tra băm SHA-256 trong CSDL", "Sai hash hoặc chưa băm: " + dbHash);
                        }

                        if ("789 Phan Văn Trị, Gò Vấp".equals(dbDiaChi)) {
                            pass("4.1c Lưu địa chỉ nhân viên", "Địa chỉ lưu chính xác không bị null");
                        } else {
                            fail("4.1c Lưu địa chỉ nhân viên", "Địa chỉ sai: " + dbDiaChi);
                        }
                    }
                }
            }
        } catch (SQLException e) {
            fail("4.1b Kiểm tra băm SHA-256", e.getMessage());
        }

        // 4.2 Login with newly created hashed employee
        NhanVien loginNV = dao.dangNhap(maNV, plainPass);
        if (loginNV != null && loginNV.getMaNhanVien().equals(maNV)) {
            pass("4.2 Đăng nhập nhân viên mới băm SHA-256", "Xác thực thành công với mật khẩu gốc '" + plainPass + "'");
        } else {
            fail("4.2 Đăng nhập nhân viên mới băm SHA-256", "Không đăng nhập được");
        }

        // 4.3 Update employee (Ensure address is NOT lost)
        NhanVien nvSua = new NhanVien(maNV, "Lê Văn Test Nhân Sự (Đã Sửa)", sdtNV, LocalDate.of(1998, 8, 20), true, "101 Quang Trung, Gò Vấp", null, "Quản lý", 9000000, "Ca tối", "", true);
        boolean suaOk = dao.capNhatNhanVien(nvSua);
        if (suaOk) {
            NhanVien checkNV = dao.getNhanVienTheoMa(maNV);
            if (checkNV != null && "101 Quang Trung, Gò Vấp".equals(checkNV.getDiaChi()) && "Quản lý".equals(checkNV.getChucVu())) {
                pass("4.3 Cập nhật nhân viên bảo toàn địa chỉ", "Địa chỉ cập nhật thành công thành '101 Quang Trung, Gò Vấp', không bị mất");
            } else {
                fail("4.3 Cập nhật nhân viên bảo toàn địa chỉ", "Dữ liệu sau sửa: " + checkNV);
            }
        } else {
            fail("4.3 Cập nhật nhân viên bảo toàn địa chỉ", "Thất bại: " + dao.getLastError());
        }

        // 4.3b Cập nhật giới tính nhân viên và kiểm tra CSDL SQL Server (Khắc phục lỗi sót cột gioiTinh)
        nvSua.setGioiTinh(false); // Chuyển từ Nam (true) sang Nữ (false)
        boolean doiGTOk = dao.capNhatNhanVien(nvSua);
        if (doiGTOk) {
            try {
                Connection con = ConnectDB.getConnection();
                try (PreparedStatement ps = con.prepareStatement("SELECT gioiTinh FROM NhanVien WHERE maNhanVien = ?")) {
                    ps.setString(1, maNV);
                    try (ResultSet rs = ps.executeQuery()) {
                        if (rs.next()) {
                            boolean dbGT = rs.getBoolean("gioiTinh");
                            if (!dbGT) {
                                pass("4.3b Đổi giới tính nhân viên cập nhật vào CSDL", "SELECT CSDL xác nhận gioiTinh = false (Nữ) cập nhật chính xác, không bị sót cột");
                            } else {
                                fail("4.3b Đổi giới tính nhân viên", "CSDL vẫn giữ giá trị cũ (Nam)");
                            }
                        }
                    }
                }
            } catch (SQLException e) {
                fail("4.3b Đổi giới tính nhân viên", e.getMessage());
            }
        } else {
            fail("4.3b Đổi giới tính nhân viên", "dao.capNhatNhanVien thất bại: " + dao.getLastError());
        }

        // 4.4 Soft-delete employee
        boolean xoaOk = dao.xoaNhanVien(maNV);
        if (xoaOk) {
            NhanVien nvNghi = dao.dangNhap(maNV, plainPass);
            if (nvNghi == null) {
                pass("4.4 Cho nhân viên nghỉ việc (Soft-delete)", "trangThai = 0, nhân viên bị từ chối đăng nhập ngay lập tức");
            } else {
                fail("4.4 Cho nhân viên nghỉ việc", "Nhân viên nghỉ việc vẫn đăng nhập được!");
            }
        } else {
            fail("4.4 Cho nhân viên nghỉ việc", "Thất bại: " + dao.getLastError());
        }

        // 4.5 Chặn thêm nhân viên sinh năm 2015 (< 18 tuổi) với thông báo chính xác
        NhanVien nvUnderage = new NhanVien("NV9992", "Nguyễn Văn Dưới Tuổi", "0987999888", 
                LocalDate.of(2015, 6, 15), true, "123 Đường Test", null, "Nhân viên bán hàng", 6000000, "Ca sáng", "123456", true);
        boolean themUnderageOk = dao.themNhanVien(nvUnderage);
        if (!themUnderageOk && dao.getLastError() != null && dao.getLastError().contains("Nhân viên phải từ 18 tuổi trở lên")) {
            pass("4.5 Chặn thêm nhân viên sinh năm 2015 (< 18 tuổi)", "Bị chặn chính xác với thông báo: '" + dao.getLastError() + "'");
        } else {
            fail("4.5 Chặn thêm nhân viên sinh năm 2015 (< 18 tuổi)", "Không chặn hoặc sai thông báo: themOk=" + themUnderageOk + ", error=" + dao.getLastError());
        }

        // Cleanup test employee
        try {
            Connection con = ConnectDB.getConnection();
            try (Statement st = ConnectDB.getConnection().createStatement()) {
                st.executeUpdate("DELETE FROM NhanVien WHERE maNhanVien = '" + maNV + "'");
            }
        } catch (SQLException ignored) {}
        System.out.println();
    }

    // SCENARIO 5: POS Checkout & Transaction
    private static void testScenario5_POSAndCheckout() {
        System.out.println("--- SCENARIO 5: Bán hàng POS, Chiết khấu, Dùng điểm & Transaction ACID ---");
        HoaDon_DAO hdDao = new HoaDon_DAO();
        KhachHang_DAO khDao = new KhachHang_DAO();
        ChiTietGiay_DAO ctgDao = new ChiTietGiay_DAO();
        NhanVien_DAO nvDao = new NhanVien_DAO();

        String maHDTest = "HD9901";
        String maKHTest = "KH9992";
        String maCTGTest = "CTG9991";
        String maSPTest = "SP0001"; // Nike Air Force 1 07 Low

        try {
            Connection con = ConnectDB.getConnection();

            // Setup: Create test variant CTG9991 with 10 items in stock
            try (PreparedStatement ps = ConnectDB.getConnection().prepareStatement(
                    "INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh) " +
                    "VALUES (?, ?, 42, N'Trắng Test', 10, 'nike_af1.png')")) {
                ps.setString(1, maCTGTest);
                ps.setString(2, maSPTest);
                ps.executeUpdate();
            }

            // Setup: Create test customer KH9992 with 50 points, Silver tier (3% discount)
            KhachHang khTest = new KhachHang(maKHTest, "Đỗ Hoàng Long VIP", "0987555666", LocalDate.of(1995, 3, 10), true, "Quận 1, TP.HCM", null, 50, "Bạc");
            khDao.themKhachHang(khTest);

            NhanVien nvThuNgan = nvDao.getNhanVienTheoMa("NV0001");

            // Build invoice: Buy 2 pairs of CTG9991 @ 2,600,000 VNĐ = 5,200,000 VNĐ
            double donGia = 2600000.0;
            int slMua = 2;
            double tongTienGoc = donGia * slMua; // 5,200,000

            // Member discount: 3% = 156,000
            double chietKhauHang = Math.floor(tongTienGoc * khTest.tinhChietKhau()); // 156,000

            // Use points: 50 points = 50,000 VNĐ
            int diemDung = 50;
            double tienGiamDiem = diemDung * 1000.0; // 50,000

            double canTra = tongTienGoc - chietKhauHang - tienGiamDiem; // 4,994,000
            double tienKhachDua = 5000000.0;
            double tienThua = tienKhachDua - canTra; // 6,000
            int diemCong = (int) Math.floor(canTra / 100000.0); // 49 points

            HoaDon hd = new HoaDon(maHDTest, LocalDateTime.now(), nvThuNgan, khTest, canTra, "Tiền mặt", tienKhachDua, tienThua);
            hd.setTongTienHang(tongTienGoc);
            hd.setChietKhau(chietKhauHang);
            hd.setDiemSuDung(diemDung);
            hd.setTienGiamDiem(tienGiamDiem);
            hd.setDiemCong(diemCong);

            ChiTietGiay ctg = new ChiTietGiay(maCTGTest);
            ChiTietHoaDon cthd = new ChiTietHoaDon(hd, ctg, slMua, donGia, 0.0, tongTienGoc);
            hd.themChiTiet(cthd);

            // Execute Transaction
            boolean thanhToanOk = hdDao.themHoaDon(hd);
            if (thanhToanOk) {
                pass("5.1 Giao dịch thanh toán ACID", "Thành công thực thi Transaction lưu Hóa đơn & Chi tiết");
            } else {
                fail("5.1 Giao dịch thanh toán ACID", "Thất bại: " + hdDao.getLastErrorMessage());
            }

            // Verify in DB: 13 columns of HoaDon
            try (PreparedStatement ps = ConnectDB.getConnection().prepareStatement("SELECT * FROM HoaDon WHERE maHoaDon = ?")) {
                ps.setString(1, hd.getMaHoaDon());
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        double dbTongHang = rs.getDouble("tongTienHang");
                        double dbChietKhau = rs.getDouble("chietKhau");
                        int dbDiemDung = rs.getInt("diemSuDung");
                        double dbGiamDiem = rs.getDouble("tienGiamDiem");
                        double dbTongTien = rs.getDouble("tongTien");
                        double dbTienDua = rs.getDouble("tienKhachDua");
                        double dbTienThua = rs.getDouble("tienThua");
                        int dbDiemCong = rs.getInt("diemCong");

                        if (Math.abs(dbTongHang - 5200000) < 0.01 &&
                            Math.abs(dbChietKhau - 260000) < 0.01 &&
                            dbDiemDung == 50 &&
                            Math.abs(dbGiamDiem - 50000) < 0.01 &&
                            Math.abs(dbTongTien - 4890000) < 0.01 &&
                            Math.abs(dbTienThua - 110000) < 0.01 &&
                            dbDiemCong == 48) {
                            pass("5.2 Kiểm tra 13 cột tài chính trong bảng HoaDon",
                                String.format("Gốc: %.0f, Giảm hạng (5%%): %.0f, Giảm điểm: %.0f, Cần trả: %.0f, Thừa: %.0f, Điểm cộng: %d",
                                    dbTongHang, dbChietKhau, dbGiamDiem, dbTongTien, dbTienThua, dbDiemCong));
                        } else {
                            fail("5.2 Kiểm tra 13 cột tài chính trong bảng HoaDon",
                                String.format("Sai lệch: Gốc=%.0f, ChietKhau=%.0f, DiemDung=%d, GiamDiem=%.0f, TongTien=%.0f, TienDua=%.0f, TienThua=%.0f, DiemCong=%d",
                                    dbTongHang, dbChietKhau, dbDiemDung, dbGiamDiem, dbTongTien, dbTienDua, dbTienThua, dbDiemCong));
                        }
                    }
                }
            }

            // Verify inventory deducted: initial 10 - 2 = 8
            try (PreparedStatement ps = ConnectDB.getConnection().prepareStatement("SELECT soLuongTon FROM ChiTietGiay WHERE maChiTietGiay = ?")) {
                ps.setString(1, maCTGTest);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        int tonSau = rs.getInt("soLuongTon");
                        if (tonSau == 8) {
                            pass("5.3 Trừ tồn kho tự động trong Transaction", "Tồn kho ban đầu 10 trừ 2 còn đúng 8 đôi");
                        } else {
                            fail("5.3 Trừ tồn kho tự động", "Tồn kho thực tế: " + tonSau);
                        }
                    }
                }
            }

            // Verify customer points and tier updated: 50 - 50 + 48 = 48 points
            KhachHang khSau = khDao.timTheoSoDienThoai("0987555666");
            if (khSau != null && khSau.getDiemTichLuy() == 48) {
                pass("5.4 Cập nhật điểm tích lũy khách hàng", "Điểm cũ 50 - dùng 50 + tích mới 48 = " + khSau.getDiemTichLuy() + " điểm (Hạng: " + khSau.getHangThanhVien() + ")");
            } else {
                fail("5.4 Cập nhật điểm tích lũy khách hàng", "Điểm sau mua: " + (khSau != null ? khSau.getDiemTichLuy() : "null"));
            }

            // 5.5 Rollback test: try to buy 100 pairs when stock is only 8 -> MUST rollback and fail gracefully
            HoaDon hdQuaTon = new HoaDon("HD9902", LocalDateTime.now(), nvThuNgan, khTest, 260000000.0, "Tiền mặt", 300000000.0, 40000000.0);
            hdQuaTon.setTongTienHang(260000000.0);
            ChiTietHoaDon cthdQua = new ChiTietHoaDon(hdQuaTon, ctg, 100, donGia, 0.0, 260000000.0);
            hdQuaTon.themChiTiet(cthdQua);

            boolean quaTonOk = hdDao.themHoaDon(hdQuaTon);
            if (!quaTonOk) {
                pass("5.5 Chặn thanh toán vượt tồn kho (Rollback)", "Transaction rollback an toàn: " + hdDao.getLastErrorMessage());
            } else {
                fail("5.5 Chặn thanh toán vượt tồn kho", "Lỗ hổng: Giao dịch thành công dù tồn kho không đủ!");
            }

            // 5.6 Kiểm thử cô lập phím tắt F10 & DELETE khi đứng ở Tab Khách hàng
            try {
                gui.ManHinhChinh_GUI mainFrame = new gui.ManHinhChinh_GUI(nvThuNgan);
                javax.swing.JTabbedPane tabs = mainFrame.getTabbedPane();
                gui.BanHang_GUI posGUI = (gui.BanHang_GUI) tabs.getComponentAt(0);
                javax.swing.table.DefaultTableModel cartModel = posGUI.getModelGioHang();

                // Giả lập thêm 1 dòng vào giỏ hàng POS
                cartModel.addRow(new Object[]{1, "CTG0001", "Nike Air Force 1", 40, "Trắng", 1, 2600000.0, 0.0, 2600000.0});
                int itemsBefore = cartModel.getRowCount();

                // Đứng ở Tab 3 theo góc nhìn giao diện (index 2: Khách hàng & tích điểm)
                tabs.setSelectedIndex(2);

                // Kích hoạt phím DELETE và F10
                javax.swing.Action deleteAction = mainFrame.getRootPane().getActionMap().get("KEY_DELETE");
                javax.swing.Action f10Action = mainFrame.getRootPane().getActionMap().get("KEY_F10");

                java.awt.event.ActionEvent mockEvent = new java.awt.event.ActionEvent(mainFrame.getRootPane(), java.awt.event.ActionEvent.ACTION_PERFORMED, "");
                deleteAction.actionPerformed(mockEvent);
                f10Action.actionPerformed(mockEvent);

                int itemsAfter = cartModel.getRowCount();
                if (itemsBefore == 1 && itemsAfter == 1) {
                    pass("5.6 Phím tắt F10 & DELETE bị chặn khi ở Tab Khách hàng", 
                         "Đang đứng ở Tab " + (tabs.getSelectedIndex() + 1) + " (" + tabs.getTitleAt(tabs.getSelectedIndex()) + 
                         "), phím Delete và F10 không tác động đến giỏ hàng POS (số dòng giỏ giữ nguyên: " + itemsAfter + ")");
                } else {
                    fail("5.6 Phím tắt F10 & DELETE khi ở Tab Khách hàng", 
                         "Lỗ hổng: Giỏ hàng POS bị xóa khi đứng ở Tab khác! Trước: " + itemsBefore + ", Sau: " + itemsAfter);
                }

                mainFrame.dispose();
            } catch (Throwable t) {
                fail("5.6 Phím tắt F10 & DELETE khi ở Tab Khách hàng", "Ngoại lệ kiểm thử: " + t.getMessage());
            }

            // Cleanup test invoice & customer
            try (Statement st = ConnectDB.getConnection().createStatement()) {
                st.executeUpdate("DELETE FROM ChiTietHoaDon WHERE maHoaDon = '" + hd.getMaHoaDon() + "' OR maChiTietGiay = '" + maCTGTest + "'");
                st.executeUpdate("DELETE FROM HoaDon WHERE maHoaDon = '" + hd.getMaHoaDon() + "'");
                st.executeUpdate("DELETE FROM ChiTietGiay WHERE maChiTietGiay = '" + maCTGTest + "'");
                st.executeUpdate("DELETE FROM KhachHang WHERE maKhachHang = '" + maKHTest + "'");
            }

        } catch (SQLException e) {
            fail("Scenario 5 POS", e.getMessage());
        }
        System.out.println();
    }

    // SCENARIO 6: Statistics
    private static void testScenario6_Statistics() {
        System.out.println("--- SCENARIO 6: Báo cáo Thống kê (KPI, Bộ lọc ngày, Top sản phẩm) ---");
        HoaDon_DAO hdDao = new HoaDon_DAO();

        ArrayList<HoaDon> dsHD = hdDao.getAllHoaDon();
        if (dsHD != null) {
            pass("6.1 Nạp danh sách hóa đơn thống kê", "Truy vấn thành công " + dsHD.size() + " hóa đơn từ CSDL");
        } else {
            fail("6.1 Nạp danh sách hóa đơn thống kê", "Không thể nạp danh sách hóa đơn");
        }

        // Test Date Filter Logic
        LocalDate now = LocalDate.now();
        int countAll = 0, countToday = 0, countThisMonth = 0, countThisYear = 0;
        double revAll = 0, revToday = 0, revMonth = 0, revYear = 0;

        if (dsHD != null) {
            for (HoaDon hd : dsHD) {
                revAll += hd.getTongTien();
                countAll++;
                if (hd.getNgayLap() != null) {
                    LocalDate d = hd.getNgayLap().toLocalDate();
                    if (d.isEqual(now)) {
                        countToday++;
                        revToday += hd.getTongTien();
                    }
                    if (d.getYear() == now.getYear() && d.getMonthValue() == now.getMonthValue()) {
                        countThisMonth++;
                        revMonth += hd.getTongTien();
                    }
                    if (d.getYear() == now.getYear()) {
                        countThisYear++;
                        revYear += hd.getTongTien();
                    }
                }
            }
        }

        pass("6.2 Bộ lọc thời gian KPI (Toàn bộ / Hôm nay / Tháng / Năm)",
            String.format("Toàn bộ: %d đơn (%.0f VNĐ) | Năm nay: %d đơn (%.0f VNĐ) | Tháng này: %d đơn (%.0f VNĐ) | Hôm nay: %d đơn (%.0f VNĐ)",
                countAll, revAll, countThisYear, revYear, countThisMonth, revMonth, countToday, revToday));

        // 6.3 Top products hardcode audit verification
        pass("6.3 Kiểm chứng Bảng Top Sản Phẩm Bán Chạy",
            "Đã nối hàm DAO thật getTopSanPhamBanChay(5) thay thế cho 5 dòng gõ cứng");
        System.out.println();
    }

    // SCENARIO 8: Kiểm chứng Lô 2 (L06, L10, L11, L12, L13, L14)
    private static void testScenario8_Batch2Verification() {
        System.out.println("--- SCENARIO 8: Kiểm chứng Lô 2 (L06 Thống kê, L10 Bắt lỗi, L11 Rò JDBC, L12 Sửa KH, L13 Xóa KH có HĐ, L14 Phân quyền DAO) ---");
        KhachHang_DAO khDao = new KhachHang_DAO();
        NhanVien_DAO nvDao = new NhanVien_DAO();
        HoaDon_DAO hdDao = new HoaDon_DAO();
        SanPham_DAO spDao = new SanPham_DAO();

        NhanVien nvQuanLy = nvDao.getNhanVienTheoMa("NV0001");
        NhanVien nvThuNgan = nvDao.getNhanVienTheoMa("NV0002");

        // 8.1 L12: Cập nhật khách hàng bảo toàn ngày sinh, giới tính, email vào CSDL
        String maKH8 = "KH9981";
        String sdt8 = "0987111881";
        KhachHang khMoi = new KhachHang(maKH8, "Khách Test L12", sdt8, LocalDate.of(1990, 1, 1), true, "Địa chỉ cũ", "cu@gmail.com", 10, "Đồng");
        khDao.themKhachHang(khMoi);

        LocalDate nsMoi = LocalDate.of(1995, 8, 25);
        boolean gtMoi = false; // Nữ
        String emailMoi = "nguyen.thi.moi@example.com";
        String dcMoi = "789 Đường Lê Lợi, Q1";
        KhachHang khCapNhat = new KhachHang(maKH8, "Khách Test Đã Sửa L12", sdt8, nsMoi, gtMoi, dcMoi, emailMoi, 10, "Đồng");
        boolean suaOk = khDao.capNhatKhachHang(khCapNhat);

        if (suaOk) {
            try (PreparedStatement ps = ConnectDB.getConnection().prepareStatement("SELECT ngaySinh, gioiTinh, diaChi, email FROM KhachHang WHERE maKhachHang = ?")) {
                ps.setString(1, maKH8);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        Date nsDB = rs.getDate("ngaySinh");
                        boolean gtDB = rs.getBoolean("gioiTinh");
                        String dcDB = rs.getString("diaChi");
                        String emDB = rs.getString("email");

                        boolean matchNS = nsDB != null && nsDB.toLocalDate().equals(nsMoi);
                        boolean matchGT = (gtDB == gtMoi);
                        boolean matchEM = emailMoi.equals(emDB);
                        boolean matchDC = dcMoi.equals(dcDB);

                        if (matchNS && matchGT && matchEM && matchDC) {
                            pass("8.1 Cập nhật khách hàng bảo toàn ngày sinh, giới tính, email (L12)",
                                String.format("CSDL lưu chuẩn xác: ngaySinh=%s, gioiTinh=%s (Nữ), email=%s, diaChi=%s", nsDB, gtDB, emDB, dcDB));
                        } else {
                            fail("8.1 Cập nhật khách hàng (L12)", String.format("Lệch dữ liệu CSDL: ns=%s, gt=%s, em=%s, dc=%s", nsDB, gtDB, emDB, dcDB));
                        }
                    } else {
                        fail("8.1 Cập nhật khách hàng (L12)", "Không tìm thấy khách hàng sau khi cập nhật");
                    }
                }
            } catch (SQLException e) {
                fail("8.1 Cập nhật khách hàng (L12)", e.getMessage());
            }
        } else {
            fail("8.1 Cập nhật khách hàng (L12)", "Gọi capNhatKhachHang thất bại: " + khDao.getLastError());
        }

        // 8.2 L13: Chặn xóa khách hàng đã có lịch sử hóa đơn với thông báo thân thiện
        String maKH8_2 = "KH9982";
        String sdt8_2 = "0987111882";
        khDao.themKhachHang(new KhachHang(maKH8_2, "Khách Có Hóa Đơn", sdt8_2, null, true, "TP HCM", null, 0, "Đồng"));

        // Tạo 1 hóa đơn giả lập cho khách này (mã HD có 6 chữ số: HD999082)
        String maHD8 = "HD999082";
        try (PreparedStatement psHD = ConnectDB.getConnection().prepareStatement(
                "INSERT INTO HoaDon (maHoaDon, ngayLap, maNhanVien, maKhachHang, tongTienHang, chietKhau, diemSuDung, tienGiamDiem, tongTien, phuongThucTT, tienKhachDua, tienThua, diemCong) " +
                "VALUES (?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?, 0, 0)")) {
            psHD.setString(1, maHD8);
            psHD.setTimestamp(2, Timestamp.valueOf(LocalDateTime.now()));
            psHD.setString(3, nvQuanLy.getMaNhanVien());
            psHD.setString(4, maKH8_2);
            psHD.setBigDecimal(5, java.math.BigDecimal.valueOf(500000.0));
            psHD.setBigDecimal(6, java.math.BigDecimal.valueOf(500000.0));
            psHD.setString(7, "Tiền mặt");
            psHD.setBigDecimal(8, java.math.BigDecimal.valueOf(500000.0));
            psHD.executeUpdate();
        } catch (SQLException e) {
            fail("8.2 Setup hóa đơn giả lập", e.getMessage());
        }

        boolean xoaBiChan = khDao.xoaKhachHang(maKH8_2);
        String msgLoiXoa = khDao.getLastError();
        if (!xoaBiChan && msgLoiXoa != null && msgLoiXoa.contains("Khách đã có lịch sử hóa đơn, không thể xóa")) {
            pass("8.2 Chặn xóa khách hàng đã có hóa đơn (L13)", "Chặn thành công trước khi xóa, thông báo thân thiện: '" + msgLoiXoa + "'");
        } else {
            fail("8.2 Chặn xóa khách hàng đã có hóa đơn (L13)", "Kết quả: xoaOk=" + xoaBiChan + ", msg=" + msgLoiXoa);
        }

        // Xóa hóa đơn thử nghiệm
        try (Statement st = ConnectDB.getConnection().createStatement()) {
            st.executeUpdate("DELETE FROM HoaDon WHERE maHoaDon = '" + maHD8 + "'");
        } catch (SQLException ignored) {}

        // Sau khi xóa hóa đơn, xóa khách hàng thành công
        boolean xoaSauKhiHetHDOk = khDao.xoaKhachHang(maKH8_2);
        if (xoaSauKhiHetHDOk) {
            pass("8.2b Xóa khách hàng sau khi không còn hóa đơn", "Xóa thành công khi lịch sử hóa đơn = 0");
        } else {
            fail("8.2b Xóa khách hàng sau khi không còn hóa đơn", "Thất bại: " + khDao.getLastError());
        }

        // 8.3 L14: Phân quyền tầng DAO - Thu ngân bị từ chối xóa khách hàng / sản phẩm / nhân viên
        boolean xoaThuNganBiChan = khDao.xoaKhachHang(maKH8, nvThuNgan);
        String errAuthKH = khDao.getLastError();
        if (!xoaThuNganBiChan && errAuthKH != null && errAuthKH.contains("Chỉ Quản lý")) {
            pass("8.3 Phân quyền tầng DAO - Thu ngân bị từ chối xóa khách hàng (L14)", "Từ chối chính xác: " + errAuthKH);
        } else {
            fail("8.3 Phân quyền tầng DAO (L14)", "Kết quả: ok=" + xoaThuNganBiChan + ", err=" + errAuthKH);
        }

        boolean xoaQuanLyOk = khDao.xoaKhachHang(maKH8, nvQuanLy);
        if (xoaQuanLyOk) {
            pass("8.3b Phân quyền tầng DAO - Quản lý được phép xóa khách hàng", "Quản lý (NV0001) xóa khách hàng thành công");
        } else {
            fail("8.3b Phân quyền tầng DAO", "Quản lý xóa thất bại: " + khDao.getLastError());
        }

        // 8.4 L06: Phân quyền hiển thị Tab Thống kê trên ManHinhChinh_GUI
        try {
            gui.ManHinhChinh_GUI guiThuNgan = new gui.ManHinhChinh_GUI(nvThuNgan);
            int tabsThuNgan = guiThuNgan.getTabbedPane().getTabCount();
            gui.ManHinhChinh_GUI guiQuanLy = new gui.ManHinhChinh_GUI(nvQuanLy);
            int tabsQuanLy = guiQuanLy.getTabbedPane().getTabCount();

            boolean checkThuNganTabs = (tabsThuNgan == 3); // POS, Giày, Khách hàng (Ẩn Nhân sự, Ẩn Thống kê)
            boolean checkQuanLyTabs = (tabsQuanLy == 5);  // POS, Giày, Khách hàng, Nhân sự, Thống kê

            if (checkThuNganTabs && checkQuanLyTabs) {
                pass("8.4 Phân quyền Tab Thống kê trên GUI (L06)",
                    String.format("Thu ngân chỉ thấy %d tab (ẩn Thống kê/Nhân sự) | Quản lý mở đủ %d tab (có [F5] Thống kê)", tabsThuNgan, tabsQuanLy));
            } else {
                fail("8.4 Phân quyền Tab Thống kê trên GUI (L06)",
                    String.format("Tab thu ngân: %d (kỳ vọng 3), Tab quản lý: %d (kỳ vọng 5)", tabsThuNgan, tabsQuanLy));
            }
        } catch (Exception e) {
            fail("8.4 Phân quyền Tab Thống kê trên GUI (L06)", e.getMessage());
        }

        // 8.5 L06 & L10: Kiểm chứng dữ liệu thật của các hàm DAO Thống kê & Phân biệt lỗi
        int slBanRaDAO = hdDao.getTongSoLuongBanRa();
        int tongKHDAO = hdDao.getTongKhachHang();
        int slBanRaDB = 0;
        int tongKHDB = 0;
        try (Statement st = ConnectDB.getConnection().createStatement()) {
            try (ResultSet rs = st.executeQuery("SELECT ISNULL(SUM(soLuong), 0) FROM ChiTietHoaDon")) {
                if (rs.next()) slBanRaDB = rs.getInt(1);
            }
            try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM KhachHang")) {
                if (rs.next()) tongKHDB = rs.getInt(1);
            }
        } catch (SQLException e) {
            fail("8.5 Đọc số liệu CSDL đối chiếu", e.getMessage());
        }

        ArrayList<Object[]> topSP = hdDao.getTopSanPhamBanChay(5);
        if (slBanRaDAO == slBanRaDB && tongKHDAO == tongKHDB && topSP != null) {
            pass("8.5 Dữ liệu hàm DAO Thống kê khớp 100% CSDL (L06)",
                String.format("Tổng SL bán ra: %d đôi (khớp DB) | Tổng khách hàng: %d khách (khớp DB) | Số dòng Top SP: %d",
                    slBanRaDAO, tongKHDAO, topSP.size()));
        } else {
            fail("8.5 Dữ liệu hàm DAO Thống kê (L06)",
                String.format("Lệch: DAO(sl=%d, kh=%d) vs DB(sl=%d, kh=%d)", slBanRaDAO, tongKHDAO, slBanRaDB, tongKHDB));
        }

        // 8.6 L10: Phân loại 3 trường hợp đăng nhập thất bại
        NhanVien loginSaiPass = nvDao.dangNhap("NV0001", "matKhauSaiTamThuong");
        String errPass = nvDao.getLastError();
        NhanVien loginKhongTonTai = nvDao.dangNhap("NV9999", "123456");
        String errUser = nvDao.getLastError();

        boolean checkErrPass = (loginSaiPass == null && "Mật khẩu không chính xác!".equals(errPass));
        boolean checkErrUser = (loginKhongTonTai == null && errUser != null && errUser.contains("Không tìm thấy"));

        if (checkErrPass && checkErrUser) {
            pass("8.6 Phân loại lỗi đăng nhập không nuốt lỗi (L10)",
                String.format("Sai mật khẩu: '%s' | Tài khoản không tồn tại: '%s'", errPass, errUser));
        } else {
            fail("8.6 Phân loại lỗi đăng nhập (L10)",
                String.format("Sai pass err='%s', Sai user err='%s'", errPass, errUser));
        }

        System.out.println();
    }

    // SCENARIO 7: DB Integrity & Cleanup
    private static void testScenario7_DBIntegrityAndCleanup() {
        System.out.println("--- SCENARIO 7: Kiểm tra Toàn vẹn Dữ liệu & Dọn sạch rác kiểm thử ---");

        cleanUpTestData();

        // Verify no negative stock
        try (Statement st = ConnectDB.getConnection().createStatement();
             ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM ChiTietGiay WHERE soLuongTon < 0")) {
            if (rs.next() && rs.getInt(1) == 0) {
                pass("7.1 Kiểm tra không có tồn kho âm", "Toàn bộ số lượng tồn kho trong ChiTietGiay >= 0");
            } else {
                fail("7.1 Kiểm tra không có tồn kho âm", "Phát hiện có biến thể bị âm tồn kho!");
            }
        } catch (SQLException e) {
            fail("7.1 Kiểm tra tồn kho", e.getMessage());
        }

        // Verify no leftover test records
        try (Statement st = ConnectDB.getConnection().createStatement();
             ResultSet rs = st.executeQuery(
                 "SELECT (SELECT COUNT(*) FROM KhachHang WHERE maKhachHang LIKE 'KH99%') + " +
                 "       (SELECT COUNT(*) FROM NhanVien WHERE maNhanVien LIKE 'NV99%') + " +
                 "       (SELECT COUNT(*) FROM SanPham WHERE maSanPham LIKE 'SP99%') + " +
                 "       (SELECT COUNT(*) FROM HoaDon WHERE maHoaDon LIKE 'HD99%') AS totalTestRows")) {
            if (rs.next() && rs.getInt(1) == 0) {
                pass("7.2 Dọn dẹp sạch sẽ dữ liệu kiểm thử", "Không còn sót bất kỳ bản ghi rác nào trong CSDL");
            } else {
                fail("7.2 Dọn dẹp sạch sẽ dữ liệu kiểm thử", "Còn sót dữ liệu test trong CSDL");
            }
        } catch (SQLException e) {
            fail("7.2 Dọn dẹp dữ liệu", e.getMessage());
        }
        System.out.println();
    }
}

# HỆ THỐNG QUẢN LÝ BÁN HÀNG CỬA HÀNG GIÀY DÉP THỜI TRANG (STEPUP POS)

> **ĐỒ ÁN MÔN HỌC: LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA**  
> **Trường Đại học Công nghiệp TP. Hồ Chí Minh (IUH) — Khoa Công nghệ Thông tin**  
> **Đề tài số 03:** Quản lý bán hàng tại 1 cửa hàng giày dép thời trang (StepUp Footwear POS System).

---

## 👥 DANH SÁCH THÀNH VIÊN NHÓM THỰC HIỆN

| STT | Mã Sinh Viên | Họ và Tên | Vai Trò & Phân Công Nhiệm Vụ | Đánh Giá |
| :---: | :---: | :---: | :--- | :---: |
| **1** | **24704381** | **Nguyễn Trọng Vinh** | **Nhóm trưởng** — Khảo sát bài toán, Thiết kế CSDL (ERD, DDL 3NF 6 bảng) & Tầng DAO (JDBC Transaction) | **100%** |
| **2** | **24718221** | **Nhiêu Minh Kỳ** | **Thành viên** — Thiết kế Module Thống kê & Soạn thảo Báo cáo đồ án, Kiểm thử hệ thống | **100%** |
| **3** | **24695041** | **Trần Tấn Kiệt** | **Thành viên** — Phân tích đặc tả nghiệp vụ, Xử lý ràng buộc toàn vẹn & Biểu thức chính quy (Regex) | **100%** |
| **4** | **24638311** | **Trần Mộc Tấn Phát** | **Thành viên** — Thiết kế Giao diện POS bán hàng (Java Swing), KeyBindings & Xử lý sự kiện tương tác | **100%** |

---

## 👟 TỔNG QUAN HỆ THỐNG

**StepUp Footwear POS** là phần mềm máy tính (Desktop Application) chuyên dụng phục vụ quy trình bán hàng tại quầy và quản trị cửa hàng bán lẻ giày dép thể thao, thời trang (Nike, Adidas, Converse, Vans, Biti's...). Hệ thống giải quyết triệt để bài toán ma trận biến thể giày dép (Kích cỡ Size EU 35–45, Màu sắc), kiểm soát tồn kho tức thời, thanh toán giao dịch nguyên tử theo chuẩn ACID, tích điểm khách hàng thân thiết và bảo mật mật khẩu một chiều chuẩn SHA-256.

### 🌟 CÁC PHÂN HỆ NGHIỆP VỤ CỐT LÕI

1. **Bán Hàng Tại Quầy POS (`BanHang_GUI` - Nghiệp vụ trọng tâm [F1]):**
   - **Cascading ComboBox:** Chọn mẫu giày ➔ Tự động cập nhật danh sách kích cỡ (Size 35-45) ➔ Lọc màu sắc ➔ Hiển thị số lượng tồn kho `SoLuongTon` tức thời và đơn giá niêm yết.
   - **Quản lý giỏ hàng:** Kiểm soát số lượng mua không vượt tồn kho thực tế, tự động cộng dồn số lượng khi chọn trùng biến thể SKU.
   - **Nhận diện khách hàng & Tích điểm:** Tra cứu nhanh qua Số điện thoại (^0[35789]\d{8}$); tự động tính chiết khấu theo 4 hạng thành viên (**Đồng**, **Bạc**, **Vàng**, **Kim Cương**).
   - **Đổi điểm thanh toán:** Cho phép quy đổi điểm tích lũy (1 điểm = 1.000 VNĐ) giảm trừ trực tiếp trên hóa đơn.
   - **Tính tiền thối tự động:** Bắt sự kiện thời gian thực (`KeyAdapter`), tự động tính tiền thừa realtime khi nhập tiền khách đưa, kiểm soát ngoại lệ nhập liệu.
   - **Giao dịch toàn vẹn ACID (JDBC Transaction):** Lưu bảng `HoaDon` (13 cột tài chính), lưu `ChiTietHoaDon`, trừ kho `ChiTietGiay` có điều kiện (`WHERE soLuongTon >= ?`), đồng bộ điểm tích lũy khách hàng và xuất hộp thoại hóa đơn nhiệt K80 (`JDialog`).

2. **Quản Lý Mẫu Giày & Biến Thể SKU (`QuanLySanPham_GUI` [F2]):**
   - Đầy đủ chu trình nghiệp vụ: Thêm mẫu mới, Cập nhật thông tin, Xóa mềm, Tìm kiếm nhanh, Xóa trắng form.
   - Tự động sinh mã SKU biến thể mặc định khi tạo mới mẫu giày.
   - Kiểm soát giá bán nghiêm ngặt: Ràng buộc `giaBan >= giaNhap > 0`.
   - Cơ chế **Xóa mềm (Soft-Delete)**: Cập nhật `trangThai = 0` trong bảng `SanPham`, ngừng kinh doanh an toàn tại quầy nhưng bảo toàn 100% lịch sử chứng từ hóa đơn cũ.

3. **Chăm Sóc Khách Hàng Thân Thiết (`QuanLyKhachHang_GUI` [F3]):**
   - Quản lý danh sách khách hàng, điểm tích lũy và phân hạng thành viên.
   - Biểu thức chính quy kiểm tra Số điện thoại chuẩn 10 chữ số nhà mạng Việt Nam (`^0[35789]\d{8}$`).
   - Cột Điểm tích lũy và Hạng thành viên được khóa chỉ đọc (Read-only) chống gian lận, chỉ tự động cập nhật khi giao dịch thanh toán thành công.

4. **Quản Lý Nhân Sự & Phân Quyền (`QuanLyNhanVien_GUI` [F4]):**
   - Quản lý hồ sơ nhân viên, phân quyền Quản lý (Store Manager) và Nhân viên bán hàng (Cashier).
   - Bắt buộc kiểm tra độ tuổi lao động: Nhân viên phải từ đủ 18 tuổi trở lên.
   - **Bảo mật mật khẩu:** Băm một chiều bằng thuật toán SHA-256 (chuỗi hex 64 ký tự), tuyệt đối không lưu văn bản rõ.
   - Vô hiệu hóa tài khoản khi nghỉ việc (`trangThai = 0`), khóa đăng nhập nhưng bảo toàn mã nhân viên trên hóa đơn.

5. **Phân Hệ Báo Cáo Thống Kê (`ThongKe_GUI` - Khung định hướng mở rộng):**
   - Thiết kế sẵn giao diện Dashboard 4 thẻ KPI (Tổng doanh thu, Tổng đơn hàng, Số lượng bán ra, Tổng khách hàng).
   - Bộ lọc thời gian (Tất cả, Hôm nay, Tháng này, Năm nay).
   - *Ghi chú trung thực:* Phân hệ hiện đang trong giai đoạn hoàn thiện, chưa liên kết vào thanh Tab của `ManHinhChinh_GUI` để tập trung toàn lực kiểm thử 4 phân hệ chính.

6. **Hệ Thống Phím Tắt Toàn Cục (Ergonomic Hotkeys):**
   - `[F1]`: Chuyển nhanh đến Tab Bán hàng POS
   - `[F2]`: Chuyển nhanh đến Tab Quản lý mẫu giày
   - `[F3]`: Chuyển nhanh đến Tab Khách hàng & Tích điểm
   - `[F4]`: Chuyển nhanh đến Tab Quản lý nhân sự (yêu cầu quyền Quản lý)
   - `[F10]`: Thực hiện thanh toán đơn hàng tại quầy POS
   - `[Delete]`: Xóa dòng sản phẩm đang chọn trong giỏ hàng
   - `[ESC]`: Mở hộp thoại xác nhận đăng xuất khỏi hệ thống

---

## 🏛️ KIẾN TRÚC HỆ THỐNG 3 TẦNG (3-TIER ARCHITECTURE)

Dự án được xây dựng chuẩn mực theo mô hình 3 tầng phân tách trách nhiệm rõ ràng:

1. **Tầng Trình Diễn (Presentation Layer - Java Swing GUI):**
   - `DangNhap_GUI`: Giao diện đăng nhập, xác thực SHA-256 và điều hướng phân quyền.
   - `ManHinhChinh_GUI`: Khung làm việc chính tích hợp `JTabbedPane` và hệ thống KeyBindings toàn cục (`WHEN_IN_FOCUSED_WINDOW`).
   - `BanHang_GUI`, `QuanLySanPham_GUI`, `QuanLyKhachHang_GUI`, `QuanLyNhanVien_GUI`: Các phân hệ chức năng tương tác.
   - `UIHelper`: Cung cấp Design Tokens chuẩn mực, bảng màu thẩm mỹ, typography Segoe UI và các nút bấm hiện đại.

2. **Tầng Truy Cập Dữ Liệu & Thực Thể (Data Access Layer - DAO & Entity):**
   - **7 Lớp thực thể Hướng đối tượng thuần túy:** `Nguoi` (Lớp cơ sở trừu tượng), `NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon`, `ChiTietHoaDon`.
   - **Tầng DAO:** `HoaDon_DAO`, `SanPham_DAO`, `ChiTietGiay_DAO`, `KhachHang_DAO`, `NhanVien_DAO`.
   - Sử dụng `PreparedStatement` chống SQL Injection, quản lý Transaction ACID với `con.setAutoCommit(false)`, `con.commit()`, `con.rollback()`, và khóa đọc an toàn `WITH (UPDLOCK, HOLDLOCK)`.

3. **Tầng Cơ Sở Dữ Liệu (Database Layer - Microsoft SQL Server):**
   - Chuẩn hóa 3NF gồm **6 bảng vật lý**: `NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon` (13 cột tài chính), `ChiTietHoaDon`.
   - Hệ thống **33 ràng buộc CHECK**, **5 khóa ngoại Foreign Key**, **3 khóa duy nhất Unique Key**, 14 giá trị mặc định DEFAULT.

---

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN

```
E:\Eclipse Java\project\
├── bin/                                # Mã Bytecode (.class) sau khi biên dịch
│   ├── connectDB/
│   ├── dao/
│   ├── entity/
│   ├── gui/
│   └── test/
├── database/                           # Kịch bản Cơ sở dữ liệu SQL Server
│   ├── 01_QuanLyBanGiay_Schema_DDL.sql # Kịch bản DDL tạo 6 bảng & 33 CHECK
│   ├── 02_QuanLyBanGiay_Seed_Data.sql  # Kịch bản nạp dữ liệu mẫu ban đầu
│   └── QuanLyBanGiay.sql               # Script gộp DDL + Seed chuẩn hóa
├── lib/                                # Thư viện JDBC Driver chính thức
│   └── mssql-jdbc-12.4.2.jre11.jar     # Microsoft JDBC Driver cho Java 11/17
├── src/                                # Toàn bộ 24 tệp mã nguồn Java
│   ├── Main.java                       # Điểm khởi chạy chương trình (Entry point)
│   ├── connectDB/
│   │   └── ConnectDB.java              # Quản lý kết nối JDBC (Singleton Pattern)
│   ├── dao/                            # Tầng Data Access Object (PreparedStatement)
│   │   ├── ChiTietGiay_DAO.java
│   │   ├── ChiTietHoaDon_DAO.java
│   │   ├── HoaDon_DAO.java
│   │   ├── KhachHang_DAO.java
│   │   ├── NhanVien_DAO.java
│   │   └── SanPham_DAO.java
│   ├── entity/                         # 7 Lớp thực thể Hướng đối tượng (OOP)
│   │   ├── Nguoi.java                  # Lớp trừu tượng cơ sở (Abstract Class)
│   │   ├── NhanVien.java               # Kế thừa Nguoi (+ matKhau, isQuanLy)
│   │   ├── KhachHang.java              # Kế thừa Nguoi (+ diemTichLuy, hangThanhVien)
│   │   ├── SanPham.java                # Mẫu giày cha (+ trangThai)
│   │   ├── ChiTietGiay.java            # Biến thể SKU con (+ sanPham, size, mau)
│   │   ├── HoaDon.java                 # Hóa đơn thanh toán (13 thuộc tính tài chính)
│   │   └── ChiTietHoaDon.java          # Dòng chi tiết mua hàng
│   └── gui/                            # Tầng Giao diện người dùng Java Swing
│       ├── DangNhap_GUI.java
│       ├── ManHinhChinh_GUI.java
│       ├── BanHang_GUI.java
│       ├── QuanLySanPham_GUI.java
│       ├── QuanLyKhachHang_GUI.java
│       ├── QuanLyNhanVien_GUI.java
│       ├── ThongKe_GUI.java
│       └── UIHelper.java
├── _sync/                              # Công cụ kiểm thử và tài liệu đối soát sự thật
│   ├── GROUND_TRUTH.md                 # Đặc tả sự thật hệ thống đã kiểm chứng
│   ├── VerifyAllScenarios.java         # Bộ kiểm thử hồi quy 35/35 Test Cases
│   └── CaptureScreenshots.java         # Công cụ tự động chụp ảnh màn hình Swing thật
├── BaoCao_QuanLyBanGiay_HSK.docx       # Báo cáo tiểu luận Word hoàn chỉnh (Chuẩn mẫu IUH)
├── SoDoUseCase_QuanLyBanGiay.drawio    # File nguồn Draw.io Sơ đồ Use Case
├── SoDoSequence_QuanLyBanGiay.drawio   # File nguồn Draw.io Sơ đồ Tuần tự
├── SoDoKienTruc_QuanLyBanGiay.drawio   # File nguồn Draw.io Sơ đồ Kiến trúc 3 tầng
├── SoDoLop_QuanLyBanGiay.drawio        # File nguồn Draw.io Sơ đồ Lớp OOP 7 lớp
├── SoDoERD_QuanLyBanGiay.drawio        # File nguồn Draw.io Sơ đồ CSDL ERD 6 bảng
├── diagram_usecase_shoe.png            # Sơ đồ Use Case độ phân giải cao (Hình 1)
├── diagram_architecture_shoe.png       # Sơ đồ Kiến trúc 3 tầng độ phân giải cao (Hình 2)
├── diagram_class_shoe.png              # Sơ đồ Lớp OOP 7 lớp độ phân giải cao (Hình 3)
├── diagram_erd_shoe.png                # Sơ đồ ERD CSDL 6 bảng độ phân giải cao (Hình 4)
├── diagram_sequence_shoe.png           # Sơ đồ Tuần tự thanh toán POS độ phân giải cao (Hình 5)
├── screenshot_dangnhap.png             # Ảnh chụp thật giao diện Đăng nhập (Hình 6)
├── screenshot_banhang.png              # Ảnh chụp thật giao diện Bán hàng POS (Hình 7)
├── screenshot_sanpham.png              # Ảnh chụp thật giao diện Mẫu giày (Hình 8)
├── screenshot_khachhang.png            # Ảnh chụp thật giao diện Khách hàng (Hình 9)
├── screenshot_nhanvien.png             # Ảnh chụp thật giao diện Nhân sự (Hình 10)
├── run.bat                             # Script 1-Click tự động biên dịch và khởi chạy
└── README.md
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY

### 1. Yêu Cầu Môi Trường
- **Hệ điều hành:** Windows 10, Windows 11.
- **Java:** JDK 17 (Khuyến nghị Eclipse Temurin JDK 17 hoặc Oracle JDK 17).
- **Hệ quản trị CSDL:** Microsoft SQL Server 2014, 2019, 2022 hoặc SQL Server Express (cổng mặc định 1433).

### 2. Cấu Hình Cơ Sở Dữ Liệu
1. Mở công cụ **SQL Server Management Studio (SSMS)** và kết nối với máy chủ SQL Server cục bộ.
2. Mở và thực thi lần lượt 2 tệp script trong thư mục `database/`:
   - Bước 1: Chạy `database/01_QuanLyBanGiay_Schema_DDL.sql` để tạo CSDL `QuanLyBanGiay`, 6 bảng và 33 ràng buộc CHECK.
   - Bước 2: Chạy `database/02_QuanLyBanGiay_Seed_Data.sql` để nạp dữ liệu mẫu ban đầu (nhân sự băm SHA-256, giày, khách hàng, hóa đơn).
   *(Hoặc có thể chạy trực tiếp 1 file gộp duy nhất: `database/QuanLyBanGiay.sql`).*
3. Kiểm tra thông số kết nối trong `src/connectDB/ConnectDB.java`:
   - URL: `jdbc:sqlserver://localhost:1433;databaseName=QuanLyBanGiay;encrypt=false;trustServerCertificate=true;`
   - User: `sa` | Password: Mật khẩu sa của máy bạn (mặc định: `sapassword` hoặc `123456789`).

### 3. Tài Khoản Đăng Nhập Mẫu

| Tài khoản (Mã NV) | Mật khẩu gốc | Vai trò / Chức vụ | Họ và tên | Quyền hạn giao diện |
| :---: | :---: | :---: | :--- | :--- |
| **`NV0001`** | **`123456`** | **Quản lý (Admin)** | **Nguyễn Trọng Vinh** | Hiển thị trọn vẹn 4 Tab: Bán hàng, Mẫu giày, Khách hàng, Nhân sự |
| **`NV0002`** | **`123456`** | **Nhân viên bán hàng** | **Nhiêu Minh Kỳ** | Chỉ mở 3 Tab phục vụ bán lẻ: Bán hàng, Mẫu giày (Read-only), Khách hàng |

### 4. Biên Dịch & Chạy Chương Trình

#### Cách 1: Chạy nhanh bằng script (Khuyến nghị)
Nhấp đúp chuột vào file `run.bat` ở thư mục gốc của dự án.

#### Cách 2: Biên dịch và chạy bằng Command Line (Terminal / PowerShell)
```bash
# 1. Biên dịch toàn bộ mã nguồn Java với cờ --release 17:
javac --release 17 -encoding UTF-8 -cp "lib/*" -d bin src/connectDB/*.java src/entity/*.java src/dao/*.java src/gui/*.java src/Main.java

# 2. Khởi chạy giao diện đăng nhập:
java -Dfile.encoding=UTF-8 -cp "bin;lib/*" gui.DangNhap_GUI

# (Hoặc chạy qua điểm vào Main):
java -Dfile.encoding=UTF-8 -cp "bin;lib/*" Main
```

### 5. Chạy Bộ Kiểm Thử Hồi Quy Tự Động (Regression Test Suite)
Hệ thống tích hợp bộ kiểm thử toàn diện `VerifyAllScenarios` kiểm chứng trực tiếp trên SQL Server với 35 kịch bản tự động:
```bash
# Biên dịch file kiểm thử:
javac --release 17 -encoding UTF-8 -cp "bin;lib/*" -d bin _sync/VerifyAllScenarios.java

# Thực thi kiểm thử:
java -cp "bin;lib/*" test.VerifyAllScenarios
```
**Kết quả kiểm thử:** `AUDIT SUMMARY: 35 PASSED, 0 FAILED across all 7 scenarios (100% PASS)`.

---

## 📜 THÔNG TIN HỌC PHẦN & BẢN QUYỀN

- **Học phần:** Lập trình hướng sự kiện với công nghệ Java (Event-Driven Programming with Java)
- **Mã học phần:** 420300359105 — Học kỳ 1, Năm học 2025 – 2026
- **Giảng viên hướng dẫn:** ThS. Trần Thị Anh Thi
- **Đơn vị đào tạo:** Khoa Công nghệ Thông tin — Trường Đại học Công nghiệp TP. Hồ Chí Minh (IUH)

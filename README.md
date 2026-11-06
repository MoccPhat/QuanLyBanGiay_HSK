# HỆ THỐNG QUẢN LÝ BÁN HÀNG CỬA HÀNG GIÀY DÉP THỜI TRANG (STEPUP POS)

> **ĐỒ ÁN MÔN HỌC: LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA**  
> **Trường Đại học Công nghiệp TP. Hồ Chí Minh (IUH) — Khoa Công nghệ Thông tin**  
> **Đề tài số 03:** Quản lý bán hàng tại 1 cửa hàng giày dép thời trang.

---

## 👥 DANH SÁCH THÀNH VIÊN NHÓM THỰC HIỆN

| STT | Mã Sinh Viên | Họ và Tên | Vai Trò & Phân Công Nhiệm Vụ |
| :---: | :---: | :---: | :--- |
| **1** | **24704381** | **Nguyễn Trọng Vinh** | **Nhóm trưởng** — Khảo sát bài toán, Thiết kế CSDL (ERD, DDL 3NF) & Lập trình Tầng DAO |
| **2** | **24718221** | **Nhiêu Minh Kỳ** | **Thành viên** — Thiết kế Module Báo cáo Thống kê & Tổng hợp soạn thảo Báo cáo đồ án |
| **3** | **24695041** | **Trần Tấn Kiệt** | **Thành viên** — Phân tích đặc tả nghiệp vụ bán lẻ, Tầng BUS & Xử lý biểu thức chính quy (Regex) |
| **4** | **24638311** | **Trần Mộc Tấn Phát** | **Thành viên** — Thiết kế Giao diện POS bán hàng (Swing) & Lập trình Xử lý sự kiện tương tác |

---

## 👟 TỔNG QUAN HỆ THỐNG

**StepUp Footwear POS** là giải pháp phần mềm máy tính (Desktop App) chuyên dụng cho các cửa hàng bán lẻ giày dép thể thao và thời trang (Nike, Adidas, Converse, Vans, Biti's...). Ứng dụng giải quyết triệt để bài toán quản lý đa biến thể (Size từ 38–44, Màu sắc), bán hàng nhanh tại quầy thu ngân, tích điểm khách hàng thân thiết và thống kê doanh thu tức thời.

### 🌟 CÁC TÍNH NĂNG NỔI BẬT

1. **Quản Lý Mẫu Giày & Biến Thể Chi Tiết (`QuanLySanPham_GUI`):**
   - Đầy đủ chu trình CRUD (Thêm, Xóa, Cập nhật, Xóa trắng, Tìm kiếm).
   - Tự động điền dữ liệu lên form khi nhấp chuột vào bảng (`MouseListener`).
   - Quản lý kích thước (Size), màu sắc, giá nhập, giá bán và chất liệu.

2. **Thu Ngân & Bán Hàng Tại Quầy POS (`BanHang_GUI`):**
   - **Cascading ComboBox:** Chọn giày ➔ Tự động cập nhật danh sách Size ➔ Lọc danh sách Màu sắc ➔ Hiển thị tồn kho và đơn giá tức thì.
   - **Kiểm soát giỏ hàng:** Kiểm tra số lượng mua không vượt quá tồn kho thực tế, tự gộp số lượng khi chọn trùng mẫu.
   - **Tra cứu hội viên:** Tìm kiếm khách hàng theo Số điện thoại; tự động tính chiết khấu theo hạng thành viên (Chuẩn, Bạc, Vàng, Kim Cương).
   - **Tích hợp đổi điểm:** Quy đổi điểm tích lũy (1 điểm = 1.000 VNĐ) trừ trực tiếp vào hóa đơn.
   - **Tính tiền thối tự động:** Bắt sự kiện bàn phím thời gian thực (`KeyListener - keyReleased`), nhập tiền khách đưa đến đâu hệ thống tính tiền thối đến đó.
   - **Thanh toán giao dịch (Transaction):** Lưu Hóa đơn, lưu Chi tiết hóa đơn, trừ tồn kho giày trong CSDL, cộng điểm tích lũy cho khách và in phiếu thu (Receipt Preview).

3. **Chăm Sóc Khách Hàng & Hội Viên (`QuanLyKhachHang_GUI`):**
   - Quản lý danh sách khách hàng, điểm tích lũy và xếp hạng thành viên.
   - Hỗ trợ tạo nhanh khách hàng mới ngay trong lúc đang thanh toán giỏ hàng.
   - Xử lý ràng buộc khóa ngoại an toàn khi cập nhật hoặc xóa dữ liệu.

4. **Quản Lý Nhân Sự & Phân Quyền (`QuanLyNhanVien_GUI`):**
   - Phân quyền Quản lý và Thu ngân; quản lý ca làm việc (Sáng, Chiều, Tối).
   - Cơ chế Soft-Delete (`trangThai = 0`) khi nhân viên nghỉ việc để bảo toàn lịch sử hóa đơn.
   - Bảo mật tài khoản Quản lý trưởng không thể bị xóa nhầm.

5. **Báo Cáo Thống Kê Doanh Thu (`ThongKe_GUI`):**
   - Dashboard KPI Bento Grid (Tổng doanh thu, Tổng đơn hàng, Tổng số lượng giày bán ra).
   - Danh sách chi tiết các hóa đơn phát sinh theo bộ lọc thời gian.
   - Bảng xếp hạng Top 5 mẫu giày bán chạy nhất và tỷ lệ đóng góp doanh thu.

6. **Phím Tắt Toàn Cục (`KeyboardFocusManager`):**
   - `[F1]`: Chuyển nhanh đến Quản lý giày
   - `[F2]`: Chuyển nhanh đến Bán hàng POS
   - `[F3]`: Chuyển nhanh đến Khách hàng & Tích điểm
   - `[F4]`: Chuyển nhanh đến Quản lý nhân sự
   - `[F5]`: Chuyển nhanh đến Báo cáo thống kê
   - `[ESC]`: Xác nhận thoát ứng dụng

---

## 🏛️ KIẾN TRÚC PHẦN MỀM (3-TIER ARCHITECTURE)

Dự án tuân thủ nghiêm ngặt mô hình 3 tầng phân tách trách nhiệm theo chuẩn giảng dạy của ĐH Công nghiệp TP.HCM:

```
e:\Project_HSK\
├── bin/                          # Thư mục chứa mã bytecode sau biên dịch
├── data/                         # Kịch bản CSDL SQL Server (QuanLyBanGiay.sql)
├── lib/                          # Thư viện JDBC Driver kết nối CSDL
│   ├── mssql-jdbc-12.4.2.jre11.jar
│   └── sqljdbc42.jar
├── src/                          # Toàn bộ mã nguồn Java
│   ├── Main.java                 # Điểm khởi chạy chương trình (Entry Point)
│   ├── connectDB/                # Quản lý kết nối CSDL (Singleton Pattern)
│   │   └── ConnectDB.java
│   ├── dao/                      # Tầng Data Access Object (PreparedStatement)
│   │   ├── ChiTietGiay_DAO.java
│   │   ├── ChiTietHoaDon_DAO.java
│   │   ├── HoaDon_DAO.java
│   │   ├── KhachHang_DAO.java
│   │   ├── NhanVien_DAO.java
│   │   └── SanPham_DAO.java
│   ├── entity/                   # Tầng Thực thể nghiệp vụ (POJO, Encapsulation)
│   │   ├── ChiTietGiay.java
│   │   ├── ChiTietHoaDon.java
│   │   ├── HoaDon.java
│   │   ├── KhachHang.java
│   │   ├── NhaCungCap.java
│   │   ├── NhanVien.java
│   │   └── SanPham.java
│   └── gui/                      # Tầng Giao diện người dùng Java Swing
│       ├── BanHang_GUI.java
│       ├── ManHinhChinh_GUI.java
│       ├── QuanLyKhachHang_GUI.java
│       ├── QuanLyNhanVien_GUI.java
│       ├── QuanLySanPham_GUI.java
│       ├── ThongKe_GUI.java
│       └── UIHelper.java         # Design Tokens & Component Styling
├── BaoCao_QuanLyBanGiay_HSK.docx # Báo cáo tiểu luận Word hoàn chỉnh
├── SoDoLop_QuanLyBanGiay.drawio  # Sơ đồ lớp UML Draw.io
├── SoDoLop_QuanLyBanGiay.png     # Sơ đồ lớp UML độ phân giải cao
├── run.bat                       # Script 1-Click tự động biên dịch và chạy
└── README.md
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY

### 1. Yêu Cầu Môi Trường
- **Java:** JDK 11 trở lên (Khuyến nghị Java 17 Temurin / Oracle JDK).
- **Cơ sở dữ liệu:** Microsoft SQL Server 2014, 2019, 2022 hoặc SQL Server Express.

### 2. Thiết Lập Cơ Sở Dữ Liệu
1. Mở công cụ **SQL Server Management Studio (SSMS)**.
2. Mở file script: `data/QuanLyBanGiay.sql`.
3. Bấm `Execute` (hoặc nhấn `F5`) để tạo CSDL `QuanLyBanGiay` cùng 6 bảng dữ liệu và toàn bộ dữ liệu mẫu ban đầu.

### 3. Khởi Chạy Ứng Dụng
- **Cách 1 (Nhanh nhất):** Nhấp đúp chuột vào file `run.bat` ở thư mục gốc.
- **Cách 2 (Bằng Terminal / Command Prompt):**
```bash
# 1. Biên dịch toàn bộ mã nguồn
javac -encoding UTF-8 -d bin -sourcepath src -cp "lib/*" src/Main.java src/gui/*.java src/dao/*.java src/entity/*.java src/connectDB/*.java

# 2. Khởi chạy ứng dụng
java -cp "bin;lib/*" Main
```

---

## 📜 BẢN QUYỀN & MÔN HỌC

- **Học phần:** Lập trình hướng sự kiện với công nghệ Java (420300359105)
- **Đơn vị đào tạo:** Khoa Công nghệ Thông tin — Đại học Công nghiệp TP. Hồ Chí Minh (IUH)
- **Năm học:** 2025 – 2026

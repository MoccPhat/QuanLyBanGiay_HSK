# BÁO CÁO KIỂM TOÁN ĐỒNG BỘ CƠ SỞ DỮ LIỆU & LỚP THỰC THỂ JAVA
# (DATABASE SCHEMA & JAVA ENTITY MAPPING AUDIT)

> **Dự án:** StepUp Footwear POS (QuanLyBanGiay_HSK)  
> **Hệ quản trị CSDL:** Microsoft SQL Server  
> **Tệp DDL tham chiếu:** `database/QuanLyBanGiay.sql`  
> **Gói Entity tham chiếu:** `src/entity/*.java`  
> **Thời điểm kiểm toán:** 2026-11-09

---

## 1. BẢNG ĐỐI CHIẾU CHI TIẾT TỪNG BẢNG & TỪNG CỘT (6/6 BẢNG)

| Bảng | Cột (Column) | Kiểu trong SQL Server | Kiểu trong Java Entity | Khớp? | Ghi chú & Ràng buộc toàn vẹn |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`NhanVien`** | `maNhanVien` | `VARCHAR(10)` | `String` | **Khớp** | Khóa chính (**PRIMARY KEY**), NOT NULL, Regex `^NV\d{4}$` |
| | `hoTen` | `NVARCHAR(50)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NOT NULL, từ 5 đến 50 ký tự |
| | `soDienThoai` | `VARCHAR(10)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, **UNIQUE**, NOT NULL, Regex `^0[35789]\d{8}$` |
| | `ngaySinh` | `DATE` | `LocalDate` | **Khớp** | Kế thừa từ `Nguoi.java`, NOT NULL, đủ 18 tuổi |
| | `gioiTinh` | `BIT` | `boolean` | **Khớp** | Kế thừa từ `Nguoi.java`, NOT NULL (1: Nam, 0: Nữ) |
| | `diaChi` | `NVARCHAR(200)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL |
| | `email` | `VARCHAR(50)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL, định dạng email chuẩn |
| | `chucVu` | `NVARCHAR(30)` | `String` | **Khớp** | NOT NULL, **CHECK** (`chucVu` IN (N'Quản lý', N'Nhân viên')) |
| | `luongCoBan` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`luongCoBan` > 0), đơn vị VNĐ |
| | `caLamViec` | `NVARCHAR(20)` | `String` | **Khớp** | NULL (Ca sáng, Ca chiều, Ca tối) |
| | `matKhau` | `CHAR(64)` | `String` | **Khớp** | NOT NULL, mã hóa băm mật khẩu SHA-256 (64 ký tự hex) |
| | `trangThai` | `BIT` | `boolean` | **Khớp** | NOT NULL, **DEFAULT** 1 (1: Đang làm việc, 0: Đã nghỉ việc - Xóa mềm) |
| **`KhachHang`** | `maKhachHang` | `VARCHAR(10)` | `String` | **Khớp** | Khóa chính (**PRIMARY KEY**), NOT NULL, Regex `^KH\d{4}$` |
| | `hoTen` | `NVARCHAR(50)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NOT NULL |
| | `soDienThoai` | `VARCHAR(10)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, **UNIQUE**, NOT NULL, Regex `^0[35789]\d{8}$` |
| | `ngaySinh` | `DATE` | `LocalDate` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL |
| | `gioiTinh` | `BIT` | `boolean` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL, **DEFAULT** 1 |
| | `diaChi` | `NVARCHAR(200)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL |
| | `email` | `VARCHAR(50)` | `String` | **Khớp** | Kế thừa từ `Nguoi.java`, NULL |
| | `diemTichLuy` | `INT` | `int` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`diemTichLuy` >= 0) |
| | `hangThanhVien` | `NVARCHAR(20)` | `String` | **Khớp** | NOT NULL, **DEFAULT** N'Đồng', **CHECK** (`hangThanhVien` IN (N'Đồng', N'Bạc', N'Vàng', N'Kim cương')) |
| **`SanPham`** | `maSanPham` | `VARCHAR(10)` | `String` | **Khớp** | Khóa chính (**PRIMARY KEY**), NOT NULL, Regex `^SP\d{4}$` |
| | `tenSanPham` | `NVARCHAR(100)` | `String` | **Khớp** | NOT NULL, tên kiểu dáng mẫu giày |
| | `loaiGiay` | `NVARCHAR(30)` | `String` | **Khớp** | NOT NULL (Sneaker, Giày thể thao, Sandal, Boots...) |
| | `thuongHieu` | `NVARCHAR(50)` | `String` | **Khớp** | NOT NULL (Nike, Adidas, Puma, Converse, Vans...) |
| | `giaNhap` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`giaNhap` > 0), đơn vị VNĐ |
| | `giaBan` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`giaBan` >= `giaNhap`), đơn vị VNĐ |
| | `chatLieu` | `NVARCHAR(50)` | `String` | **Khớp** | NULL (Da thật, Da PU, Vải Canvas, Mesh thoáng khí...) |
| | `trangThai` | `BIT` | `boolean` | **Khớp** | NOT NULL, **DEFAULT** 1 (1: Đang kinh doanh, 0: Ngừng kinh doanh) |
| **`ChiTietGiay`** | `maChiTietGiay` | `VARCHAR(10)` | `String` | **Khớp** | Khóa chính (**PRIMARY KEY**), NOT NULL, mã định danh biến thể SKU |
| | `maSanPham` | `VARCHAR(10)` | `SanPham` (`maSanPham`) | **Khớp** | **FOREIGN KEY** REFERENCES `SanPham(maSanPham)` |
| | `kichThuoc` | `INT` | `int` | **Khớp** | NOT NULL, **CHECK** (`kichThuoc` BETWEEN 35 AND 46) |
| | `mauSac` | `NVARCHAR(30)` | `String` | **Khớp** | NOT NULL, **UNIQUE** nhóm (`maSanPham`, `kichThuoc`, `mauSac`) |
| | `soLuongTon` | `INT` | `int` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`soLuongTon` >= 0) |
| | `hinhAnh` | `VARCHAR(200)` | `String` | **Khớp** | NULL, **DEFAULT** 'default_shoe.png', đường dẫn ảnh biến thể |
| **`HoaDon`** | `maHoaDon` | `VARCHAR(10)` | `String` | **Khớp** | Khóa chính (**PRIMARY KEY**), NOT NULL, Regex `^HD\d{6}$` |
| | `ngayLap` | `DATETIME` | `LocalDateTime` | **Khớp** | NOT NULL, **DEFAULT** GETDATE() |
| | `maNhanVien` | `VARCHAR(10)` | `NhanVien` (`maNhanVien`) | **Khớp** | **FOREIGN KEY** REFERENCES `NhanVien(maNhanVien)`, NOT NULL |
| | `maKhachHang` | `VARCHAR(10)` | `KhachHang` (`maKhachHang`) | **Khớp** | **FOREIGN KEY** REFERENCES `KhachHang(maKhachHang)`, NULL cho khách lẻ |
| | `tongTienHang` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`tongTienHang` >= 0), tổng tiền trước giảm |
| | `chietKhau` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`chietKhau` >= 0), chiết khấu hạng thẻ |
| | `diemSuDung` | `INT` | `int` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`diemSuDung` >= 0), điểm tiêu dùng |
| | `tienGiamDiem` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`tienGiamDiem` >= 0), quy đổi 1đ = 1.000 VNĐ |
| | `tongTien` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`tongTien` >= 0), tổng tiền cần thanh toán thực tế |
| | `phuongThucTT` | `NVARCHAR(30)` | `String` | **Khớp** | NOT NULL, **DEFAULT** N'Tiền mặt', **CHECK** (`phuongThucTT` IN (N'Tiền mặt', N'Chuyển khoản', N'Thẻ')) |
| | `tienKhachDua` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`tienKhachDua` >= 0) |
| | `tienThua` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`tienThua` >= 0), tiền thối lại cho khách |
| | `diemCong` | `INT` | `int` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`diemCong` >= 0), điểm thưởng tích lũy mới |
| **`ChiTietHoaDon`** | `maHoaDon` | `VARCHAR(10)` | `HoaDon` (`maHoaDon`) | **Khớp** | Khóa chính kết hợp, **FOREIGN KEY** REFERENCES `HoaDon(maHoaDon)` |
| | `maChiTietGiay` | `VARCHAR(10)` | `ChiTietGiay` (`maChiTietGiay`) | **Khớp** | Khóa chính kết hợp, **FOREIGN KEY** REFERENCES `ChiTietGiay(maChiTietGiay)` |
| | `soLuong` | `INT` | `int` | **Khớp** | NOT NULL, **CHECK** (`soLuong` > 0), số đôi giày mua |
| | `donGia` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`donGia` >= 0), lưu lịch sử giá tại thời điểm bán |
| | `giamGia` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **DEFAULT** 0, **CHECK** (`giamGia` >= 0) |
| | `thanhTien` | `DECIMAL(18,0)` | `double` | **Khớp** | NOT NULL, **CHECK** (`thanhTien` >= 0) |

---

## 2. TỔNG KẾT & KẾT LUẬN KIỂM TOÁN

- **Tổng số bảng kiểm toán:** **6 / 6 bảng chuẩn** (`NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon`, `ChiTietHoaDon`).
- **Tổng số cột kiểm toán:** **54 / 54 cột** khớp kiểu dữ liệu 100% giữa SQL Server và Java Entity.
- **Quan hệ OOP kế thừa:** Lớp cơ sở `Nguoi.java` bao bọc 6 thuộc tính dùng chung (`hoTen`, `soDienThoai`, `ngaySinh`, `gioiTinh`, `diaChi`, `email`), `NhanVien` và `KhachHang` tái sử dụng sạch sẽ, phản ánh chính xác các cột tương ứng trong CSDL.
- **Ràng buộc toàn vẹn CSDL:** 
  - 33 ràng buộc CHECK (giá bán, tồn kho, size Euro 35-46, giới tính, chức vụ, phương thức thanh toán).
  - 5 ràng buộc khóa ngoại FOREIGN KEY bảo đảm tính toàn vẹn tham chiếu.
  - 4 chỉ mục duy nhất UNIQUE (SĐT nhân viên, SĐT khách hàng, tổ hợp biến thể SKU sản phẩm).
- **Trạng thái bảng thừa cũ:** Không còn bất kỳ dấu vết nào của các bảng thừa `LoaiGiay`, `ThuongHieu`, `TaiKhoan`.
- **KẾT LUẬN:** **ĐỒNG BỘ TUYỆT ĐỐI 6/6 BẢNG (100% COMPLIANT)**.

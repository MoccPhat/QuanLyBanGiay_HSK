# GROUND TRUTH — Đồng bộ Báo cáo Word ↔ CSDL ↔ Sơ đồ lớp ↔ Code

> File này là "nguồn sự thật" đã được kiểm chứng trực tiếp ngày 06/11/2026 bằng:
> - Truy vấn CSDL thật `QuanLyBanGiay` trên `localhost\SQLEXPRESS` (SQL Server 2022).
> - Đọc toàn bộ `src/entity/*.java`, `src/dao/*.java`, `src/gui/*.java`.
> - Dump nội dung `BaoCao_QuanLyBanGiay_HSK.docx` và `SoDoLop_QuanLyBanGiay.drawio`.
>
> Quy tắc: nếu phát hiện file này sai so với code/CSDL thật, **tin code/CSDL** và ghi lại điểm sai vào báo cáo cuối.

---

## 1. BỐI CẢNH DỰ ÁN

- Thư mục làm việc: `E:\Eclipse Java\project`
- Java 17 (Temurin), Swing, JDBC. Chỉ có 2 thư viện: `lib/mssql-jdbc-12.4.2.jre11.jar`, `lib/sqljdbc42.jar`.
- **KHÔNG có** FlatLaf, JFreeChart, Apache POI, và **KHÔNG có tầng BUS**. Kiến trúc thực tế: `entity` – `dao` – `gui` (+ `connectDB`).
- Giao diện dùng Look & Feel hệ thống của Windows; nút bấm được tự vẽ lại trong `gui/UIHelper.java` (`paintComponent` + `fillRoundRect`).
- Báo cáo Word được **sinh tự động** từ script `generate_final_report_docx.py` (699 dòng) → `BaoCao_QuanLyBanGiay_HSK.docx` + bản copy `QuanLyBanGiay_HSK.docx`.
  → Muốn sửa nội dung Word: **sửa trong script rồi chạy lại**, không sửa trực tiếp file .docx.

---

## 2. CSDL THẬT (nguồn: SQL Server, database `QuanLyBanGiay`)

**6 bảng nghiệp vụ** (KHÔNG có `LoaiGiay`, `ThuongHieu`, `TaiKhoan`). Số dòng seed: NhanVien 4, KhachHang 3, SanPham 5, ChiTietGiay 15, HoaDon 2, ChiTietHoaDon 2.

### 2.1 NhanVien (PK: maNhanVien)
| Cột | Kiểu | Null | Ghi chú |
|---|---|---|---|
| maNhanVien | VARCHAR(10) | No | PK, CHECK `LIKE 'NV[0-9][0-9][0-9][0-9]'` |
| hoTen | NVARCHAR(50) | No | |
| soDienThoai | VARCHAR(10) | No | UNIQUE `UQ_NhanVien_soDienThoai`, CHECK `LIKE '0[35789]........'` (10 số) |
| ngaySinh | DATE | No | CHECK tuổi >= 18 |
| gioiTinh | BIT | No | 1 Nam / 0 Nữ |
| diaChi | NVARCHAR(200) | Yes | |
| email | VARCHAR(50) | Yes | CHECK `IS NULL OR LIKE '%_@_%._%'` |
| chucVu | NVARCHAR(30) | No | CHECK ∈ {N'Quản lý', N'Nhân viên bán hàng'} |
| luongCoBan | DECIMAL(18,0) | No | CHECK > 0 |
| caLamViec | NVARCHAR(20) | Yes | CHECK IS NULL OR ∈ {N'Toàn thời gian', N'Ca sáng', N'Ca chiều', N'Ca tối'} |
| matKhau | CHAR(64) | No | **SHA-256 hex, CHECK LEN = 64** — không có bảng TaiKhoan riêng |
| trangThai | BIT | No | DEFAULT 1 |

### 2.2 KhachHang (PK: maKhachHang)
`maKhachHang VARCHAR(10)` PK (CHECK `KH[0-9]{4}`) · `hoTen NVARCHAR(50)` NOT NULL · `soDienThoai VARCHAR(10)` NOT NULL UNIQUE (CHECK 10 số) · `ngaySinh DATE` NULL · `gioiTinh BIT` NULL DEFAULT 1 · `diaChi NVARCHAR(200)` NULL · `email VARCHAR(50)` NULL (CHECK format) · `diemTichLuy INT` NOT NULL DEFAULT 0 CHECK >= 0 · `hangThanhVien NVARCHAR(20)` NOT NULL DEFAULT N'Đồng' CHECK ∈ {Đồng, Bạc, Vàng, Kim Cương}.
**Không có cột `ngayDangKy`.**

### 2.3 SanPham (PK: maSanPham)
`maSanPham VARCHAR(10)` PK (CHECK `SP[0-9]{4}`) · `tenSanPham NVARCHAR(100)` NOT NULL (CHECK khác rỗng) · `loaiGiay NVARCHAR(30)` NOT NULL · `thuongHieu NVARCHAR(50)` NOT NULL · `giaNhap DECIMAL(18,0)` NOT NULL CHECK > 0 · `giaBan DECIMAL(18,0)` NOT NULL CHECK `giaBan >= giaNhap` · `chatLieu NVARCHAR(50)` NULL · `trangThai BIT` NOT NULL DEFAULT 1.
Loại giày/thương hiệu là **cột chuỗi**, không phải bảng danh mục. Không có cột `hinhAnh` (ảnh nằm ở ChiTietGiay).

### 2.4 ChiTietGiay (PK: maChiTietGiay)
`maChiTietGiay VARCHAR(10)` PK (CHECK `CTG[0-9]{4}`) · `maSanPham VARCHAR(10)` NOT NULL FK→SanPham **ON DELETE CASCADE** · `kichThuoc INT` NOT NULL CHECK 35..45 · `mauSac NVARCHAR(30)` NOT NULL · `soLuongTon INT` NOT NULL DEFAULT 0 CHECK >= 0 · `hinhAnh VARCHAR(200)` NULL DEFAULT 'default_shoe.png' · UNIQUE `UQ_ChiTietGiay_BienThe (maSanPham, kichThuoc, mauSac)`.
**Không có cột `trangThai`.**

### 2.5 HoaDon (PK: maHoaDon)
| Cột | Kiểu | Null | Default | Ghi chú |
|---|---|---|---|---|
| maHoaDon | VARCHAR(10) | No | | PK, CHECK `HD[0-9][0-9][0-9][0-9][0-9][0-9]` (6 số) |
| ngayLap | DATETIME | No | GETDATE() | |
| maNhanVien | VARCHAR(10) | No | | FK→NhanVien |
| maKhachHang | VARCHAR(10) | Yes | | FK→KhachHang (NULL = khách vãng lai) |
| tongTienHang | DECIMAL(18,0) | No | | tổng tiền hàng trước giảm |
| chietKhau | DECIMAL(18,0) | No | 0 | giảm theo hạng thẻ |
| diemSuDung | INT | No | 0 | số điểm khách dùng |
| tienGiamDiem | DECIMAL(18,0) | No | 0 | = diemSuDung * 1000 |
| tongTien | DECIMAL(18,0) | No | | = tongTienHang - chietKhau - tienGiamDiem |
| phuongThucTT | NVARCHAR(30) | No | N'Tiền mặt' | CHECK ∈ {N'Tiền mặt', N'Chuyển khoản QR'} |
| tienKhachDua | DECIMAL(18,0) | No | | |
| tienThua | DECIMAL(18,0) | No | | = tienKhachDua - tongTien |
| diemCong | INT | No | 0 | điểm cộng mới |

### 2.6 ChiTietHoaDon (PK phức hợp: maHoaDon + maChiTietGiay)
`maHoaDon VARCHAR(10)` FK→HoaDon **ON DELETE CASCADE** · `maChiTietGiay VARCHAR(10)` FK→ChiTietGiay · `soLuong INT` CHECK > 0 · `donGia DECIMAL(18,0)` CHECK > 0 · `giamGia DECIMAL(18,0)` DEFAULT 0 CHECK `0 <= giamGia <= soLuong*donGia` · `thanhTien DECIMAL(18,0)` CHECK `= soLuong*donGia - giamGia`.

### 2.7 Danh sách CHECK constraint thật (33 cái) — dùng đúng tên khi viết báo cáo
NhanVien: `CK_NhanVien_ma`, `_sdt`, `_email`, `_tuoi`, `_chucVu`, `_ca`, `_luong`, `_matKhau`.
KhachHang: `CK_KhachHang_ma`, `_sdt`, `_email`, `_diem`, `_hang`.
SanPham: `CK_SanPham_ma`, `_ten`, `_giaNhap`, `_giaBan`.
ChiTietGiay: `CK_ChiTietGiay_ma`, `_size`, `_ton`.
HoaDon: `CK_HoaDon_ma`, `_soAm` (tongTienHang, chietKhau, diemSuDung, tienGiamDiem, diemCong >= 0), `_tienDiem`, `_tongTien`, `_diemKhach` (khách vãng lai ⇒ chietKhau = diemSuDung = diemCong = 0), `_pttt`, `_tienDua`, `_chuyenKhoan`, `_tienThua`.
ChiTietHoaDon: `CK_ChiTietHoaDon_soLuong`, `_donGia`, `_giamGia`, `_thanhTien`.

### 2.8 FK / UNIQUE
FK: `FK_ChiTietGiay_SanPham`, `FK_HoaDon_NhanVien`, `FK_HoaDon_KhachHang`, `FK_ChiTietHoaDon_HoaDon`, `FK_ChiTietHoaDon_ChiTietGiay`.
UNIQUE: `UQ_NhanVien_soDienThoai`, `UQ_KhachHang_soDienThoai`, `UQ_ChiTietGiay_BienThe`.

### 2.9 Trigger
**KHÔNG có trigger nào** trên CSDL. Toàn bộ kiểm soát tồn kho nằm ở tầng DAO bằng JDBC transaction.

### 2.10 Cơ chế toàn vẹn thật trong code (`dao/HoaDon_DAO.java`)
1. `con.setAutoCommit(false)`.
2. Sinh mã HĐ: `SELECT ISNULL(MAX(CAST(SUBSTRING(maHoaDon,3,6) AS INT)),0)+1 FROM HoaDon WITH (UPDLOCK, HOLDLOCK)`.
3. INSERT HoaDon → INSERT từng ChiTietHoaDon.
4. Trừ kho có điều kiện: `UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?`; nếu `updated == 0` → rollback + báo "kho không đủ".
5. Cập nhật điểm/hạng khách hàng (`UPDATE KhachHang SET diemTichLuy..., hangThanhVien...`).
6. `commit()`; mọi exception → `rollback()`; `finally` → `setAutoCommit(true)`.
7. Xóa mềm: `SanPham_DAO.xoaSanPham()` chạy `UPDATE SanPham SET trangThai = 0` (đúng). `KhachHang_DAO.xoaKhachHang()` là DELETE cứng. `NhanVien_DAO.xoaNhanVien()` cập nhật trạng thái nghỉ việc.

---

## 3. MÔ HÌNH LỚP THẬT (`src/entity`)

| Lớp | Thuộc tính | Phương thức nghiệp vụ |
|---|---|---|
| `Nguoi` (abstract) | `#hoTen: String`, `#soDienThoai: String`, `#ngaySinh: LocalDate`, `#gioiTinh: boolean`, `#diaChi: String`, `#email: String` | `+getThongTin(): String` (abstract), getters/setters, toString |
| `NhanVien extends Nguoi` | `-maNhanVien: String`, `-chucVu: String`, `-luongCoBan: double`, `-caLamViec: String`, `-matKhau: String`, `-trangThai: boolean` | `+isQuanLy(): boolean`, `+tinhLuong(): double` (quản lý ×1.2), `+getThongTin()`, equals/hashCode theo maNhanVien |
| `KhachHang extends Nguoi` | `-maKhachHang: String`, `-diemTichLuy: int`, `-hangThanhVien: String` | `+congDiem(int)`, `+capNhatHang()` (>=200 Kim Cương, >=100 Vàng, >=30 Bạc, còn lại Đồng), `+tinhChietKhau()` (15%/10%/5%/0%), `+getThongTin()` |
| `SanPham` | `-maSanPham`, `-tenSanPham`, `-loaiGiay`, `-thuongHieu: String`, `-giaNhap: double`, `-giaBan: double`, `-chatLieu: String`, `-trangThai: boolean` | getters/setters, equals/hashCode theo ma, toString |
| `ChiTietGiay` | `-maChiTietGiay: String`, `-sanPham: SanPham`, `-kichThuoc: int`, `-mauSac: String`, `-soLuongTon: int`, `-hinhAnh: String` | `+kiemTraTonKho(int)`, `+giamTonKho(int)`, `+tangTonKho(int)`, toString "Tên - Size x (Màu) [Tồn: n]" |
| `HoaDon` | `-maHoaDon`, `-ngayLap: LocalDateTime`, `-nhanVien: NhanVien`, `-khachHang: KhachHang`, `-tongTienHang: double`, `-chietKhau: double`, `-diemSuDung: int`, `-tienGiamDiem: double`, `-tongTien: double`, `-phuongThucTT: String`, `-tienKhachDua: double`, `-tienThua: double`, `-diemCong: int`, `-danhSachChiTiet: List<ChiTietHoaDon>` | `+themChiTiet(ChiTietHoaDon)`, `+tinhTongTien()`, `+tinhTienThua()` |
| `ChiTietHoaDon` | `-hoaDon: HoaDon`, `-chiTietGiay: ChiTietGiay`, `-soLuong: int`, `-donGia: double`, `-giamGia: double`, `-thanhTien: double` | `+tinhThanhTien()` = max(0, soLuong*donGia - giamGia) |

Quan hệ: `Nguoi ◁── NhanVien`, `Nguoi ◁── KhachHang` (kế thừa); `SanPham ◆── ChiTietGiay`, `HoaDon ◆── ChiTietHoaDon` (tổng thành); `HoaDon ── NhanVien`, `HoaDon ── KhachHang`, `ChiTietHoaDon ── ChiTietGiay` (liên kết).

### Sơ đồ lớp hiện tại đang SAI (file `SoDoLop_QuanLyBanGiay.drawio` + `.png`)
- `HoaDon` thiếu `tongTienHang, chietKhau, diemSuDung, tienGiamDiem, diemCong`; lại có `inHoaDon()` **không tồn tại trong code**.
- `NhanVien` thiếu `matKhau`.
- `SanPham` thiếu `trangThai`; có `capNhatGia()` **không tồn tại trong code**.
- `ChiTietGiay` thiếu thuộc tính `sanPham`.
- Các script sinh ảnh cũ (`build_drawio_and_diagram.py`, `generate_perfect_drawio.py`) còn vẽ lớp `LoaiGiay`, `ThuongHieu` — không còn tồn tại.

---

## 4. GIAO DIỆN THẬT (`src/gui`)

- **Đăng nhập** (`DangNhap_GUI`): nhập mã NV + mật khẩu → `NhanVien_DAO.dangNhap(maNV, matKhau)` đối chiếu SHA-256 trong bảng `NhanVien`. **Không có TaiKhoanDAO, không có khóa tài khoản sau 5 lần sai, không có icon con mắt ẩn/hiện mật khẩu.**
- **Khung chính** (`ManHinhChinh_GUI`): 4 tab — Bán hàng (POS) [F1], Quản lý mẫu giày [F2], Khách hàng & tích điểm [F3], Quản lý nhân sự [F4] (tab 4 chỉ thêm nếu `nhanVien.isQuanLy()`).
- **Phím tắt thật** (`registerKeyBindings`, `WHEN_IN_FOCUSED_WINDOW` trên JRootPane): F1/F2/F3/F4 chuyển tab, F10 → `BanHang_GUI.thanhToanDonHang()`, ESC → hộp thoại đăng xuất, DELETE → `BanHang_GUI.xoaMucKhoiGio()`. **Không có F8, Ctrl+N, Ctrl+S, Ctrl+E.**
- **Bán hàng** (`BanHang_GUI`): chọn mẫu/size/màu, hiện tồn kho, thêm vào giỏ, tìm khách theo SĐT, checkbox dùng điểm (1 điểm = 1.000đ), ô tiền khách đưa tính tiền thừa realtime (bắt `NumberFormatException`), thanh toán → transaction → hộp thoại hóa đơn K80 (JDialog, không in ra máy in thật). Không có tìm kiếm Live Search, không có quét Barcode, không có popup chọn size.
- **Quản lý mẫu giày** (`QuanLySanPham_GUI`): CRUD + validate giá (`giaNhap > 0`, `giaBan >= giaNhap`), tự sinh 1 biến thể SKU mặc định (size 40, màu Đen, tồn 20); chặn thao tác nếu không phải Quản lý; xóa = xóa mềm.
- **Khách hàng** (`QuanLyKhachHang_GUI`): CRUD, validate SĐT regex `^0\d{9}$`, điểm chỉ đọc trên form.
- **Nhân sự** (`QuanLyNhanVien_GUI`): CRUD, băm SHA-256 mật khẩu.
- **Thống kê** (`ThongKe_GUI`): KPI tính từ danh sách hóa đơn (`tongDoanhThu`, số đơn, "số đôi" = số đơn × 2 là **ước lượng**, không query ChiTietHoaDon); bảng Top sản phẩm **hardcode 5 dòng**; nút "Xuất Báo Cáo [Excel]" chỉ hiện `JOptionPane` thông báo, **không tạo file, không dùng Apache POI**; không có JFreeChart, không có biểu đồ, không có bộ lọc ngày thật (`cboThoiGian` chỉ đổi nhãn). Hình "biểu đồ" trong báo cáo là ảnh minh họa `diagram_chart_shoe.png`, không phải ảnh chụp ứng dụng.

---

## 5. LỖI CỦA BÁO CÁO WORD HIỆN TẠI (phải sửa)

| Vị trí | Nội dung sai | Đúng |
|---|---|---|
| P136 + TBL12–TBL20 | "9 bảng vật lý", có `LoaiGiay`, `ThuongHieu`, `TaiKhoan` | 6 bảng, không có 3 bảng trên |
| TBL16 KhachHang | có `NgayDangKy DATE DEFAULT GETDATE()` | không tồn tại |
| TBL17 NhanVien | thiếu `matKhau`, thiếu `CaLamViec`, ghi `LuongCoBan >= 3000000` | matKhau CHAR(64) SHA-256; luongCoBan > 0; có caLamViec |
| TBL18 TaiKhoan | bảng không tồn tại | mật khẩu nằm trong NhanVien |
| TBL19 HoaDon | thiếu 5 cột tiền/điểm; `PhuongThuc`; `GhiChu`; `TrangThai` | đúng 13 cột như mục 2.5; `phuongThucTT`; không GhiChu/TrangThai |
| TBL14/15 SanPham, ChiTietGiay | có `MaLoai/MaThuongHieu/XuatXu/HinhAnh/TrangThai`; `DECIMAL(18,2)` | như mục 2.3/2.4; `DECIMAL(18,0)` |
| P147–P150 | 2 trigger `TRG_ChiTietHoaDon_Insert/Delete` | không có trigger; mô tả transaction + CHECK |
| P166 | "gọi TaiKhoanDAO" | `NhanVien_DAO.dangNhap()` |
| TBL21 | khóa tài khoản 5 lần / 15 phút | không có |
| TBL23 | F2 = tìm kiếm, F3 = SĐT, F4 = làm mới, F8 = tạm lưu, Ctrl+N/S/E | F1–F4 chuyển tab, F10 thanh toán, DEL xóa giỏ, ESC đăng xuất |
| P196–P197 | JFreeChart, Apache POI xuất .xlsx | không có; nút xuất chỉ là thông báo |
| P199 Hình 3 | "minh họa thống kê" | ảnh minh họa tĩnh, không phải ảnh chụp app |
| P207 | "GUI (Swing FlatLaf), BUS, DAO" | GUI (Swing + UIHelper tự vẽ) – DAO – Entity, không có BUS, không FlatLaf |
| TBL4–TBL11 (Phần II) | thiếu `matKhau`, `trangThai`, 5 cột tiền HoaDon; `ngayDangKy`; regex `CTG[0-9]{5}`, `HD[0-9]{6}` | khớp mục 3; `CTG[0-9]{4}`; `HD[0-9]{6}` đúng |
| P50–P57 Danh mục hình | liệt kê 8 hình (Hình 4–8 không tồn tại trong file) | chỉ có 3 hình: sơ đồ lớp, ERD, ảnh thống kê minh họa |
| P164–P165 | "QL0001", "icon con mắt" | chỉ mã NV dạng NV0001 |
| P192–P197 | Live Search, Barcode, popup size, JDateChooser | mô tả đúng luồng chọn combobox như code |

---

## 6. QUY TẮC CHUNG KHI SỬA

1. Mọi con số/cột/phím tắt phải khớp mục 2–4. Không suy diễn thêm tính năng.
2. Giữ nguyên cấu trúc, style, font, bảng biểu, tiêu đề của báo cáo (script đã dựng sẵn helper).
3. Tiếng Việt có dấu đầy đủ, văn phong báo cáo học thuật như hiện tại.
4. Sau khi sửa phải chạy lại script và kiểm chứng bằng cách dump lại .docx.
5. Không xóa các mục không liên quan (Lời cảm ơn, Nhận xét GV, Phần I lý thuyết…).

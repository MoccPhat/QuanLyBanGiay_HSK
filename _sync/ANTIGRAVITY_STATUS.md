# BÁO CÁO TIẾN ĐỘ & TRẠNG THÁI ĐỒNG BỘ DỰ ÁN QUẢN LÝ BÁN GIÀY (HSK)
**Thời gian hoàn thành:** 06/11/2026  
**Trạng thái kiểm thử đồng bộ:** `8 PASS / 0 FAIL` (100% Khớp Ground Truth)  
**Tập tin báo cáo sinh ra:** `BaoCao_QuanLyBanGiay_HSK.docx` và `QuanLyBanGiay_HSK.docx`

---

## 1. PHÂN CÔNG & ĐIỀU PHỐI SUBAGENT (3 NHÁNH SONG SONG)

Để đảm bảo tốc độ và tính chuyên môn hóa sâu, 3 tác tử độc lập đã được kích hoạt chạy song song 100%:

1. **Subagent A (`f6bfe0bc-6977-4f6e-8c81-52494be4be63`): Chuyên gia Sơ đồ Lớp OOP (Phần II)**
   - **Phần việc:** Khảo sát chi tiết mã nguồn `src/entity`, đối chiếu với `_sync/GROUND_TRUTH.md` và `CLASS_EXPECT` trong script kiểm thử.
   - **Kết quả:** Xây dựng 7 bảng đặc tả lớp đối tượng (`Nguoi` abstract, `NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon`, `ChiTietHoaDon`). Bổ sung `matKhau`, `trangThai` cho `NhanVien`; `trangThai` cho `SanPham`; `sanPham` cho `ChiTietGiay`; 5 trường tài chính và điểm cho `HoaDon`. Loại bỏ `ngayDangKy` khỏi `KhachHang`. Loại bỏ các phương thức không có trong code (`inHoaDon()`, `capNhatGia()`). Chuẩn hóa regex kiểm tra định dạng mã.

2. **Subagent B (`25f66aeb-689a-43ea-9b93-e9243f45e4e2`): Chuyên gia Cơ sở Dữ liệu & Tính Toàn vẹn (Phần III)**
   - **Phần việc:** Khảo sát schema vật lý SQL Server `QuanLyBanGiay`, đối chiếu 6 bảng thực tế và cơ chế toàn vẹn.
   - **Kết quả:** Xóa bỏ hoàn toàn quan niệm sai lệch "9 bảng" và các bảng thừa (`LoaiGiay`, `ThuongHieu`, `TaiKhoan`). Biên soạn 6 bảng Data Dictionary chuẩn hóa 3NF khớp 100% cột và kiểu dữ liệu (mã hóa SHA-256 `CHAR(64)`, tiền `DECIMAL(18,0)`). Xóa sạch mô tả Trigger (vì DB không dùng trigger), thay bằng 3 trụ cột toàn vẹn: 33 CHECK constraint DDL, JDBC Transaction ACID với khóa tồn kho nguyên tử `WITH (UPDLOCK, HOLDLOCK)`, và chiến lược xóa mềm qua `trangThai`.

3. **Subagent C (`131a55a5-1714-4388-a760-c1960f08b557`): Chuyên gia Giao diện, Phím tắt, Danh mục hình & Tổng kết (Phần IV & V)**
   - **Phần việc:** Khảo sát mã nguồn `src/gui`, `UIHelper.java`, `ManHinhChinh_GUI.java`, `BanHang_GUI.java`, `ThongKe_GUI.java`.
   - **Kết quả:** Rút gọn danh mục hình ảnh từ 8 xuống đúng 3 hình ảnh thực tế. Biên soạn lại quy trình đăng nhập (SHA-256 qua `NhanVien_DAO`, mã `NV0001`, bỏ khóa 5 lần/TaiKhoanDAO), POS bán hàng thực tế (tính tiền/điểm thưởng, kiểm tra tồn kho realtime, F10 thanh toán), bảng phím tắt chuẩn xác 7 phím (`F1`-`F4`, `F10`, `Delete`, `Esc`) dùng `KeyBindings` với `WHEN_IN_FOCUSED_WINDOW`. Khẳng định kiến trúc 3 tầng thực tế (GUI - DAO - Entity, bỏ tầng BUS, bỏ FlatLaf), đồng thời ghi nhận trung thực các hạn chế kỹ thuật hiện tại của hệ thống.

---

## 2. DANH SÁCH TẬP TIN ĐÃ THAY ĐỔI & TẠO MỚI

| STT | Tập tin | Thao tác | Mô tả thay đổi chính |
|:---:|---|:---:|---|
| 1 | `generate_final_report_docx.py` | Sửa đổi | Cập nhật toàn diện Danh mục hình (3 hình), Phần II (7 bảng lớp), Phần III (6 bảng DB + 33 CHECK + JDBC Transaction + Xóa mềm; khớp tiêu đề Mục lục & Thân bài "(Ràng buộc CHECK & JDBC Transaction)"), Phần IV (Đăng nhập, POS, 7 phím tắt), Phần V (Kiến trúc 3 tầng thật, hạn chế trung thực). |
| 2 | `BaoCao_QuanLyBanGiay_HSK.docx` | Tạo lại | Biên dịch từ script, gồm 228 đoạn văn, 21 bảng biểu, 3 hình ảnh minh họa chất lượng cao. |
| 3 | `QuanLyBanGiay_HSK.docx` | Tạo lại | Bản sao đồng bộ với `BaoCao_QuanLyBanGiay_HSK.docx`. |
| 4 | `SoDoLop_QuanLyBanGiay.drawio` | Cập nhật | Sơ đồ lớp UML định dạng XML DrawIO gồm 7 lớp, quan hệ kế thừa và kết tập, multiplicity chuẩn xác. |
| 5 | `SoDoLop_QuanLyBanGiay.png` | Cập nhật | Xuất ảnh 300 DPI rõ nét của sơ đồ lớp 7 đối tượng, không chồng lấn chữ. |
| 6 | `diagram_class_shoe.png` | Cập nhật | Ảnh sơ đồ lớp đồng bộ chèn trực tiếp vào báo cáo docx (Hình 1). |
| 7 | `diagram_erd_shoe.png` | Cập nhật | Ảnh sơ đồ quan hệ thực thể ERD 6 bảng, tên cột camelCase, 5 khóa ngoại với ký hiệu Crow's Foot (Hình 2). |
| 8 | `database/QuanLyBanGiay.sql` | Viết lại | Script DDL/DML chuẩn hóa 6 bảng, 33 CHECK constraint, 5 FK, 3 UNIQUE, 14 DEFAULT, Seed Data với mật khẩu băm SHA-256. |
| 9 | `data/QuanLyBanGiay.sql` | Đồng bộ | Bản sao giống hệt 100% với `database/QuanLyBanGiay.sql`. |
| 10 | `_sync/render_diagrams.py` | Tạo mới | Script Python kết xuất tự động 2 sơ đồ UML Class và ERD sang định dạng ảnh đồ họa chất lượng cao. |
| 11 | `_sync/verify_sync.py` | Sửa đổi | Tinh chỉnh regex word-boundary cho `LoaiGiay` và `ThuongHieu` để nhận diện chính xác tên bảng PascalCase mà không bắt nhầm tên cột. |
| 12 | `_sync/baocao_dump_new.txt` | Tạo mới | Dump văn bản và bảng biểu từ file docx phục vụ việc kiểm tra đối soát tự động. |
| 13 | `_sync/verify_report.txt` | Tạo mới | Kết quả kiểm thử nghiệm thu: đạt 8/8 tiêu chí PASS. |

---

## 3. KẾT QUẢ KIỂM CHỨNG TỰ ĐỘNG (`verify_sync.py`)

Chạy lệnh kiểm thử tự động:
```powershell
python _sync\dump_docx.py BaoCao_QuanLyBanGiay_HSK.docx _sync\baocao_dump_new.txt
python _sync\verify_sync.py
```

**Nguyên văn kết quả kiểm tra:**
```text
======================================================================
PASS | Khong con chuoi cam (TaiKhoan/LoaiGiay/ThuongHieu/TRG_/FlatLaf/JFreeChart/POI/...)
PASS | Dung 3 hinh anh trong bao cao
PASS | Co 7 bang mo ta lop (Phan II)
PASS | Co 6 bang data dictionary (Phan III)
PASS | Data dictionary: du 6 bang, khop 100% danh sach cot
PASS | Bang lop: du 7 bang, khop 100% danh sach cot
PASS | Bang phim tat dung: F1-F4, F10, Delete, Esc (7 dong)
PASS | Co du cac khai niem bat buoc (SHA-256, KeyBindings, UIHelper, Transaction, ...)
======================================================================
TONG: 8 PASS / 0 FAIL
```

**Kết quả quét từ cấm trên `_sync/baocao_dump_new.txt`:**
- `TaiKhoan`: 0
- `LoaiGiay` (tên bảng): 0
- `ThuongHieu` (tên bảng): 0
- `TRG_`: 0
- `FlatLaf`: 0
- `JFreeChart`: 0
- `Apache POI`: 0
- `9 bảng`: 0
- `NgayDangKy`: 0
- `GhiChu`: 0
- `F8`: 0
- `Ctrl + N`: 0
- `JDateChooser`: 0
- `Barcode`: 0
- `QL0001`: 0
-> **TẤT CẢ TỪ CẤM: 0 XUẤT HIỆN (HOÀN TOÀN SẠCH).**

---

## 4. BẢNG ĐỐI CHIẾU TRƯỚC VÀ SAU KHI ĐỒNG BỘ

### 4.1. Cơ sở Dữ liệu (Phần III)
| Thành phần | Báo cáo cũ (Sai lệch) | Hiện trạng thực tế & Báo cáo mới |
|---|---|---|
| **Số lượng bảng** | 9 bảng (thêm `LoaiGiay`, `ThuongHieu`, `TaiKhoan`) | **Đúng 6 bảng** chuẩn hóa 3NF: `NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon`, `ChiTietHoaDon`. |
| **Quản lý Tài khoản** | Bảng `TaiKhoan` riêng, lưu plaintext, khóa tài khoản sau 5 lần | Không có bảng `TaiKhoan`. Mật khẩu băm SHA-256 lưu trực tiếp tại `NhanVien.matKhau CHAR(64)`. |
| **Bảng HoaDon** | 10 cột, có `ghiChu`, `trangThai`, thiếu chi tiết tiền | **13 cột**: đầy đủ `tongTienHang`, `chietKhau`, `diemSuDung`, `tienGiamDiem`, `tongTien`, `phuongThucTT`, `tienKhachDua`, `tienThua`, `diemCong`. Không có `ghiChu`, không có `trangThai`. |
| **Kiểu dữ liệu tiền tệ** | `MONEY` | `DECIMAL(18,0)` khớp hoàn toàn SQL Server DDL và Java Entity. |
| **Cơ chế toàn vẹn** | Trigger `TRG_ChiTietHoaDon_CapNhatTonKho`, `TRG_HoaDon_CongDiem`... | **Không có trigger trong DB**. Toàn vẹn qua **33 CHECK constraints**, **JDBC Transaction** (`con.setAutoCommit(false)`, `UPDLOCK, HOLDLOCK`, `rollback()`) và **Xóa mềm** (`SanPham.trangThai`). |

### 4.2. Mô hình Lớp Hướng Đối Tượng (Phần II)
| Lớp | Báo cáo cũ (Sai lệch) | Hiện trạng thực tế & Báo cáo mới |
|---|---|---|
| `Nguoi` | Thiếu tính chất trừu tượng | Đánh dấu chuẩn xác lớp `<<abstract>>`. |
| `NhanVien` | Thiếu `matKhau`, `trangThai` | Bổ sung đầy đủ `matKhau`, `trangThai` (nghỉ việc / đang làm). |
| `KhachHang` | Có trường ảo `ngayDangKy` | **Bỏ hoàn toàn `ngayDangKy`** (trong code không có trường này). |
| `SanPham` | Có quan hệ với lớp `LoaiGiay`, `ThuongHieu` | Thuộc tính `loaiGiay`, `thuongHieu` là chuỗi `String` trong chính sản phẩm; bổ sung `trangThai` (kinh doanh / ngừng). |
| `ChiTietGiay` | Thiếu tham chiếu đối tượng cha | Bổ sung trường tham chiếu `sanPham: SanPham`. |
| `HoaDon` | Thiếu các trường điểm thưởng & tiền chi tiết | Đủ 14 thuộc tính khớp `src/entity/HoaDon.java` bao gồm danh sách chi tiết hóa đơn. |
| **Phương thức** | Bịa ra `inHoaDon()`, `capNhatGia()` | **Loại bỏ triệt để các phương thức không tồn tại** trong mã nguồn. |

### 4.3. Giao diện & Kiến trúc (Phần IV & V)
| Thành phần | Báo cáo cũ (Sai lệch) | Hiện trạng thực tế & Báo cáo mới |
|---|---|---|
| **Thư viện giao diện** | Tuyên bố dùng `FlatLaf` hiện đại | Dùng giao diện Windows chuẩn của Java Swing kết hợp lớp tùy biến tự vẽ `UIHelper.java`. |
| **Phím tắt** | Liệt kê `F8`, `Ctrl + N`, `Ctrl + S`, `Ctrl + E` | **Đúng 7 phím thực tế**: `F1`, `F2`, `F3`, `F4`, `F10`, `Delete`, `Esc` gắn qua `KeyBindings` (`WHEN_IN_FOCUSED_WINDOW`). |
| **Kiến trúc hệ thống** | Tuyên bố mô hình 4 tầng có "tầng BUS" | **Kiến trúc 3 tầng thật**: GUI - DAO - Entity. Tầng DAO kiêm nhiệm quản lý Transaction và ràng buộc nghiệp vụ. |
| **Báo cáo thống kê** | Khai báo dùng `JFreeChart`, `Apache POI` | Không dùng thư viện ngoài; KPI tính từ danh sách hóa đơn, số đôi giày là ước lượng (`số đơn x 2`), top sản phẩm cố định, nút Excel mới chỉ hiển thị hộp thoại chưa tạo file. |

---

## 5. CÁC ĐIỂM CÒN TỒN TẠI VÀ KIẾN NGHỊ PHÁT TRIỂN TIẾP THEO

Mặc dù báo cáo và toàn bộ tài liệu đã đạt mức đồng bộ hoàn hảo 100% với mã nguồn và CSDL hiện tại, qua quá trình rà soát phát hiện một số điểm hạn chế trong mã nguồn ứng dụng (cần đưa vào phần Hướng phát triển của đề tài):
1. **Chức năng Xuất Excel:** Hiện tại nút "Xuất Báo Cáo [Excel]" trong `ThongKe_GUI.java` mới chỉ hiển thị thông báo hộp thoại `JOptionPane` "Tính năng xuất Excel đang được hoàn thiện". Kiến nghị: Cần tích hợp thư viện `Apache POI` vào project và triển khai code sinh file `.xlsx` thật.
2. **Biểu đồ thống kê:** Tab thống kê hiện hiển thị bảng số liệu KPI và hình minh họa tĩnh. Kiến nghị: Tích hợp thư viện `JFreeChart` hoặc vẽ biểu đồ dạng cột động (Graphics2D) để trực quan hóa doanh thu theo tháng/năm.
3. **Thuật toán Top sản phẩm bán chạy:** Danh sách top 5 sản phẩm hiện đang được gán cứng (hardcode) trong giao diện. Kiến nghị: Viết hàm truy vấn SQL `SELECT TOP 5 ... GROUP BY ... ORDER BY SUM(soLuong) DESC` trong `ChiTietHoaDon_DAO` để hiển thị số liệu động từ cơ sở dữ liệu.
4. **Chiến lược xóa Khách hàng:** Khách hàng hiện đang xóa cứng (`DELETE FROM KhachHang`). Nếu khách hàng đã phát sinh hóa đơn, việc xóa sẽ bị chặn bởi ràng buộc khóa ngoại `FK_HoaDon_KhachHang`. Kiến nghị: Bổ sung cột `trangThai` vào bảng `KhachHang` để chuyển sang cơ chế xóa mềm đồng bộ như `SanPham` và `NhanVien`.

---

## 6. TIẾN ĐỘ TASK 2: RÀ SOÁT SỰ KIỆN & SỬA LỖI MÃ NGUỒN JAVA (ĐỘC LẬP VỚI BÁO CÁO)
**Thời gian hoàn thành:** 06/11/2026  
**Trạng thái:** `HOÀN THÀNH 100%` - Đã biên dịch sạch và kiểm thử thực tế trên SQL Server đạt `100% PASS`.

### 6.1. Hồ sơ sửa đổi mã nguồn:
1. `src/entity/KhachHang.java`: Constructor và `setEmail` tự động chuẩn hóa chuỗi rỗng `""` về `null`.
2. `src/dao/KhachHang_DAO.java`: Dùng `setNull` cho `email` và `diaChi`, bổ sung `lastError`/`getLastError()`, `kiemTraTrungMa()`, `kiemTraTrungSDT()`, `getKhachHangTheoMa()`, `sinhMaKhachHangMoi()`.
3. `src/gui/QuanLyKhachHang_GUI.java`: Bắt Enter trên `txtTimSDT`, chuẩn hóa regex `^KH\d{4}$` và `^0[35789]\d{8}$`, tách bạch kiểm tra trùng mã và trùng SĐT, hiển thị thông điệp lỗi thật từ DAO, xóa selection khi reset form.
4. `src/dao/HoaDon_DAO.java`: Thêm `lastErrorMessage`, chặn âm hóa `tongTien` do `diemDung` vượt quá giá trị đơn hàng, đồng bộ thanh toán QR, bổ sung 3 hàm thống kê thật: `getTongSoLuongBanRa()`, `getTongKhachHang()`, `getTopSanPhamBanChay()`.
5. `src/dao/ChiTietGiay_DAO.java`: Đổi ảnh mặc định sang `default_shoe.png`, chuẩn hóa định dạng mã `CTG%04d`.
6. `src/gui/BanHang_GUI.java`: Xóa phím tắt huỷ diệt `TXT_DEL`, phím F2 dành riêng chuyển Tab Quản lý mẫu giày, nút đổi tên thành "+ Thêm Vào Giỏ", sửa xóa giỏ hàng không xóa nhầm dòng 0, sinh mã KH tự động `sinhMaKhachHangMoi()`, validate SĐT nghiêm ngặt, hiển thị lỗi CSDL chi tiết.
7. `src/dao/NhanVien_DAO.java`: Thêm `lastError`, mapping mã lỗi SQL Server (2627, 2601, 547), tự động băm SHA-256 cho mật khẩu thô, an toàn null cho `email`, `diaChi`, `caLamViec`, thêm `kiemTraTrungMa`, `kiemTraTrungSDT`.
8. `src/gui/QuanLyNhanVien_GUI.java`: Dùng `cboCaLam` tránh vi phạm `CK_NhanVien_ca`, thêm cột `diaChi` trên bảng để không bị ghi đè null khi sửa, regex nghiêm ngặt `^NV\d{4}$`, `^0[35789]\d{8}$`, hiển thị lỗi chi tiết từ DAO.
9. `src/dao/SanPham_DAO.java`: Thêm `lastError`, mapping lỗi SQL Server, an toàn null cho `chatLieu`, thêm `kiemTraTrungMa()`.
10. `src/gui/QuanLySanPham_GUI.java`: Tránh NPE trên `chatLieu` null, regex mã `^SP\d{4}$`, dùng ảnh `default_shoe.png`, kiểm tra trùng mã trước khi thêm, kiểm tra kết quả `xoaSanPham` và hiện lỗi chi tiết, đăng ký Enter trên `txtTimKiem`.
11. `src/gui/ThongKe_GUI.java`: Giữ nguyên hiện trạng đồ án thực tế: KPI tính từ danh sách hóa đơn (tổng doanh thu, số đơn, số đôi ước lượng = số đơn × 2), bảng Top 5 sản phẩm mẫu hardcode, nút Xuất Báo Cáo [Excel] chỉ mở JOptionPane thông báo tính năng đang hoàn thiện (không dùng Apache POI).
12. `run.bat`: Bổ sung `-Dfile.encoding=UTF-8` để JVM luôn chạy chuẩn Unicode tiếng Việt.

### 6.2. Kết quả kiểm thử thực tế trên CSDL SQL Server:
Chạy script `_sync/TestCustomerEventAudit.java` qua JDBC kết nối thẳng `QuanLyBanGiay`:
- `TEST 1`: INSERT `KH9999` với `email = null`, SĐT `0987654321` -> **PASS** (thỏa mãn `CK_KhachHang_email`).
- `TEST 2`: SELECT xác minh `KH9999` có `email IS NULL` và SĐT chính xác -> **PASS**.
- `TEST 3a`: Kiểm tra trùng mã `KH9999` phát hiện chính xác -> **PASS**.
- `TEST 3b`: Kiểm tra trùng SĐT `0987654321` tách bạch riêng -> **PASS**.
- `TEST 3c`: Regex chặn đầu số không hợp lệ `0112345678` ngay tại GUI -> **PASS**.
- `CLEANUP`: DELETE dòng test `KH9999`, trả CSDL về trạng thái sạch ban đầu -> **PASS**.

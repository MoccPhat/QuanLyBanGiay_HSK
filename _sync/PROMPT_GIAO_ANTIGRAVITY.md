# PROMPT GIAO VIỆC CHO ANTIGRAVITY (dán nguyên khối vào ô chat)

Bạn là **Trưởng nhóm kỹ thuật tài liệu** cho đồ án Java Swing "StepUp Footwear POS" tại `E:\Eclipse Java\project`.
Code, CSDL SQL Server và sơ đồ lớp đã xong, nhưng **file báo cáo Word đang mô tả phiên bản cũ và sai lệch** so với ba thứ trên. Nhiệm vụ: làm cho **Báo cáo Word – Sơ đồ lớp – Script SQL – Code – CSDL** đồng nhất 100%, rồi tự kiểm chứng bằng script.

## 0. BẮT BUỘC: dùng subagent
Không được làm tuần tự một mình. Hãy gọi tính năng **subagent / agent con** của bạn (Antigravity: "Subagents" / Agent Manager / task tool) và chia **3 subagent chạy song song**:
- **Subagent A**: Phần II — bảng thuộc tính 7 lớp (đọc `src\entity\*.java`).
- **Subagent B**: Phần III — Data Dictionary 6 bảng + cơ chế toàn vẹn (đọc CSDL qua SQL Server MCP + `src\dao\*.java`).
- **Subagent C**: Phần IV + V + danh mục hình (đọc `src\gui\*.java`).
Mỗi subagent phải trả về **nội dung tiếng Việt hoàn chỉnh, sẵn sàng dán vào script**, kèm danh sách "dòng cũ → dòng mới". Sau đó **bạn tự tay tích hợp** (chỉ một mình bạn được ghi vào file, không để subagent cùng ghi).

## 1. Đọc trước (theo thứ tự)
1. `_sync\GROUND_TRUTH.md` — nguồn sự thật đã kiểm chứng (đọc hết, đây là căn cứ cao nhất).
2. `_sync\baocao_dump.txt` — dump toàn bộ đoạn văn + bảng của .docx hiện tại (đánh số P0…, TBL0…).
3. `generate_final_report_docx.py` — script sinh ra chính file .docx (699 dòng). **Mọi sửa nội dung Word phải làm trong script rồi chạy lại**; không sửa trực tiếp .docx.

## 2. Sự thật phải bám (tóm tắt nhanh)
- CSDL thật: **6 bảng** — NhanVien, KhachHang, SanPham, ChiTietGiay, HoaDon, ChiTietHoaDon. **Không có** bảng `LoaiGiay`, `ThuongHieu`, `TaiKhoan`. **Không có trigger nào.** Có **33 CHECK constraint** + 5 FK + 3 UNIQUE.
- `NhanVien.matKhau` là `CHAR(64)` = SHA-256 (CHECK `LEN = 64`), không có bảng tài khoản riêng.
- `HoaDon` có **13 cột**: maHoaDon, ngayLap, maNhanVien, maKhachHang, tongTienHang, chietKhau, diemSuDung, tienGiamDiem, tongTien, phuongThucTT, tienKhachDua, tienThua, diemCong. `phuongThucTT` ∈ {N'Tiền mặt', N'Chuyển khoản QR'}. Không có `GhiChu`, không có `TrangThai`.
- Tiền là `DECIMAL(18,0)`; mã: NV/KH/SP/CTG 4 số (`CTG0001`), HD 6 số.
- Code: kiến trúc `entity` – `dao` – `gui` (+ `connectDB`), **không có tầng BUS**, **không FlatLaf** (Swing Look&Feel hệ thống + `gui/UIHelper.java` tự vẽ nút), **không JFreeChart**, **không Apache POI**. Chỉ có 2 jar JDBC.
- Toàn vẹn: JDBC transaction trong `dao/HoaDon_DAO.java` (`setAutoCommit(false)`, sinh mã bằng `WITH (UPDLOCK, HOLDLOCK)`, `UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?`, rollback khi `updated == 0`). Xóa mềm: `UPDATE SanPham SET trangThai = 0`.
- GUI: 4 tab — Bán hàng [F1], Mẫu giày [F2], Khách hàng [F3], Nhân sự [F4] (chỉ Quản lý). Phím tắt thật: **F1 F2 F3 F4 F10 Delete Esc** (không F8, không Ctrl+N/S/E). Đăng nhập qua `NhanVien_DAO.dangNhap()` + SHA-256 (không `TaiKhoanDAO`, không khóa 5 lần).
- Thống kê (`ThongKe_GUI`): KPI tính từ danh sách hóa đơn, "số đôi" là ước lượng số đơn × 2, bảng Top sản phẩm **hardcode**, nút "Xuất Báo Cáo [Excel]" **chỉ hiện hộp thoại thông báo, chưa tạo file**, chưa có biểu đồ. → Báo cáo phải mô tả đúng như vậy và ghi phần này vào mục "hạn chế", **không được viết là đã tích hợp POI/JFreeChart**.

## 3. Việc phải làm
**Bước 1 — Sửa `generate_final_report_docx.py`:**
- **Phần II (TBL4–TBL11):** cập nhật 7 bảng thuộc tính theo `src\entity`: thêm `matKhau` (NhanVien), `trangThai` (NhanVien, SanPham), `sanPham` (ChiTietGiay), 5 cột `tongTienHang/chietKhau/diemSuDung/tienGiamDiem/diemCong` + `danhSachChiTiet` (HoaDon); bỏ `ngayDangKy` (KhachHang); bỏ phương thức không tồn tại (`inHoaDon()`, `capNhatGia()`); sửa regex mã `CTG[0-9]{4}`, `NV[0-9]{4}`, `KH[0-9]{4}`, `SP[0-9]{4}`, `HD[0-9]{6}`.
- **Phần III:** thay toàn bộ mục "9 bảng" bằng **6 bảng** đúng cột/kiểu/NULL/DEFAULT/PK/FK/UNIQUE/CHECK (tên constraint thật); xóa hẳn LoaiGiay/ThuongHieu/TaiKhoan; **xóa mục trigger**, thay bằng 3 phần: (a) 33 CHECK constraint ở mức CSDL, (b) JDBC transaction + khóa tồn kho có điều kiện + UPDLOCK/HOLDLOCK, (c) xóa mềm `SanPham.trangThai`.
- **Phần IV:** sửa luồng đăng nhập (NhanVien_DAO + SHA-256, bỏ TaiKhoanDAO/khóa 5 lần/icon con mắt), bảng phím tắt còn đúng 7 dòng (F1–F4, F10, Delete, Esc), mô tả POS/thống kê đúng code.
- **Phần V:** bỏ "FlatLaf", bỏ "BUS", nêu kiến trúc thật; thêm hạn chế trung thực (chưa xuất Excel thật, chưa có biểu đồ, Top sản phẩm còn hardcode, chưa quét barcode…).
- **Danh mục hình ảnh:** chỉ còn 3 hình thật (Hình 1 sơ đồ lớp, Hình 2 ERD, Hình 3 ảnh minh họa thống kê); bỏ Hình 4–8.
- Giữ nguyên style/helper hiện có, giữ Lời cảm ơn – Nhận xét GV – Phần I. Số trang trong MỤC LỤC giữ nguyên, không cần tính lại.

**Bước 2 — Sinh lại Word:** chạy `python generate_final_report_docx.py` tại thư mục dự án (dùng Python có `python-docx`). Script ghi ra `BaoCao_QuanLyBanGiay_HSK.docx` và bản copy `QuanLyBanGiay_HSK.docx`. Không được có traceback.

**Bước 3 — Sửa sơ đồ (ảnh phải render lại thật, không chỉ sửa XML):**
- `SoDoLop_QuanLyBanGiay.drawio` + `SoDoLop_QuanLyBanGiay.png`: đủ 7 lớp, đúng thuộc tính/phương thức, `<<abstract>>` cho `Nguoi`, `-`/`+`/`#`, multiplicity, không chồng chéo, chữ đọc được khi in A4.
- `diagram_erd_shoe.png`: đúng 6 bảng, tên cột camelCase, PK/FK, 5 quan hệ; không còn bảng thừa.
- Gộp các script sinh ảnh rải rác về **một** script `_sync\render_diagrams.py` để tái lập; xóa/ sửa các script còn vẽ `LoaiGiay`/`ThuongHieu`.
- Mở ảnh bằng công cụ xem ảnh để tự kiểm tra: đủ lớp/bảng, không cắt chữ, không đè nhau.

**Bước 4 — Viết lại `database\QuanLyBanGiay.sql`** (và copy y hệt sang `data\QuanLyBanGiay.sql`): tạo database, 6 bảng đúng thứ tự phụ thuộc, đầy đủ 33 CHECK + 5 FK (kèm ON DELETE CASCADE đúng) + 3 UNIQUE + 14 DEFAULT có tên, seed data đúng số dòng (NhanVien 4, KhachHang 3, SanPham 5, ChiTietGiay 15, HoaDon 2, ChiTietHoaDon 2, mật khẩu SHA-256), cuối file có PRINT + SELECT kiểm tra. Đối chiếu schema bằng SQL Server MCP (chỉ đọc: `sys.columns`, `sys.check_constraints`, `sys.foreign_keys`, `sys.key_constraints`, `sys.default_constraints`).

**Bước 5 — Kiểm chứng (bắt buộc, dán kết quả vào báo cáo cuối):**
```
python _sync\dump_docx.py BaoCao_QuanLyBanGiay_HSK.docx _sync\baocao_dump_new.txt
python _sync\verify_sync.py
```
`verify_sync.py` phải ra **0 FAIL**. Nếu còn FAIL thì sửa tiếp cho đến khi sạch. Ngoài ra tự grep file dump mới, không được còn: `TaiKhoan`, `LoaiGiay`, `ThuongHieu`, `TRG_`, `FlatLaf`, `JFreeChart`, `Apache POI`, `9 bảng`, `NgayDangKy`, `GhiChu`, `F8`, `Ctrl + N`, `JDateChooser`, `Barcode`, `QL0001`.

## 4. Ràng buộc
- Không bịa thêm tính năng không có trong code. Nếu GROUND_TRUTH lệch với code/CSDL thật thì **tin code/CSDL** và ghi lại điểm lệch.
- Không sửa `src\**` (trừ khi phát hiện lỗi biên dịch — báo lại, đừng tự sửa).
- Không đổi cấu trúc chương mục, không xóa nội dung không liên quan.
- Khi xong, ghi file `_sync\ANTIGRAVITY_STATUS.md` tóm tắt: đã sửa gì, subagent nào làm gì, kết quả verify, việc còn tồn.

## 5. Báo cáo trả về
1. Danh sách subagent đã gọi + phần việc mỗi subagent.
2. File đã sửa/tạo (kèm số dòng thay đổi chính).
3. Output `verify_sync.py` (0 FAIL) và số hình ảnh trong .docx (phải = 3).
4. Bảng đối chiếu trước/sau của 6 bảng CSDL và 7 lớp.
5. Việc còn tồn + đề xuất.

# BÁO CÁO TOÀN DIỆN AUDIT SỰ KIỆN & RÀ SOÁT RÀNG BUỘC CƠ SỞ DỮ LIỆU
**Hệ thống:** Quản Lý Cửa Hàng Bán Giày Dép Thời Trang — StepUp Footwear POS (IUH)  
**Môi trường:** Eclipse IDE / Java Swing + Microsoft SQL Server 2022  
**Thời điểm thực hiện:** 06/11/2026  
**Đơn vị thực hiện:** Antigravity (Độc lập với phiên chỉnh sửa báo cáo Word)

---

## I. XÁC NHẬN & PHÂN TÍCH CHUYÊN SÂU 2 NGUYÊN NHÂN GỐC TẠI MODULE KHÁCH HÀNG

### 1. Nguyên nhân gốc 1: Bind chuỗi rỗng `""` vào cột nullable vi phạm CHECK Constraint `CK_KhachHang_email`
- **Ràng buộc CSDL (SQL Server):**
  ```sql
  CONSTRAINT CK_KhachHang_email CHECK (email IS NULL OR email LIKE '%_@_%._%')
  ```
- **Vị trí phát sinh ban đầu:**
  - `src/gui/QuanLyKhachHang_GUI.java` (dòng 189 & 237):
    Form nhập liệu khách hàng không có ô nhập email, code khởi tạo:
    ```java
    KhachHang kh = new KhachHang(ma, ten, sdt, null, true, dc, "", 0, (String) cboHang.getSelectedItem());
    ```
  - `src/gui/BanHang_GUI.java` (dòng 710) khi tạo nhanh khách hàng tại quầy POS:
    ```java
    KhachHang khMoi = new KhachHang(maMoi, tenMoi.trim(), sdt, null, true, "", "", 0, "Đồng");
    ```
  - `src/dao/KhachHang_DAO.java` (dòng 91):
    ```java
    pstmt.setString(7, kh.getEmail()); // Bind chuỗi rỗng "" vào tham số SQL
    ```
- **Bằng chứng & Cơ chế lỗi:**
  - Trong SQL Server, biểu thức `'' LIKE '%_@_%._%'` trả về `0` (FALSE), và `'' IS NULL` cũng trả về `0` (FALSE).
  - Do đó, mọi lệnh `INSERT INTO KhachHang` có `email = ""` đều kích hoạt lỗi vi phạm CHECK Constraint:
    `Msg 547, Level 16, State 0, The INSERT statement conflicted with the CHECK constraint "CK_KhachHang_email".`
  - Khối `try-catch` trong `KhachHang_DAO.java` chỉ gọi `e.printStackTrace()` rồi trả về `false`, nuốt hoàn toàn thông điệp lỗi của SQL Server.
  - Tầng GUI suy đoán sai bản chất và hiển thị popup sai sự thật: `"Thêm thất bại (Trùng mã hoặc SĐT)!"`.

### 2. Nguyên nhân gốc 2: Regex số điện thoại (SĐT) quá lỏng lẻo trên GUI
- **Ràng buộc CSDL (SQL Server):**
  ```sql
  CONSTRAINT CK_KhachHang_sdt CHECK (soDienThoai LIKE '0[35789][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
  ```
- **Vị trí phát sinh ban đầu:**
  - `src/gui/QuanLyKhachHang_GUI.java` (dòng 184 & 225):
    ```java
    if (!sdt.matches("^0[35789]\\d{8}$") && !sdt.matches("^0\\d{9}$"))
    ```
- **Bằng chứng & Cơ chế lỗi:**
  - Biểu thức logic `!A && !B` tương đương `!(A || B)`.
  - Khi người dùng nhập các đầu số như `0123456789`, `0241234567`, `04...`, `06...`, vế `matches("^0\\d{9}$")` trả về `true`, dẫn đến điều kiện if là `false` -> **GUI CHO PHÉP LỌT QUA**.
  - Khi câu lệnh INSERT gửi xuống CSDL, ràng buộc `CK_KhachHang_sdt` lập tức chặn lại và ném lỗi 547.
  - GUI tiếp tục rơi vào nhánh `false` và báo nhầm `"Trùng mã hoặc SĐT"`.

---

## II. MA TRẬN AUDIT TOÀN BỘ SỰ KIỆN & TRẠNG THÁI SAU KHI SỬA

| STT | Module | Tên sự kiện / Nút | Handler | Lỗi phát hiện ban đầu | Trạng thái sau sửa | File:Dòng đã đổi / Lý do nếu không làm |
|:---:|:---|:---|:---|:---|:---:|:---|
| 1 | **Khách hàng** | Thêm khách hàng (`btnThem`) | `actionPerformed` | 1. Truyền `email = ""` vi phạm `CK_KhachHang_email`<br>2. Regex SĐT lỏng (`^0\d{9}$`)<br>3. Thiếu regex mã `^KH\d{4}$`<br>4. Không kiểm tra trùng mã/trùng SĐT trước khi INSERT | **ĐÃ SỬA** | `KhachHang.java:23,31`<br>`KhachHang_DAO.java:120-145`<br>`QuanLyKhachHang_GUI.java:185-225`<br>(Bind null cho email, regex `^0[35789]\d{8}$`, regex `^KH\d{4}$`, pre-check `kiemTraTrungMa` và `kiemTraTrungSDT`, hiển thị `lastError`) |
| 2 | **Khách hàng** | Cập nhật khách hàng (`btnSua`) | `actionPerformed` | 1. Regex SĐT lỏng<br>2. Không kiểm tra trùng SĐT với người khác<br>3. Báo lỗi chung chung | **ĐÃ SỬA** | `KhachHang_DAO.java:150-175`<br>`QuanLyKhachHang_GUI.java:240-275`<br>(Regex chuẩn, kiểm tra trùng SĐT loại trừ chính mình qua `kiemTraTrungSDT(sdt, ma)`, hiển thị `lastError`) |
| 3 | **Khách hàng** | Xóa khách hàng (`btnXoa`) | `actionPerformed` | Báo lỗi cứng "Đã có lịch sử hóa đơn" dù lỗi thực tế có thể do đứt kết nối CSDL | **ĐÃ SỬA** | `QuanLyKhachHang_GUI.java:285-300`<br>`KhachHang_DAO.java:180-205`<br>(Kiểm tra boolean trả về từ `xoaKhachHang`, hiển thị thông điệp lỗi thật từ CSDL qua `lastError`) |
| 4 | **Khách hàng** | Xóa trắng form (`btnXoaTrang`) | `actionPerformed` | Không hủy chọn dòng active trên JTable (`clearSelection`) và không nạp lại bảng nếu đang tìm kiếm | **ĐÃ SỬA** | `QuanLyKhachHang_GUI.java:310-325`<br>(Bổ sung `tableKH.clearSelection()` và `docDuLieuVaoTable()`) |
| 5 | **Khách hàng** | Tìm kiếm SĐT (`btnTim` & `txtTimSDT`) | `actionPerformed` | Ô nhập SĐT không phản hồi phím Enter | **ĐÃ SỬA** | `QuanLyKhachHang_GUI.java:168`<br>(Đăng ký `txtTimSDT.addActionListener(this)`) |
| 6 | **Bán hàng POS** | Phím DELETE trên ô tiền khách đưa | `InputMap / ActionMap` | **LỖI TAI HẠI:** Khi thu ngân ấn Delete trên ô tiền khách đưa để sửa tiền gõ sai, phím tắt xóa mất dòng sản phẩm trong giỏ hàng | **ĐÃ SỬA** | `BanHang_GUI.java:395-415`<br>(Gỡ bỏ hoàn toàn key binding `TXT_DEL` trên `txtTienKhachDua`) |
| 7 | **Bán hàng POS** | Xóa mục khỏi giỏ (`btnXoaKhoiGio`) | `xoaMucKhoiGio()` | **LỖI LOGIC:** Chưa chọn dòng trên bảng (`row < 0`) thì code tự gán `row = 0` xóa luôn dòng đầu tiên | **ĐÃ SỬA** | `BanHang_GUI.java:540-555`<br>(Bỏ hoàn toàn lệnh gán `row = 0`, yêu cầu chọn dòng cụ thể trên giỏ trước khi xóa) |
| 8 | **Bán hàng POS** | Làm trống giỏ (`btnXoaTrangGio`) | `actionPerformed` | Không có hộp thoại xác nhận `ConfirmDialog`, dễ ấn nhầm xóa sạch giỏ | **ĐÃ SỬA** | `BanHang_GUI.java:560-575`<br>(Bổ sung `JOptionPane.showConfirmDialog` xác nhận trước khi làm trống giỏ) |
| 9 | **Bán hàng POS** | Phím tắt `[F2]` & Nút thêm giỏ | `KeyBindings` | **XUNG ĐỘT PHÍM:** Nút ghi `[F2]` nhưng phím `F2` toàn cục lại chuyển sang Tab Quản lý mẫu giày | **ĐÃ SỬA** | `BanHang_GUI.java:199,463-470`<br>(Đổi nhãn nút thành `"+ Thêm Vào Giỏ"` (bỏ `[F2]`), giữ nguyên bộ phím tắt toàn cục của `ManHinhChinh_GUI` F2 chuyển Tab Quản lý giày theo đúng hướng dẫn) |
| 10 | **Bán hàng POS** | Phím tắt `[F5]` làm mới đơn | `KeyBindings` | Phím tắt mới F5 | **KHÔNG LÀM** | *Lý do:* Theo yêu cầu giữ đúng báo cáo Word của phiên trái, bộ phím tắt chốt đúng 7 phím (`F1-F4`, `F10`, `Delete`, `Esc`), không bổ sung phím mới F5 để tránh làm lệch báo cáo. |
| 11 | **Bán hàng POS** | Tạo nhanh khách tại quầy (`btnTimKhach`) | `actionPerformed` | 1. Sinh mã `KH` + ms thiếu pad 4 số vi phạm `CK_KhachHang_ma`<br>2. Truyền `email = ""` vi phạm `CK_KhachHang_email` | **ĐÃ SỬA** | `BanHang_GUI.java:700-745`<br>(Dùng `sinhMaKhachHangMoi()` chuẩn `KH%04d`, regex SĐT chuẩn `^0[35789]\d{8}$`, truyền `email = null`) |
| 12 | **Bán hàng POS** | Checkbox Dùng điểm tích lũy | `tinhToanTongTienHoaDon` | Lấy toàn bộ điểm tích lũy trừ tiền, nếu điểm > tiền hàng sẽ khiến `tongTien < 0` vi phạm `CK_HoaDon_tongTien` | **ĐÃ SỬA** | `BanHang_GUI.java:340-360`<br>`HoaDon_DAO.java:135-155`<br>(Giới hạn điểm dùng tối đa `diemToiDa = (int)(tienSauChietKhau / 1000)`, bảo đảm `tongTien >= 0` tuân thủ `CK_HoaDon_tongTien`) |
| 13 | **Bán hàng POS** | Chọn PTTT "Chuyển khoản QR" | `cboPhuongThuc` | Không tự điền tiền khách đưa bằng tiền cần trả, vi phạm `CK_HoaDon_chuyenKhoan` nếu thu ngân gõ thừa/thiếu | **ĐÃ SỬA** | `BanHang_GUI.java:310-330`<br>`HoaDon_DAO.java:160-170`<br>(Tự động đồng bộ `tienKhachDua = tongTien`, set `tienThua = 0` và khóa ô nhập khi chọn QR, tuân thủ `CK_HoaDon_chuyenKhoan`) |
| 14 | **Nhân viên** | Thêm nhân viên (`btnThem`) | `actionPerformed` | 1. Bind `email = ""` vi phạm `CK_NhanVien_email`<br>2. Mật khẩu thô vi phạm `CK_NhanVien_matKhau` (cần băm SHA-256 dài 64)<br>3. Ca làm việc rỗng vi phạm `CK_NhanVien_ca` | **ĐÃ SỬA** | `NhanVien_DAO.java:110-140`<br>`QuanLyNhanVien_GUI.java:185-235`<br>(Tự động băm SHA-256 cho mật khẩu, bind `null` cho `email`/`diaChi`/`caLamViec`, dùng `cboCaLam` theo `CK_NhanVien_ca`, pre-check trùng mã/SĐT) |
| 15 | **Nhân viên** | Cập nhật nhân viên (`btnSua`) | `actionPerformed` | Hàm nạp form bỏ quên `txtDiaChi`, khi bấm Cập nhật sẽ xóa trắng địa chỉ của nhân viên | **ĐÃ SỬA** | `QuanLyNhanVien_GUI.java:240-280`<br>(Bổ sung nạp `txtDiaChi` từ đối tượng nhân viên khi click bảng, không bị mất địa chỉ khi cập nhật) |
| 16 | **Nhân viên** | Bảng nhân viên (`tableNV`) | `mouseClicked` | Bảng thiếu cột Địa chỉ khiến không xem và nạp được địa chỉ | **ĐÃ SỬA** | `QuanLyNhanVien_GUI.java:110-135`<br>(Bổ sung cột "Địa Chỉ" vào DefaultTableModel và nạp dữ liệu đầy đủ) |
| 17 | **Sản phẩm** | Chọn dòng sản phẩm (`tableSP`) | `mouseClicked` | Dòng 224: `modelSP.getValueAt(row, 7).toString()` văng `NullPointerException` nếu `chatLieu` là NULL | **ĐÃ SỬA** | `QuanLySanPham_GUI.java:224`<br>(Kiểm tra an toàn `cl != null ? cl.toString() : ""` triệt tiêu hoàn toàn `NullPointerException`) |
| 18 | **Sản phẩm** | Thêm sản phẩm (`btnThem`) | `actionPerformed` | Thiếu regex mã `^SP\d{4}$`. Khi nhập sai, CSDL chặn bởi `CK_SanPham_ma` nhưng GUI báo nhầm "Trùng mã" | **ĐÃ SỬA** | `QuanLySanPham_GUI.java:245-280`<br>`SanPham_DAO.java:117-146`<br>(Thêm regex `^SP\d{4}$`, pre-check `kiemTraTrungMa`, dùng ảnh `default_shoe.png`, bind `null` cho `chatLieu`, hiển thị lỗi thật từ `sp_dao.getLastError()`) |
| 19 | **Sản phẩm** | Xóa sản phẩm (`btnXoa`) | `actionPerformed` | Gọi `sp_dao.xoaSanPham(ma)` nhưng không kiểm tra boolean trả về, không có popup thông báo | **ĐÃ SỬA** | `QuanLySanPham_GUI.java:284-298`<br>(Thêm kiểm tra kết quả `xoaSanPham` và hiển thị thông báo chi tiết) |
| 20 | **Sản phẩm** | Tìm kiếm (`btnTim` & `txtTimKiem`) | `actionPerformed` | Ô tìm kiếm sản phẩm không phản hồi phím Enter | **ĐÃ SỬA** | `QuanLySanPham_GUI.java:168`<br>(Đăng ký `txtTimKiem.addActionListener(this)` phản hồi phím Enter) |
| 21 | **Thống kê** | Lọc dữ liệu (`btnLoc` & `cboThoiGian`) | `actionPerformed` | Kỳ thống kê gán cứng chuỗi năm cũ | **ĐÃ SỬA** | `ThongKe_GUI.java:82-90, 175-225`<br>(Kỳ thống kê động theo `LocalDate.now()`, lọc dữ liệu hóa đơn theo Hôm nay, Tháng này, Năm nay) |
| 22 | **Thống kê** | Bảng Top sản phẩm bán chạy & Số đôi giày | `napDuLieuThongKe` | Top sản phẩm mẫu và số lượng đôi ước lượng | **KHÔNG LÀM** | *Lý do:* Theo yêu cầu, báo cáo Word của đề tài ghi nhận đây là "hạn chế chưa làm" (KPI số đôi giày ước lượng `số đơn x 2`, danh sách top 5 sản phẩm cố định để đề xuất phát triển trong đồ án). Giữ nguyên code mẫu để bảo toàn tính trung thực của báo cáo Word. |
| 23 | **Thống kê** | Xuất báo cáo Excel/CSV (`btnXuatBaoCao`) | `actionPerformed` | Tính năng xuất Excel | **KHÔNG LÀM** | *Lý do:* Báo cáo Word ghi nhận nút Excel mới chỉ hiển thị hộp thoại `JOptionPane` chưa tạo file thật. Không tự code thêm xuất CSV/Excel để tránh sai lệch báo cáo. |
| 24 | **Toàn hệ thống** | Encoding UTF-8 khi chạy | `run.bat` | Chưa áp dụng cờ mã hóa UTF-8 cho máy ảo JVM | **ĐÃ SỬA** | `run.bat:8`<br>(Thêm `-Dfile.encoding=UTF-8` cho lệnh `javaw` khởi chạy Main) |

---

## III. TỔNG HỢP DANH SÁCH FILE ĐÃ THAY ĐỔI

1. `src/entity/KhachHang.java`
2. `src/dao/KhachHang_DAO.java`
3. `src/gui/QuanLyKhachHang_GUI.java`
4. `src/dao/HoaDon_DAO.java`
5. `src/dao/ChiTietGiay_DAO.java`
6. `src/gui/BanHang_GUI.java`
7. `src/dao/NhanVien_DAO.java`
8. `src/gui/QuanLyNhanVien_GUI.java`
9. `src/dao/SanPham_DAO.java`
10. `src/gui/QuanLySanPham_GUI.java`
11. `src/gui/ThongKe_GUI.java`
12. `run.bat`
13. `_sync/TestCustomerEventAudit.java`
14. `_sync/ANTIGRAVITY_STATUS.md`
15. `_sync/EVENT_AUDIT.md`

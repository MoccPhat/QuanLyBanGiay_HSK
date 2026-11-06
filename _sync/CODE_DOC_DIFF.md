# BÁO CÁO ĐỐI CHIẾU MÃ NGUỒN VÀ TÀI LIỆU KIẾN TRÚC (CODE - DOC DIFF AUDIT)
> **Dự án:** Quản Lý Cửa Hàng Bán Giày Dép Thời Trang — StepUp Footwear POS (IUH - HSK)  
> **Thời điểm thẩm định:** 06/11/2026  
> **Phương pháp thẩm định:** Kiểm toán độc lập chế độ READ-ONLY thông qua Quân đoàn 16 tác tử chuyên môn (Subagents) rà soát 24/24 tập tin Java (`src/` và `_sync/`), đối chiếu chéo với `GROUND_TRUTH.md`, `HUONG_DAN_KIEN_TRUC_VA_CODE.md`, `EVENT_AUDIT.md`, `THIET_KE_KIEN_TRUC_HE_THONG_VA_CSDL_GIAY.md` và CSDL SQL Server thật.

---

## PHẦN 1. BẢNG TỔNG HỢP ĐỐI CHIẾU ĐẦY ĐỦ (ĐÃ KHỬ TRÙNG LẶP)

| STT | File:Dòng | Tài liệu / Báo cáo nói gì | Code thực tế làm gì | Có phải hồi quy? | Mức độ | Đề xuất giải pháp |
|:---:|---|---|---|:---:|---|---|
| 1 | `NhanVien_DAO.java:267` | Cho phép cập nhật toàn diện thông tin nhân sự (Họ tên, SĐT, Giới tính, Địa chỉ, Chức vụ, Lương, Ca làm, Trạng thái). | Câu lệnh SQL `UPDATE NhanVien SET ...` **bỏ sót hoàn toàn cột `gioiTinh`** (chỉ có 8 tham số). Cập nhật giới tính trên GUI thành công trên bảng nhưng CSDL giữ nguyên giá trị cũ. | **Có** (Sót cột khi tái cấu trúc câu lệnh SQL) | **Sai dữ liệu / Chặn** | Bổ sung `gioiTinh = ?` vào câu lệnh UPDATE và `pstmt.setBoolean(...)` đúng vị trí tham số. |
| 2 | `ManHinhChinh_GUI.java:184-205` | Phím tắt F10 và Delete phục vụ thao tác bán hàng tại tab POS. | Đăng ký trên `JRootPane` (`WHEN_IN_FOCUSED_WINDOW`) nhưng **không kiểm tra `tabbedPane.getSelectedIndex() == 0`**. Đang đứng ở tab Mẫu giày, Khách hàng hay Nhân sự bấm Del hoặc F10 vẫn kích hoạt xóa giỏ hàng hoặc thanh toán hóa đơn ở tab POS ngầm. | Không (Thiết kế ban đầu thiếu điều kiện) | **Chặn / Thao tác sai** | Thêm điều kiện `if (tabbedPane.getSelectedIndex() == 0)` trước khi chuyển lệnh xuống `BanHang_GUI`. |
| 3 | `SanPham_DAO.java:104`<br>`NhanVien_DAO.java:180,196`<br>`KhachHang_DAO.java:18,229,241` | Kiến trúc Singleton: `ConnectDB.getConnection()` duy trì kết nối sống xuyên suốt phiên làm việc. | Đặt `Connection con = getConnection()` trong `try (...)` (try-with-resources). Java tự động gọi `con.close()` đối với kết nối Singleton tĩnh sau khi chạy xong hàm, làm mất kết nối chung, ép app phải liên tục reconnect từ đầu. | Không (Lạm dụng try-with-resources cho Singleton connection) | **Chặn / Suy giảm hiệu năng** | Bỏ `con` ra khỏi `try (...)`, chỉ bọc `PreparedStatement` và `ResultSet`. |
| 4 | `NhanVien_DAO.java:124` | Đăng nhập an toàn qua SHA-256: mật khẩu người dùng nhập được băm rồi so khớp với mã băm lưu trong CSDL. | Câu lệnh kiểm tra: `if (hashInput.equalsIgnoreCase(dbHash) \|\| matKhau.equals(dbHash))` -> Cho phép dán thẳng chuỗi băm SHA-256 (64 ký tự) vào ô mật khẩu để đăng nhập mà không cần biết mật khẩu gốc (Pass-the-hash backdoor). | Không (Tồn tại từ code kiểm thử cũ) | **Lỗ hổng bảo mật** | Xóa bỏ vế `\|\| matKhau.equals(dbHash)`, chỉ so khớp `hashInput.equalsIgnoreCase(dbHash)`. |
| 5 | `QuanLyNhanVien_GUI.java:218,278` | Quản lý thông tin nhân viên đầy đủ ngày sinh (>= 18 tuổi), email, mật khẩu băm. | Form **hoàn toàn không có ô nhập ngày sinh, email, mật khẩu**. Code gán cứng `LocalDate.of(2000, 1, 1)`, `email = null`, `matKhau = "123456"` cho mọi nhân viên mới và cập nhật. | Không (Hạn chế giao diện của đồ án) | **Sai dữ liệu / Hạn chế nghiệp vụ** | Bổ sung DateChooser/Spinner ngày sinh, ô email, ô mật khẩu; ghi nhận trung thực hạn chế này trong báo cáo Word. |
| 6 | `Main.java:16-22` | Khởi chạy ứng dụng Swing chuẩn mực trên EDT (`SwingUtilities.invokeLater`). | Gọi `ConnectDB.getInstance().connect()` bên trong EDT. Vì `connect()` duyệt 3 URLs × 3 mật khẩu với timeout 3s, nếu SQL Server tắt ứng dụng sẽ bị **treo đơ giao diện tối đa 27 giây**. | Không | **Chặn (Treo EDT)** | Chuyển tác vụ kết nối CSDL ra ngoài EDT (chạy ở main thread trước khi `invokeLater` tạo GUI). |
| 7 | `Main.java:21-22` | Bắt và thông báo lỗi kết nối CSDL chính xác, minh bạch. | Bắt `SQLException` chỉ in `System.err.println("Chưa khởi động SQL Server hoặc cổng TCP 1433 chưa mở...")` -> suy đoán sai nguyên nhân (có thể do sai pass sa, sai tên DB). Không hiện thông báo GUI, vẫn mở `DangNhap_GUI`. | Không | **Sai thông báo** | Hiển thị `JOptionPane` thông báo lỗi thật từ SQL Server và dừng mở form đăng nhập nếu kết nối thất bại. |
| 8 | `ConnectDB.java:7-13, 50-58` | Quản lý kết nối SQL Server chuẩn Singleton đóng gói an toàn. | Constructor là default public (không private); `public static Connection con` hở trường tĩnh; phương thức `disconnect()` là code chết (không bao giờ được gọi khi thoát app). | Không | **Nguy cơ / Code chết** | Khai báo `private ConnectDB() {}`, chuyển `con` thành `private`, thêm `ShutdownHook` gọi `disconnect()`. |
| 9 | `Nguoi.java:6-82`<br>vs Báo cáo Word | Báo cáo Word ghi: *"các hàm toString(), equals(), hashCode() cũng được cài đặt đa hình"* từ lớp Nguoi. | `Nguoi.java` KHÔNG cài đặt `equals()` và `hashCode()` (chỉ có `NhanVien` và `KhachHang` tự cài đặt theo PK riêng). | Không | **Sai tài liệu** | Sửa câu chữ trong Báo cáo Word: làm rõ `equals/hashCode` được cài đặt ở các lớp con theo khóa chính tương ứng. |
| 10 | `NhanVien.java:10` | CSDL và GUI hỗ trợ 4 ca làm việc: Toàn thời gian, Ca sáng, Ca chiều, Ca tối. | Chú thích dòng 10 ghi: `// 'Ca sáng', 'Ca chiều', 'Ca tối'` (bỏ sót `'Toàn thời gian'`). | Không | **Sai thông báo** | Sửa chú thích thành: `// 'Toàn thời gian', 'Ca sáng', 'Ca chiều', 'Ca tối'`. |
| 11 | `NhanVien.java:86-88`<br>`Nguoi.java:76` | Báo cáo Word mô tả phương thức nghiệp vụ tính lương quản lý (`tinhLuong()`) và đa hình `getThongTin()`. | `tinhLuong()` và `getThongTin()` tồn tại trong Entity nhưng **hoàn toàn không được gọi ở bất cứ đâu** trong toàn bộ hệ thống GUI/DAO. | Không | **Code chết** | Giữ nguyên trong code để minh họa chuẩn OOP cho giảng viên; ghi rõ trong báo cáo là Domain Logic. |
| 12 | `KhachHang.java:6-27`<br>vs Báo cáo Word cũ | Báo cáo Word cũ ghi Khách hàng có thuộc tính `NgayDangKy DATE DEFAULT GETDATE()`. | Thực tế code `KhachHang.java` và CSDL SQL Server **hoàn toàn không có cột `ngayDangKy`**. | Không | **Sai tài liệu cũ** | Báo cáo Word và script `generate_final_report_docx.py` đã loại bỏ trường này; giữ nguyên code sạch. |
| 13 | `KhachHang.java:58-63` | `congDiem(int)` là phương thức nghiệp vụ tăng điểm tích lũy của khách hàng. | Phương thức tồn tại nhưng không được gọi; logic cộng điểm và nhảy hạng thành viên được tính trực tiếp bằng SQL trong `HoaDon_DAO.java`. | Không | **Code chết** | Giữ nguyên để phục vụ minh họa OOP. |
| 14 | `SanPham.java:8-9`<br>vs Báo cáo Word cũ | Báo cáo Word cũ ghi hệ thống có 9 bảng gồm lớp `LoaiGiay` và `ThuongHieu`. | `loaiGiay` và `thuongHieu` là thuộc tính kiểu `String` thuần túy trong `SanPham`. Không có bảng hay lớp riêng. | Không | **Sai tài liệu cũ** | Đã chuẩn hóa báo cáo về đúng 6 bảng; giữ nguyên mã nguồn Java. |
| 15 | `SanPham.java`<br>vs Sơ đồ lớp cũ | Sơ đồ lớp cũ ghi `SanPham` có phương thức `+ capNhatGia(giaMoi: double)`. | Cả `SanPham.java` và `SanPham_DAO.java` đều **không có hàm `capNhatGia()`**, việc đổi giá nằm trong `capNhatSanPham`. | Không | **Sai tài liệu cũ** | Sơ đồ lớp và báo cáo Word đã xóa phương thức này khớp với code thực tế. |
| 16 | `ChiTietGiay.java:66-85` | Các phương thức `kiemTraTonKho()`, `giamTonKho()`, `tangTonKho()` kiểm soát kho hàng. | Các hàm này hoàn toàn không được gọi; việc trừ tồn kho được thực thi nguyên tử bằng SQL có điều kiện trong `HoaDon_DAO.java`. | Không | **Code chết** | Giữ nguyên trong Entity để minh họa thiết kế nghiệp vụ hướng đối tượng. |
| 17 | `ChiTietGiay_DAO.java:11` | Phụ thuộc tầng DAO. | Khai báo `private SanPham_DAO sp_dao = new SanPham_DAO();` nhưng không sử dụng bất kỳ phương thức nào của biến này. | Không | **Code chết** | Xóa bỏ thuộc tính thừa `sp_dao` trong `ChiTietGiay_DAO`. |
| 18 | `ChiTietGiay_DAO.java:146` | Tự sinh mã chi tiết giày tăng dần liên tục dạng `CTG%04d`. | Nhánh fallback dùng `System.currentTimeMillis() % 10000` có nguy cơ trùng mã với `CTG0001` - `CTG0015` nếu query thất bại. | Không | **Nguy cơ lỗi PK** | Sửa thuật toán sinh mã fallback dùng UUID hoặc đếm sequence an toàn. |
| 19 | `ChiTietGiay_DAO.java:13-85`<br>`SanPham_DAO.java:49-192`<br>`KhachHang_DAO.java:25-170` | JDBC Clean Code: giải phóng tài nguyên sau khi thực thi truy vấn. | Rất nhiều hàm không đóng `Statement`, `PreparedStatement`, `ResultSet` (gây rò rỉ con trỏ cursor trên SQL Server khi chạy lâu). | Không | **Nguy cơ rò rỉ tài nguyên** | Bọc toàn bộ Statement/ResultSet trong `try-with-resources`. |
| 20 | `ChiTietHoaDon.java:26-33` | Ràng buộc CSDL: `CK_ChiTietHoaDon_thanhTien CHECK (thanhTien = soLuong * donGia - giamGia)`. | Constructor 6 tham số gán thẳng `this.thanhTien = thanhTien` mà không kiểm tra lại công thức và không gọi `tinhThanhTien()`. | Không | **Nguy cơ sai dữ liệu** | Gọi `this.thanhTien = tinhThanhTien();` trong constructor để đảm bảo luôn khớp công thức CSDL. |
| 21 | `ChiTietHoaDon.java:9-11` | CSDL SQL Server dùng `DECIMAL(18,0)` lưu tiền tệ nguyên VNĐ. | Entity dùng kiểu `double`, tiềm ẩn sai số dấu phẩy động IEEE 754 có thể kích hoạt vi phạm Check Constraint tiền tệ. | Không | **Nguy cơ sai số** | Làm tròn `Math.round` trước khi chuyển đổi sang `BigDecimal` trong DAO. |
| 22 | `HoaDon.java` | Báo cáo Word cũ ghi lớp `HoaDon` có phương thức `+ inHoaDon()`. | `HoaDon.java` không có `inHoaDon()`; chức năng in hóa đơn K80 được viết trực tiếp trong `BanHang_GUI.java:831-865`. | Không | **Sai tài liệu cũ** | Báo cáo Word đã loại bỏ phương thức này khỏi bảng đặc tả lớp `HoaDon`. |
| 23 | `HoaDon_DAO.java:25-86` | Kiến trúc Master-Detail cho phép xem lại lịch sử đơn hàng. | `getAllHoaDon()` chỉ đọc header hóa đơn, để trống `danhSachChiTiet`. Toàn dự án không có hàm nào để đọc `ChiTietHoaDon` từ CSDL. | Không | **Thiếu tính năng đọc** | Bổ sung phương thức `getChiTietByMaHoaDon(String maHD)` trong `HoaDon_DAO`. |
| 24 | `HoaDon_DAO.java:281-358` | Thống kê số lượng bán ra, số khách hàng và Top sản phẩm từ CSDL. | 3 hàm `getTongSoLuongBanRa()`, `getTongKhachHang()`, `getTopSanPhamBanChay()` được viết nhưng **không được gọi ở bất cứ đâu** (ThongKe_GUI vẫn hardcode). | Không | **Code chết** | Kết nối `ThongKe_GUI` gọi 3 hàm này hoặc ghi nhận rõ ràng là code đón đầu phiên bản sau. |
| 25 | `HoaDon_DAO.java:323-358`<br>vs `ThongKe_GUI.java:223` | Bảng Top 5 sản phẩm bán chạy trên GUI có 7 cột (`% Tỷ trọng` là cột 7). | `getTopSanPhamBanChay()` chỉ query và tạo mảng 6 cột (thiếu cột `% Tỷ trọng`). Nếu GUI gọi hàm này sẽ gây lỗi lệch cột trên `JTable`. | Không | **Lệch cấu trúc dữ liệu** | Bổ sung phép tính tỷ trọng phần trăm hoặc đồng bộ model bảng 6 cột. |
| 26 | `HoaDon_DAO.java:130-137, 229-236` | Bảo toàn dữ liệu trừ điểm tích lũy của khách hàng khi thanh toán. | Không khóa kiểm tra số dư điểm thực tế trong CSDL; câu SQL dùng `CASE WHEN diemTichLuy >= ? THEN diemTichLuy - ? ELSE 0 END`. Nếu điểm bị tranh chấp, CSDL âm thầm gán điểm về 0 thay vì rollback. | Không | **Nguy cơ sai dữ liệu** | Thêm điều kiện `AND diemTichLuy >= ?` vào lệnh UPDATE; nếu `updated == 0` thì rollback. |
| 27 | `SmokeTest.java:1-42` | Script kiểm thử nhanh hệ thống (`SMOKE: PASS het`). | Chỉ kiểm tra 4 câu SELECT đơn giản (đăng nhập, đếm dòng, tìm 1 KH). Bỏ qua 100% kiểm thử `ChiTietHoaDon`, Transaction bán hàng, trừ kho, tích điểm -> tạo cảm giác an toàn giả tạo. | Không | **Hạn chế kiểm thử** | Bổ sung kịch bản kiểm thử tự động toàn diện cho Transaction POS và Rollback kho hàng. |
| 28 | `ManHinhChinh_GUI.java:40-56` | Hệ thống quản lý toàn diện gồm 5 phân hệ: Bán hàng, Mẫu giày, Khách hàng, Nhân sự, Thống kê. | `ThongKe_GUI` **hoàn toàn không được thêm vào tab** nào trong `ManHinhChinh_GUI` (chỉ có 4 tab). Lớp `ThongKe_GUI` bị cô lập hoàn toàn khỏi luồng sử dụng chính. | Không | **Thành phần bị cô lập** | Thêm Tab 5 "Báo cáo thống kê" (phân quyền Quản lý) vào `ManHinhChinh_GUI` khi được duyệt nâng cấp. |
| 29 | `ManHinhChinh_GUI.java:75` | Footer hiển thị danh mục phím tắt hướng dẫn người dùng. | Ghi nhãn: `[F2] Chọn giày`. Nhưng thực tế phím F2 toàn cục kích hoạt **chuyển sang Tab 2 "Quản lý mẫu giày"**. | Không | **Sai thông báo** | Sửa nhãn footer thành `[F2] Mẫu giày` hoặc `[F2] Quản lý giày`. |
| 30 | `BanHang_GUI.java:831-853` | Hóa đơn K80 thể hiện đầy đủ các yếu tố tài chính (Tổng tiền hàng, Chiết khấu thành viên, Giảm giá điểm, Khách cần trả, Tiền thừa). | Hóa đơn in ra chỉ có danh sách món rồi nhảy thẳng sang `TỔNG TIỀN` (đã trừ giảm). Hoàn toàn **bỏ quên dòng Chiết khấu, Giảm giá điểm và Điểm cộng mới**, khiến khách hàng thấy tổng tiền món không khớp với tổng tiền thanh toán. | Không | **Sai thông báo / Thiếu dữ liệu** | Bổ sung các dòng `Tổng tiền hàng`, `Chiết khấu VIP (-X đ)`, `Tiền giảm điểm (-Y đ)` và `Điểm tích lũy cộng mới (+Z đ)` vào bill K80. |
| 31 | `BanHang_GUI.java:601-628`<br>vs `381-392` | Chế độ thanh toán "Chuyển khoản QR" tự động điền đủ tiền khách đưa bằng tổng tiền cần trả và khóa ô nhập. | Khi chọn QR, ô tiền được khóa. Nhưng nếu sau đó người dùng thêm/bớt hàng trong giỏ hoặc tick "Dùng điểm", `tinhToanTongTienHoaDon()` **không cập nhật lại `txtTienKhachDua`**, gây lệch số tiền hiển thị trên form. | Không | **Sai dữ liệu trên GUI** | Thêm lệnh cập nhật `txtTienKhachDua` trong `tinhToanTongTienHoaDon()` khi đang ở chế độ QR. |
| 32 | `BanHang_GUI.java:544-569` | Cascading ComboBox: Mẫu giày -> Size -> Màu sắc -> Tồn kho, đơn giá. | Chọn Mẫu nạp Size và Màu song song. Nhưng khi chọn Size, code **không lọc lại danh sách Màu theo Size đã chọn**. Người dùng có thể chọn tổ hợp Size + Màu không có thật (hệ thống báo "0 đôi" và chặn thêm giỏ). | Không | **Hạn chế UX** | Khi thay đổi `cboSize`, lọc lại các màu sắc thực tế còn tồn kho của size đó. |
| 33 | `BanHang_GUI.java:436-498` | Phím tắt toàn cục do cửa sổ chính điều phối. | `BanHang_GUI` tự đăng ký thêm một bộ hotkey toàn cục F1-F4, ESC, DEL, F10. Phím F10 và DEL bị bắt chồng chéo 2-4 lần ở nhiều component, gây nguy cơ kích hoạt đúp. | Không | **Code thừa / Nguy cơ** | Gỡ bỏ các key binding trùng lặp trong `BanHang_GUI`, để `ManHinhChinh_GUI` làm đầu mối duy nhất. |
| 34 | `BanHang_GUI.java:500-508` | Chuyển tab giữa các màn hình trong ứng dụng. | Hàm `switchTab(int)` ép kiểu cứng `(JTabbedPane) getContentPane().getComponent(1)`. Nếu thay đổi cấu trúc layout của `ManHinhChinh_GUI` sẽ gây sập app do `ClassCastException`. | Không | **Nguy cơ / Code chết** | Xóa bỏ hàm `switchTab` chết này vì `ManHinhChinh_GUI` đã tự bắt phím chuyển tab. |
| 35 | `BanHang_GUI.java:199`<br>vs Tài liệu hướng dẫn | Tài liệu kiến trúc và Javadoc ghi nút `+ Thêm Vào Giỏ [F2]`. | Code thực tế đã đổi thành `+ Thêm Vào Giỏ` (bỏ `[F2]` để tránh đè phím F2 chuyển tab). | Không | **Sai tài liệu** | Cập nhật tài liệu kiến trúc và Javadoc bỏ `[F2]` khỏi tên nút. |
| 36 | `QuanLySanPham_GUI.java:283` | Khi thêm sản phẩm mới, tự động tạo biến thể mặc định (SKU CTG size 40 Đen tồn 20). | Lệnh `ctg_dao.themChiTietGiay(ctg)` **hoàn toàn bỏ qua giá trị trả về**. Nếu thêm biến thể thất bại (ví dụ trùng SKU), GUI vẫn thông báo "Thêm sản phẩm thành công!". | Không | **Sai thông báo / Nguy cơ** | Kiểm tra `if (ctg_dao.themChiTietGiay(ctg))` trước khi thông báo thành công cho người dùng. |
| 37 | `QuanLyKhachHang_GUI.java:77, 209` | Hạng thẻ thành viên là thuộc tính dẫn xuất từ Điểm tích lũy (>=200: Kim Cương, >=100: Vàng, >=30: Bạc, còn lại: Đồng). | Dropdown `cboHang` luôn mở cho nhân viên tự do chọn hạng thẻ (kể cả chọn "Kim Cương" cho khách hàng mới 0 điểm), tạo kẽ hở gian lận chiết khấu 15% tại quầy POS. | Không | **Lỗ hổng nghiệp vụ** | Đặt `cboHang.setEnabled(false)` hoặc tự động nhảy hạng thẻ theo số điểm thực tế. |
| 38 | `QuanLyKhachHang_GUI.java:219-236` | Xóa khách hàng chọn từ bảng danh sách. | Nút Xóa fallback lấy mã từ ô nhập `txtMaKH`. Nếu mã không có trong DB, hàm trả về false và gán nhầm thông báo: *"Xóa thất bại: Lỗi hệ thống!"*. | Không | **Sai thông báo** | Bắt buộc chọn dòng trên bảng; nếu không tìm thấy mã thì thông báo rõ "Khách hàng không tồn tại". |
| 39 | `QuanLyKhachHang_GUI.java:212, 229, 278` | Nạp lại bảng dữ liệu sau khi Thêm/Sửa/Xóa. | Code gọi `docDuLieuVaoTable()` rồi ngay sau đó gọi `xoaTrang()` (trong `xoaTrang()` lại gọi `docDuLieuVaoTable()` lần 2), gây lãng phí truy vấn CSDL kép. | **Có** (Hồi quy hiệu năng sau khi bổ sung load table vào `xoaTrang`) | **Thẩm mỹ / Hiệu năng** | Bỏ lời gọi `docDuLieuVaoTable()` thừa trước khi gọi `xoaTrang()`. |
| 40 | `QuanLyKhachHang_GUI.java:132, 323` | Lắng nghe sự kiện chọn dòng trên bảng khách hàng. | Đăng ký đồng thời cả `ListSelectionListener` và `MouseListener` (`mouseClicked`), khiến hàm hiển thị thông tin form bị chạy 2 lần mỗi khi click chuột. | **Có** (Sót `MouseListener` sau khi thêm `ListSelectionListener`) | **Code thừa** | Xóa bỏ `MouseListener` và `implements MouseListener` thừa trên `QuanLyKhachHang_GUI`. |
| 41 | `QuanLyKhachHang_GUI.java:191`<br>vs Tài liệu cũ | Tài liệu cũ ghi regex SĐT là `^0\d{9}$` (10 số bất kỳ bắt đầu bằng 0). | Code thực tế dùng `^0[35789]\d{8}$` để khớp chính xác 100% với ràng buộc CSDL SQL Server `CK_KhachHang_sdt`. | Không | **Sai tài liệu** | Cập nhật tài liệu hướng dẫn và báo cáo Word ghi đúng regex `^0[35789]\d{8}$`. |
| 42 | `ThongKe_GUI.java:213, 220, 223` | Báo cáo Word ghi nhận hạn chế: số đôi giày ước lượng `số đơn x 2`, khách hàng cố định, Top 5 sản phẩm mẫu hardcode. | Code thực tế giữ nguyên dữ liệu mẫu để bảo toàn tính trung thực của báo cáo đồ án: `countDon * 2`, `"4 khách"`, 5 dòng sản phẩm gán cứng. | Không | **Hạn chế đồ án (Đúng thỏa thuận)** | Duy trì mô tả hạn chế này trong báo cáo Word; không tự ý xóa bỏ mã nguồn mẫu. |
| 43 | `ThongKe_GUI.java:251-274` | Nút "Xuất Báo Cáo [Excel]". | Báo cáo Word ghi nhận nút này mới chỉ hiển thị hộp thoại `JOptionPane` chưa tạo file thật. Code thực tế hoàn toàn khớp mô tả này (không có Apache POI). | Không | **Hạn chế đồ án (Đúng thỏa thuận)** | Giữ nguyên hiện trạng, không cài thêm thư viện ngoài làm phình dự án. |
| 44 | `_sync/ANTIGRAVITY_STATUS.md:146` | Ghi nhận tiến độ đồng bộ các module hệ thống. | Tuyên bố: *"ThongKe_GUI.java: hiển thị số lượng đôi bán và số khách hàng từ database thật, Top 5 sản phẩm bán chạy truy vấn động từ CSDL, xuất CSV UTF-8..."* -> **Thông báo sai sự thật** so với code thực tế của `ThongKe_GUI.java`. | Không | **Sai thông báo trong log tiến độ** | Đính chính lại `ANTIGRAVITY_STATUS.md` cho khớp với thực tế mã nguồn và `EVENT_AUDIT.md`. |

---

## PHẦN 2. TOP 5 RỦI RO KỸ THUẬT CAO NHẤT (HIGHEST TECHNICAL RISKS)

### 🔴 RỦI RO 1: Mất dữ liệu khi cập nhật nhân viên do bỏ sót cột trong câu lệnh SQL
- **Vị trí:** `src/dao/NhanVien_DAO.java` dòng 267–280.
- **Hiện tượng:** Câu lệnh SQL cập nhật nhân sự:
  ```java
  String sql = "UPDATE NhanVien SET hoTen = ?, soDienThoai = ?, diaChi = ?, chucVu = ?, luongCoBan = ?, caLamViec = ?, trangThai = ? WHERE maNhanVien = ?";
  ```
  hoàn toàn không có trường `gioiTinh = ?`.
- **Hậu quả:** Khi quản lý chỉnh sửa giới tính nhân viên từ Nam sang Nữ (hoặc ngược lại) trên giao diện `QuanLyNhanVien_GUI`, bảng giao diện cập nhật ngay lập tức nhưng CSDL SQL Server vẫn giữ nguyên giá trị cũ. Khi tải lại ứng dụng, dữ liệu bị sai lệch. Đây là lỗi hồi quy phát sinh khi thêm cột `diaChi` và `trangThai` nhưng vô tình xóa mất `gioiTinh`.

---

### 🔴 RỦI RO 2: Phím tắt toàn cục kích hoạt thao tác ngầm ngoài ý muốn ở màn hình khác
- **Vị trí:** `src/gui/ManHinhChinh_GUI.java` dòng 184–205.
- **Hiện tượng:** Phím `F10` (Thanh toán) và `DELETE` (Xóa món khỏi giỏ hàng) được đăng ký ở cấp độ `JRootPane` (`WHEN_IN_FOCUSED_WINDOW`) nhưng không kiểm tra tab hiện tại:
  ```java
  am.put("KEY_DELETE", new AbstractAction() {
      @Override
      public void actionPerformed(ActionEvent e) {
          Component c0 = tabbedPane.getComponentAt(0);
          if (c0 instanceof BanHang_GUI) {
              ((BanHang_GUI) c0).xoaMucKhoiGio();
          }
      }
  });
  ```
- **Hậu quả:** Khi thu ngân đang ở Tab 2 (Quản lý giày), Tab 3 (Khách hàng) hoặc Tab 4 (Nhân sự), nếu nhấn phím Delete để xóa ký tự trong ô text hoặc nhấn F10, lệnh sẽ âm thầm gửi về tab Bán hàng và xóa mất một món hàng trong giỏ của khách đang chờ thanh toán!

---

### 🔴 RỦI RO 3: Đóng nhầm kết nối Singleton làm gián đoạn truy vấn và rò rỉ tài nguyên
- **Vị trí:** 
  - `src/dao/SanPham_DAO.java` dòng 104–105 (`kiemTraTrungMa`)
  - `src/dao/NhanVien_DAO.java` dòng 180, 196 (`kiemTraTrungMa`, `kiemTraTrungSDT`)
  - `src/dao/KhachHang_DAO.java` dòng 18, 229, 241 (`kiemTraTrungSDT`, `xoaKhachHang`, `sinhMaKhachHangMoi`)
- **Hiện tượng:** Sử dụng cú pháp `try (Connection con = getConnection(); ...)` với kết nối tĩnh Singleton của `ConnectDB`.
- **Hậu quả:** Cơ chế `AutoCloseable` của Java tự động gọi `con.close()` đóng luôn biến kết nối dùng chung của toàn hệ thống. Ngay sau đó, các thao tác thêm sản phẩm, thêm khách hàng hoặc nạp bảng buộc phải chạy lại chuỗi kiểm tra kết nối với 3 URLs và 3 passwords, gây giật lag nghiêm trọng và dễ phát sinh lỗi `Connection is closed` hoặc `SocketException` trong môi trường đa luồng Swing.

---

### 🔴 RỦI RO 4: Lỗ hổng xác thực Pass-The-Hash cho phép vượt qua mật khẩu gốc
- **Vị trí:** `src/dao/NhanVien_DAO.java` dòng 124.
- **Hiện tượng:** Hàm xác thực đăng nhập:
  ```java
  if (dbHash != null && (hashInput.equalsIgnoreCase(dbHash) || matKhau.equals(dbHash)))
  ```
- **Hậu quả:** Biểu thức `|| matKhau.equals(dbHash)` cho phép bất kỳ ai biết được chuỗi băm SHA-256 (64 ký tự hex) lưu trong CSDL chỉ cần sao chép và dán trực tiếp vào ô mật khẩu trên giao diện là có thể đăng nhập thành công với quyền hạn của nhân viên đó mà hoàn toàn không cần biết mật khẩu thực sự.

---

### 🔴 RỦI RO 5: Làm giả dữ liệu ngày sinh nhân sự để lách ràng buộc CHECK CSDL
- **Vị trí:** `src/gui/QuanLyNhanVien_GUI.java` dòng 218 và 278.
- **Hiện tượng:** Form quản lý nhân sự không thiết kế ô nhập ngày sinh, email, mật khẩu. Khi thêm mới hoặc sửa, code gán cứng:
  ```java
  LocalDate ngaySinh = LocalDate.of(2000, 1, 1); // Dòng 218
  NhanVien nv = new NhanVien(ma, ten, sdt, ngaySinh, gt, dc, null, chucVu, luong, caLam, "123456", true);
  ```
- **Hậu quả:** Toàn bộ nhân viên trong cửa hàng đều bị gán sinh ngày `01/01/2000` (để lách luật `CK_NhanVien_tuoi >= 18`). Dữ liệu nhân thân bị sai lệch hoàn toàn so với thực tế và không thể phân biệt tuổi tác của nhân viên.

---

## PHẦN 3. DANH SÁCH CHỖ TÀI LIỆU SAI SO VỚI CODE THỰC TẾ
*(Dành riêng cho Phiên Bên Trái sử dụng để hiệu chỉnh Báo Cáo Word và các tài liệu đặc tả)*

1. **Phương thức `equals()` & `hashCode()` trong lớp trừu tượng `Nguoi`:**
   - *Tài liệu nói:* Báo cáo Word ghi nhận `Nguoi` cài đặt đa hình `toString()`, `equals()`, `hashCode()`.
   - *Code thực tế:* `Nguoi.java` **chỉ có `toString()`**, không hề cài đặt `equals()` hay `hashCode()` (chỉ có 2 lớp con `NhanVien` và `KhachHang` tự cài đặt theo mã khóa chính riêng).
   - *Cần sửa:* Điều chỉnh câu chữ trong Báo cáo Word Phần II (Đặc tả lớp Nguoi).

2. **Regex số điện thoại khách hàng:**
   - *Tài liệu nói:* `HUONG_DAN_KIEN_TRUC_VA_CODE.md:397` và `GROUND_TRUTH.md:131` ghi regex là `^0\d{9}$`. Script sinh Word dòng 681 ghi `(^0[35789]\d{8}$ hoặc ^0\d{9}$)`.
   - *Code thực tế:* `QuanLyKhachHang_GUI.java:191` và `BanHang_GUI.java:710` đã siết chặt lại duy nhất biểu thức `^0[35789]\d{8}$` để tương thích hoàn toàn với ràng buộc SQL Server `CK_KhachHang_sdt`.
   - *Cần sửa:* Cập nhật tài liệu hướng dẫn và script sinh Word ghi thống nhất `^0[35789]\d{8}$`.

3. **Chức năng của phím tắt F2:**
   - *Tài liệu nói:* Javadoc dòng 24 của `BanHang_GUI`, dòng 350 của `HUONG_DAN_KIEN_TRUC_VA_CODE.md` và Footer dòng 75 của `ManHinhChinh_GUI` đều ghi `[F2] Chọn giày` / `+ Thêm Vào Giỏ [F2]`.
   - *Code thực tế:* Nút thêm giỏ hàng đã bỏ nhãn `[F2]`. Phím F2 toàn cục thực chất là chuyển sang **Tab 2: Quản lý mẫu giày**.
   - *Cần sửa:* Sửa footer giao diện và tài liệu hướng dẫn thành `[F2] Quản lý mẫu giày` / `[F2] Mẫu giày`.

4. **Trạng thái tính năng của `ThongKe_GUI` trong `ANTIGRAVITY_STATUS.md`:**
   - *Tài liệu nói:* Dòng 146 của `ANTIGRAVITY_STATUS.md` ghi rằng `ThongKe_GUI` đã truy vấn động số đôi giày, số khách hàng và Top 5 sản phẩm từ CSDL, xuất CSV UTF-8.
   - *Code thực tế:* `ThongKe_GUI` vẫn dùng dữ liệu ước lượng `countDon * 2`, `4 khách`, bảng Top 5 hardcode và nút xuất Excel chỉ mở `JOptionPane` (giữ đúng thỏa thuận hạn chế của đồ án).
   - *Cần sửa:* Đính chính dòng 146 trong `_sync/ANTIGRAVITY_STATUS.md` cho khớp với thực tế `EVENT_AUDIT.md`.

5. **Giải thích ràng buộc Check Constraint giá sản phẩm trong tài liệu:**
   - *Tài liệu nói:* `HUONG_DAN_KIEN_TRUC_VA_CODE.md:134` ghi `CK_SanPham_giaBan: giaBan > 0 và giaNhap > 0`.
   - *Code thực tế:* CSDL tách bạch thành 2 ràng buộc riêng: `CK_SanPham_giaNhap CHECK (giaNhap > 0)` và `CK_SanPham_giaBan CHECK (giaBan >= giaNhap)`.
   - *Cần sửa:* Cập nhật mục 3.2 của tài liệu hướng dẫn khớp với tên và nội dung thật của 2 ràng buộc SQL Server.

---

## PHẦN 4. DANH SÁCH CHỖ CODE SAI SO VỚI TÀI LIỆU
*(Dành riêng cho Phiên Bên Phải sử dụng để sửa lỗi mã nguồn trên nhánh `fix/regression-check`)*

1. **Sửa `src/dao/NhanVien_DAO.java` dòng 267:**
   - Bổ sung cột `gioiTinh = ?` vào câu lệnh UPDATE và gán tham số tương ứng để lưu được giới tính nhân viên xuống CSDL.

2. **Sửa `src/gui/ManHinhChinh_GUI.java` dòng 184–205:**
   - Bọc điều kiện kiểm tra `if (tabbedPane.getSelectedIndex() == 0)` cho 2 Action của phím `F10` và `DELETE`, ngăn chặn thao tác ngầm làm hỏng giỏ hàng khi đang đứng ở các tab khác.

3. **Sửa các phương thức kiểm tra trùng và xóa trong DAO:**
   - `SanPham_DAO.java:104`, `NhanVien_DAO.java:180, 196`, `KhachHang_DAO.java:18, 229, 241`:
   - Bỏ `Connection con` ra khỏi mệnh đề `try (...)` của try-with-resources. Chỉ dùng `Connection con = getConnection();` và không đóng kết nối tĩnh Singleton này.

4. **Sửa `src/dao/NhanVien_DAO.java` dòng 124:**
   - Xóa bỏ vế `|| matKhau.equals(dbHash)` trong hàm `dangNhap` để triệt tiêu hoàn toàn backdoor Pass-The-Hash.

5. **Sửa `src/gui/BanHang_GUI.java` dòng 626 & dòng 846:**
   - Dòng 626: Bổ sung cập nhật lại `txtTienKhachDua` khi đang chọn "Chuyển khoản QR" trong phương thức `tinhToanTongTienHoaDon()`.
   - Dòng 846: Bổ sung in rõ các dòng `Tổng tiền hàng`, `Chiết khấu thành viên`, `Giảm giá điểm` và `Điểm tích lũy cộng mới` trên hóa đơn K80.

6. **Sửa `src/gui/QuanLySanPham_GUI.java` dòng 283:**
   - Kiểm tra kết quả trả về của `ctg_dao.themChiTietGiay(ctg)` khi thêm sản phẩm mới; nếu thất bại thì báo lỗi rõ ràng thay vì luôn báo thành công.

7. **Sửa `src/gui/QuanLyKhachHang_GUI.java` dòng 77 & dòng 212:**
   - Dòng 77: Vô hiệu hóa `cboHang.setEnabled(false)` để ngăn chặn nhân viên tự ý gán thẻ VIP sai quy định.
   - Dòng 212, 229, 278: Xóa lệnh gọi `docDuLieuVaoTable()` trùng lặp trước lời gọi `xoaTrang()`.
   - Dòng 323–328: Xóa bỏ `MouseListener` và `mouseClicked` thừa.

8. **Sửa `src/gui/ManHinhChinh_GUI.java` dòng 75:**
   - Sửa chuỗi hiển thị Footer: `[F2] Chọn giày` ➔ `[F2] Mẫu giày`.

9. **Sửa `src/Main.java` dòng 16–22:**
   - Đưa lệnh `ConnectDB.getInstance().connect()` ra khỏi `SwingUtilities.invokeLater` để tránh làm đóng băng giao diện (EDT) khi mất kết nối CSDL.

10. **Dọn dẹp các đoạn code chết (Dead Code):**
    - `ChiTietGiay_DAO.java:11`: Xóa biến `sp_dao`.
    - `BanHang_GUI.java:500-508`: Xóa hàm `switchTab(int)`.
    - `BanHang_GUI.java:436-498`: Gỡ bỏ các key binding trùng lặp `POS_F1`..`POS_F4`, `POS_ESC`.
    - `Nguoi.java:4`: Xóa `import java.util.Objects;`.

---

## PHẦN 5. XÁC NHẬN BẢO TOÀN MÃ NGUỒN (STRICT READ-ONLY CONFIRMATION)

> **XÁC NHẬN CHÍNH THỨC:**
> 
> Tôi cam kết và xác nhận 100% rằng:
> 1. **Không sửa bất kỳ file `.java` nào** trong toàn bộ cây thư mục `src/` và `_sync/`.
> 2. **Không tạo commit mới, không tạo nhánh mới** trên Git repository.
> 3. **Không đụng chạm hay chỉnh sửa** các tập tin: `generate_final_report_docx.py`, `*.docx`, `database/*.sql`, `*.drawio`, `diagram_*.png`.
> 4. Toàn bộ 16 tác tử chuyên môn (subagents) đã hoàn tất nhiệm vụ rà soát độc lập và đã được giải phóng hoàn toàn khỏi bộ nhớ bằng lệnh `manage_subagents(Action='kill_all')`.
> 5. Tập tin báo cáo này được lập hoàn toàn ở chế độ READ-ONLY nhằm cung cấp bức tranh đối chiếu chân thực, phục vụ cho phiên trái (sửa báo cáo Word) và phiên phải (sửa code trên nhánh `fix/regression-check`).

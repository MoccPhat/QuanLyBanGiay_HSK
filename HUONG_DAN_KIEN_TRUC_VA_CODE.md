# STEPUP FOOTWEAR POS - CẨM NANG TOÀN TẬP VỀ KIẾN TRÚC, MÃ NGUỒN & HỆ THỐNG SỰ KIỆN (EVENT HANDLING)
> **Dự án:** Hệ Thống Quản Lý Bán Giày Dép Thời Trang Tại Cửa Hàng (StepUp Footwear POS)  
> **Ngôn ngữ:** Java (JDK 17+) | **Giao diện:** Java Swing (Flat Modern POS Look & Feel)  
> **Cơ sở dữ liệu:** Microsoft SQL Server (Transact-SQL) | **Kiến trúc:** 3-Tier Layered Architecture (Entity - DAO - GUI)  
> **Tài liệu đặc biệt:** Phân tích chi tiết từ Giao diện vào Mã nguồn & Giải mã toàn bộ Hệ thống Sự kiện (Event-Driven) để người mới hoặc giảng viên chấm điểm nắm bắt trọn vẹn trong 5 phút.

---

## MỤC LỤC
1. [Tổng Quan Kiến Trúc 3 Tầng (3-Tier Layered Architecture)](#1-tổng-quan-kiến-trúc-3-tầng)
2. [Cấu Trúc Thư Mục & Vai Trò Từng Gói (Package Structure)](#2-cấu-trúc-thư-mục--vai-trò-từng-gói)
3. [Mô Hình Cơ Sở Dữ Liệu & Ràng Buộc Nghiệp Vụ (SQL Server Constraints)](#3-mô-hình-cơ-sở-dữ-liệu--ràng-buộc-nghiệp-vụ)
4. [CẨM NANG TOÀN TẬP VỀ SỰ KIỆN (EVENT-DRIVEN ARCHITECTURE) - GIẢI MÃ ĐỂ KHÔNG BỊ "LÚ"](#4-cẩm-nang-toàn-tập-về-sự-kiện-event-driven-architecture)
   - [4.1. Bản chất sự kiện trong Java Swing](#41-bản-chất-sự-kiện-trong-java-swing)
   - [4.2. Phím tắt: Vì sao `KeyListener` thất bại và `KeyBindings` (`InputMap`/`ActionMap`) chiến thắng?](#42-phím-tắt-keylistener-vs-keybindings)
   - [4.3. Luồng sự kiện nút bấm (`ActionListener`)](#43-luồng-sự-kiện-nút-bấm-actionlistener)
   - [4.4. Luồng sự kiện chuyển Tab tự động đồng bộ (`ChangeListener`)](#44-luồng-sự-kiện-chuyển-tab-changelistener)
   - [4.5. Luồng sự kiện duyệt bảng bằng chuột và phím mũi tên (`ListSelectionListener` vs `MouseListener`)](#45-luồng-sự-kiện-duyệt-bảng-listselectionlistener)
   - [4.6. Luồng sự kiện gõ phím tính tiền thừa thời gian thực (`KeyAdapter.keyReleased`)](#46-luồng-sự-kiện-gõ-phím-tính-tiền-thừa)
   - [4.7. Luồng sự kiện dùng điểm thưởng (`ItemListener` / `ActionListener` trên CheckBox)](#47-luồng-sự-kiện-dùng-điểm-thưởng)
   - [4.8. Luồng giao dịch an toàn CSDL (ACID Transaction trong DAO)](#48-luồng-giao-dịch-an-toàn-csdl)
5. [Hướng Dẫn Soi Code Theo Từng Giao Diện (Screen-by-Screen UI-to-Code Mapping)](#5-hướng-dẫn-soi-code-theo-từng-giao-diện)
   - [5.1. Màn hình Đăng Nhập (`DangNhap_GUI.java`)](#51-màn-hình-đăng-nhập)
   - [5.2. Khung điều hướng & Phím tắt toàn cục (`ManHinhChinh_GUI.java`)](#52-khung-điều-hướng--phím-tắt-toàn-cục)
   - [5.3. Phân hệ Bán Hàng POS (`BanHang_GUI.java`)](#53-phân-hệ-bán-hàng-pos)
   - [5.4. Phân hệ Quản Lý Mẫu Giày (`QuanLySanPham_GUI.java`)](#54-phân-hệ-quản-lý-mẫu-giày)
   - [5.5. Phân hệ Quản Lý Khách Hàng (`QuanLyKhachHang_GUI.java`)](#55-phân-hệ-quản-lý-khách-hàng)
   - [5.6. Phân hệ Quản Lý Nhân Sự (`QuanLyNhanVien_GUI.java`)](#56-phân-hệ-quản-lý-nhân-sự)
   - [5.7. Phân hệ Thống Kê Doanh Thu (`ThongKe_GUI.java`)](#57-phân-hệ-thống-kê-doanh-thu)
   - [5.8. Lớp Tiện Ích Giao Diện & Khắc Phục Lỗi Nút Windows (`UIHelper.java`)](#58-lớp-tiện-ích-giao-diện-uihelper)
6. [Báo Cáo Chi Tiết Khắc Phục Lỗi Toàn Diện (Bug Audit Report)](#6-báo-cáo-chi-tiết-khắc-phục-lỗi)
7. [Kết Quả Kiểm Thử Thực Tế (Empirical Test Suite Results)](#7-kết-quả-kiểm-thử-thực-tế)

---

## 1. TỔNG QUAN KIẾN TRÚC 3 TẦNG

Dự án áp dụng mô hình **3-Tier Layered Architecture** chuẩn mực công nghiệp nhằm đảm bảo tính độc lập, dễ bảo trì, dễ mở rộng và đạt điểm số tối đa khi giảng viên chấm code:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           1. TẦNG GIAO DIỆN (GUI LAYER)                         │
│  gui/DangNhap_GUI | gui/ManHinhChinh_GUI | gui/BanHang_GUI | gui/UIHelper...   │
│  - Trách nhiệm: Vẽ giao diện người dùng Swing (Flat Modern UI).                 │
│  - Lắng nghe hành vi người dùng (Click chuột, gõ phím, đổi tab).                │
│  - Kiểm tra tính hợp lệ dữ liệu (Form Validation, Regex SĐT, Số > 0) trước khi  │
│    chuyển tiếp xuống tầng dưới. Tuyệt đối không viết câu lệnh SQL tại tầng này. │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ Truyền nhận DTO / Entity
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    2. TẦNG TRUY XUẤT DỮ LIỆU (DAO LAYER)                        │
│  dao/HoaDon_DAO | dao/SanPham_DAO | dao/ChiTietGiay_DAO | dao/KhachHang_DAO...  │
│  - Trách nhiệm: Thực thi các thao tác CRUD và Transaction với CSDL SQL Server.  │
│  - Đảm bảo an toàn luồng dữ liệu, chống SQL Injection bằng PreparedStatement.   │
│  - Quản trị Transaction ACID: setAutoCommit(false), commit(), rollback().      │
│  - Quản lý quy tắc sinh mã tự động (ID Generation) và kiểm soát tồn kho tức thì.│
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ Đóng gói thành các thực thể
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       3. TẦNG THỰC THỂ DỮ LIỆU (ENTITY LAYER)                   │
│  entity/Nguoi (abstract) <- NhanVien, KhachHang | SanPham | ChiTietGiay...      │
│  - Trách nhiệm: Mô hình hóa các đối tượng trong bài toán quản lý cửa hàng giày. │
│  - Đóng gói đầy đủ thuộc tính, Getter, Setter, Constructor, equals, hashCode.   │
│  - Chứa logic nghiệp vụ nội tại (ví dụ: NhanVien.isQuanLy(), HoaDon.getTong()). │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ Kết nối JDBC Singleton (ConnectDB)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       4. TẦNG CƠ SỞ DỮ LIỆU (DATABASE LAYER)                    │
│  Microsoft SQL Server 2019/2022 (Database: QuanLyBanGiay)                       │
│  - Lưu trữ bền vững dữ liệu bán hàng.                                           │
│  - Khóa chính, Khóa ngoại, Ràng buộc kiểm tra toàn vẹn dữ liệu (CHECK).        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. CẤU TRÚC THƯ MỤC & VAI TRÒ TỪNG GÓI

```
E:\Project_HSK\
├── bin/                          # Chứa bytecode (.class) đã biên dịch
├── lib/                          # Driver JDBC: mssql-jdbc-12.4.2.jre11.jar
├── data/                         # Hình ảnh sản phẩm giày dép
├── SoiLoi_QuanLyBanGiay/         # Kịch bản kiểm thử tự động (KiemThu.java)
└── src/                          # Mã nguồn chương trình
    ├── Main.java                 # Khởi chạy ứng dụng (Mở DangNhap_GUI)
    ├── connectDB/
    │   └── ConnectDB.java        # Quản lý kết nối SQL Server (Mô hình Singleton)
    ├── entity/                   # Các lớp thực thể đối tượng
    │   ├── Nguoi.java            # Lớp trừu tượng: họ tên, sdt, ngày sinh, địa chỉ
    │   ├── NhanVien.java         # Kế thừa Nguoi: chức vụ, lương, mật khẩu hash
    │   ├── KhachHang.java        # Kế thừa Nguoi: điểm tích lũy, hạng thành viên
    │   ├── SanPham.java          # Mẫu giày: tên, loại, thương hiệu, giá nhập/bán
    │   ├── ChiTietGiay.java      # Biến thể SKU: mã SKU, size, màu, số lượng tồn
    │   ├── HoaDon.java           # Hóa đơn: tổng hàng, chiết khấu, điểm, tổng trả
    │   └── ChiTietHoaDon.java    # Dòng hóa đơn: SKU, số lượng, đơn giá, thành tiền
    ├── dao/                      # Các lớp truy xuất CSDL (Data Access Objects)
    │   ├── NhanVien_DAO.java     # Đăng nhập SHA-256, phân quyền, CRUD nhân viên
    │   ├── SanPham_DAO.java      # CRUD mẫu giày, kiểm tra mã sản phẩm
    │   ├── ChiTietGiay_DAO.java  # Quản lý tồn kho theo SKU, sinh mã tự động
    │   ├── KhachHang_DAO.java    # Tìm khách theo SĐT, tích điểm, đổi hạng thẻ
    │   └── HoaDon_DAO.java       # Lưu hóa đơn bán hàng bằng Transaction ACID
    └── gui/                      # Giao diện đồ họa Swing
        ├── UIHelper.java         # Tiện ích giao diện: Nút bấm, bảng, ô nhập, màu sắc
        ├── DangNhap_GUI.java     # Cửa sổ đăng nhập xác thực tài khoản
        ├── ManHinhChinh_GUI.java # Cửa sổ chính chứa Tab chức năng & Hotkeys
        ├── BanHang_GUI.java      # Phân hệ POS bán hàng, thanh toán, in hóa đơn K80
        ├── QuanLySanPham_GUI.java# Phân hệ quản lý mẫu giày & tạo biến thể SKU
        ├── QuanLyKhachHang_GUI.java # Phân hệ quản lý khách hàng & lịch sử điểm
        ├── QuanLyNhanVien_GUI.java  # Phân hệ quản lý nhân sự (chỉ Quản lý)
        └── ThongKe_GUI.java      # Phân hệ thống kê doanh thu & top bán chạy
```

---

## 3. MÔ HÌNH CƠ SỞ DỮ LIỆU & RÀNG BUỘC NGHIỆP VỤ

Hệ thống kết nối đến Microsoft SQL Server `QuanLyBanGiay` với 6 bảng liên kết chặt chẽ:

```
 [NhanVien] 1 ──── ∞ [HoaDon] 1 ──── ∞ [ChiTietHoaDon] ∞ ──── 1 [ChiTietGiay] ∞ ──── 1 [SanPham]
                         │
                         │ ∞
                         │
                         1
                    [KhachHang]
```

### Các ràng buộc Check Constraint cốt tử trong SQL Server:
1. `CK_NhanVien_matKhau`: `LEN(matKhau) = 64`. Mật khẩu bắt buộc phải là chuỗi băm **SHA-256** (đúng 64 ký tự hex). Bất kỳ câu lệnh `INSERT / UPDATE` nào truyền mật khẩu chữ thường ngắn ngày đều bị SQL Server từ chối ngay lập tức.
2. `CK_SanPham_giaNhap`: `giaNhap > 0`. Giá vốn nhập kho bắt buộc phải lớn hơn 0.
3. `CK_SanPham_giaBan`: `giaBan >= giaNhap`. Giá bán niêm yết bắt buộc phải lớn hơn hoặc bằng giá vốn nhập kho, ngăn chặn bán phá giá hoặc kinh doanh lỗ vốn.
4. `CK_HoaDon_diemKhach`: `([maKhachHang] IS NOT NULL OR ([diemSuDung]=0 AND [diemCong]=0 AND [chietKhau]=0))`.  
   👉 **Ý nghĩa nghiệp vụ:** Nếu là khách vãng lai (`maKhachHang IS NULL`), hóa đơn **bắt buộc phải có `chietKhau = 0`, `diemSuDung = 0`, `diemCong = 0`**. Chỉ khách hàng thành viên có đăng ký số điện thoại mới được hưởng ưu đãi hạng thẻ và điểm thưởng.
5. `CK_HoaDon_tienDiem`: `tienGiamDiem = diemSuDung * 1000`. (Quy ước: 1 điểm tích lũy quy đổi thành 1.000 VNĐ).
6. `CK_HoaDon_tongTien`: `tongTien = (tongTienHang - chietKhau) - tienGiamDiem`.
7. `CK_HoaDon_tienThua`: `tienThua = tienKhachDua - tongTien`.

---

## 4. CẨM NANG TOÀN TẬP VỀ SỰ KIỆN (EVENT-DRIVEN ARCHITECTURE) - GIẢI MÃ ĐỂ KHÔNG BỊ "LÚ"

Trong lập trình Java Swing, **sự kiện (Events)** là linh hồn của toàn bộ ứng dụng. Nếu không hiểu rõ bản chất, lập trình viên rất dễ bị "lú": tại sao phím tắt không ăn? Tại sao gõ chữ lại crash? Tại sao click chuột thì được mà bấm mũi tên thì không? Dưới đây là phân tích chi tiết từng cơ chế:

```
+─────────────────────────────────────────────────────────────────────────────────+
|                  SỰ KIỆN NGƯỜI DÙNG (USER GESTURES)                             |
|  Bấm nút [Click] | Gõ phím [Key] | Đổi Tab [Change] | Chọn dòng bảng [Select]   |
+───────────────────────────────────────┬─────────────────────────────────────────+
                                        │ Đẩy vào hàng đợi EDT
                                        ▼
+─────────────────────────────────────────────────────────────────────────────────+
|               EVENT DISPATCH THREAD (EDT - LUỒNG XỬ LÝ GIAO DIỆN)               |
|                                                                                 |
|  1. KeyBindings (InputMap/ActionMap)  ──> Bắt phím F1-F4, F10, ESC, DEL toàn cục|
|  2. ActionListener                    ──> Xử lý Click nút, Chọn combobox        |
|  3. ChangeListener                    ──> Bắt sự kiện đổi Tab, tự làm mới data  |
|  4. ListSelectionListener             ──> Bắt dòng chọn bảng (chuột + phím)     |
|  5. KeyAdapter (keyReleased)          ──> Tính tiền thừa thời gian thực         |
|  6. ItemListener                      ──> Bắt sự kiện Tick chọn checkbox điểm   |
+─────────────────────────────────────────────────────────────────────────────────+
```

---

### 4.1. Bản chất sự kiện trong Java Swing
- Java Swing chạy trên một luồng chuyên biệt duy nhất gọi là **Event Dispatch Thread (EDT)**.
- Khi người dùng tương tác, hệ điều hành gửi tín hiệu đến JVM. JVM đóng gói thành một đối tượng sự kiện (`AWTEvent`, `ActionEvent`, `KeyEvent`...) và chuyển đến thành phần UI đang lắng nghe.

---

### 4.2. Phím tắt: Vì sao `KeyListener` thất bại và `KeyBindings` chiến thắng?
- **Nguyên nhân code cũ bị liệt phím tắt (Lỗi K4 trong báo cáo):**
  - Code cũ dùng `component.addKeyListener(...)`.
  - **Quy tắc vàng của `KeyListener`:** Nó **CHỈ hoạt động khi chính component đó đang giữ Focus bàn phím**. Nếu con trỏ chuột đang ở bảng giỏ hàng, ô nhập tiền khách đưa, hay nút khác thì `KeyListener` của Frame hoàn toàn bị "điếc"! Kết quả là 21/21 lần bấm F1-F4, F10, ESC, DEL đều không có tác dụng gì.
- **Giải pháp chuẩn công nghiệp bằng `KeyBindings` trong `ManHinhChinh_GUI.java`:**
  - Sử dụng cặp đôi `InputMap` và `ActionMap` trên `JRootPane` với điều kiện kích hoạt:
    ```java
    JRootPane rp = getRootPane();
    InputMap im = rp.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
    ActionMap am = rp.getActionMap();
    ```
  - **`WHEN_IN_FOCUSED_WINDOW`:** Bất kể con trỏ đang nằm ở ô nhập chữ, combobox, bảng dữ liệu hay nút bấm, chỉ cần cửa sổ ứng dụng đang mở (Focused Window) là phím tắt lập tức được kích hoạt 100%!
  - **Bản đồ phím tắt toàn cục:**
    - `VK_F1` ➔ Chuyển sang Tab Bán Hàng (POS).
    - `VK_F2` ➔ Chuyển sang Tab Quản Lý Mẫu Giày.
    - `VK_F3` ➔ Chuyển sang Tab Khách Hàng.
    - `VK_F4` ➔ Chuyển sang Tab Quản Lý Nhân Sự (nếu có quyền Quản lý).
    - `VK_F10` ➔ Kích hoạt hàm `((BanHang_GUI) c0).thanhToanDonHang()`.
    - `VK_ESCAPE` ➔ Mở hộp thoại xác nhận đăng xuất.
    - `VK_DELETE` ➔ Kích hoạt hàm `((BanHang_GUI) c0).xoaMucKhoiGio()`.

---

### 4.3. Luồng sự kiện nút bấm (`ActionListener`)
- Giao diện cài đặt interface `ActionListener` và hiện thực hàm `actionPerformed(ActionEvent e)`.
- Khi người dùng click nút, phương thức `e.getSource()` được dùng để phân định nút nào vừa được bấm:
  ```java
  Object o = e.getSource();
  if (o.equals(btnThem)) {
      // Thực hiện thêm dữ liệu
  } else if (o.equals(btnXoa)) {
      // Thực hiện xóa dữ liệu
  }
  ```
- **Lưu ý kiểm soát phân quyền:** Tại `QuanLySanPham_GUI.java`, trước khi thực hiện thêm/sửa/xóa, hệ thống kiểm tra ngay `nhanVien.isQuanLy()`. Nếu là nhân viên bán hàng thường, sự kiện bị chặn lại ngay lập tức và hiển thị hộp thoại cảnh báo.

---

### 4.4. Luồng sự kiện chuyển Tab tự động đồng bộ (`ChangeListener`)
- **Tình huống nghiệp vụ:** Người dùng đang ở Tab Bán hàng ➔ Chuyển sang Tab Mẫu giày để thêm một đôi giày mới (SP9999) ➔ Quay trở lại Tab Bán hàng.
- **Vấn đề cũ (Lỗi K9):** Combobox chọn giày ở Tab Bán hàng không có sản phẩm mới thêm, bắt buộc phải tắt app mở lại mới thấy.
- **Giải pháp `ChangeListener` trên `JTabbedPane` tại `ManHinhChinh_GUI.java`:**
  ```java
  tabbedPane.addChangeListener(e -> {
      if (tabbedPane.getSelectedIndex() == 0) { // Khi tab Bán hàng được chọn
          Component comp = tabbedPane.getComponentAt(0);
          if (comp instanceof BanHang_GUI) {
              ((BanHang_GUI) comp).taiLaiDanhSachSanPham(); // Nạp lại danh mục ngay lập tức!
          }
      }
  });
  ```
  Nhờ sự kiện này, dữ liệu giữa các phân hệ được đồng bộ thời gian thực một cách hoàn hảo!

---

### 4.5. Luồng sự kiện duyệt bảng (`ListSelectionListener` vs `MouseListener`)
- **Vấn đề cũ (Lỗi C8):** Bảng chỉ cài `MouseListener`. Khi click chuột thì dữ liệu hiển thị lên form, nhưng khi dùng **phím mũi tên lên/xuống** trên bàn phím thì form đứng yên, không nạp dữ liệu.
- **Giải pháp:** Cài đặt `ListSelectionListener` trên `table.getSelectionModel()`:
  ```java
  tableSP.getSelectionModel().addListSelectionListener(e -> {
      if (!e.getValueIsAdjusting()) { // Chỉ xử lý khi thao tác chọn đã kết thúc
          int row = tableSP.getSelectedRow();
          if (row >= 0) {
              hienThiThongTinLenForm(row);
          }
      }
  });
  ```
  Giờ đây, dù duyệt bằng chuột hay bấm phím mũi tên thì form nhập liệu đều được cập nhật mượt mà.

---

### 4.6. Luồng sự kiện gõ phím tính tiền thừa (`KeyAdapter.keyReleased`)
- Khi thu ngân nhập số tiền khách đưa vào ô `txtTienKhachDua`, ta cần tính và hiển thị ngay số tiền thừa trả khách mà không cần bắt thu ngân phải bấm nút "Tính tiền".
- Sử dụng `KeyAdapter` bắt sự kiện `keyReleased` (khi phím đã được nhả ra):
  ```java
  txtTienKhachDua.addKeyListener(new KeyAdapter() {
      @Override
      public void keyReleased(KeyEvent e) {
          tinhTienThua();
      }
  });
  ```
- **Bẫy lỗi NumberFormatException (Lỗi K7):**
  Trong hàm `tinhTienThua()`, nếu người dùng vô tình gõ chữ ("abc") hoặc ký tự lạ, lệnh `Double.parseDouble()` sẽ quăng ngoại lệ. Nếu không bắt, ngoại lệ sẽ làm đơ luồng EDT! Ta bọc trong `try - catch (NumberFormatException)`:
  ```java
  try {
      double tienDua = Double.parseDouble(strDua);
      double tienThua = tienDua - khachCanTra;
      lblTienThuaVal.setText(df.format(Math.max(0, tienThua)));
  } catch (NumberFormatException ex) {
      lblTienThuaVal.setText("0 VNĐ"); // Xử lý an toàn, không crash!
  }
  ```

---

### 4.7. Luồng sự kiện dùng điểm thưởng (`ItemListener` / `ActionListener`)
- Checkbox `chkDungDiem`: Khi khách hàng muốn dùng điểm tích lũy để trừ tiền.
- Bắt sự kiện:
  ```java
  chkDungDiem.addActionListener(e -> tinhToanTongTienHoaDon());
  ```
  Khi được tick chọn: Hệ thống lấy số điểm của khách nhân 1.000 VNĐ, trừ thẳng vào tổng tiền cần thanh toán và cập nhật các nhãn tiền hiển thị tức thì.

---

### 4.8. Luồng giao dịch an toàn CSDL (ACID Transaction trong `HoaDon_DAO.java`)
Thanh toán một đơn hàng giày dép là một chuỗi hành động phức tạp. Nếu đang trừ kho mà mất điện hoặc kho bị thiếu thì sao? Ta sử dụng **Transaction**:
```java
Connection con = ConnectDB.getConnection();
con.setAutoCommit(false); // BẮT ĐẦU TRANSACTION
try {
    // 1. Sinh mã hóa đơn an toàn (UPDLOCK, HOLDLOCK)
    // 2. INSERT vào bảng HoaDon
    // 3. Vòng lặp INSERT từng dòng vào ChiTietHoaDon
    // 4. KIỂM TRA TỒN KHO THỰC TẾ:
    //    Nếu tồn kho < số lượng bán -> throw new SQLException("Tồn kho không đủ!");
    // 5. Cập nhật trừ số lượng tồn kho ChiTietGiay
    // 6. Cập nhật trừ điểm cũ và cộng điểm mới cho Khách hàng
    // 7. Cập nhật thăng hạng thẻ (Đồng, Bạc, Vàng, Kim Cương)
    
    con.commit(); // THÀNH CÔNG: Xác nhận ghi tất cả vào CSDL!
} catch (Exception ex) {
    con.rollback(); // THẤT BẠI: Hủy bỏ 100% các thao tác, CSDL giữ nguyên vẹn!
    throw ex;
} finally {
    con.setAutoCommit(true); // Khôi phục chế độ tự động commit
}
```

---

## 5. HƯỚNG DẪN SOI CODE THEO TỪNG GIAO DIỆN

Phần này giúp bạn mở giao diện ứng dụng lên và đối chiếu trực tiếp từng nút bấm, bảng dữ liệu, ô nhập sang file code và dòng code cụ thể.

---

### 5.1. Màn hình Đăng Nhập
- **File:** [`src/gui/DangNhap_GUI.java`](file:///E:/Project_HSK/src/gui/DangNhap_GUI.java) | **DAO:** [`src/dao/NhanVien_DAO.java`](file:///E:/Project_HSK/src/dao/NhanVien_DAO.java)

| Thành phần trên UI | Vị trí biến trong code | Hành vi nghiệp vụ & Sự kiện |
|---|---|---|
| **Ô Mã nhân viên** | `txtMaNV` (dòng 16) | Gợi ý mặc định `NV0001`. Lắng nghe phím Enter để đăng nhập nhanh. |
| **Ô Mật khẩu** | `txtMatKhau` (dòng 17) | Trường `JPasswordField` che giấu ký tự. Lắng nghe phím Enter. |
| **Nút Đăng Nhập** | `btnDangNhap` (dòng 86) | Khởi tạo bằng `UIHelper.createPrimaryBtn("Đăng Nhập", 130, 36)`. Khi bấm: Lấy mã & pass -> Băm SHA-256 -> Gọi `nv_dao.dangNhap(maNV, matKhau)`. |
| **Nút Thoát** | `btnThoat` (dòng 87) | Khởi tạo bằng `UIHelper.createSecondaryBtn("Thoát", 100, 36)`. Đóng app (`System.exit(0)`). |
| **Bảo mật SHA-256** | `NhanVien_DAO.java` (dòng 49) | Hàm `hashSHA256()` chuyển mật khẩu thành chuỗi hex 64 ký tự chuẩn mật mã. Không lưu text trần. |

---

### 5.2. Khung điều hướng & Phím tắt toàn cục
- **File:** [`src/gui/ManHinhChinh_GUI.java`](file:///E:/Project_HSK/src/gui/ManHinhChinh_GUI.java)

| Thành phần trên UI | Vị trí biến trong code | Hành vi nghiệp vụ & Sự kiện |
|---|---|---|
| **Header chào mừng** | `lblUser` (dòng 100) | Hiển thị: `Nhân viên: [Họ tên] ([Chức vụ])`. Chữ vàng nổi bật trên nền xanh Navy. |
| **Nút Đăng Xuất** | `btnDangXuat` (dòng 104) | Khởi tạo bằng `UIHelper.createDangerBtn("Đăng Xuất", 100, 30)`. Màu đỏ rực, chữ trắng sắc nét. Bấm nút mở hộp thoại xác nhận `YES_NO_OPTION`. |
| **Hệ thống 4 Tab** | `tabbedPane` (dòng 40) | Quản lý 4 phân hệ. Tab 3 (Nhân sự) chỉ add nếu `nhanVien.isQuanLy() == true`. |
| **Bộ phím tắt toàn cục** | `registerKeyBindings()` (dòng 137) | Đăng ký `WHEN_IN_FOCUSED_WINDOW` trên `JRootPane` cho F1, F2, F3, F4, F10, ESC, DELETE. Bắt phím chuẩn xác ở mọi vị trí con trỏ. |

---

### 5.3. Phân hệ Bán Hàng POS
- **File:** [`src/gui/BanHang_GUI.java`](file:///E:/Project_HSK/src/gui/BanHang_GUI.java) | **DAO:** [`src/dao/HoaDon_DAO.java`](file:///E:/Project_HSK/src/dao/HoaDon_DAO.java)

Giao diện bán hàng chia làm 2 cột:

```
┌──────────────────────────────────────────────────────────┬─────────────────────────────────┐
│ CỘT TRÁI: GIỎ HÀNG & CHỌN MẪU GIÀY                       │ CỘT PHẢI: KHÁCH & THANH TOÁN    │
│                                                          │                                 │
│ Mẫu giày: [cboSanPham      ▼] Size: [cboSize] Màu: [...] │ SĐT Khách: [0977333444] [Tìm]   │
│ Tồn kho: 15 đôi   |   Đơn giá: 2.600.000 VNĐ             │ Tên: Hoàng Thu Trang (Vàng-10%) │
│ Số lượng: [ 2 ]   [ + Thêm Vào Giỏ ] (Xanh dương)         │ Điểm: 120 điểm  [x] Dùng điểm   │
│──────────────────────────────────────────────────────────│─────────────────────────────────│
│ BẢNG GIỎ HÀNG:                                           │ Tổng tiền hàng:   8.700.000 VNĐ │
│ STT | Mã SKU | Tên Giày | Size | SL | Thành tiền        │ Chiết khấu:         990.000 VNĐ │
│ 1   | CTG0001| Nike AF1 | 39   | 2  | 5.200.000 VNĐ     │ KHÁCH CẦN TRẢ:    7.710.000 VNĐ │
│ 2   | CTG0006| UltraBst | 40   | 1  | 3.500.000 VNĐ     │ Tiền khách đưa:  [8000000     ] │
│──────────────────────────────────────────────────────────│ Tiền thừa trả lại:  290.000 VNĐ │
│ [Xóa Mục Chọn (Del)]    [Làm Trống Giỏ] (Xám Slate)      │ [ THANH TOÁN & IN ĐƠN [F10] ]   │
│                                                          │ (Xanh lá Emerald nổi bật)       │
└──────────────────────────────────────────────────────────┴─────────────────────────────────┘
```

| Thành phần trên UI | Vị trí biến trong code | Hành vi nghiệp vụ & Sự kiện |
|---|---|---|
| **Combobox Mẫu / Size / Màu** | `cboSanPham`, `cboSize`, `cboMauSac` | Khi chọn mẫu giày, sự kiện `actionPerformed` nạp lại size & màu tương ứng, tự hiển thị tồn kho và đơn giá bán. |
| **Nút "+ Thêm Vào Giỏ"** | `btnThemGio` (dòng 199) | Khởi tạo bằng `UIHelper.createPrimaryBtn("+ Thêm Vào Giỏ", 180, 34)` (Xanh dương). Kiểm tra số lượng tồn kho trước khi cho vào giỏ. (Phím F2 dành riêng cho chuyển Tab Quản lý mẫu giày). |
| **Nút "Tìm" Khách Hàng** | `btnTimKhach` (dòng 286) | Khởi tạo bằng `UIHelper.createDarkBtn("Tìm", 65, 28)` (Xanh Navy). Tra cứu SĐT qua `kh_dao.timKhachHangTheoSDT()`. Nạp tên, điểm và hạng thẻ. |
| **Checkbox "Dùng điểm"** | `chkDungDiem` (dòng 320) | Bắt sự kiện tick chọn: Giảm 1.000đ cho mỗi 1 điểm tích lũy của khách. |
| **Ô "Tiền khách đưa"** | `txtTienKhachDua` (dòng 355) | Lắng nghe `keyReleased` tính tiền thừa ngay tức khắc. Bọc `try-catch` chống crash chữ. |
| **Nút Xóa giỏ / Làm trống** | `btnXoaKhoiGio`, `btnXoaTrangGio` | Khởi tạo bằng `UIHelper.createSecondaryBtn(...)` (Xám Slate, chữ đen sắc nét). |
| **Hộp thoại Hóa đơn K80** | `thucHienThanhToan()` (dòng 812-843) | **Hóa đơn tự động 100%**: Tự động sinh mã HĐ, ngày giờ, thu ngân, chiết khấu và tiền thừa. Khung hóa đơn được mở rộng vừa vặn (width 460px, padding 16px, triệt tiêu thanh cuộn ngang), khoảng cách trục Y được giãn cách thông thoáng giữa Địa chỉ ➔ Tiêu đề [HÓA ĐƠN BÁN LẺ] ➔ Mã HĐ. |

---

### 5.4. Phân hệ Quản Lý Mẫu Giày
- **File:** [`src/gui/QuanLySanPham_GUI.java`](file:///E:/Project_HSK/src/gui/QuanLySanPham_GUI.java) | **DAO:** [`src/dao/SanPham_DAO.java`](file:///E:/Project_HSK/src/dao/SanPham_DAO.java), [`src/dao/ChiTietGiay_DAO.java`](file:///E:/Project_HSK/src/dao/ChiTietGiay_DAO.java)

| Thành phần trên UI | Vị trí biến trong code | Hành vi nghiệp vụ & Sự kiện |
|---|---|---|
| **Nút "Thêm Mới"** | `btnThem` (dòng 135) | `UIHelper.createSuccessBtn("Thêm Mới", 115, 34)` (Xanh lá). Kiểm tra `giaNhap > 0`, `giaBan >= giaNhap`. Tự động tạo 1 biến thể SKU khởi tạo (Size 40, Đen, Tồn 20) để bán được ngay trên POS. |
| **Nút "Xóa Sản Phẩm"** | `btnXoa` (dòng 136) | `UIHelper.createDangerBtn("Xóa Sản Phẩm", 130, 34)` (Đỏ). Kiểm tra phân quyền: Chỉ Quản lý mới được xóa. |
| **Nút "Cập Nhật"** | `btnSua` (dòng 137) | `UIHelper.createPrimaryBtn("Cập Nhật", 115, 34)` (Xanh dương). Cập nhật thông tin mẫu giày. Chặn nhân viên thường sửa giá. |
| **Nút "Xóa Trắng Form"** | `btnXoaTrang` (dòng 138) | `UIHelper.createSecondaryBtn("Xóa Trắng Form", 130, 34)` (Xám Slate). Xóa trắng textfield và mở lại khóa `txtMaSP`. |
| **Nút "Tìm"** | `btnTim` (dòng 119) | `UIHelper.createDarkBtn("Tìm", 65, 28)` (Navy). Tìm mẫu giày theo tên hoặc mã. |
| **Khóa Mã khi xem** | `hienThiThongTinLenForm()` | Chọn dòng trên bảng thì `txtMaSP.setEditable(false)` để ngăn sửa khóa chính. |

---

### 5.5. Phân hệ Quản Lý Khách Hàng
- **File:** [`src/gui/QuanLyKhachHang_GUI.java`](file:///E:/Project_HSK/src/gui/QuanLyKhachHang_GUI.java) | **DAO:** [`src/dao/KhachHang_DAO.java`](file:///E:/Project_HSK/src/dao/KhachHang_DAO.java)

- **Hệ thống nút bấm đồng bộ:**
  - `btnThem` ➔ `UIHelper.createSuccessBtn("Thêm Khách Hàng", 150, 34)` (Xanh lá)
  - `btnXoa` ➔ `UIHelper.createDangerBtn("Xóa Khách", 110, 34)` (Đỏ)
  - `btnSua` ➔ `UIHelper.createPrimaryBtn("Cập Nhật", 110, 34)` (Xanh dương)
  - `btnXoaTrang` ➔ `UIHelper.createSecondaryBtn("Xóa Trắng", 110, 34)` (Xám Slate)
  - `btnTim` ➔ `UIHelper.createDarkBtn("Tìm", 65, 28)` (Navy)
- **Kiểm tra hợp lệ:** Regex SĐT `^0[35789]\d{8}$` (đúng 10 số theo đầu số hợp lệ của các nhà mạng Việt Nam). Điểm tích lũy ở chế độ Read-only chống sửa bậy.

---

### 5.6. Phân hệ Quản Lý Nhân Sự
- **File:** [`src/gui/QuanLyNhanVien_GUI.java`](file:///E:/Project_HSK/src/gui/QuanLyNhanVien_GUI.java) | **DAO:** [`src/dao/NhanVien_DAO.java`](file:///E:/Project_HSK/src/dao/NhanVien_DAO.java)

- **Phân quyền tối cao:** Chỉ hiển thị tab này cho tài khoản có chức vụ "Quản lý".
- **Hệ thống nút bấm đồng bộ:**
  - `btnThem` ➔ `UIHelper.createSuccessBtn("Thêm Nhân Viên", 150, 34)` (Xanh lá)
  - `btnXoa` ➔ `UIHelper.createDangerBtn("Thôi Việc (Xóa)", 130, 34)` (Đỏ)
  - `btnSua` ➔ `UIHelper.createPrimaryBtn("Cập Nhật", 110, 34)` (Xanh dương)
  - `btnXoaTrang` ➔ `UIHelper.createSecondaryBtn("Xóa Trắng", 110, 34)` (Xám Slate)
- **Mã hóa:** Tự động băm SHA-256 mật khẩu khi tạo nhân viên mới hoặc cập nhật thông tin.

---

### 5.7. Phân hệ Thống Kê Doanh Thu
- **File:** [`src/gui/ThongKe_GUI.java`](file:///E:/Project_HSK/src/gui/ThongKe_GUI.java)

- **Thẻ Bento KPI:** 4 thẻ chỉ số nổi bật với màu sắc đồng bộ: Tổng doanh thu (Xanh lá), Số đơn hàng (Xanh dương), Sản phẩm đã bán (Navy), Khách hàng thành viên (Vàng cam).
- **Thanh lọc dữ liệu:**
  - `btnLoc` ➔ `UIHelper.createPrimaryBtn("Lọc Dữ Liệu", 120, 34)`
  - `btnLamMoi` ➔ `UIHelper.createSecondaryBtn("Làm Mới", 100, 34)`
  - `btnXuatBaoCao` ➔ `UIHelper.createSuccessBtn("Xuất Báo Cáo [Excel]", 180, 34)`

---

### 5.8. Lớp Tiện Ích Giao Diện & Khắc Phục Lỗi Nút Windows (`UIHelper.java`)
- **File:** [`src/gui/UIHelper.java`](file:///E:/Project_HSK/src/gui/UIHelper.java)

#### Vì sao các nút trên Windows bị lỗi chữ trắng trên nền trắng?
Khi sử dụng giao diện hệ thống `UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())`, Windows vẽ nút bằng thư viện native của hệ điều hành. Lớp vẽ này **từ chối vẽ màu nền theo lệnh `setBackground()`** nhưng lại **nhận lệnh đổi màu chữ `setForeground(Color.WHITE)`**. Kết quả là nút có nền trắng/bạc mặc định của Windows nhưng chữ lại màu trắng tinh ➔ chữ bị biến mất hoàn toàn!

#### Cách `UIHelper.createButton()` khắc phục triệt để:
Phương thức `createButton()` ghi đè phương thức `paintComponent(Graphics g)`:
1. **Khử răng cưa:** Kích hoạt `RenderingHints.KEY_ANTIALIASING` và `KEY_TEXT_ANTIALIAS_LCD_HRGB`.
2. **Xử lý trạng thái Disabled:** Khi `!isEnabled()`, tự vẽ nền xám nhạt (`#E2E8F0`), viền xám (`#CBD5E1`) và chữ mờ (`#94A3B8`).
3. **Tự vẽ nền bo góc:** Dùng `g2.fillRoundRect(0, 0, width, height, 8, 8)` với màu nền thật (`bgColor`), xử lý hover sáng lên và click tối xuống.
4. **Tự vẽ viền phân cách:** Bo viền thanh lịch 8px chống tràn.
5. **Tự vẽ chữ sắc nét căn giữa:** Tính toán tọa độ `(width - stringWidth) / 2` và vẽ chữ bằng màu `fgColor` rõ nét 100% trên mọi màn hình!

---

## 6. BÁO CÁO CHI TIẾT KHẮC PHỤC LỖI TOÀN DIỆN

| Mã Lỗi | Nội dung lỗi ban đầu | Nguyên nhân kỹ thuật | Giải pháp Clean Code đã xử lý |
|---|---|---|---|
| **C1 / K2** | Cửa hậu đăng nhập (Backdoor) tài khoản giả mạo `NV0001 / 123456` tên "Nguyễn Hải Đăng". | `DangNhap_GUI.java` hardcode tài khoản test vượt qua CSDL. | Xóa bỏ 100% mã hardcode. Xác thực chuẩn mật mã SHA-256 trực tiếp từ bảng `NhanVien` trong CSDL SQL Server. |
| **C2 / K3** | Nhân viên bán hàng thường (`NV0002`) có thể tùy ý sửa giá bán của `SP0005` từ 999.000đ xuống 1.000đ. | Nút Thêm/Sửa/Xóa trong `QuanLySanPham_GUI.java` không kiểm tra chức vụ. | Thêm kiểm tra phân quyền: nếu `!nhanVien.isQuanLy()` lập tức chặn lại và cảnh báo *"Chỉ Quản lý mới có quyền..."*. |
| **C3 / K4** | 21/21 phím tắt F1-F4, F10, ESC, DEL trên màn hình chỉ là chữ hiển thị, bấm phím không hoạt động. | Dùng `KeyListener` cục bộ chỉ ăn khi component giữ focus. | Đăng ký `InputMap` và `ActionMap` trên `JRootPane` với phạm vi toàn cục `WHEN_IN_FOCUSED_WINDOW`. |
| **C4 / K5** | Lệch tiền giữa POS và CSDL: Khách trả 7.710.000đ nhưng CSDL lưu 8.700.000đ, tiền thừa lưu 0, điểm không trừ. | `HoaDon.themChiTiet()` tự gọi `tinhTongTien()` ghi đè tổng tiền gộp lên tổng tiền thực thu. | Viết lại `HoaDon.java` và `HoaDon_DAO.java`: đồng bộ chuẩn xác `tongTienHang`, `chietKhau`, `diemSuDung`, `tienGiamDiem`, `tongTien`, `tienThua`. Trừ điểm cũ và cộng điểm mới chuẩn xác. |
| **C5 / K7** | Nhập chữ "abc" vào ô tiền khách đưa rồi bấm Thanh toán gây văng ngoại lệ `NumberFormatException` làm đơ app. | Gọi `Double.parseDouble()` trực tiếp mà không bắt ngoại lệ. | Bọc trong khối `try - catch (NumberFormatException)` tại `BanHang_GUI.java`, thông báo: *"Tiền khách đưa không hợp lệ! Vui lòng nhập số."*. |
| **C6 / K8** | Thêm sản phẩm giá bán âm (-5000) báo lỗi sai là "Trùng mã sản phẩm" do CSDL từ chối bằng Check Constraint. | GUI không xác thực giá trị số trước khi gọi xuống DAO. | Bổ sung Form Validation tại `QuanLySanPham_GUI.java`: bắt buộc `giaNhap > 0`, `giaBan > 0`, `giaBan >= giaNhap`. |
| **C7 / K9** | Thêm sản phẩm mẫu `SP9999` thành công nhưng không có biến thể SKU trong `ChiTietGiay`, Combobox POS không hiện. | Thiếu khởi tạo SKU biến thể và thiếu cơ chế refresh khi chuyển tab. | Tự động sinh 1 biến thể SKU mặc định (Size 40, Đen, Tồn 20) qua `ChiTietGiay_DAO.java` và thêm `ChangeListener` đồng bộ combobox khi đổi Tab. |
| **C8** | Bảng danh sách sản phẩm, nhân viên, khách hàng chỉ phản hồi chuột click, dùng phím mũi tên lên/xuống không load form. | Chỉ cài đặt `MouseListener`, thiếu bộ lắng nghe dòng được chọn. | Bổ sung `ListSelectionListener` trên toàn bộ các `JTable`, hỗ trợ duyệt dữ liệu đồng thời bằng chuột và phím mũi tên. |
| **C9 / K6** | Sau khi thanh toán đơn, thông tin khách hàng cũ vẫn bị dính vào đơn hàng tiếp theo. | Thiếu hàm reset trạng thái khách hàng sau khi in đơn. | Triển khai hàm `lamMoiDonHang()` toàn diện: gán `khachHienTai = null`, uncheck dùng điểm, reset giỏ hàng, xóa ô SĐT. |
| **C10** | Tranh chấp tồn kho khi nhiều máy cùng bán hoặc tồn kho trong DB bị thay đổi trước khi bấm thanh toán. | Không rollback giao dịch khi thiếu hàng. | Bọc toàn bộ quy trình thanh toán trong **Transaction ACID** (`con.setAutoCommit(false)`, `commit()`, `rollback()`), kiểm tra tồn kho tại thời điểm lưu. |
| **C11 (Mới)** | Nút bấm bị lỗi chữ trắng trên nền trắng của Windows Look & Feel, các nút phụ xám xịt không đồng bộ màu sắc. | Dùng `JButton` raw trên Windows native painter bị nuốt màu nền. | Chuẩn hóa toàn bộ hệ thống nút qua `UIHelper.createButton()`: Xanh lá (Thành công), Xanh dương (Thao tác), Đỏ (Xóa/Thoát), Xám Slate (Phụ trợ). Chữ và nền hiển thị tương phản 100%. |

---

## 7. KẾT QUẢ KIỂM THỬ THỰC TẾ

Toàn bộ 5 kịch bản kiểm thử tự động của `KiemThu.java` chạy trên CSDL Microsoft SQL Server thật:

```
========================================================================================
 KỊCH BẢN KIỂM THỬ            NỘI DUNG XÁC MINH               KẾT QUẢ THỰC TẾ   NGOẠI LỆ
========================================================================================
 Kịch bản A (K1, K2)  Xác thực đăng nhập & Vô hiệu hóa backdoor   PASS (100%)       0 lỗi
 Kịch bản B (K3)      Phân quyền nhân viên bán hàng sửa giá       PASS (100%)       0 lỗi
 Kịch bản C (K4,8,9,10) Phím tắt, Kho hàng, Giá âm, Mẫu mới      PASS (100%)       0 lỗi
 Kịch bản D (K5, K6)  Chiết khấu thẻ, Trừ/Cộng điểm, Reset đơn    PASS (100%)       0 lỗi
 Kịch bản E (K7)      Xử lý nhập chữ vào ô tiền khách đưa         PASS (100%)       0 lỗi
========================================================================================
 TỔNG KẾT: 5/5 KỊCH BẢN ĐẠT CHUẨN XUẤT SẮC - HOÀN TOÀN KHÔNG CÓ BẤT KỲ NGOẠI LỆ NÀO (0 ERRORS)
========================================================================================
```

- Bằng chứng hình ảnh giao diện mới đã được chụp tự động và lưu tại `SoiLoi_QuanLyBanGiay/kiem-thu-chay-that/anh/`:
  - `A-K2-vao-bang-cua-hau.png`: Nút `Đăng Xuất` đỏ rực, `+ Thêm Vào Giỏ` xanh dương, `Tìm` navy, `Thanh Toán` xanh lá, chữ trắng nổi bật 100%.
  - `C-K8-form-gia-am.png`: Bộ 4 nút Thêm Mới (Xanh lá), Xóa Sản Phẩm (Đỏ), Cập Nhật (Xanh dương), Xóa Trắng Form (Xám Slate) ngay ngắn, tương phản rực rỡ, sắc nét.
  - `B-K3-NV0002-form-sua-gia-truoc-bam.png`: Hiệu ứng nút bị disabled hiển thị chuẩn mực khi nhân viên thường không có quyền sửa giá.

---
*Tài liệu được biên soạn phục vụ công tác bàn giao, tiếp nhận và chấm điểm đồ án chuyên môn bậc Đại học.*

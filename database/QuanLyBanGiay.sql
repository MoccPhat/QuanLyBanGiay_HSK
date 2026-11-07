-- =========================================================================
-- KỊCH BẢN TẠO CƠ SỞ DỮ LIỆU: QUẢN LÝ BÁN HÀNG CỬA HÀNG GIÀY DÉP THỜI TRANG
-- DỰ ÁN: StepUp Footwear POS (IUH) - LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA
-- CẤU TRÚC: 6 BẢNG CHUẨN HOÁ 3NF, ĐỒNG BỘ 100% OOP ENTITY & CSDL THẬT
-- ĐẶC TẢ RÀNG BUỘC: 33 CHECK, 14 DEFAULT, 6 PK, 3 UNIQUE, 5 FK (NO ACTION)
-- AN TOÀN BẢO MẬT: MẬT KHẨU BĂM SHA-256 (64 KÝ TỰ HEX), TIỀN TỆ DECIMAL(18,0)
-- =========================================================================

USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'QuanLyBanGiay')
BEGIN
    ALTER DATABASE QuanLyBanGiay SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE QuanLyBanGiay;
END
GO

CREATE DATABASE QuanLyBanGiay;
GO

USE QuanLyBanGiay;
GO

-- =========================================================================
-- 1. BẢNG NHÂN VIÊN (Kế thừa Nguoi: chứa thông tin nhân thân + tài khoản + lương)
-- =========================================================================
CREATE TABLE NhanVien (
    maNhanVien VARCHAR(10) NOT NULL,
    hoTen NVARCHAR(50) NOT NULL,
    soDienThoai VARCHAR(10) NOT NULL,
    ngaySinh DATE NOT NULL,
    gioiTinh BIT NOT NULL,
    diaChi NVARCHAR(200) NULL,
    email VARCHAR(50) NULL,
    chucVu NVARCHAR(30) NOT NULL,
    luongCoBan DECIMAL(18,0) NOT NULL,
    caLamViec NVARCHAR(20) NULL,
    matKhau CHAR(64) NOT NULL,
    trangThai BIT NOT NULL CONSTRAINT DF_NhanVien_trangThai DEFAULT 1,
    CONSTRAINT PK_NhanVien PRIMARY KEY (maNhanVien),
    CONSTRAINT UQ_NhanVien_soDienThoai UNIQUE (soDienThoai),
    CONSTRAINT CK_NhanVien_ma CHECK (maNhanVien LIKE 'NV[0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_NhanVien_sdt CHECK (soDienThoai LIKE '0[35789][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_NhanVien_tuoi CHECK (ngaySinh <= DATEADD(year, -18, CONVERT(date, GETDATE()))),
    CONSTRAINT CK_NhanVien_chucVu CHECK (chucVu = N'Nhân viên bán hàng' OR chucVu = N'Quản lý'),
    CONSTRAINT CK_NhanVien_ca CHECK (caLamViec IS NULL OR (caLamViec = N'Toàn thời gian' OR caLamViec = N'Ca tối' OR caLamViec = N'Ca chiều' OR caLamViec = N'Ca sáng')),
    CONSTRAINT CK_NhanVien_email CHECK (email IS NULL OR email LIKE '%_@_%._%'),
    CONSTRAINT CK_NhanVien_luong CHECK (luongCoBan > 0),
    CONSTRAINT CK_NhanVien_matKhau CHECK (LEN(matKhau) = 64)
);
GO

-- =========================================================================
-- 2. BẢNG KHÁCH HÀNG (Kế thừa Nguoi: chứa thông tin nhân thân + tích điểm)
-- =========================================================================
CREATE TABLE KhachHang (
    maKhachHang VARCHAR(10) NOT NULL,
    hoTen NVARCHAR(50) NOT NULL,
    soDienThoai VARCHAR(10) NOT NULL,
    ngaySinh DATE NULL,
    gioiTinh BIT NULL CONSTRAINT DF_KhachHang_gioiTinh DEFAULT 1,
    diaChi NVARCHAR(200) NULL,
    email VARCHAR(50) NULL,
    diemTichLuy INT NOT NULL CONSTRAINT DF_KhachHang_diem DEFAULT 0,
    hangThanhVien NVARCHAR(20) NOT NULL CONSTRAINT DF_KhachHang_hang DEFAULT N'Đồng',
    CONSTRAINT PK_KhachHang PRIMARY KEY (maKhachHang),
    CONSTRAINT UQ_KhachHang_soDienThoai UNIQUE (soDienThoai),
    CONSTRAINT CK_KhachHang_ma CHECK (maKhachHang LIKE 'KH[0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_KhachHang_sdt CHECK (soDienThoai LIKE '0[35789][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_KhachHang_diem CHECK (diemTichLuy >= 0),
    CONSTRAINT CK_KhachHang_hang CHECK (hangThanhVien = N'Kim Cương' OR hangThanhVien = N'Vàng' OR hangThanhVien = N'Bạc' OR hangThanhVien = N'Đồng'),
    CONSTRAINT CK_KhachHang_email CHECK (email IS NULL OR email LIKE '%_@_%._%')
);
GO

-- =========================================================================
-- 3. BẢNG SẢN PHẨM (Mẫu giày thời trang tổng quát)
-- =========================================================================
CREATE TABLE SanPham (
    maSanPham VARCHAR(10) NOT NULL,
    tenSanPham NVARCHAR(100) NOT NULL,
    loaiGiay NVARCHAR(30) NOT NULL,
    thuongHieu NVARCHAR(50) NOT NULL,
    giaNhap DECIMAL(18,0) NOT NULL,
    giaBan DECIMAL(18,0) NOT NULL,
    chatLieu NVARCHAR(50) NULL,
    trangThai BIT NOT NULL CONSTRAINT DF_SanPham_trangThai DEFAULT 1,
    CONSTRAINT PK_SanPham PRIMARY KEY (maSanPham),
    CONSTRAINT CK_SanPham_ma CHECK (maSanPham LIKE 'SP[0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_SanPham_ten CHECK (LEN(LTRIM(RTRIM(tenSanPham))) > 0),
    CONSTRAINT CK_SanPham_giaNhap CHECK (giaNhap > 0),
    CONSTRAINT CK_SanPham_giaBan CHECK (giaBan >= giaNhap)
);
GO

-- =========================================================================
-- 4. BẢNG CHI TIẾT GIÀY (Biến thể SKU: Kích cỡ & Màu sắc - Bản sắc bài Giày dép)
-- =========================================================================
CREATE TABLE ChiTietGiay (
    maChiTietGiay VARCHAR(10) NOT NULL,
    maSanPham VARCHAR(10) NOT NULL,
    kichThuoc INT NOT NULL,
    mauSac NVARCHAR(30) NOT NULL,
    soLuongTon INT NOT NULL CONSTRAINT DF_ChiTietGiay_ton DEFAULT 0,
    hinhAnh VARCHAR(200) NULL CONSTRAINT DF_ChiTietGiay_anh DEFAULT 'default_shoe.png',
    CONSTRAINT PK_ChiTietGiay PRIMARY KEY (maChiTietGiay),
    CONSTRAINT UQ_ChiTietGiay_BienThe UNIQUE (maSanPham, kichThuoc, mauSac),
    CONSTRAINT FK_ChiTietGiay_SanPham FOREIGN KEY (maSanPham) REFERENCES SanPham(maSanPham) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_ChiTietGiay_ma CHECK (maChiTietGiay LIKE 'CTG[0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_ChiTietGiay_size CHECK (kichThuoc >= 35 AND kichThuoc <= 45),
    CONSTRAINT CK_ChiTietGiay_ton CHECK (soLuongTon >= 0)
);
GO

-- =========================================================================
-- 5. BẢNG HÓA ĐƠN (Giao dịch bán hàng tại quầy POS - 13 cột tài chính)
-- =========================================================================
CREATE TABLE HoaDon (
    maHoaDon VARCHAR(10) NOT NULL,
    ngayLap DATETIME NOT NULL CONSTRAINT DF_HoaDon_ngayLap DEFAULT GETDATE(),
    maNhanVien VARCHAR(10) NOT NULL,
    maKhachHang VARCHAR(10) NULL,
    tongTienHang DECIMAL(18,0) NOT NULL,
    chietKhau DECIMAL(18,0) NOT NULL CONSTRAINT DF_HoaDon_chietKhau DEFAULT 0,
    diemSuDung INT NOT NULL CONSTRAINT DF_HoaDon_diemSuDung DEFAULT 0,
    tienGiamDiem DECIMAL(18,0) NOT NULL CONSTRAINT DF_HoaDon_tienGiamDiem DEFAULT 0,
    tongTien DECIMAL(18,0) NOT NULL,
    phuongThucTT NVARCHAR(30) NOT NULL CONSTRAINT DF_HoaDon_pttt DEFAULT N'Tiền mặt',
    tienKhachDua DECIMAL(18,0) NOT NULL,
    tienThua DECIMAL(18,0) NOT NULL,
    diemCong INT NOT NULL CONSTRAINT DF_HoaDon_diemCong DEFAULT 0,
    CONSTRAINT PK_HoaDon PRIMARY KEY (maHoaDon),
    CONSTRAINT FK_HoaDon_NhanVien FOREIGN KEY (maNhanVien) REFERENCES NhanVien(maNhanVien) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_HoaDon_KhachHang FOREIGN KEY (maKhachHang) REFERENCES KhachHang(maKhachHang) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_HoaDon_ma CHECK (maHoaDon LIKE 'HD[0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_HoaDon_pttt CHECK (phuongThucTT = N'Chuyển khoản QR' OR phuongThucTT = N'Tiền mặt'),
    CONSTRAINT CK_HoaDon_soAm CHECK (tongTienHang >= 0 AND chietKhau >= 0 AND diemSuDung >= 0 AND tienGiamDiem >= 0 AND diemCong >= 0),
    CONSTRAINT CK_HoaDon_tongTien CHECK (tongTien = (tongTienHang - chietKhau) - tienGiamDiem AND tongTien >= 0),
    CONSTRAINT CK_HoaDon_tienDiem CHECK (tienGiamDiem = diemSuDung * 1000),
    CONSTRAINT CK_HoaDon_tienDua CHECK (tienKhachDua >= tongTien),
    CONSTRAINT CK_HoaDon_tienThua CHECK (tienThua = tienKhachDua - tongTien),
    CONSTRAINT CK_HoaDon_chuyenKhoan CHECK (phuongThucTT <> N'Chuyển khoản QR' OR tienKhachDua = tongTien),
    CONSTRAINT CK_HoaDon_diemKhach CHECK (maKhachHang IS NOT NULL OR (diemSuDung = 0 AND diemCong = 0 AND chietKhau = 0))
);
GO

-- =========================================================================
-- 6. BẢNG CHI TIẾT HÓA ĐƠN (Từng đôi giày cụ thể theo biến thể được xuất bán)
-- =========================================================================
CREATE TABLE ChiTietHoaDon (
    maHoaDon VARCHAR(10) NOT NULL,
    maChiTietGiay VARCHAR(10) NOT NULL,
    soLuong INT NOT NULL,
    donGia DECIMAL(18,0) NOT NULL,
    giamGia DECIMAL(18,0) NOT NULL CONSTRAINT DF_ChiTietHoaDon_giamGia DEFAULT 0,
    thanhTien DECIMAL(18,0) NOT NULL,
    CONSTRAINT PK_ChiTietHoaDon PRIMARY KEY (maHoaDon, maChiTietGiay),
    CONSTRAINT FK_ChiTietHoaDon_HoaDon FOREIGN KEY (maHoaDon) REFERENCES HoaDon(maHoaDon) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_ChiTietHoaDon_ChiTietGiay FOREIGN KEY (maChiTietGiay) REFERENCES ChiTietGiay(maChiTietGiay) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_ChiTietHoaDon_soLuong CHECK (soLuong > 0),
    CONSTRAINT CK_ChiTietHoaDon_donGia CHECK (donGia > 0),
    CONSTRAINT CK_ChiTietHoaDon_giamGia CHECK (giamGia >= 0 AND giamGia <= soLuong * donGia),
    CONSTRAINT CK_ChiTietHoaDon_thanhTien CHECK (thanhTien = soLuong * donGia - giamGia)
);
GO

-- =========================================================================
-- DỮ LIỆU MẪU BAN ĐẦU (SEED DATA TRÍCH XUẤT TỪ CƠ SỞ DỮ LIỆU THẬT)
-- MẬT KHẨU NHÂN VIÊN: BĂM SHA-256 CỦA "123456" (8d969eef...6c92)
-- =========================================================================

-- 1. Thêm Nhân viên (4 thành viên ban đầu, Mật khẩu đã băm SHA-256)
INSERT INTO NhanVien (maNhanVien, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, chucVu, luongCoBan, caLamViec, matKhau, trangThai)
VALUES 
('NV0001', N'Nguyễn Trọng Vinh', '0912345678', '2004-05-12', 1, N'12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM', 'trongvinh@stepup.vn', N'Quản lý', 12000000, N'Toàn thời gian', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1),
('NV0002', N'Nhiêu Minh Kỳ', '0987654321', '2004-08-20', 1, N'45 Lê Đức Thọ, Gò Vấp, TP.HCM', 'minhky@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca sáng', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1),
('NV0003', N'Trần Tấn Kiệt', '0903123456', '2004-11-03', 1, N'78 Quang Trung, Gò Vấp, TP.HCM', 'tankiet@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca chiều', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1),
('NV0004', N'Trần Mộc Tấn Phát', '0933456789', '2004-02-18', 1, N'102 Phan Văn Trị, Gò Vấp, TP.HCM', 'tanphat@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca tối', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1);
GO

-- 2. Thêm Khách hàng mẫu
INSERT INTO KhachHang (maKhachHang, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, diemTichLuy, hangThanhVien)
VALUES
('KH0001', N'Phạm Minh Tuấn', '0938111222', '1998-03-15', 1, N'Quận 12, TP.HCM', 'tuanpm@gmail.com', 45, N'Bạc'),
('KH0002', N'Hoàng Thu Trang', '0977333444', '2001-09-22', 0, N'Bình Thạnh, TP.HCM', 'tranght@gmail.com', 120, N'Vàng'),
('KH0003', N'Ngô Văn Long', '0966555666', '1995-12-05', 1, N'Tân Bình, TP.HCM', 'longnv@gmail.com', 10, N'Đồng');
GO

-- 3. Thêm Sản phẩm giày dép
INSERT INTO SanPham (maSanPham, tenSanPham, loaiGiay, thuongHieu, giaNhap, giaBan, chatLieu, trangThai)
VALUES
('SP0001', N'Nike Air Force 1 07 Low', N'Sneaker', N'Nike', 1800000, 2600000, N'Da thật cao cấp', 1),
('SP0002', N'Adidas Ultraboost Light 23', N'Chạy bộ', N'Adidas', 2400000, 3500000, N'Vải dệt Primeknit', 1),
('SP0003', N'Vans Old Skool Classic', N'Sneaker', N'Vans', 1100000, 1750000, N'Vải Canvas & Da lộn', 1),
('SP0004', N'Converse Chuck Taylor 1970s', N'Sneaker', N'Converse', 1200000, 1900000, N'Vải Canvas dày dặn', 1),
('SP0005', N'Biti''s Hunter Street Vintage', N'Sneaker', N'Biti''s', 650000, 999000, N'Da tổng hợp & Vải lưới', 1);
GO

-- 4. Thêm Chi tiết biến thể giày (Size & Màu sắc & Tồn kho thực tế)
INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh)
VALUES
('CTG0001', 'SP0001', 39, N'Trắng', 15, 'nike_af1_white.png'),
('CTG0002', 'SP0001', 40, N'Trắng', 17, 'nike_af1_white.png'),
('CTG0003', 'SP0001', 41, N'Trắng', 18, 'nike_af1_white.png'),
('CTG0004', 'SP0001', 42, N'Trắng', 12, 'nike_af1_white.png'),
('CTG0005', 'SP0001', 40, N'Đen', 8, 'nike_af1_black.png'),
('CTG0006', 'SP0002', 40, N'Đen Phối Trắng', 10, 'ub_black.png'),
('CTG0007', 'SP0002', 41, N'Đen Phối Trắng', 14, 'ub_black.png'),
('CTG0008', 'SP0002', 42, N'Xám Khói', 9, 'ub_grey.png'),
('CTG0009', 'SP0003', 38, N'Đen Sọc Trắng', 15, 'vans_black.png'),
('CTG0010', 'SP0003', 39, N'Đen Sọc Trắng', 22, 'vans_black.png'),
('CTG0011', 'SP0003', 40, N'Đen Sọc Trắng', 20, 'vans_black.png'),
('CTG0012', 'SP0004', 39, N'Vàng Parchment', 10, 'conv_yellow.png'),
('CTG0013', 'SP0004', 40, N'Đen Cổ Cao', 17, 'conv_black.png'),
('CTG0014', 'SP0005', 40, N'Xám Phối Cam', 30, 'hunter_grey.png'),
('CTG0015', 'SP0005', 41, N'Xám Phối Cam', 28, 'hunter_grey.png');
GO

-- 5. Thêm Hóa đơn mẫu thực tế (2 đơn hàng chuẩn, đủ 13 cột)
INSERT INTO HoaDon (maHoaDon, ngayLap, maNhanVien, maKhachHang, tongTienHang, chietKhau, diemSuDung, tienGiamDiem, tongTien, phuongThucTT, tienKhachDua, tienThua, diemCong)
VALUES
('HD000001', '2026-11-01 10:15:00', 'NV0002', 'KH0001', 2600000, 130000, 0, 0, 2470000, N'Tiền mặt', 2500000, 30000, 24),
('HD000002', '2026-11-02 15:45:00', 'NV0003', 'KH0002', 3500000, 350000, 0, 0, 3150000, N'Chuyển khoản QR', 3150000, 0, 31);
GO

-- 6. Thêm Chi tiết hóa đơn
INSERT INTO ChiTietHoaDon (maHoaDon, maChiTietGiay, soLuong, donGia, giamGia, thanhTien)
VALUES
('HD000001', 'CTG0002', 1, 2600000, 0, 2600000),
('HD000002', 'CTG0007', 1, 3500000, 0, 3500000);
GO

PRINT N'Khởi tạo Cơ sở dữ liệu QuanLyBanGiay thành công 100%!';
GO

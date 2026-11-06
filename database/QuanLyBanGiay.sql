-- =========================================================================
-- KỊCH BẢN TẠO CƠ SỞ DỮ LIỆU: QUẢN LÝ BÁN HÀNG CỬA HÀNG GIÀY DÉP THỜI TRANG
-- MÔN: LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA (IUH)
-- CẤU TRÚC 6 BẢNG ĐỒNG BỘ 100% VỚI CÁC OBJECT ENTITY OOP
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

-- 1. BẢNG NHÂN VIÊN (Kế thừa Nguoi: chứa thông tin nhân thân + tài khoản + lương)
CREATE TABLE NhanVien (
    maNhanVien VARCHAR(10) PRIMARY KEY,
    hoTen NVARCHAR(50) NOT NULL,
    soDienThoai VARCHAR(15) NOT NULL,
    ngaySinh DATE NOT NULL,
    gioiTinh BIT NOT NULL, -- 1: Nam, 0: Nữ
    diaChi NVARCHAR(200),
    email VARCHAR(50),
    chucVu NVARCHAR(30) NOT NULL, -- 'Quản lý', 'Nhân viên bán hàng'
    luongCoBan FLOAT NOT NULL CHECK (luongCoBan >= 0),
    caLamViec NVARCHAR(20), -- 'Ca sáng', 'Ca chiều', 'Ca tối'
    matKhau VARCHAR(50) NOT NULL DEFAULT '123456',
    trangThai BIT NOT NULL DEFAULT 1 -- 1: Đang làm, 0: Đã nghỉ
);
GO

-- 2. BẢNG KHÁCH HÀNG (Kế thừa Nguoi: chứa thông tin nhân thân + tích điểm)
CREATE TABLE KhachHang (
    maKhachHang VARCHAR(10) PRIMARY KEY,
    hoTen NVARCHAR(50) NOT NULL,
    soDienThoai VARCHAR(15) NOT NULL UNIQUE,
    ngaySinh DATE,
    gioiTinh BIT DEFAULT 1,
    diaChi NVARCHAR(200),
    email VARCHAR(50),
    diemTichLuy INT NOT NULL DEFAULT 0 CHECK (diemTichLuy >= 0),
    hangThanhVien NVARCHAR(20) NOT NULL DEFAULT N'Đồng' -- 'Đồng', 'Bạc', 'Vàng', 'Kim Cương'
);
GO

-- 3. BẢNG SẢN PHẨM (Mẫu giày thời trang tổng quát)
CREATE TABLE SanPham (
    maSanPham VARCHAR(10) PRIMARY KEY,
    tenSanPham NVARCHAR(100) NOT NULL,
    loaiGiay NVARCHAR(30) NOT NULL, -- 'Sneaker', 'Sandal', 'Giày Da', 'Chạy bộ'
    thuongHieu NVARCHAR(50) NOT NULL, -- 'Nike', 'Adidas', 'Converse', 'Vans', 'Biti''s'
    giaNhap FLOAT NOT NULL CHECK (giaNhap > 0),
    giaBan FLOAT NOT NULL CHECK (giaBan > 0),
    chatLieu NVARCHAR(50), -- 'Vải Canvas', 'Da thật', 'Da PU', 'Lưới thoáng khí'
    trangThai BIT NOT NULL DEFAULT 1 -- 1: Đang kinh doanh, 0: Ngừng kinh doanh
);
GO

-- 4. BẢNG CHI TIẾT GIÀY (Biến thể SKU: Kích cỡ & Màu sắc - Bản sắc bài Giày dép)
CREATE TABLE ChiTietGiay (
    maChiTietGiay VARCHAR(10) PRIMARY KEY,
    maSanPham VARCHAR(10) NOT NULL REFERENCES SanPham(maSanPham) ON DELETE CASCADE,
    kichThuoc INT NOT NULL CHECK (kichThuoc BETWEEN 35 AND 45),
    mauSac NVARCHAR(30) NOT NULL,
    soLuongTon INT NOT NULL DEFAULT 0 CHECK (soLuongTon >= 0),
    hinhAnh NVARCHAR(200) DEFAULT 'default_shoe.png',
    CONSTRAINT UQ_BienThe UNIQUE (maSanPham, kichThuoc, mauSac)
);
GO

-- 5. BẢNG HÓA ĐƠN (Giao dịch bán hàng tại quầy POS)
CREATE TABLE HoaDon (
    maHoaDon VARCHAR(10) PRIMARY KEY,
    ngayLap DATETIME NOT NULL DEFAULT GETDATE(),
    maNhanVien VARCHAR(10) NOT NULL REFERENCES NhanVien(maNhanVien),
    maKhachHang VARCHAR(10) REFERENCES KhachHang(maKhachHang),
    tongTien FLOAT NOT NULL DEFAULT 0 CHECK (tongTien >= 0),
    phuongThucTT NVARCHAR(30) NOT NULL DEFAULT N'Tiền mặt', -- 'Tiền mặt', 'Chuyển khoản'
    tienKhachDua FLOAT NOT NULL DEFAULT 0,
    tienThua FLOAT NOT NULL DEFAULT 0
);
GO

-- 6. BẢNG CHI TIẾT HÓA ĐƠN (Từng đôi giày cụ thể theo size/màu được xuất bán)
CREATE TABLE ChiTietHoaDon (
    maHoaDon VARCHAR(10) NOT NULL REFERENCES HoaDon(maHoaDon) ON DELETE CASCADE,
    maChiTietGiay VARCHAR(10) NOT NULL REFERENCES ChiTietGiay(maChiTietGiay),
    soLuong INT NOT NULL CHECK (soLuong > 0),
    donGia FLOAT NOT NULL CHECK (donGia >= 0),
    giamGia FLOAT NOT NULL DEFAULT 0 CHECK (giamGia >= 0),
    thanhTien FLOAT NOT NULL CHECK (thanhTien >= 0),
    PRIMARY KEY (maHoaDon, maChiTietGiay)
);
GO

-- =========================================================================
-- DỮ LIỆU MẪU BAN ĐẦU (SEED DATA THỰC TẾ)
-- =========================================================================

-- Thêm Nhân viên (4 thành viên trong nhóm, Mật khẩu mặc định: 123456)
INSERT INTO NhanVien (maNhanVien, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, chucVu, luongCoBan, caLamViec, matKhau, trangThai)
VALUES 
('NV0001', N'Nguyễn Trọng Vinh', '0912345678', '2004-05-12', 1, N'12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM', 'trongvinh@stepup.vn', N'Quản lý', 12000000, N'Toàn thời gian', '123456', 1),
('NV0002', N'Nhiêu Minh Kỳ', '0987654321', '2004-08-20', 1, N'45 Lê Đức Thọ, Gò Vấp, TP.HCM', 'minhky@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca sáng', '123456', 1),
('NV0003', N'Trần Tấn Kiệt', '0903123456', '2004-11-03', 1, N'78 Quang Trung, Gò Vấp, TP.HCM', 'tankiet@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca chiều', '123456', 1),
('NV0004', N'Trần Mộc Tấn Phát', '0933456789', '2004-02-18', 1, N'102 Phan Văn Trị, Gò Vấp, TP.HCM', 'tanphat@stepup.vn', N'Nhân viên bán hàng', 6500000, N'Ca tối', '123456', 1);
GO

-- Thêm Khách hàng
INSERT INTO KhachHang (maKhachHang, hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email, diemTichLuy, hangThanhVien)
VALUES
('KH0001', N'Phạm Minh Tuấn', '0938111222', '1998-03-15', 1, N'Quận 12, TP.HCM', 'tuanpm@gmail.com', 45, N'Bạc'),
('KH0002', N'Hoàng Thu Trang', '0977333444', '2001-09-22', 0, N'Bình Thạnh, TP.HCM', 'tranght@gmail.com', 120, N'Vàng'),
('KH0003', N'Ngô Văn Long', '0966555666', '1995-12-05', 1, N'Tân Bình, TP.HCM', 'longnv@gmail.com', 10, N'Đồng');
GO

-- Thêm Sản phẩm giày dép
INSERT INTO SanPham (maSanPham, tenSanPham, loaiGiay, thuongHieu, giaNhap, giaBan, chatLieu, trangThai)
VALUES
('SP0001', N'Nike Air Force 1 07 Low', N'Sneaker', N'Nike', 1800000, 2600000, N'Da thật cao cấp', 1),
('SP0002', N'Adidas Ultraboost Light 23', N'Chạy bộ', N'Adidas', 2400000, 3500000, N'Vải dệt Primeknit', 1),
('SP0003', N'Vans Old Skool Classic', N'Sneaker', N'Vans', 1100000, 1750000, N'Vải Canvas & Da lộn', 1),
('SP0004', N'Converse Chuck Taylor 1970s', N'Sneaker', N'Converse', 1200000, 1900000, N'Vải Canvas dày dặn', 1),
('SP0005', N'Biti''s Hunter Street Vintage', N'Sneaker', N'Biti''s', 650000, 999000, N'Da tổng hợp & Vải lưới', 1);
GO

-- Thêm Chi tiết biến thể giày (Size & Màu sắc & Tồn kho)
INSERT INTO ChiTietGiay (maChiTietGiay, maSanPham, kichThuoc, mauSac, soLuongTon, hinhAnh)
VALUES
-- Nike Air Force 1
('CTG0001', 'SP0001', 39, N'Trắng', 15, 'nike_af1_white.png'),
('CTG0002', 'SP0001', 40, N'Trắng', 20, 'nike_af1_white.png'),
('CTG0003', 'SP0001', 41, N'Trắng', 18, 'nike_af1_white.png'),
('CTG0004', 'SP0001', 42, N'Trắng', 12, 'nike_af1_white.png'),
('CTG0005', 'SP0001', 40, N'Đen', 8, 'nike_af1_black.png'),
-- Adidas Ultraboost
('CTG0006', 'SP0002', 40, N'Đen Phối Trắng', 10, 'ub_black.png'),
('CTG0007', 'SP0002', 41, N'Đen Phối Trắng', 14, 'ub_black.png'),
('CTG0008', 'SP0002', 42, N'Xám Khói', 9, 'ub_grey.png'),
-- Vans Old Skool
('CTG0009', 'SP0003', 38, N'Đen Sọc Trắng', 16, 'vans_black.png'),
('CTG0010', 'SP0003', 39, N'Đen Sọc Trắng', 22, 'vans_black.png'),
('CTG0011', 'SP0003', 40, N'Đen Sọc Trắng', 25, 'vans_black.png'),
-- Converse 1970s
('CTG0012', 'SP0004', 39, N'Vàng Parchment', 11, 'conv_yellow.png'),
('CTG0013', 'SP0004', 40, N'Đen Cổ Cao', 17, 'conv_black.png'),
-- Biti's Hunter
('CTG0014', 'SP0005', 40, N'Xám Phối Cam', 30, 'hunter_grey.png'),
('CTG0015', 'SP0005', 41, N'Xám Phối Cam', 28, 'hunter_grey.png');
GO

-- Thêm Hóa đơn mẫu ban đầu
INSERT INTO HoaDon (maHoaDon, ngayLap, maNhanVien, maKhachHang, tongTien, phuongThucTT, tienKhachDua, tienThua)
VALUES
('HD0001', '2026-11-01 10:15:00', 'NV0002', 'KH0001', 2600000, N'Tiền mặt', 3000000, 400000),
('HD0002', '2026-11-02 15:45:00', 'NV0003', 'KH0002', 3500000, N'Chuyển khoản', 3500000, 0);
GO

-- Thêm Chi tiết hóa đơn
INSERT INTO ChiTietHoaDon (maHoaDon, maChiTietGiay, soLuong, donGia, giamGia, thanhTien)
VALUES
('HD0001', 'CTG0002', 1, 2600000, 0, 2600000),
('HD0002', 'CTG0007', 1, 3500000, 0, 3500000);
GO

PRINT N'Khởi tạo Cơ sở dữ liệu QuanLyBanGiay thành công 100%!';
GO

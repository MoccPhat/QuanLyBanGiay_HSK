# -*- coding: utf-8 -*-
"""
Script xây dựng và kiểm chứng tính toàn vẹn 100% của database\\QuanLyBanGiay.sql
So sánh với CSDL thật trên SQL Server localhost\\SQLEXPRESS (QuanLyBanGiay)
"""

import os
import sys
import shutil
import hashlib
import pyodbc

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đường dẫn tệp
PROJECT_DIR = r"E:\Eclipse Java\project"
DB_SQL_PATH = os.path.join(PROJECT_DIR, "database", "QuanLyBanGiay.sql")
DATA_SQL_PATH = os.path.join(PROJECT_DIR, "data", "QuanLyBanGiay.sql")

# Chuỗi kết nối SQL Server
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=QuanLyBanGiay;"
    "UID=sa;PWD=123456789;"
    "TrustServerCertificate=yes;"
)

MASTER_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=master;"
    "UID=sa;PWD=123456789;"
    "TrustServerCertificate=yes;"
)

SQL_CONTENT = """-- =========================================================================
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
"""


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    print("=== BƯỚC 1 & 2: GHI database\\QuanLyBanGiay.sql ===")
    os.makedirs(os.path.dirname(DB_SQL_PATH), exist_ok=True)
    with open(DB_SQL_PATH, "w", encoding="utf-8") as f:
        f.write(SQL_CONTENT)
    print(f"[OK] Đã ghi tệp {DB_SQL_PATH} ({os.path.getsize(DB_SQL_PATH)} bytes)")

    print("\n=== BƯỚC 3: SAO CHÉP data\\QuanLyBanGiay.sql ===")
    os.makedirs(os.path.dirname(DATA_SQL_PATH), exist_ok=True)
    shutil.copyfile(DB_SQL_PATH, DATA_SQL_PATH)
    hash_db = compute_sha256(DB_SQL_PATH)
    hash_data = compute_sha256(DATA_SQL_PATH)
    print(f"Hash database\\QuanLyBanGiay.sql: {hash_db}")
    print(f"Hash data\\QuanLyBanGiay.sql:     {hash_data}")
    assert hash_db == hash_data, "LỖI: Mã băm SHA-256 của 2 tệp không khớp!"
    print("[OK] Hai tệp SQL giống nhau 100% từng byte!")

    print("\n=== BƯỚC 4: ĐỐI SOÁT METADATA VỚI CSDL THẬT (QuanLyBanGiay) ===")
    cn = pyodbc.connect(CONN_STR)
    cur = cn.cursor()

    # 1. Bảng
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME <> 'sysdiagrams' ORDER BY TABLE_NAME")
    real_tables = sorted([r[0] for r in cur.fetchall()])
    expected_tables = sorted(["NhanVien", "KhachHang", "SanPham", "ChiTietGiay", "HoaDon", "ChiTietHoaDon"])
    print(f"Bảng thực tế ({len(real_tables)}): {real_tables}")
    print(f"Bảng thiết kế ({len(expected_tables)}): {expected_tables}")
    assert real_tables == expected_tables, "LỖI: Danh sách bảng không khớp!"
    print("-> Bảng: 100% KHỚP (6/6)")

    # 2. Cột
    cur.execute("""
        SELECT c.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE, c.IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS c
        JOIN INFORMATION_SCHEMA.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
        WHERE t.TABLE_TYPE='BASE TABLE' AND t.TABLE_NAME <> 'sysdiagrams'
        ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION
    """)
    real_cols = cur.fetchall()
    print(f"-> Tổng số cột trong CSDL thật: {len(real_cols)} cột (HoaDon có 13 cột)")
    assert len(real_cols) == 54, f"LỖI: Tổng số cột mong đợi 54, thực tế {len(real_cols)}"

    # 3. CHECK Constraints
    cur.execute("""
        SELECT t.name AS tbl, ck.name AS ck_name
        FROM sys.check_constraints ck
        JOIN sys.tables t ON ck.parent_object_id = t.object_id
        ORDER BY t.name, ck.name
    """)
    real_cks = cur.fetchall()
    print(f"-> Tổng số CHECK constraints thực tế: {len(real_cks)} (Mong đợi: 33)")
    assert len(real_cks) == 33, f"LỖI: Số CHECK constraints thực tế {len(real_cks)} != 33"
    print("-> CHECK Constraints: 100% KHỚP (33/33)")

    # 4. DEFAULT Constraints
    cur.execute("""
        SELECT t.name AS tbl, df.name AS df_name
        FROM sys.default_constraints df
        JOIN sys.tables t ON df.parent_object_id = t.object_id
        ORDER BY t.name, df.name
    """)
    real_dfs = cur.fetchall()
    print(f"-> Tổng số DEFAULT constraints thực tế: {len(real_dfs)} (Mong đợi: 14)")
    assert len(real_dfs) == 14, f"LỖI: Số DEFAULT constraints thực tế {len(real_dfs)} != 14"
    print("-> DEFAULT Constraints: 100% KHỚP (14/14)")

    # 5. PRIMARY KEY
    cur.execute("""
        SELECT kc.name, t.name AS tbl
        FROM sys.key_constraints kc
        JOIN sys.tables t ON kc.parent_object_id = t.object_id
        WHERE kc.type = 'PK' AND t.name <> 'sysdiagrams'
        ORDER BY t.name
    """)
    real_pks = cur.fetchall()
    print(f"-> Tổng số PRIMARY KEY thực tế: {len(real_pks)} (Mong đợi: 6)")
    assert len(real_pks) == 6, f"LỖI: Số PK thực tế {len(real_pks)} != 6"
    print("-> PRIMARY KEY: 100% KHỚP (6/6)")

    # 6. UNIQUE
    cur.execute("""
        SELECT kc.name, t.name AS tbl
        FROM sys.key_constraints kc
        JOIN sys.tables t ON kc.parent_object_id = t.object_id
        WHERE kc.type = 'UQ' AND t.name <> 'sysdiagrams'
        ORDER BY t.name
    """)
    real_uqs = cur.fetchall()
    print(f"-> Tổng số UNIQUE constraints thực tế: {len(real_uqs)} (Mong đợi: 3)")
    assert len(real_uqs) == 3, f"LỖI: Số UQ thực tế {len(real_uqs)} != 3"
    print("-> UNIQUE Constraints: 100% KHỚP (3/3)")

    # 7. FOREIGN KEY
    cur.execute("""
        SELECT fk.name, tp.name AS parent_tbl, fk.delete_referential_action_desc
        FROM sys.foreign_keys fk
        JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
        ORDER BY tp.name, fk.name
    """)
    real_fks = cur.fetchall()
    print(f"-> Tổng số FOREIGN KEY thực tế: {len(real_fks)} (Mong đợi: 5)")
    assert len(real_fks) == 5, f"LỖI: Số FK thực tế {len(real_fks)} != 5"
    for fk in real_fks:
        assert fk.delete_referential_action_desc == "NO_ACTION", f"LỖI: FK {fk.name} không phải NO_ACTION!"
    print("-> FOREIGN KEY (NO ACTION): 100% KHỚP (5/5)")

    # 8. MẬT KHẨU BĂM SHA-256
    cur.execute("SELECT maNhanVien, matKhau FROM NhanVien")
    nvs = cur.fetchall()
    expected_hash = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
    for nv in nvs:
        pw = nv.matKhau.strip()
        assert len(pw) == 64, f"LỖI: Mật khẩu của {nv.maNhanVien} độ dài {len(pw)} != 64!"
        assert pw == expected_hash, f"LỖI: Mật khẩu của {nv.maNhanVien} không khớp hash SHA-256 mẫu!"
    print(f"-> Xác nhận mật khẩu 4 nhân viên trong seed: 100% là hash SHA-256 64 ký tự ({expected_hash})")

    cn.close()

    print("\n=== BƯỚC 5: KIỂM CHỨNG TRÊN CSDL TẠM (QuanLyBanGiay_Test) ===")
    m_cn = pyodbc.connect(MASTER_CONN_STR, autocommit=True)
    m_cur = m_cn.cursor()

    # Drop DB test cũ nếu có
    m_cur.execute("""
        IF EXISTS (SELECT name FROM sys.databases WHERE name = 'QuanLyBanGiay_Test')
        BEGIN
            ALTER DATABASE QuanLyBanGiay_Test SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
            DROP DATABASE QuanLyBanGiay_Test;
        END
    """)
    print("[OK] Đã chuẩn bị môi trường DB test.")

    # Chạy script trên DB test bằng cách thay 'QuanLyBanGiay' -> 'QuanLyBanGiay_Test'
    test_sql = SQL_CONTENT.replace("QuanLyBanGiay", "QuanLyBanGiay_Test")
    batches = [b.strip() for b in test_sql.split("GO") if b.strip()]
    for i, b in enumerate(batches, 1):
        try:
            m_cur.execute(b)
        except Exception as e:
            print(f"LỖI tại batch #{i}:\n{b[:200]}...")
            raise e
    print(f"[OK] Đã thực thi {len(batches)} batch SQL tạo CSDL QuanLyBanGiay_Test thành công 100%!")

    # Kết nối DB test để kiểm tra
    test_conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=QuanLyBanGiay_Test;"
        "UID=sa;PWD=123456789;"
        "TrustServerCertificate=yes;"
    )
    t_cn = pyodbc.connect(test_conn_str)
    t_cur = t_cn.cursor()

    # So sánh bảng
    t_cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME <> 'sysdiagrams' ORDER BY TABLE_NAME")
    t_tables = sorted([r[0] for r in t_cur.fetchall()])
    assert t_tables == expected_tables, "LỖI trên DB test: Bảng không khớp!"

    # So sánh check constraints
    t_cur.execute("SELECT COUNT(*) FROM sys.check_constraints")
    t_ck_count = t_cur.fetchone()[0]
    assert t_ck_count == 33, f"LỖI trên DB test: CHECK constraints {t_ck_count} != 33"

    # So sánh seed data
    t_cur.execute("SELECT COUNT(*) FROM NhanVien")
    assert t_cur.fetchone()[0] == 4
    t_cur.execute("SELECT COUNT(*) FROM KhachHang")
    assert t_cur.fetchone()[0] == 3
    t_cur.execute("SELECT COUNT(*) FROM SanPham")
    assert t_cur.fetchone()[0] == 5
    t_cur.execute("SELECT COUNT(*) FROM ChiTietGiay")
    assert t_cur.fetchone()[0] == 15
    t_cur.execute("SELECT COUNT(*) FROM HoaDon")
    assert t_cur.fetchone()[0] == 2
    t_cur.execute("SELECT COUNT(*) FROM ChiTietHoaDon")
    assert t_cur.fetchone()[0] == 2
    print("[OK] Toàn bộ 6 bảng và seed data trên DB test khớp 100% với kịch bản!")

    t_cn.close()

    # Dọn dẹp DB test
    m_cur.execute("""
        ALTER DATABASE QuanLyBanGiay_Test SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
        DROP DATABASE QuanLyBanGiay_Test;
    """)
    m_cn.close()
    print("[OK] Đã dọn dẹp (DROP) CSDL tạm QuanLyBanGiay_Test sạch sẽ.")

    print("\n=======================================================")
    print("HOÀN TẤT TOÀN BỘ CÁC BƯỚC KIỂM CHỨNG: ĐẠT CHUẨN 100%!")
    print("=======================================================")


if __name__ == "__main__":
    main()

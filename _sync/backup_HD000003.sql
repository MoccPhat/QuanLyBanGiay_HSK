-- =========================================================================
-- FILE BACKUP HÓA ĐƠN RÁC HD000003 ĐỂ KHÔI PHỤC KHI CẦN THIẾT
-- NGÀY TẠO BACKUP: 2026-11-08
-- DỰ ÁN: StepUp Footwear POS (QuanLyBanGiay)
-- =========================================================================

USE QuanLyBanGiay;
GO

-- 1. Khôi phục bảng HoaDon (13 cột chuẩn)
IF NOT EXISTS (SELECT 1 FROM HoaDon WHERE maHoaDon = 'HD000003')
BEGIN
    INSERT INTO HoaDon (
        maHoaDon, ngayLap, maNhanVien, maKhachHang, 
        tongTienHang, chietKhau, diemSuDung, tienGiamDiem, 
        tongTien, phuongThucTT, tienKhachDua, tienThua, diemCong
    ) VALUES (
        'HD000003', 
        '2026-11-06 22:46:58.147', 
        'NV0001', 
        NULL, 
        8750000, 
        0, 
        0, 
        0, 
        8750000, 
        N'Tiền mặt', 
        900000000, 
        891250000, 
        0
    );
END
GO

-- 2. Khôi phục bảng ChiTietHoaDon
IF NOT EXISTS (SELECT 1 FROM ChiTietHoaDon WHERE maHoaDon = 'HD000003' AND maChiTietGiay = 'CTG0011')
BEGIN
    INSERT INTO ChiTietHoaDon (
        maHoaDon, maChiTietGiay, soLuong, donGia, giamGia, thanhTien
    ) VALUES (
        'HD000003', 
        'CTG0011', 
        5, 
        1750000, 
        0, 
        8750000
    );
END
GO

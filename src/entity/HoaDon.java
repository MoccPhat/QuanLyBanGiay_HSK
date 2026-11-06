package entity;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class HoaDon {
    private String maHoaDon;
    private LocalDateTime ngayLap;
    private NhanVien nhanVien;
    private KhachHang khachHang; // Có thể null nếu khách vãng lai
    private double tongTien;
    private String phuongThucTT; // 'Tiền mặt', 'Chuyển khoản'
    private double tienKhachDua;
    private double tienThua;
    private List<ChiTietHoaDon> danhSachChiTiet;

    public HoaDon() {
        super();
        this.ngayLap = LocalDateTime.now();
        this.phuongThucTT = "Tiền mặt";
        this.danhSachChiTiet = new ArrayList<>();
    }

    public HoaDon(String maHoaDon) {
        this.maHoaDon = maHoaDon;
        this.ngayLap = LocalDateTime.now();
        this.phuongThucTT = "Tiền mặt";
        this.danhSachChiTiet = new ArrayList<>();
    }

    public HoaDon(String maHoaDon, LocalDateTime ngayLap, NhanVien nhanVien, KhachHang khachHang,
                  double tongTien, String phuongThucTT, double tienKhachDua, double tienThua) {
        this.maHoaDon = maHoaDon;
        this.ngayLap = (ngayLap != null) ? ngayLap : LocalDateTime.now();
        this.nhanVien = nhanVien;
        this.khachHang = khachHang;
        this.tongTien = tongTien;
        this.phuongThucTT = phuongThucTT;
        this.tienKhachDua = tienKhachDua;
        this.tienThua = tienThua;
        this.danhSachChiTiet = new ArrayList<>();
    }

    public String getMaHoaDon() {
        return maHoaDon;
    }

    public void setMaHoaDon(String maHoaDon) {
        this.maHoaDon = maHoaDon;
    }

    public LocalDateTime getNgayLap() {
        return ngayLap;
    }

    public void setNgayLap(LocalDateTime ngayLap) {
        this.ngayLap = ngayLap;
    }

    public NhanVien getNhanVien() {
        return nhanVien;
    }

    public void setNhanVien(NhanVien nhanVien) {
        this.nhanVien = nhanVien;
    }

    public KhachHang getKhachHang() {
        return khachHang;
    }

    public void setKhachHang(KhachHang khachHang) {
        this.khachHang = khachHang;
    }

    public double getTongTien() {
        return tongTien;
    }

    public void setTongTien(double tongTien) {
        this.tongTien = tongTien;
    }

    public String getPhuongThucTT() {
        return phuongThucTT;
    }

    public void setPhuongThucTT(String phuongThucTT) {
        this.phuongThucTT = phuongThucTT;
    }

    public double getTienKhachDua() {
        return tienKhachDua;
    }

    public void setTienKhachDua(double tienKhachDua) {
        this.tienKhachDua = tienKhachDua;
        tinhTienThua();
    }

    public double getTienThua() {
        return tienThua;
    }

    public void setTienThua(double tienThua) {
        this.tienThua = tienThua;
    }

    public List<ChiTietHoaDon> getDanhSachChiTiet() {
        return danhSachChiTiet;
    }

    public void setDanhSachChiTiet(List<ChiTietHoaDon> danhSachChiTiet) {
        this.danhSachChiTiet = danhSachChiTiet;
    }

    public void themChiTiet(ChiTietHoaDon cthd) {
        if (cthd != null) {
            this.danhSachChiTiet.add(cthd);
            tinhTongTien();
        }
    }

    public double tinhTongTien() {
        double tong = 0;
        for (ChiTietHoaDon ct : danhSachChiTiet) {
            tong += ct.getThanhTien();
        }
        this.tongTien = tong;
        tinhTienThua();
        return tong;
    }

    public double tinhTienThua() {
        this.tienThua = Math.max(0, this.tienKhachDua - this.tongTien);
        return this.tienThua;
    }

    @Override
    public int hashCode() {
        return Objects.hash(maHoaDon);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        HoaDon other = (HoaDon) obj;
        return Objects.equals(maHoaDon, other.maHoaDon);
    }

    @Override
    public String toString() {
        return "HD: " + maHoaDon + " - Tổng: " + String.format("%,.0f VNĐ", tongTien);
    }
}

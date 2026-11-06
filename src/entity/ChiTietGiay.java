package entity;

import java.util.Objects;

public class ChiTietGiay {
    private String maChiTietGiay;
    private SanPham sanPham;
    private int kichThuoc; // 35 - 45
    private String mauSac;
    private int soLuongTon;
    private String hinhAnh;

    public ChiTietGiay() {
        super();
        this.soLuongTon = 0;
    }

    public ChiTietGiay(String maChiTietGiay) {
        this.maChiTietGiay = maChiTietGiay;
    }

    public ChiTietGiay(String maChiTietGiay, SanPham sanPham, int kichThuoc, String mauSac, int soLuongTon, String hinhAnh) {
        this.maChiTietGiay = maChiTietGiay;
        this.sanPham = sanPham;
        this.kichThuoc = kichThuoc;
        this.mauSac = mauSac;
        this.soLuongTon = soLuongTon;
        this.hinhAnh = hinhAnh;
    }

    public String getMaChiTietGiay() {
        return maChiTietGiay;
    }

    public void setMaChiTietGiay(String maChiTietGiay) {
        this.maChiTietGiay = maChiTietGiay;
    }

    public SanPham getSanPham() {
        return sanPham;
    }

    public void setSanPham(SanPham sanPham) {
        this.sanPham = sanPham;
    }

    public int getKichThuoc() {
        return kichThuoc;
    }

    public void setKichThuoc(int kichThuoc) {
        this.kichThuoc = kichThuoc;
    }

    public String getMauSac() {
        return mauSac;
    }

    public void setMauSac(String mauSac) {
        this.mauSac = mauSac;
    }

    public int getSoLuongTon() {
        return soLuongTon;
    }

    public void setSoLuongTon(int soLuongTon) {
        this.soLuongTon = soLuongTon;
    }

    public String getHinhAnh() {
        return hinhAnh;
    }

    public void setHinhAnh(String hinhAnh) {
        this.hinhAnh = hinhAnh;
    }

    public boolean kiemTraTonKho(int soLuong) {
        return this.soLuongTon >= soLuong;
    }

    public void giamTonKho(int soLuong) {
        if (kiemTraTonKho(soLuong)) {
            this.soLuongTon -= soLuong;
        }
    }

    public void tangTonKho(int soLuong) {
        if (soLuong > 0) {
            this.soLuongTon += soLuong;
        }
    }

    @Override
    public int hashCode() {
        return Objects.hash(maChiTietGiay);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ChiTietGiay other = (ChiTietGiay) obj;
        return Objects.equals(maChiTietGiay, other.maChiTietGiay);
    }

    @Override
    public String toString() {
        String tenSP = (sanPham != null) ? sanPham.getTenSanPham() : "";
        return tenSP + " - Size " + kichThuoc + " (" + mauSac + ") [Tồn: " + soLuongTon + "]";
    }
}

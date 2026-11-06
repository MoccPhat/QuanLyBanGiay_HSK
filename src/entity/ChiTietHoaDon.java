package entity;

import java.util.Objects;

public class ChiTietHoaDon {
    private HoaDon hoaDon;
    private ChiTietGiay chiTietGiay;
    private int soLuong;
    private double donGia;
    private double giamGia;
    private double thanhTien;

    public ChiTietHoaDon() {
        super();
    }

    public ChiTietHoaDon(HoaDon hoaDon, ChiTietGiay chiTietGiay, int soLuong, double donGia, double giamGia) {
        this.hoaDon = hoaDon;
        this.chiTietGiay = chiTietGiay;
        this.soLuong = soLuong;
        this.donGia = donGia;
        this.giamGia = giamGia;
        this.thanhTien = tinhThanhTien();
    }

    public ChiTietHoaDon(HoaDon hoaDon, ChiTietGiay chiTietGiay, int soLuong, double donGia, double giamGia, double thanhTien) {
        this.hoaDon = hoaDon;
        this.chiTietGiay = chiTietGiay;
        this.soLuong = soLuong;
        this.donGia = donGia;
        this.giamGia = giamGia;
        this.thanhTien = thanhTien;
    }

    public HoaDon getHoaDon() {
        return hoaDon;
    }

    public void setHoaDon(HoaDon hoaDon) {
        this.hoaDon = hoaDon;
    }

    public ChiTietGiay getChiTietGiay() {
        return chiTietGiay;
    }

    public void setChiTietGiay(ChiTietGiay chiTietGiay) {
        this.chiTietGiay = chiTietGiay;
    }

    public int getSoLuong() {
        return soLuong;
    }

    public void setSoLuong(int soLuong) {
        this.soLuong = soLuong;
        tinhThanhTien();
    }

    public double getDonGia() {
        return donGia;
    }

    public void setDonGia(double donGia) {
        this.donGia = donGia;
        tinhThanhTien();
    }

    public double getGiamGia() {
        return giamGia;
    }

    public void setGiamGia(double giamGia) {
        this.giamGia = giamGia;
        tinhThanhTien();
    }

    public double getThanhTien() {
        return thanhTien;
    }

    public double tinhThanhTien() {
        this.thanhTien = Math.max(0, (this.soLuong * this.donGia) - this.giamGia);
        return this.thanhTien;
    }

    @Override
    public int hashCode() {
        return Objects.hash(hoaDon, chiTietGiay);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ChiTietHoaDon other = (ChiTietHoaDon) obj;
        return Objects.equals(hoaDon, other.hoaDon) && Objects.equals(chiTietGiay, other.chiTietGiay);
    }

    @Override
    public String toString() {
        String tenGiay = (chiTietGiay != null) ? chiTietGiay.toString() : "";
        return tenGiay + " x " + soLuong + " = " + String.format("%,.0f VNĐ", thanhTien);
    }
}

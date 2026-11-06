package entity;

import java.util.Objects;

public class SanPham {
    private String maSanPham;
    private String tenSanPham;
    private String loaiGiay; // 'Sneaker', 'Sandal', 'Giày Da', 'Chạy bộ'
    private String thuongHieu; // 'Nike', 'Adidas', 'Vans', 'Converse', 'Biti''s'
    private double giaNhap;
    private double giaBan;
    private String chatLieu;
    private boolean trangThai; // true: Đang kinh doanh, false: Ngừng kinh doanh

    public SanPham() {
        super();
        this.trangThai = true;
    }

    public SanPham(String maSanPham) {
        this.maSanPham = maSanPham;
        this.trangThai = true;
    }

    public SanPham(String maSanPham, String tenSanPham, String loaiGiay, String thuongHieu,
                   double giaNhap, double giaBan, String chatLieu, boolean trangThai) {
        this.maSanPham = maSanPham;
        this.tenSanPham = tenSanPham;
        this.loaiGiay = loaiGiay;
        this.thuongHieu = thuongHieu;
        this.giaNhap = giaNhap;
        this.giaBan = giaBan;
        this.chatLieu = chatLieu;
        this.trangThai = trangThai;
    }

    public String getMaSanPham() {
        return maSanPham;
    }

    public void setMaSanPham(String maSanPham) {
        this.maSanPham = maSanPham;
    }

    public String getTenSanPham() {
        return tenSanPham;
    }

    public void setTenSanPham(String tenSanPham) {
        this.tenSanPham = tenSanPham;
    }

    public String getLoaiGiay() {
        return loaiGiay;
    }

    public void setLoaiGiay(String loaiGiay) {
        this.loaiGiay = loaiGiay;
    }

    public String getThuongHieu() {
        return thuongHieu;
    }

    public void setThuongHieu(String thuongHieu) {
        this.thuongHieu = thuongHieu;
    }

    public double getGiaNhap() {
        return giaNhap;
    }

    public void setGiaNhap(double giaNhap) {
        this.giaNhap = giaNhap;
    }

    public double getGiaBan() {
        return giaBan;
    }

    public void setGiaBan(double giaBan) {
        this.giaBan = giaBan;
    }

    public String getChatLieu() {
        return chatLieu;
    }

    public void setChatLieu(String chatLieu) {
        this.chatLieu = chatLieu;
    }

    public boolean isTrangThai() {
        return trangThai;
    }

    public void setTrangThai(boolean trangThai) {
        this.trangThai = trangThai;
    }

    @Override
    public int hashCode() {
        return Objects.hash(maSanPham);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        SanPham other = (SanPham) obj;
        return Objects.equals(maSanPham, other.maSanPham);
    }

    @Override
    public String toString() {
        return tenSanPham + " (" + thuongHieu + ")";
    }
}

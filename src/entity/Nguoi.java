package entity;

import java.time.LocalDate;
import java.util.Objects;

public abstract class Nguoi {
    protected String hoTen;
    protected String soDienThoai;
    protected LocalDate ngaySinh;
    protected boolean gioiTinh; // true: Nam, false: Nữ
    protected String diaChi;
    protected String email;

    public Nguoi() {
        super();
    }

    public Nguoi(String hoTen, String soDienThoai, LocalDate ngaySinh, boolean gioiTinh, String diaChi, String email) {
        this.hoTen = hoTen;
        this.soDienThoai = soDienThoai;
        this.ngaySinh = ngaySinh;
        this.gioiTinh = gioiTinh;
        this.diaChi = diaChi;
        this.email = email;
    }

    public String getHoTen() {
        return hoTen;
    }

    public void setHoTen(String hoTen) {
        this.hoTen = hoTen;
    }

    public String getSoDienThoai() {
        return soDienThoai;
    }

    public void setSoDienThoai(String soDienThoai) {
        this.soDienThoai = soDienThoai;
    }

    public LocalDate getNgaySinh() {
        return ngaySinh;
    }

    public void setNgaySinh(LocalDate ngaySinh) {
        this.ngaySinh = ngaySinh;
    }

    public boolean isGioiTinh() {
        return gioiTinh;
    }

    public void setGioiTinh(boolean gioiTinh) {
        this.gioiTinh = gioiTinh;
    }

    public String getDiaChi() {
        return diaChi;
    }

    public void setDiaChi(String diaChi) {
        this.diaChi = diaChi;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    // Phương thức trừu tượng - Đặc trưng OOP
    public abstract String getThongTin();

    @Override
    public String toString() {
        return hoTen + " - SĐT: " + soDienThoai;
    }
}

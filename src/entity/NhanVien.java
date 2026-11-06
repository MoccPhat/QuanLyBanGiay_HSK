package entity;

import java.time.LocalDate;
import java.util.Objects;

public class NhanVien extends Nguoi {
    private String maNhanVien;
    private String chucVu; // 'Quản lý', 'Nhân viên bán hàng'
    private double luongCoBan;
    private String caLamViec; // 'Ca sáng', 'Ca chiều', 'Ca tối'
    private String matKhau;
    private boolean trangThai; // true: Đang làm, false: Đã nghỉ

    public NhanVien() {
        super();
    }

    public NhanVien(String maNhanVien) {
        this.maNhanVien = maNhanVien;
    }

    public NhanVien(String maNhanVien, String hoTen, String soDienThoai, LocalDate ngaySinh, boolean gioiTinh,
                   String diaChi, String email, String chucVu, double luongCoBan, String caLamViec,
                   String matKhau, boolean trangThai) {
        super(hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email);
        this.maNhanVien = maNhanVien;
        this.chucVu = chucVu;
        this.luongCoBan = luongCoBan;
        this.caLamViec = caLamViec;
        this.matKhau = matKhau;
        this.trangThai = trangThai;
    }

    public String getMaNhanVien() {
        return maNhanVien;
    }

    public void setMaNhanVien(String maNhanVien) {
        this.maNhanVien = maNhanVien;
    }

    public String getChucVu() {
        return chucVu;
    }

    public void setChucVu(String chucVu) {
        this.chucVu = chucVu;
    }

    public double getLuongCoBan() {
        return luongCoBan;
    }

    public void setLuongCoBan(double luongCoBan) {
        this.luongCoBan = luongCoBan;
    }

    public String getCaLamViec() {
        return caLamViec;
    }

    public void setCaLamViec(String caLamViec) {
        this.caLamViec = caLamViec;
    }

    public String getMatKhau() {
        return matKhau;
    }

    public void setMatKhau(String matKhau) {
        this.matKhau = matKhau;
    }

    public boolean isTrangThai() {
        return trangThai;
    }

    public void setTrangThai(boolean trangThai) {
        this.trangThai = trangThai;
    }

    public boolean isQuanLy() {
        return "Quản lý".equalsIgnoreCase(this.chucVu);
    }

    public double tinhLuong() {
        return isQuanLy() ? this.luongCoBan * 1.2 : this.luongCoBan;
    }

    @Override
    public String getThongTin() {
        return "[" + maNhanVien + "] " + hoTen + " - Chức vụ: " + chucVu;
    }

    @Override
    public int hashCode() {
        return Objects.hash(maNhanVien);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        NhanVien other = (NhanVien) obj;
        return Objects.equals(maNhanVien, other.maNhanVien);
    }

    @Override
    public String toString() {
        return hoTen + " (" + maNhanVien + ")";
    }
}

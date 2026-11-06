package entity;

import java.time.LocalDate;
import java.util.Objects;

public class KhachHang extends Nguoi {
    private String maKhachHang;
    private int diemTichLuy;
    private String hangThanhVien; // 'Đồng', 'Bạc', 'Vàng', 'Kim Cương'

    public KhachHang() {
        super();
        this.hangThanhVien = "Đồng";
        this.diemTichLuy = 0;
    }

    public KhachHang(String maKhachHang) {
        this.maKhachHang = maKhachHang;
    }

    public KhachHang(String maKhachHang, String hoTen, String soDienThoai, LocalDate ngaySinh, boolean gioiTinh,
                     String diaChi, String email, int diemTichLuy, String hangThanhVien) {
        super(hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email);
        this.maKhachHang = maKhachHang;
        this.diemTichLuy = diemTichLuy;
        this.hangThanhVien = hangThanhVien;
    }

    public String getMaKhachHang() {
        return maKhachHang;
    }

    public void setMaKhachHang(String maKhachHang) {
        this.maKhachHang = maKhachHang;
    }

    public int getDiemTichLuy() {
        return diemTichLuy;
    }

    public void setDiemTichLuy(int diemTichLuy) {
        this.diemTichLuy = diemTichLuy;
    }

    public String getHangThanhVien() {
        return hangThanhVien;
    }

    public void setHangThanhVien(String hangThanhVien) {
        this.hangThanhVien = hangThanhVien;
    }

    public void congDiem(int diem) {
        if (diem > 0) {
            this.diemTichLuy += diem;
            capNhatHang();
        }
    }

    public void capNhatHang() {
        if (diemTichLuy >= 200) {
            this.hangThanhVien = "Kim Cương";
        } else if (diemTichLuy >= 100) {
            this.hangThanhVien = "Vàng";
        } else if (diemTichLuy >= 30) {
            this.hangThanhVien = "Bạc";
        } else {
            this.hangThanhVien = "Đồng";
        }
    }

    public double tinhChietKhau() {
        switch (hangThanhVien) {
            case "Kim Cương": return 0.15; // 15%
            case "Vàng": return 0.10;      // 10%
            case "Bạc": return 0.05;       // 5%
            default: return 0.0;
        }
    }

    @Override
    public String getThongTin() {
        return "[" + maKhachHang + "] " + hoTen + " - Hạng: " + hangThanhVien + " (" + diemTichLuy + " điểm)";
    }

    @Override
    public int hashCode() {
        return Objects.hash(maKhachHang);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        KhachHang other = (KhachHang) obj;
        return Objects.equals(maKhachHang, other.maKhachHang);
    }

    @Override
    public String toString() {
        return hoTen + " (" + soDienThoai + ")";
    }
}

package entity;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Lớp Entity biểu diễn Hóa đơn bán hàng tại quầy (StepUp Footwear POS).
 * Khớp chuẩn 100% với bảng HoaDon trong CSDL SQL Server QuanLyBanGiay:
 * - maHoaDon, ngayLap, maNhanVien, maKhachHang
 * - tongTienHang (tổng tiền gốc trước giảm giá)
 * - chietKhau (tiền giảm giá theo hạng thẻ thành viên)
 * - diemSuDung (số điểm tích lũy dùng để thanh toán)
 * - tienGiamDiem (số tiền tương ứng với điểm: 1 điểm = 1.000 VNĐ)
 * - tongTien (tổng tiền thực tế khách cần thanh toán sau khi trừ mọi chiết khấu)
 * - phuongThucTT, tienKhachDua, tienThua, diemCong
 */
public class HoaDon {
    private String maHoaDon;
    private LocalDateTime ngayLap;
    private NhanVien nhanVien;
    private KhachHang khachHang; // null nếu là khách vãng lai
    private double tongTienHang; // Tổng tiền các sản phẩm trong giỏ (chưa giảm)
    private double chietKhau;    // Số tiền giảm theo hạng thành viên (5%, 10%, 15%)
    private int diemSuDung;      // Số điểm khách dùng
    private double tienGiamDiem; // Số tiền giảm từ điểm dùng
    private double tongTien;     // Tiền khách thực tế phải trả (= tongTienHang - chietKhau - tienGiamDiem)
    private String phuongThucTT; // "Tiền mặt", "Chuyển khoản QR"
    private double tienKhachDua; // Tiền khách đưa
    private double tienThua;     // Tiền thối lại cho khách
    private int diemCong;        // Số điểm tích lũy được cộng mới (mỗi 100.000đ = 1 điểm)
    private List<ChiTietHoaDon> danhSachChiTiet;

    public HoaDon() {
        super();
        this.ngayLap = LocalDateTime.now();
        this.phuongThucTT = "Tiền mặt";
        this.danhSachChiTiet = new ArrayList<>();
    }

    public HoaDon(String maHoaDon) {
        this();
        this.maHoaDon = maHoaDon;
    }

    public HoaDon(String maHoaDon, LocalDateTime ngayLap, NhanVien nhanVien, KhachHang khachHang,
                  double tongTien, String phuongThucTT, double tienKhachDua, double tienThua) {
        this();
        this.maHoaDon = maHoaDon;
        this.ngayLap = (ngayLap != null) ? ngayLap : LocalDateTime.now();
        this.nhanVien = nhanVien;
        this.khachHang = khachHang;
        this.tongTien = tongTien;
        this.phuongThucTT = phuongThucTT;
        this.tienKhachDua = tienKhachDua;
        this.tienThua = tienThua;
        this.tongTienHang = tongTien;
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

    public double getTongTienHang() {
        return tongTienHang;
    }

    public void setTongTienHang(double tongTienHang) {
        this.tongTienHang = tongTienHang;
    }

    public double getChietKhau() {
        return chietKhau;
    }

    public void setChietKhau(double chietKhau) {
        this.chietKhau = chietKhau;
    }

    public int getDiemSuDung() {
        return diemSuDung;
    }

    public void setDiemSuDung(int diemSuDung) {
        this.diemSuDung = diemSuDung;
    }

    public double getTienGiamDiem() {
        return tienGiamDiem;
    }

    public void setTienGiamDiem(double tienGiamDiem) {
        this.tienGiamDiem = tienGiamDiem;
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

    public int getDiemCong() {
        return diemCong;
    }

    public void setDiemCong(int diemCong) {
        this.diemCong = diemCong;
    }

    public List<ChiTietHoaDon> getDanhSachChiTiet() {
        return danhSachChiTiet;
    }

    public void setDanhSachChiTiet(List<ChiTietHoaDon> danhSachChiTiet) {
        this.danhSachChiTiet = danhSachChiTiet;
    }

    /**
     * Thêm một dòng chi tiết sản phẩm vào hóa đơn.
     * Bảo toàn tongTien đã tính toán chiết khấu (không để bị ghi đè số thô).
     */
    public void themChiTiet(ChiTietHoaDon cthd) {
        if (cthd != null) {
            this.danhSachChiTiet.add(cthd);
            if (this.tongTienHang <= 0) {
                this.tongTienHang = tinhTongTien();
            }
        }
    }

    public double tinhTongTien() {
        double tong = 0;
        for (ChiTietHoaDon ct : danhSachChiTiet) {
            tong += ct.getThanhTien();
        }
        if (this.tongTien <= 0) {
            this.tongTien = tong;
        }
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
        return "HD: " + maHoaDon + " - Tổng phải trả: " + String.format("%,.0f VNĐ", tongTien);
    }
}

package entity;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Lớp thực thể biểu diễn Hóa đơn bán lẻ tại quầy trong hệ thống (tầng Entity).
 * Khớp chuẩn 100% với bảng HoaDon (13 cột) trong CSDL SQL Server QuanLyBanGiay:
 * quản lý thông tin nhân viên, khách hàng, tổng tiền hàng gốc, chiết khấu hạng thẻ,
 * điểm tích lũy sử dụng, tiền thanh toán thực, phương thức thanh toán và tiền thối.
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

    /**
     * Khởi tạo đối tượng Hóa đơn mặc định với ngày lập hiện tại, phương thức Tiền mặt và danh sách chi tiết rỗng.
     */
    public HoaDon() {
        super();
        this.ngayLap = LocalDateTime.now();
        this.phuongThucTT = "Tiền mặt";
        this.danhSachChiTiet = new ArrayList<>();
    }

    /**
     * Khởi tạo đối tượng Hóa đơn với mã định danh duy nhất.
     *
     * @param maHoaDon mã hóa đơn định danh (định dạng HDxxxxxx)
     */
    public HoaDon(String maHoaDon) {
        this();
        this.maHoaDon = maHoaDon;
    }

    /**
     * Khởi tạo đối tượng Hóa đơn với các thông tin thanh toán cơ bản.
     *
     * @param maHoaDon mã hóa đơn định danh
     * @param ngayLap thời điểm lập hóa đơn
     * @param nhanVien nhân viên thu ngân phụ trách
     * @param khachHang khách hàng mua hàng (hoặc null nếu là khách vãng lai)
     * @param tongTien tổng số tiền thực tế khách cần thanh toán (VNĐ)
     * @param phuongThucTT phương thức thanh toán ('Tiền mặt' hoặc 'Chuyển khoản QR')
     * @param tienKhachDua số tiền khách đưa (VNĐ)
     * @param tienThua số tiền thối lại cho khách (VNĐ)
     */
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

    /**
     * Lấy mã hóa đơn định danh.
     *
     * @return chuỗi mã hóa đơn
     */
    public String getMaHoaDon() {
        return maHoaDon;
    }

    /**
     * Cập nhật mã hóa đơn định danh.
     *
     * @param maHoaDon mã hóa đơn mới
     */
    public void setMaHoaDon(String maHoaDon) {
        this.maHoaDon = maHoaDon;
    }

    /**
     * Lấy thời điểm lập hóa đơn.
     *
     * @return thời điểm lập hóa đơn dạng LocalDateTime
     */
    public LocalDateTime getNgayLap() {
        return ngayLap;
    }

    /**
     * Cập nhật thời điểm lập hóa đơn.
     *
     * @param ngayLap thời điểm lập hóa đơn mới dạng LocalDateTime
     */
    public void setNgayLap(LocalDateTime ngayLap) {
        this.ngayLap = ngayLap;
    }

    /**
     * Lấy đối tượng nhân viên thu ngân lập hóa đơn.
     *
     * @return đối tượng NhanVien
     */
    public NhanVien getNhanVien() {
        return nhanVien;
    }

    /**
     * Cập nhật nhân viên thu ngân lập hóa đơn.
     *
     * @param nhanVien đối tượng NhanVien mới
     */
    public void setNhanVien(NhanVien nhanVien) {
        this.nhanVien = nhanVien;
    }

    /**
     * Lấy đối tượng khách hàng giao dịch.
     *
     * @return đối tượng KhachHang hoặc null nếu là khách vãng lai
     */
    public KhachHang getKhachHang() {
        return khachHang;
    }

    /**
     * Cập nhật thông tin khách hàng giao dịch.
     *
     * @param khachHang đối tượng KhachHang mới
     */
    public void setKhachHang(KhachHang khachHang) {
        this.khachHang = khachHang;
    }

    /**
     * Lấy tổng tiền hàng gốc trước khi giảm giá và chiết khấu.
     *
     * @return số tiền hàng gốc (VNĐ)
     */
    public double getTongTienHang() {
        return tongTienHang;
    }

    /**
     * Cập nhật tổng tiền hàng gốc trước khi giảm giá.
     *
     * @param tongTienHang số tiền hàng gốc mới (VNĐ)
     */
    public void setTongTienHang(double tongTienHang) {
        this.tongTienHang = tongTienHang;
    }

    /**
     * Lấy số tiền được giảm giá theo hạng thẻ thành viên.
     *
     * @return số tiền chiết khấu (VNĐ)
     */
    public double getChietKhau() {
        return chietKhau;
    }

    /**
     * Cập nhật số tiền giảm giá theo hạng thẻ thành viên.
     *
     * @param chietKhau số tiền chiết khấu mới (VNĐ)
     */
    public void setChietKhau(double chietKhau) {
        this.chietKhau = chietKhau;
    }

    /**
     * Lấy số điểm tích lũy khách hàng sử dụng trong giao dịch.
     *
     * @return số điểm sử dụng
     */
    public int getDiemSuDung() {
        return diemSuDung;
    }

    /**
     * Cập nhật số điểm tích lũy khách hàng sử dụng.
     *
     * @param diemSuDung số điểm sử dụng mới
     */
    public void setDiemSuDung(int diemSuDung) {
        this.diemSuDung = diemSuDung;
    }

    /**
     * Lấy số tiền giảm trừ quy đổi từ điểm tích lũy (1 điểm = 1.000 VNĐ).
     *
     * @return số tiền giảm trừ từ điểm (VNĐ)
     */
    public double getTienGiamDiem() {
        return tienGiamDiem;
    }

    /**
     * Cập nhật số tiền giảm trừ quy đổi từ điểm tích lũy.
     *
     * @param tienGiamDiem số tiền giảm trừ mới (VNĐ)
     */
    public void setTienGiamDiem(double tienGiamDiem) {
        this.tienGiamDiem = tienGiamDiem;
    }

    /**
     * Lấy tổng số tiền khách thực tế phải trả sau khi áp dụng chiết khấu và giảm điểm.
     *
     * @return tổng tiền thanh toán thực tế (VNĐ)
     */
    public double getTongTien() {
        return tongTien;
    }

    /**
     * Cập nhật tổng số tiền khách thực tế phải trả.
     *
     * @param tongTien tổng tiền thanh toán mới (VNĐ)
     */
    public void setTongTien(double tongTien) {
        this.tongTien = tongTien;
    }

    /**
     * Lấy phương thức thanh toán của đơn hàng.
     *
     * @return chuỗi phương thức thanh toán ('Tiền mặt' hoặc 'Chuyển khoản QR')
     */
    public String getPhuongThucTT() {
        return phuongThucTT;
    }

    /**
     * Cập nhật phương thức thanh toán của đơn hàng.
     *
     * @param phuongThucTT chuỗi phương thức thanh toán mới
     */
    public void setPhuongThucTT(String phuongThucTT) {
        this.phuongThucTT = phuongThucTT;
    }

    /**
     * Lấy số tiền khách đưa cho thu ngân.
     *
     * @return số tiền khách đưa (VNĐ)
     */
    public double getTienKhachDua() {
        return tienKhachDua;
    }

    /**
     * Cập nhật số tiền khách đưa và tự động tính lại số tiền thừa trả lại.
     *
     * @param tienKhachDua số tiền khách đưa mới (VNĐ)
     */
    public void setTienKhachDua(double tienKhachDua) {
        this.tienKhachDua = tienKhachDua;
        tinhTienThua();
    }

    /**
     * Lấy số tiền thừa trả lại cho khách hàng.
     *
     * @return số tiền thừa (VNĐ)
     */
    public double getTienThua() {
        return tienThua;
    }

    /**
     * Cập nhật số tiền thừa trả lại cho khách hàng.
     *
     * @param tienThua số tiền thừa mới (VNĐ)
     */
    public void setTienThua(double tienThua) {
        this.tienThua = tienThua;
    }

    /**
     * Lấy số điểm thưởng tích lũy được cộng mới từ đơn hàng này.
     *
     * @return số điểm thưởng tích lũy
     */
    public int getDiemCong() {
        return diemCong;
    }

    /**
     * Cập nhật số điểm thưởng tích lũy được cộng mới.
     *
     * @param diemCong số điểm thưởng mới
     */
    public void setDiemCong(int diemCong) {
        this.diemCong = diemCong;
    }

    /**
     * Lấy danh sách các dòng chi tiết sản phẩm thuộc về hóa đơn.
     *
     * @return danh sách các đối tượng ChiTietHoaDon
     */
    public List<ChiTietHoaDon> getDanhSachChiTiet() {
        return danhSachChiTiet;
    }

    /**
     * Cập nhật danh sách các dòng chi tiết sản phẩm thuộc về hóa đơn.
     *
     * @param danhSachChiTiet danh sách các đối tượng ChiTietHoaDon mới
     */
    public void setDanhSachChiTiet(List<ChiTietHoaDon> danhSachChiTiet) {
        this.danhSachChiTiet = danhSachChiTiet;
    }

    /**
     * Thêm một dòng chi tiết sản phẩm vào hóa đơn và bảo toàn tổng tiền đã tính toán chiết khấu.
     *
     * @param cthd đối tượng dòng sản phẩm ChiTietHoaDon cần thêm
     */
    public void themChiTiet(ChiTietHoaDon cthd) {
        if (cthd != null) {
            this.danhSachChiTiet.add(cthd);
            if (this.tongTienHang <= 0) {
                this.tongTienHang = tinhTongTien();
            }
        }
    }

    /**
     * Tính tổng thành tiền của toàn bộ các sản phẩm có trong giỏ hàng và cập nhật tiền thừa.
     *
     * @return tổng tiền các dòng sản phẩm (VNĐ)
     */
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

    /**
     * Tính số tiền thối lại cho khách dựa trên tiền khách đưa và số tiền thực tế cần thanh toán.
     *
     * @return số tiền thừa hoàn trả (VNĐ)
     */
    public double tinhTienThua() {
        this.tienThua = Math.max(0, this.tienKhachDua - this.tongTien);
        return this.tienThua;
    }

    /**
     * Tính mã băm hashCode dựa trên mã hóa đơn duy nhất.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(maHoaDon);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Hóa đơn theo mã hóa đơn định danh.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng mã hóa đơn, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        HoaDon other = (HoaDon) obj;
        return Objects.equals(maHoaDon, other.maHoaDon);
    }

    /**
     * Trả về chuỗi thông tin định danh mã hóa đơn và tổng số tiền phải trả.
     *
     * @return chuỗi mô tả hóa đơn định dạng rút gọn
     */
    @Override
    public String toString() {
        return "HD: " + maHoaDon + " - Tổng phải trả: " + String.format("%,.0f VNĐ", tongTien);
    }
}

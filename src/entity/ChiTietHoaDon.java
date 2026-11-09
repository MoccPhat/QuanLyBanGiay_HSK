package entity;

import java.util.Objects;

/**
 * Lớp thực thể đại diện cho Chi tiết hóa đơn (tầng Entity), liên kết giữa Hóa đơn và Biến thể giày (SKU),
 * lưu trữ thông tin về số lượng mua, đơn giá bán, giảm giá dòng hàng và thành tiền thực tế.
 */
public class ChiTietHoaDon {
    private HoaDon hoaDon;
    private ChiTietGiay chiTietGiay;
    private int soLuong;
    private double donGia;
    private double giamGia;
    private double thanhTien;

    /**
     * Khởi tạo đối tượng Chi tiết hóa đơn mặc định không tham số.
     */
    public ChiTietHoaDon() {
        super();
    }

    /**
     * Khởi tạo dòng chi tiết hóa đơn và tự động tính thành tiền dựa trên số lượng, đơn giá và giảm giá.
     *
     * @param hoaDon đối tượng Hóa đơn chứa dòng sản phẩm này
     * @param chiTietGiay đối tượng Biến thể giày (SKU) được xuất bán
     * @param soLuong số lượng sản phẩm xuất bán
     * @param donGia đơn giá bán tại thời điểm giao dịch (VNĐ)
     * @param giamGia số tiền giảm giá trên dòng sản phẩm (VNĐ)
     */
    public ChiTietHoaDon(HoaDon hoaDon, ChiTietGiay chiTietGiay, int soLuong, double donGia, double giamGia) {
        this.hoaDon = hoaDon;
        this.chiTietGiay = chiTietGiay;
        this.soLuong = soLuong;
        this.donGia = donGia;
        this.giamGia = giamGia;
        this.thanhTien = tinhThanhTien();
    }

    /**
     * Khởi tạo dòng chi tiết hóa đơn với đầy đủ thông tin bao gồm thành tiền định sẵn.
     *
     * @param hoaDon đối tượng Hóa đơn chứa dòng sản phẩm này
     * @param chiTietGiay đối tượng Biến thể giày (SKU) được xuất bán
     * @param soLuong số lượng sản phẩm xuất bán
     * @param donGia đơn giá bán tại thời điểm giao dịch (VNĐ)
     * @param giamGia số tiền giảm giá trên dòng sản phẩm (VNĐ)
     * @param thanhTien tổng số tiền thành tiền của dòng sản phẩm (VNĐ)
     */
    public ChiTietHoaDon(HoaDon hoaDon, ChiTietGiay chiTietGiay, int soLuong, double donGia, double giamGia, double thanhTien) {
        this.hoaDon = hoaDon;
        this.chiTietGiay = chiTietGiay;
        this.soLuong = soLuong;
        this.donGia = donGia;
        this.giamGia = giamGia;
        this.thanhTien = thanhTien;
    }

    /**
     * Lấy đối tượng hóa đơn chứa dòng sản phẩm này.
     *
     * @return đối tượng HoaDon
     */
    public HoaDon getHoaDon() {
        return hoaDon;
    }

    /**
     * Cập nhật đối tượng hóa đơn chứa dòng sản phẩm này.
     *
     * @param hoaDon đối tượng HoaDon mới
     */
    public void setHoaDon(HoaDon hoaDon) {
        this.hoaDon = hoaDon;
    }

    /**
     * Lấy đối tượng biến thể giày chi tiết được mua.
     *
     * @return đối tượng ChiTietGiay
     */
    public ChiTietGiay getChiTietGiay() {
        return chiTietGiay;
    }

    /**
     * Cập nhật đối tượng biến thể giày chi tiết được mua.
     *
     * @param chiTietGiay đối tượng ChiTietGiay mới
     */
    public void setChiTietGiay(ChiTietGiay chiTietGiay) {
        this.chiTietGiay = chiTietGiay;
    }

    /**
     * Lấy số lượng sản phẩm xuất bán.
     *
     * @return số lượng mua nguyên
     */
    public int getSoLuong() {
        return soLuong;
    }

    /**
     * Cập nhật số lượng sản phẩm xuất bán và tự động tính lại thành tiền.
     *
     * @param soLuong số lượng mua mới
     */
    public void setSoLuong(int soLuong) {
        this.soLuong = soLuong;
        tinhThanhTien();
    }

    /**
     * Lấy đơn giá bán của sản phẩm.
     *
     * @return đơn giá bán (VNĐ)
     */
    public double getDonGia() {
        return donGia;
    }

    /**
     * Cập nhật đơn giá bán và tự động tính lại thành tiền.
     *
     * @param donGia đơn giá bán mới (VNĐ)
     */
    public void setDonGia(double donGia) {
        this.donGia = donGia;
        tinhThanhTien();
    }

    /**
     * Lấy số tiền giảm giá áp dụng cho dòng sản phẩm.
     *
     * @return số tiền giảm giá (VNĐ)
     */
    public double getGiamGia() {
        return giamGia;
    }

    /**
     * Cập nhật số tiền giảm giá áp dụng cho dòng sản phẩm và tự động tính lại thành tiền.
     *
     * @param giamGia số tiền giảm giá mới (VNĐ)
     */
    public void setGiamGia(double giamGia) {
        this.giamGia = giamGia;
        tinhThanhTien();
    }

    /**
     * Lấy tổng số tiền thành tiền của dòng sản phẩm sau khi trừ giảm giá.
     *
     * @return số tiền thành tiền (VNĐ)
     */
    public double getThanhTien() {
        return thanhTien;
    }

    /**
     * Tính toán số tiền thành tiền theo công thức: (số lượng * đơn giá) - giảm giá.
     *
     * @return số tiền thành tiền sau khi trừ giảm giá (VNĐ)
     */
    public double tinhThanhTien() {
        this.thanhTien = Math.max(0, (this.soLuong * this.donGia) - this.giamGia);
        return this.thanhTien;
    }

    /**
     * Tính mã băm hashCode dựa trên sự kết hợp giữa hóa đơn và biến thể chi tiết giày.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(hoaDon, chiTietGiay);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Chi tiết hóa đơn theo hóa đơn và biến thể giày.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng thuộc một hóa đơn và cùng một biến thể giày, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ChiTietHoaDon other = (ChiTietHoaDon) obj;
        return Objects.equals(hoaDon, other.hoaDon) && Objects.equals(chiTietGiay, other.chiTietGiay);
    }

    /**
     * Trả về chuỗi mô tả thông tin dòng sản phẩm, số lượng và tổng thành tiền.
     *
     * @return chuỗi mô tả chi tiết dòng hóa đơn
     */
    @Override
    public String toString() {
        String tenGiay = (chiTietGiay != null) ? chiTietGiay.toString() : "";
        return tenGiay + " x " + soLuong + " = " + String.format("%,.0f VNĐ", thanhTien);
    }
}

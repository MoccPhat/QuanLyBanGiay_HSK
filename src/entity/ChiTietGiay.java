package entity;

import java.util.Objects;

/**
 * Lớp thực thể đại diện cho Biến thể chi tiết của giày trong hệ thống (tầng Entity),
 * định danh theo SKU duy nhất, quản lý kích thước, màu sắc, số lượng tồn kho và hình ảnh.
 */
public class ChiTietGiay {
    private String maChiTietGiay;
    private SanPham sanPham;
    private int kichThuoc; // 35 - 45
    private String mauSac;
    private int soLuongTon;
    private String hinhAnh;

    /**
     * Khởi tạo đối tượng Biến thể giày mặc định với tồn kho bằng 0.
     */
    public ChiTietGiay() {
        super();
        this.soLuongTon = 0;
    }

    /**
     * Khởi tạo đối tượng Biến thể giày với mã SKU định danh.
     *
     * @param maChiTietGiay mã SKU biến thể (định dạng CTGxxxx)
     */
    public ChiTietGiay(String maChiTietGiay) {
        this.maChiTietGiay = maChiTietGiay;
    }

    /**
     * Khởi tạo đối tượng Biến thể giày với đầy đủ thuộc tính chi tiết.
     *
     * @param maChiTietGiay mã SKU biến thể định danh
     * @param sanPham đối tượng Sản phẩm gốc mà biến thể trực thuộc
     * @param kichThuoc kích cỡ giày (size số nguyên từ 35 đến 45)
     * @param mauSac màu sắc của biến thể giày
     * @param soLuongTon số lượng hàng tồn kho thực tế
     * @param hinhAnh tên tệp hình ảnh minh họa của biến thể
     */
    public ChiTietGiay(String maChiTietGiay, SanPham sanPham, int kichThuoc, String mauSac, int soLuongTon, String hinhAnh) {
        this.maChiTietGiay = maChiTietGiay;
        this.sanPham = sanPham;
        this.kichThuoc = kichThuoc;
        this.mauSac = mauSac;
        this.soLuongTon = soLuongTon;
        this.hinhAnh = hinhAnh;
    }

    /**
     * Lấy mã biến thể giày SKU.
     *
     * @return chuỗi mã biến thể SKU
     */
    public String getMaChiTietGiay() {
        return maChiTietGiay;
    }

    /**
     * Cập nhật mã biến thể giày SKU.
     *
     * @param maChiTietGiay mã SKU biến thể mới
     */
    public void setMaChiTietGiay(String maChiTietGiay) {
        this.maChiTietGiay = maChiTietGiay;
    }

    /**
     * Lấy đối tượng sản phẩm gốc của biến thể.
     *
     * @return đối tượng SanPham
     */
    public SanPham getSanPham() {
        return sanPham;
    }

    /**
     * Cập nhật đối tượng sản phẩm gốc.
     *
     * @param sanPham đối tượng SanPham mới
     */
    public void setSanPham(SanPham sanPham) {
        this.sanPham = sanPham;
    }

    /**
     * Lấy kích cỡ giày của biến thể.
     *
     * @return cỡ giày số nguyên
     */
    public int getKichThuoc() {
        return kichThuoc;
    }

    /**
     * Cập nhật kích cỡ giày của biến thể.
     *
     * @param kichThuoc cỡ giày mới (35 - 45)
     */
    public void setKichThuoc(int kichThuoc) {
        this.kichThuoc = kichThuoc;
    }

    /**
     * Lấy tên màu sắc của biến thể giày.
     *
     * @return chuỗi màu sắc
     */
    public String getMauSac() {
        return mauSac;
    }

    /**
     * Cập nhật tên màu sắc của biến thể giày.
     *
     * @param mauSac chuỗi màu sắc mới
     */
    public void setMauSac(String mauSac) {
        this.mauSac = mauSac;
    }

    /**
     * Lấy số lượng hàng còn tồn trong kho.
     *
     * @return số lượng tồn kho nguyên
     */
    public int getSoLuongTon() {
        return soLuongTon;
    }

    /**
     * Cập nhật số lượng hàng tồn trong kho.
     *
     * @param soLuongTon số lượng tồn kho mới
     */
    public void setSoLuongTon(int soLuongTon) {
        this.soLuongTon = soLuongTon;
    }

    /**
     * Lấy tên tệp hình ảnh minh họa của biến thể.
     *
     * @return tên tệp hình ảnh
     */
    public String getHinhAnh() {
        return hinhAnh;
    }

    /**
     * Cập nhật tên tệp hình ảnh minh họa của biến thể.
     *
     * @param hinhAnh tên tệp hình ảnh mới
     */
    public void setHinhAnh(String hinhAnh) {
        this.hinhAnh = hinhAnh;
    }

    /**
     * Kiểm tra số lượng tồn kho thực tế có đủ đáp ứng nhu cầu xuất bán hay không.
     *
     * @param soLuong số lượng hàng yêu cầu cần kiểm tra
     * @return true nếu lượng tồn kho lớn hơn hoặc bằng số lượng yêu cầu, ngược lại false
     */
    public boolean kiemTraTonKho(int soLuong) {
        return this.soLuongTon >= soLuong;
    }

    /**
     * Giảm số lượng hàng tồn kho sau khi thực hiện giao dịch xuất bán thành công.
     *
     * @param soLuong số lượng hàng cần xuất trừ khỏi kho
     */
    public void giamTonKho(int soLuong) {
        if (kiemTraTonKho(soLuong)) {
            this.soLuongTon -= soLuong;
        }
    }

    /**
     * Tăng số lượng hàng tồn kho khi nhập thêm hàng hoặc hoàn trả đơn hàng.
     *
     * @param soLuong số lượng hàng cần cộng thêm vào kho
     */
    public void tangTonKho(int soLuong) {
        if (soLuong > 0) {
            this.soLuongTon += soLuong;
        }
    }

    /**
     * Tính mã băm hashCode dựa trên mã SKU biến thể duy nhất.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(maChiTietGiay);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Biến thể giày theo mã SKU định danh.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng mã SKU, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ChiTietGiay other = (ChiTietGiay) obj;
        return Objects.equals(maChiTietGiay, other.maChiTietGiay);
    }

    /**
     * Trả về chuỗi mô tả tên sản phẩm, kích thước, màu sắc và số lượng tồn kho.
     *
     * @return chuỗi mô tả chi tiết biến thể giày
     */
    @Override
    public String toString() {
        String tenSP = (sanPham != null) ? sanPham.getTenSanPham() : "";
        return tenSP + " - Size " + kichThuoc + " (" + mauSac + ") [Tồn: " + soLuongTon + "]";
    }
}

package entity;

import java.util.Objects;

/**
 * Lớp thực thể đại diện cho Sản phẩm giày dép trong hệ thống (tầng Entity),
 * quản lý thông tin chung về mã, tên, phân loại, thương hiệu, giá cả và chất liệu.
 */
public class SanPham {
    private String maSanPham;
    private String tenSanPham;
    private String loaiGiay; // 'Sneaker', 'Sandal', 'Giày Da', 'Chạy bộ'
    private String thuongHieu; // 'Nike', 'Adidas', 'Vans', 'Converse', 'Biti''s'
    private double giaNhap;
    private double giaBan;
    private String chatLieu;
    private boolean trangThai; // true: Đang kinh doanh, false: Ngừng kinh doanh

    /**
     * Khởi tạo đối tượng Sản phẩm mặc định với trạng thái đang kinh doanh.
     */
    public SanPham() {
        super();
        this.trangThai = true;
    }

    /**
     * Khởi tạo đối tượng Sản phẩm với mã định danh duy nhất.
     *
     * @param maSanPham mã sản phẩm định danh (định dạng SPxxxx)
     */
    public SanPham(String maSanPham) {
        this.maSanPham = maSanPham;
        this.trangThai = true;
    }

    /**
     * Khởi tạo đối tượng Sản phẩm với đầy đủ thông tin chi tiết.
     *
     * @param maSanPham mã sản phẩm định danh
     * @param tenSanPham tên gọi của sản phẩm
     * @param loaiGiay phân loại giày ('Sneaker', 'Sandal', 'Giày Da', 'Chạy bộ')
     * @param thuongHieu thương hiệu sản xuất ('Nike', 'Adidas', 'Vans', 'Converse', 'Biti''s')
     * @param giaNhap đơn giá nhập hàng từ nhà cung cấp (VNĐ)
     * @param giaBan đơn giá bán niêm yết tại quầy (VNĐ)
     * @param chatLieu chất liệu chính cấu thành sản phẩm
     * @param trangThai trạng thái kinh doanh (true: Đang kinh doanh, false: Ngừng kinh doanh)
     */
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

    /**
     * Lấy mã sản phẩm định danh.
     *
     * @return chuỗi mã sản phẩm
     */
    public String getMaSanPham() {
        return maSanPham;
    }

    /**
     * Cập nhật mã sản phẩm định danh.
     *
     * @param maSanPham mã sản phẩm mới
     */
    public void setMaSanPham(String maSanPham) {
        this.maSanPham = maSanPham;
    }

    /**
     * Lấy tên gọi của sản phẩm.
     *
     * @return chuỗi tên sản phẩm
     */
    public String getTenSanPham() {
        return tenSanPham;
    }

    /**
     * Cập nhật tên gọi của sản phẩm.
     *
     * @param tenSanPham tên sản phẩm mới
     */
    public void setTenSanPham(String tenSanPham) {
        this.tenSanPham = tenSanPham;
    }

    /**
     * Lấy phân loại kiểu dáng của giày.
     *
     * @return chuỗi loại giày
     */
    public String getLoaiGiay() {
        return loaiGiay;
    }

    /**
     * Cập nhật phân loại kiểu dáng của giày.
     *
     * @param loaiGiay phân loại giày mới
     */
    public void setLoaiGiay(String loaiGiay) {
        this.loaiGiay = loaiGiay;
    }

    /**
     * Lấy thương hiệu sản xuất của sản phẩm.
     *
     * @return chuỗi tên thương hiệu
     */
    public String getThuongHieu() {
        return thuongHieu;
    }

    /**
     * Cập nhật thương hiệu sản xuất của sản phẩm.
     *
     * @param thuongHieu tên thương hiệu mới
     */
    public void setThuongHieu(String thuongHieu) {
        this.thuongHieu = thuongHieu;
    }

    /**
     * Lấy đơn giá nhập hàng từ nhà phân phối.
     *
     * @return đơn giá nhập hàng dạng số thực (VNĐ)
     */
    public double getGiaNhap() {
        return giaNhap;
    }

    /**
     * Cập nhật đơn giá nhập hàng từ nhà phân phối.
     *
     * @param giaNhap đơn giá nhập hàng mới (VNĐ)
     */
    public void setGiaNhap(double giaNhap) {
        this.giaNhap = giaNhap;
    }

    /**
     * Lấy đơn giá bán niêm yết tại quầy.
     *
     * @return đơn giá bán niêm yết dạng số thực (VNĐ)
     */
    public double getGiaBan() {
        return giaBan;
    }

    /**
     * Cập nhật đơn giá bán niêm yết tại quầy.
     *
     * @param giaBan đơn giá bán mới (VNĐ)
     */
    public void setGiaBan(double giaBan) {
        this.giaBan = giaBan;
    }

    /**
     * Lấy chất liệu chính cấu tạo nên sản phẩm.
     *
     * @return chuỗi chất liệu
     */
    public String getChatLieu() {
        return chatLieu;
    }

    /**
     * Cập nhật chất liệu chính cấu tạo nên sản phẩm.
     *
     * @param chatLieu chuỗi chất liệu mới
     */
    public void setChatLieu(String chatLieu) {
        this.chatLieu = chatLieu;
    }

    /**
     * Kiểm tra trạng thái kinh doanh của sản phẩm.
     *
     * @return true nếu đang kinh doanh, false nếu đã ngừng kinh doanh
     */
    public boolean isTrangThai() {
        return trangThai;
    }

    /**
     * Cập nhật trạng thái kinh doanh của sản phẩm.
     *
     * @param trangThai true nếu đang kinh doanh, false nếu ngừng kinh doanh
     */
    public void setTrangThai(boolean trangThai) {
        this.trangThai = trangThai;
    }

    /**
     * Tính mã băm hashCode dựa trên mã sản phẩm duy nhất.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(maSanPham);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Sản phẩm theo mã định danh duy nhất.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng mã sản phẩm, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        SanPham other = (SanPham) obj;
        return Objects.equals(maSanPham, other.maSanPham);
    }

    /**
     * Trả về chuỗi tên sản phẩm kèm thương hiệu để hiển thị trên giao diện người dùng.
     *
     * @return chuỗi tên sản phẩm kèm thương hiệu trong ngoặc
     */
    @Override
    public String toString() {
        return tenSanPham + " (" + thuongHieu + ")";
    }
}

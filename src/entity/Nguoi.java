package entity;

import java.time.LocalDate;

/**
 * Lớp thực thể trừu tượng đại diện cho một người trong hệ thống (tầng Entity),
 * định nghĩa các thuộc tính thông tin cá nhân cơ bản dùng chung cho Nhân viên và Khách hàng.
 */
public abstract class Nguoi {
    protected String hoTen;
    protected String soDienThoai;
    protected LocalDate ngaySinh;
    protected boolean gioiTinh; // true: Nam, false: Nữ
    protected String diaChi;
    protected String email;

    /**
     * Khởi tạo đối tượng Nguoi mặc định không tham số.
     */
    public Nguoi() {
        super();
    }

    /**
     * Khởi tạo đối tượng Nguoi với đầy đủ thông tin cá nhân cơ bản.
     *
     * @param hoTen họ và tên đầy đủ
     * @param soDienThoai số điện thoại liên lạc
     * @param ngaySinh ngày tháng năm sinh
     * @param gioiTinh giới tính (true: Nam, false: Nữ)
     * @param diaChi địa chỉ nơi cư trú
     * @param email địa chỉ thư điện tử
     */
    public Nguoi(String hoTen, String soDienThoai, LocalDate ngaySinh, boolean gioiTinh, String diaChi, String email) {
        this.hoTen = hoTen;
        this.soDienThoai = soDienThoai;
        this.ngaySinh = ngaySinh;
        this.gioiTinh = gioiTinh;
        this.diaChi = diaChi;
        this.email = email;
    }

    /**
     * Lấy họ và tên của người.
     *
     * @return chuỗi họ và tên
     */
    public String getHoTen() {
        return hoTen;
    }

    /**
     * Cập nhật họ và tên của người.
     *
     * @param hoTen chuỗi họ và tên mới
     */
    public void setHoTen(String hoTen) {
        this.hoTen = hoTen;
    }

    /**
     * Lấy số điện thoại liên lạc.
     *
     * @return chuỗi số điện thoại
     */
    public String getSoDienThoai() {
        return soDienThoai;
    }

    /**
     * Cập nhật số điện thoại liên lạc.
     *
     * @param soDienThoai chuỗi số điện thoại mới
     */
    public void setSoDienThoai(String soDienThoai) {
        this.soDienThoai = soDienThoai;
    }

    /**
     * Lấy ngày tháng năm sinh.
     *
     * @return ngày sinh dạng LocalDate
     */
    public LocalDate getNgaySinh() {
        return ngaySinh;
    }

    /**
     * Cập nhật ngày tháng năm sinh.
     *
     * @param ngaySinh ngày sinh mới dạng LocalDate
     */
    public void setNgaySinh(LocalDate ngaySinh) {
        this.ngaySinh = ngaySinh;
    }

    /**
     * Kiểm tra giới tính của người.
     *
     * @return true nếu là Nam, false nếu là Nữ
     */
    public boolean isGioiTinh() {
        return gioiTinh;
    }

    /**
     * Cập nhật giới tính của người.
     *
     * @param gioiTinh true nếu là Nam, false nếu là Nữ
     */
    public void setGioiTinh(boolean gioiTinh) {
        this.gioiTinh = gioiTinh;
    }

    /**
     * Lấy địa chỉ nơi cư trú.
     *
     * @return chuỗi địa chỉ
     */
    public String getDiaChi() {
        return diaChi;
    }

    /**
     * Cập nhật địa chỉ nơi cư trú.
     *
     * @param diaChi chuỗi địa chỉ mới
     */
    public void setDiaChi(String diaChi) {
        this.diaChi = diaChi;
    }

    /**
     * Lấy địa chỉ thư điện tử.
     *
     * @return chuỗi địa chỉ email
     */
    public String getEmail() {
        return email;
    }

    /**
     * Cập nhật địa chỉ thư điện tử.
     *
     * @param email chuỗi địa chỉ email mới
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     * Lấy chuỗi tóm tắt thông tin định danh của người (phương thức trừu tượng thể hiện tính đa hình OOP).
     *
     * @return chuỗi thông tin tóm tắt
     */
    public abstract String getThongTin();

    /**
     * Trả về chuỗi biểu diễn đối tượng người gồm họ tên và số điện thoại.
     *
     * @return chuỗi thông tin gồm họ tên và số điện thoại
     */
    @Override
    public String toString() {
        return hoTen + " - SĐT: " + soDienThoai;
    }
}

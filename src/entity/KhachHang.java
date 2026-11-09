package entity;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Lớp thực thể đại diện cho Khách hàng trong hệ thống (tầng Entity), kế thừa từ Nguoi,
 * quản lý điểm tích lũy, cơ chế xếp hạng thành viên và tỷ lệ chiết khấu ưu đãi.
 */
public class KhachHang extends Nguoi {
    private String maKhachHang;
    private int diemTichLuy;
    private String hangThanhVien; // 'Đồng', 'Bạc', 'Vàng', 'Kim Cương'

    /**
     * Khởi tạo đối tượng Khách hàng mặc định với hạng 'Đồng' và 0 điểm tích lũy.
     */
    public KhachHang() {
        super();
        this.hangThanhVien = "Đồng";
        this.diemTichLuy = 0;
    }

    /**
     * Khởi tạo đối tượng Khách hàng với mã khách hàng định danh.
     *
     * @param maKhachHang mã khách hàng định danh (định dạng KHxxxx)
     */
    public KhachHang(String maKhachHang) {
        this.maKhachHang = maKhachHang;
    }

    /**
     * Khởi tạo đối tượng Khách hàng với đầy đủ thông tin cá nhân, điểm thưởng và hạng thẻ.
     *
     * @param maKhachHang mã khách hàng định danh
     * @param hoTen họ và tên đầy đủ
     * @param soDienThoai số điện thoại liên lạc
     * @param ngaySinh ngày tháng năm sinh
     * @param gioiTinh giới tính (true: Nam, false: Nữ)
     * @param diaChi địa chỉ nơi cư trú
     * @param email địa chỉ thư điện tử
     * @param diemTichLuy số điểm thưởng tích lũy hiện có
     * @param hangThanhVien hạng thẻ thành viên ('Đồng', 'Bạc', 'Vàng', 'Kim Cương')
     */
    public KhachHang(String maKhachHang, String hoTen, String soDienThoai, LocalDate ngaySinh, boolean gioiTinh,
                     String diaChi, String email, int diemTichLuy, String hangThanhVien) {
        super(hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, (email != null && email.trim().isEmpty()) ? null : email);
        this.maKhachHang = maKhachHang;
        this.diemTichLuy = diemTichLuy;
        this.hangThanhVien = hangThanhVien;
    }

    /**
     * Cập nhật địa chỉ email của khách hàng, chuyển chuỗi rỗng thành null để khớp chuẩn CSDL.
     *
     * @param email địa chỉ thư điện tử mới
     */
    @Override
    public void setEmail(String email) {
        super.setEmail((email != null && email.trim().isEmpty()) ? null : email);
    }

    /**
     * Lấy mã khách hàng định danh.
     *
     * @return chuỗi mã khách hàng
     */
    public String getMaKhachHang() {
        return maKhachHang;
    }

    /**
     * Cập nhật mã khách hàng định danh.
     *
     * @param maKhachHang mã khách hàng mới
     */
    public void setMaKhachHang(String maKhachHang) {
        this.maKhachHang = maKhachHang;
    }

    /**
     * Lấy số điểm thưởng tích lũy hiện có.
     *
     * @return số điểm tích lũy nguyên
     */
    public int getDiemTichLuy() {
        return diemTichLuy;
    }

    /**
     * Cập nhật số điểm thưởng tích lũy.
     *
     * @param diemTichLuy số điểm tích lũy mới
     */
    public void setDiemTichLuy(int diemTichLuy) {
        this.diemTichLuy = diemTichLuy;
    }

    /**
     * Lấy tên hạng thẻ thành viên hiện tại.
     *
     * @return chuỗi hạng thành viên ('Đồng', 'Bạc', 'Vàng', 'Kim Cương')
     */
    public String getHangThanhVien() {
        return hangThanhVien;
    }

    /**
     * Cập nhật hạng thẻ thành viên.
     *
     * @param hangThanhVien chuỗi hạng thành viên mới
     */
    public void setHangThanhVien(String hangThanhVien) {
        this.hangThanhVien = hangThanhVien;
    }

    /**
     * Cộng thêm điểm thưởng tích lũy sau giao dịch và tự động cập nhật lại hạng thành viên tương ứng.
     *
     * @param diem số điểm thưởng được cộng thêm
     */
    public void congDiem(int diem) {
        if (diem > 0) {
            this.diemTichLuy += diem;
            capNhatHang();
        }
    }

    /**
     * Tự động xếp hạng thẻ thành viên dựa trên tổng số điểm tích lũy hiện có:
     * - Từ 200 điểm trở lên: Kim Cương
     * - Từ 100 điểm trở lên: Vàng
     * - Từ 30 điểm trở lên: Bạc
     * - Dưới 30 điểm: Đồng
     */
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

    /**
     * Tính tỷ lệ chiết khấu giảm giá hóa đơn theo quy định của từng hạng thành viên.
     *
     * @return tỷ lệ chiết khấu số thực (15% cho Kim Cương, 10% cho Vàng, 5% cho Bạc, 0% cho Đồng)
     */
    public double tinhChietKhau() {
        switch (hangThanhVien) {
            case "Kim Cương": return 0.15; // 15%
            case "Vàng": return 0.10;      // 10%
            case "Bạc": return 0.05;       // 5%
            default: return 0.0;
        }
    }

    /**
     * Lấy chuỗi tóm tắt thông tin mã, tên, hạng và điểm tích lũy của khách hàng.
     *
     * @return chuỗi thông tin tóm tắt khách hàng
     */
    @Override
    public String getThongTin() {
        return "[" + maKhachHang + "] " + hoTen + " - Hạng: " + hangThanhVien + " (" + diemTichLuy + " điểm)";
    }

    /**
     * Tính mã băm hashCode dựa trên mã khách hàng duy nhất.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(maKhachHang);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Khách hàng theo mã định danh duy nhất.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng mã khách hàng, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        KhachHang other = (KhachHang) obj;
        return Objects.equals(maKhachHang, other.maKhachHang);
    }

    /**
     * Trả về chuỗi họ tên kèm số điện thoại để hiển thị trên giao diện người dùng.
     *
     * @return chuỗi họ tên kèm số điện thoại trong ngoặc
     */
    @Override
    public String toString() {
        return hoTen + " (" + soDienThoai + ")";
    }
}

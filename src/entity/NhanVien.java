package entity;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Lớp thực thể đại diện cho Nhân viên trong hệ thống (tầng Entity), kế thừa từ Nguoi,
 * lưu trữ thông tin chức vụ, lương, ca làm việc và phân quyền đăng nhập.
 */
public class NhanVien extends Nguoi {
    private String maNhanVien;
    private String chucVu; // 'Quản lý', 'Nhân viên bán hàng'
    private double luongCoBan;
    private String caLamViec; // 'Ca sáng', 'Ca chiều', 'Ca tối'
    private String matKhau;
    private boolean trangThai; // true: Đang làm, false: Đã nghỉ

    /**
     * Khởi tạo đối tượng Nhân viên mặc định không tham số.
     */
    public NhanVien() {
        super();
    }

    /**
     * Khởi tạo đối tượng Nhân viên với mã nhân viên định danh.
     *
     * @param maNhanVien mã nhân viên định danh (định dạng NVxxxx)
     */
    public NhanVien(String maNhanVien) {
        this.maNhanVien = maNhanVien;
    }

    /**
     * Khởi tạo đối tượng Nhân viên với đầy đủ thông tin cá nhân và hợp đồng làm việc.
     *
     * @param maNhanVien mã nhân viên định danh
     * @param hoTen họ và tên đầy đủ
     * @param soDienThoai số điện thoại liên lạc
     * @param ngaySinh ngày tháng năm sinh
     * @param gioiTinh giới tính (true: Nam, false: Nữ)
     * @param diaChi địa chỉ nơi cư trú
     * @param email địa chỉ thư điện tử
     * @param chucVu chức vụ công tác ('Quản lý' hoặc 'Nhân viên bán hàng')
     * @param luongCoBan mức lương cơ bản (VNĐ)
     * @param caLamViec ca làm việc được phân công
     * @param matKhau chuỗi băm mật khẩu bảo mật
     * @param trangThai trạng thái công tác (true: Đang làm, false: Đã nghỉ)
     */
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

    /**
     * Lấy mã nhân viên định danh.
     *
     * @return chuỗi mã nhân viên
     */
    public String getMaNhanVien() {
        return maNhanVien;
    }

    /**
     * Cập nhật mã nhân viên định danh.
     *
     * @param maNhanVien mã nhân viên mới
     */
    public void setMaNhanVien(String maNhanVien) {
        this.maNhanVien = maNhanVien;
    }

    /**
     * Lấy chức vụ công tác của nhân viên.
     *
     * @return chuỗi chức vụ ('Quản lý' hoặc 'Nhân viên bán hàng')
     */
    public String getChucVu() {
        return chucVu;
    }

    /**
     * Cập nhật chức vụ công tác của nhân viên.
     *
     * @param chucVu chuỗi chức vụ mới
     */
    public void setChucVu(String chucVu) {
        this.chucVu = chucVu;
    }

    /**
     * Lấy mức lương cơ bản theo hợp đồng.
     *
     * @return số tiền lương cơ bản (VNĐ)
     */
    public double getLuongCoBan() {
        return luongCoBan;
    }

    /**
     * Cập nhật mức lương cơ bản theo hợp đồng.
     *
     * @param luongCoBan số tiền lương cơ bản mới (VNĐ)
     */
    public void setLuongCoBan(double luongCoBan) {
        this.luongCoBan = luongCoBan;
    }

    /**
     * Lấy ca làm việc được phân công.
     *
     * @return chuỗi ca làm việc
     */
    public String getCaLamViec() {
        return caLamViec;
    }

    /**
     * Cập nhật ca làm việc được phân công.
     *
     * @param caLamViec chuỗi ca làm việc mới
     */
    public void setCaLamViec(String caLamViec) {
        this.caLamViec = caLamViec;
    }

    /**
     * Lấy chuỗi băm mật khẩu tài khoản.
     *
     * @return chuỗi băm mật khẩu
     */
    public String getMatKhau() {
        return matKhau;
    }

    /**
     * Cập nhật chuỗi băm mật khẩu tài khoản.
     *
     * @param matKhau chuỗi băm mật khẩu mới
     */
    public void setMatKhau(String matKhau) {
        this.matKhau = matKhau;
    }

    /**
     * Kiểm tra trạng thái làm việc của nhân viên.
     *
     * @return true nếu đang làm việc, false nếu đã nghỉ việc
     */
    public boolean isTrangThai() {
        return trangThai;
    }

    /**
     * Cập nhật trạng thái làm việc của nhân viên.
     *
     * @param trangThai true nếu đang làm việc, false nếu đã nghỉ việc
     */
    public void setTrangThai(boolean trangThai) {
        this.trangThai = trangThai;
    }

    /**
     * Kiểm tra nhân viên có giữ vai trò Quản lý hay không để phân quyền truy cập.
     *
     * @return true nếu giữ chức vụ Quản lý, false nếu là Nhân viên thông thường
     */
    public boolean isQuanLy() {
        return "Quản lý".equalsIgnoreCase(this.chucVu);
    }

    /**
     * Tính tổng mức lương thực nhận theo hệ số phụ cấp chức vụ (Quản lý nhân hệ số 1.2).
     *
     * @return số tiền lương thực nhận (VNĐ)
     */
    public double tinhLuong() {
        return isQuanLy() ? this.luongCoBan * 1.2 : this.luongCoBan;
    }

    /**
     * Lấy chuỗi tóm tắt mã, họ tên và chức vụ của nhân viên.
     *
     * @return chuỗi thông tin tóm tắt nhân viên
     */
    @Override
    public String getThongTin() {
        return "[" + maNhanVien + "] " + hoTen + " - Chức vụ: " + chucVu;
    }

    /**
     * Tính mã băm hashCode dựa trên mã nhân viên duy nhất.
     *
     * @return giá trị băm nguyên
     */
    @Override
    public int hashCode() {
        return Objects.hash(maNhanVien);
    }

    /**
     * So sánh tính bằng nhau giữa hai đối tượng Nhân viên theo mã nhân viên định danh.
     *
     * @param obj đối tượng cần so sánh
     * @return true nếu cùng mã nhân viên, ngược lại false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        NhanVien other = (NhanVien) obj;
        return Objects.equals(maNhanVien, other.maNhanVien);
    }

    /**
     * Trả về chuỗi họ tên kèm mã nhân viên để hiển thị trên giao diện người dùng.
     *
     * @return chuỗi họ tên kèm mã nhân viên trong ngoặc
     */
    @Override
    public String toString() {
        return hoTen + " (" + maNhanVien + ")";
    }
}

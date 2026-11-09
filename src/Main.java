import connectDB.ConnectDB;
import gui.DangNhap_GUI;

import javax.swing.*;
import java.sql.SQLException;

/**
 * Điểm khởi chạy chính của ứng dụng Quản lý bán hàng cửa hàng giày dép StepUp.
 */
public class Main {
    /**
     * Phương thức khởi động ứng dụng, thiết lập giao diện hệ thống, kết nối cơ sở dữ liệu và hiển thị màn hình đăng nhập.
     *
     * @param args mảng tham số dòng lệnh truyền vào khi khởi chạy chương trình
     */
    public static void main(String[] args) {
        // Cài đặt Look & Feel hệ thống
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            ConnectDB.getInstance().connect();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        SwingUtilities.invokeLater(() -> {
            // Khởi động màn hình Đăng Nhập
            DangNhap_GUI login = new DangNhap_GUI();
            login.setVisible(true);
        });
    }
}

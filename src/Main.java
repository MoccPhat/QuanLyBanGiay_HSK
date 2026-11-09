import connectDB.ConnectDB;
import gui.DangNhap_GUI;

import javax.swing.*;
import java.sql.SQLException;

public class Main {
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

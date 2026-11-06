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

        SwingUtilities.invokeLater(() -> {
            try {
                ConnectDB.getInstance().connect();
                System.out.println("Kết nối Microsoft SQL Server thành công!");
            } catch (SQLException e) {
                System.err.println("Chưa khởi động SQL Server hoặc cổng TCP 1433 chưa mở: " + e.getMessage());
            }

            // Khởi động màn hình Đăng Nhập
            DangNhap_GUI login = new DangNhap_GUI();
            login.setVisible(true);
        });
    }
}

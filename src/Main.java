import connectDB.ConnectDB;
import dao.NhanVien_DAO;
import entity.NhanVien;
import gui.ManHinhChinh_GUI;

import javax.swing.*;
import java.sql.SQLException;
import java.time.LocalDate;

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
                System.err.println("Thông báo: Chưa kết nối SQL Server, đang chạy chế độ Demo.");
            }

            // Bỏ qua hoàn toàn đăng nhập, vào thẳng Màn hình Quản lý với tài khoản Quản lý cửa hàng
            NhanVien nv = new NhanVien("NV0001", "Nguyễn Trọng Vinh", "0912345678",
                    LocalDate.of(2004, 5, 12), true,
                    "12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM", "trongvinh@stepup.vn",
                    "Quản lý", 12000000, "Toàn thời gian", "123456", true);

            ManHinhChinh_GUI mainFrame = new ManHinhChinh_GUI(nv);
            mainFrame.setVisible(true);
        });
    }
}

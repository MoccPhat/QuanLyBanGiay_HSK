package test;

import connectDB.ConnectDB;
import dao.NhanVien_DAO;
import entity.NhanVien;
import gui.*;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.lang.reflect.Field;
import java.time.LocalDate;

public class CaptureScreenshots {
    public static void main(String[] args) {
        try {
            System.out.println(">>> Đang kết nối CSDL và khởi tạo giao diện Swing...");
            ConnectDB.getInstance().connect();
            NhanVien_DAO nvDao = new NhanVien_DAO();
            NhanVien admin = nvDao.dangNhap("NV0001", "123456");
            if (admin == null) {
                admin = new NhanVien("NV0001", "Nguyễn Trọng Vinh", "0901234567", LocalDate.of(1990, 1, 1), true, "123 Quang Trung, Gò Vấp", "vinh@stepup.vn", "Quản lý", 15000000, "Toàn thời gian", "123456", true);
            }

            // 1. Chụp màn hình Đăng Nhập
            DangNhap_GUI dangNhap = new DangNhap_GUI();
            try {
                Field fMa = DangNhap_GUI.class.getDeclaredField("txtMaNV");
                fMa.setAccessible(true);
                JTextField txtMa = (JTextField) fMa.get(dangNhap);
                txtMa.setText("NV0001");

                Field fMk = DangNhap_GUI.class.getDeclaredField("txtMatKhau");
                fMk.setAccessible(true);
                JPasswordField txtMk = (JPasswordField) fMk.get(dangNhap);
                txtMk.setText("123456");
            } catch (Exception ignored) {}

            dangNhap.pack();
            dangNhap.setSize(480, 320);
            dangNhap.setLocationRelativeTo(null);
            dangNhap.setVisible(true);
            Thread.sleep(700);
            saveComponent(dangNhap, "screenshot_dangnhap.png");
            dangNhap.dispose();

            // 2. Chụp các tab Màn Hình Chính
            ManHinhChinh_GUI mainFrame = new ManHinhChinh_GUI(admin);
            mainFrame.setSize(1350, 800);
            mainFrame.setLocationRelativeTo(null);
            mainFrame.setVisible(true);
            Thread.sleep(1200);

            Field fTab = ManHinhChinh_GUI.class.getDeclaredField("tabbedPane");
            fTab.setAccessible(true);
            JTabbedPane tabs = (JTabbedPane) fTab.get(mainFrame);

            // Tab 0: Bán hàng (POS)
            tabs.setSelectedIndex(0);
            Thread.sleep(800);
            saveComponent(mainFrame, "screenshot_banhang.png");

            // Tab 1: Mẫu giày
            tabs.setSelectedIndex(1);
            Thread.sleep(800);
            saveComponent(mainFrame, "screenshot_sanpham.png");

            // Tab 2: Khách hàng
            tabs.setSelectedIndex(2);
            Thread.sleep(800);
            saveComponent(mainFrame, "screenshot_khachhang.png");

            // Tab 3: Nhân sự
            tabs.setSelectedIndex(3);
            Thread.sleep(800);
            saveComponent(mainFrame, "screenshot_nhanvien.png");

            mainFrame.dispose();
            System.out.println("=== TOÀN BỘ 5 ẢNH CHỤP ỨNG DỤNG THẬT ĐÃ HOÀN TẤT ===");
            System.exit(0);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static void saveComponent(Component comp, String filename) throws Exception {
        BufferedImage img = new BufferedImage(comp.getWidth(), comp.getHeight(), BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = img.createGraphics();
        comp.paint(g2);
        g2.dispose();
        ImageIO.write(img, "png", new File(filename));
        System.out.println(" [PASS] Đã chụp: " + filename + " (" + comp.getWidth() + "x" + comp.getHeight() + ")");
    }
}

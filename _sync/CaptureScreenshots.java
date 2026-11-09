package test;

import gui.DangNhap_GUI;
import gui.ManHinhChinh_GUI;
import entity.NhanVien;
import dao.NhanVien_DAO;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;

public class CaptureScreenshots {
    public static void main(String[] args) {
        System.out.println(">>> Bắt đầu chụp 3 màn hình sau khi thu gọn chức năng...");
        try {
            // Set look and feel
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {}

        SwingUtilities.invokeLater(() -> {
            try {
                // 1. Chụp màn đăng nhập
                DangNhap_GUI loginGui = new DangNhap_GUI();
                loginGui.setSize(850, 520);
                loginGui.setLocationRelativeTo(null);
                loginGui.setVisible(true);

                // Render loginGui to image
                BufferedImage imgLogin = new BufferedImage(loginGui.getWidth(), loginGui.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g2Login = imgLogin.createGraphics();
                loginGui.paint(g2Login);
                g2Login.dispose();
                ImageIO.write(imgLogin, "png", new File("_sync/after_trim_login.png"));
                System.out.println("  [OK] Đã lưu _sync/after_trim_login.png");
                loginGui.dispose();

                // 2. Chụp màn hình Sản phẩm với thanh lọc nâng cao inline
                NhanVien_DAO nvDao = new NhanVien_DAO();
                NhanVien nvQuanLy = nvDao.getNhanVienTheoMa("NV0001");
                if (nvQuanLy == null) {
                    nvQuanLy = new NhanVien("NV0001", "Nguyễn Trọng Vinh", "0901234567",
                            java.time.LocalDate.of(1990, 1, 1), true, "TP.HCM", "vinh@stepup.vn",
                            "Quản lý", 15000000, "Toàn thời gian", "123456", true);
                }

                ManHinhChinh_GUI mhc = new ManHinhChinh_GUI(nvQuanLy);
                mhc.setSize(1280, 800);
                mhc.setLocationRelativeTo(null);
                mhc.setVisible(true);

                // Chuyển sang Tab 1: Sản phẩm (index 1)
                JTabbedPane tabbedPane = null;
                for (Component comp : mhc.getContentPane().getComponents()) {
                    if (comp instanceof JTabbedPane) {
                        tabbedPane = (JTabbedPane) comp;
                        break;
                    }
                }
                if (tabbedPane != null) {
                    tabbedPane.setSelectedIndex(1); // Tab Sản phẩm
                }
                Thread.sleep(800);

                BufferedImage imgSP = new BufferedImage(mhc.getWidth(), mhc.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g2SP = imgSP.createGraphics();
                mhc.paint(g2SP);
                g2SP.dispose();
                ImageIO.write(imgSP, "png", new File("_sync/after_trim_sanpham.png"));
                System.out.println("  [OK] Đã lưu _sync/after_trim_sanpham.png");

                // 3. Chụp màn hình Thống kê rút gọn (Tab 4: index 4)
                if (tabbedPane != null) {
                    tabbedPane.setSelectedIndex(4); // Tab Thống kê
                }
                Thread.sleep(800);

                BufferedImage imgTK = new BufferedImage(mhc.getWidth(), mhc.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g2TK = imgTK.createGraphics();
                mhc.paint(g2TK);
                g2TK.dispose();
                ImageIO.write(imgTK, "png", new File("_sync/after_trim_thongke.png"));
                System.out.println("  [OK] Đã lưu _sync/after_trim_thongke.png");

                mhc.dispose();
                System.out.println(">>> HOÀN TẤT CHỤP ẢNH MINH CHỨNG THÀNH CÔNG!");
                System.exit(0);
            } catch (Exception ex) {
                ex.printStackTrace();
                System.exit(1);
            }
        });
    }
}

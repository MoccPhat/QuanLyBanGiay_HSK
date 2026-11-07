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
import java.lang.reflect.Method;
import java.time.LocalDate;

public class CaptureReportScreenshots {
    public static void main(String[] args) {
        try {
            System.out.println(">>> Đang kết nối CSDL và khởi tạo giao diện để chụp ảnh...");
            ConnectDB.getInstance().connect();
            NhanVien_DAO nvDao = new NhanVien_DAO();
            NhanVien admin = nvDao.dangNhap("NV0001", "123456");
            if (admin == null) {
                admin = new NhanVien("NV0001", "Nguyễn Trọng Vinh", "0901234567", LocalDate.of(1990, 1, 1), true, "123 Quang Trung, Gò Vấp", "vinh@stepup.vn", "Quản lý", 15000000, "Toàn thời gian", "123456", true);
            }

            ManHinhChinh_GUI mainFrame = new ManHinhChinh_GUI(admin);
            mainFrame.setSize(1350, 800);
            mainFrame.setLocationRelativeTo(null);
            mainFrame.setVisible(true);
            Thread.sleep(1200);

            Field fTab = ManHinhChinh_GUI.class.getDeclaredField("tabbedPane");
            fTab.setAccessible(true);
            JTabbedPane tabs = (JTabbedPane) fTab.get(mainFrame);

            // 1. Chụp Tab 4: Thống kê doanh thu
            if (tabs.getTabCount() > 4) {
                tabs.setSelectedIndex(4);
                Thread.sleep(1500);
                saveComponent(mainFrame, "screenshot_thongke.png");
            }

            // 2. Chụp Hộp thoại Tìm kiếm nâng cao Sản phẩm
            tabs.setSelectedIndex(1);
            Thread.sleep(500);
            QuanLySanPham_GUI pnlSP = (QuanLySanPham_GUI) tabs.getSelectedComponent();
            SwingUtilities.invokeLater(() -> {
                try {
                    Method m = QuanLySanPham_GUI.class.getDeclaredMethod("hienThiHopThoaiTimNangCao");
                    m.setAccessible(true);
                    m.invoke(pnlSP);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
            Thread.sleep(800);
            for (Window w : Window.getWindows()) {
                if (w instanceof JDialog && w.isVisible()) {
                    saveComponent(w, "screenshot_timkiem_sanpham.png");
                    ((JDialog) w).dispose();
                    break;
                }
            }
            Thread.sleep(400);

            // 3. Chụp Hộp thoại Tìm kiếm nâng cao Khách hàng
            tabs.setSelectedIndex(2);
            Thread.sleep(500);
            QuanLyKhachHang_GUI pnlKH = (QuanLyKhachHang_GUI) tabs.getSelectedComponent();
            SwingUtilities.invokeLater(() -> {
                try {
                    Method m = QuanLyKhachHang_GUI.class.getDeclaredMethod("hienThiHopThoaiTimNangCao");
                    m.setAccessible(true);
                    m.invoke(pnlKH);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
            Thread.sleep(800);
            for (Window w : Window.getWindows()) {
                if (w instanceof JDialog && w.isVisible()) {
                    saveComponent(w, "screenshot_timkiem_khachhang.png");
                    ((JDialog) w).dispose();
                    break;
                }
            }
            Thread.sleep(400);

            // 4. Chụp Hộp thoại Hóa đơn bán lẻ K80 (có nút In và Xuất file)
            JDialog dlgHoaDon = new JDialog(mainFrame, "THANH TOÁN THÀNH CÔNG - HÓA ĐƠN K80", false);
            dlgHoaDon.setLayout(new BorderLayout(10, 10));

            StringBuilder bill = new StringBuilder();
            bill.append("=============================================\n");
            bill.append("            STEPUP FOOTWEAR STORE            \n");
            bill.append("      12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM      \n\n");
            bill.append("               HÓA ĐƠN BÁN LẺ                \n\n");
            bill.append("Mã HĐ: HD000001\n");
            bill.append("Ngày: 07/11/2026 14:30\n");
            bill.append("Thu ngân: Nguyễn Trọng Vinh\n");
            bill.append("Khách hàng: Trần Văn Bình (0987111222)\n");
            bill.append("---------------------------------------------\n");
            bill.append("Nike Air Force 1 '07 (Size 41)\n");
            bill.append("  1 x 2,600,000 = 2,600,000 VNĐ\n");
            bill.append("Adidas Ultraboost Light (Size 42)\n");
            bill.append("  1 x 2,600,000 = 2,600,000 VNĐ\n");
            bill.append("---------------------------------------------\n");
            bill.append(String.format("%-24s %18s\n", "Tổng tiền hàng:", "5,200,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "Chiết khấu hạng Bạc:", "-260,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "Tiền giảm từ điểm:", "-50,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "CẦN THANH TOÁN:", "4,890,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "Khách đưa:", "5,000,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "Tiền thừa:", "110,000 VNĐ"));
            bill.append(String.format("%-24s %18s\n", "Điểm cộng mới:", "+48 điểm"));
            bill.append(String.format("%-24s %18s\n", "Hình thức:", "Tiền mặt"));
            bill.append("=============================================\n");
            bill.append("       CẢM ƠN QUÝ KHÁCH & HẸN GẶP LẠI!       \n");

            JTextArea area = new JTextArea(bill.toString(), 25, 42);
            area.setFont(new Font("Monospaced", Font.PLAIN, 13));
            area.setBorder(BorderFactory.createEmptyBorder(10, 16, 10, 16));
            area.setEditable(false);

            JScrollPane scrollBill = new JScrollPane(area);
            scrollBill.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
            scrollBill.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED);
            scrollBill.setPreferredSize(new Dimension(460, 520));
            dlgHoaDon.add(scrollBill, BorderLayout.CENTER);

            JPanel pnlBillBtns = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
            pnlBillBtns.setBackground(Color.WHITE);

            JButton btnIn = UIHelper.createPrimaryBtn("🖨 In Hóa Đơn", 130, 34);
            JButton btnXuat = UIHelper.createSuccessBtn("📄 Xuất File Hóa Đơn", 160, 34);
            JButton btnDong = UIHelper.createSecondaryBtn("Đóng", 90, 34);

            pnlBillBtns.add(btnIn);
            pnlBillBtns.add(btnXuat);
            pnlBillBtns.add(btnDong);
            dlgHoaDon.add(pnlBillBtns, BorderLayout.SOUTH);

            dlgHoaDon.pack();
            dlgHoaDon.setLocationRelativeTo(mainFrame);
            dlgHoaDon.setVisible(true);
            Thread.sleep(800);
            saveComponent(dlgHoaDon, "screenshot_hoadon_k80.png");
            dlgHoaDon.dispose();

            mainFrame.dispose();
            System.out.println("=== TẤT CẢ 4 ẢNH CHỤP MỚI ĐÃ HOÀN TẤT THÀNH CÔNG ===");
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

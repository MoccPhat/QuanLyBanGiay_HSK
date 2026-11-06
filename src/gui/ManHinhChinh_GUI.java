package gui;

import entity.NhanVien;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ManHinhChinh_GUI extends JFrame implements ActionListener {
    private NhanVien nhanVien;
    private JTabbedPane tabbedPane;
    private JButton btnThoat;

    public ManHinhChinh_GUI(NhanVien nv) {
        this.nhanVien = nv;

        setTitle("HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG - STEPUP POS");
        setSize(1350, 800);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // Header trên cùng
        JPanel pnlHeader = buildHeaderPanel();
        add(pnlHeader, BorderLayout.NORTH);

        // JTabbedPane chứa các phân hệ
        tabbedPane = new JTabbedPane(JTabbedPane.TOP);
        tabbedPane.setFont(new Font("Arial", Font.BOLD, 13));

        // 1. Phân hệ Quản lý sản phẩm giày (Vào thẳng trang Quản lý khi khởi động)
        tabbedPane.addTab("👟 QUẢN LÝ MẪU GIÀY [F1]", new QuanLySanPham_GUI());

        // 2. Phân hệ Bán hàng (POS)
        tabbedPane.addTab("🛒 BÁN HÀNG (POS) [F2]", new BanHang_GUI(nhanVien));

        // 3. Phân hệ Khách hàng
        tabbedPane.addTab("👥 KHÁCH HÀNG & TÍCH ĐIỂM [F3]", new QuanLyKhachHang_GUI());

        // 4. Phân hệ Nhân viên (Chỉ mở nếu là Quản lý)
        if (nhanVien.isQuanLy()) {
            tabbedPane.addTab("👔 QUẢN LÝ NHÂN SỰ [F4]", new QuanLyNhanVien_GUI());
        }

        // 5. Phân hệ Báo cáo Thống kê
        tabbedPane.addTab("📊 BÁO CÁO THỐNG KÊ [F5]", new ThongKe_GUI());

        // Đảm bảo mở ngay trang Quản lý khi khởi động
        tabbedPane.setSelectedIndex(0);

        add(tabbedPane, BorderLayout.CENTER);

        // Đăng ký phím tắt toàn cục [F1]..[F5] & [ESC]
        KeyboardFocusManager.getCurrentKeyboardFocusManager().addKeyEventDispatcher(e -> {
            if (e.getID() == KeyEvent.KEY_PRESSED) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_F1:
                        if (tabbedPane.getTabCount() > 0) tabbedPane.setSelectedIndex(0);
                        return true;
                    case KeyEvent.VK_F2:
                        if (tabbedPane.getTabCount() > 1) tabbedPane.setSelectedIndex(1);
                        return true;
                    case KeyEvent.VK_F3:
                        if (tabbedPane.getTabCount() > 2) tabbedPane.setSelectedIndex(2);
                        return true;
                    case KeyEvent.VK_F4:
                        if (tabbedPane.getTabCount() > 3) tabbedPane.setSelectedIndex(3);
                        return true;
                    case KeyEvent.VK_F5:
                        if (tabbedPane.getTabCount() > 4) tabbedPane.setSelectedIndex(4);
                        return true;
                    case KeyEvent.VK_ESCAPE:
                        btnThoat.doClick();
                        return true;
                }
            }
            return false;
        });

        // Footer dưới cùng
        JPanel pnlFooter = new JPanel(new FlowLayout(FlowLayout.RIGHT, 20, 4));
        pnlFooter.setBackground(new Color(241, 245, 249));
        JLabel lblHotkeys = new JLabel("Phím tắt: [F1] Giày | [F2] POS | [F3] Khách | [F4] Nhân sự | [F5] Thống kê | [ESC] Thoát");
        lblHotkeys.setFont(new Font("Arial", Font.ITALIC, 11));
        lblHotkeys.setForeground(new Color(100, 116, 139));
        pnlFooter.add(lblHotkeys);
        add(pnlFooter, BorderLayout.SOUTH);
    }

    private JPanel buildHeaderPanel() {
        JPanel pnl = new JPanel(new BorderLayout());
        pnl.setBackground(new Color(30, 58, 138)); // Xanh navy đậm phong cách IUH
        pnl.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));

        // Logo & Tên cửa hàng
        JLabel lblBrand = new JLabel("STEPUP FOOTWEAR POS - QUẢN LÝ BÁN HÀNG GIÀY DÉP");
        lblBrand.setFont(new Font("Arial", Font.BOLD, 16));
        lblBrand.setForeground(Color.WHITE);
        pnl.add(lblBrand, BorderLayout.WEST);

        // Thông tin thu ngân
        JPanel pnlUser = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 0));
        pnlUser.setOpaque(false);

        String info = "Nhân viên: " + nhanVien.getHoTen() + " (" + nhanVien.getChucVu() + ")";
        JLabel lblUser = new JLabel(info);
        lblUser.setFont(new Font("Arial", Font.BOLD, 13));
        lblUser.setForeground(new Color(254, 240, 138)); // Vàng nhạt nổi bật

        btnThoat = UIHelper.createDangerBtn("Thoát", 90, 32);
        btnThoat.addActionListener(this);

        pnlUser.add(lblUser);
        pnlUser.add(btnThoat);
        pnl.add(pnlUser, BorderLayout.EAST);

        return pnl;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource().equals(btnThoat)) {
            int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc chắn muốn thoát ứng dụng?", "Thoát ứng dụng", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                System.exit(0);
            }
        }
    }
}

package gui;

import entity.NhanVien;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Cửa sổ làm việc chính của hệ thống StepUp Footwear POS.
 * Điều phối các phân hệ chức năng thông qua JTabbedPane:
 * - Tab 0: Bán hàng tại quầy (POS) [F1]
 * - Tab 1: Quản lý danh mục mẫu giày [F2]
 * - Tab 2: Quản lý khách hàng & tích điểm [F3]
 * - Tab 3: Quản lý nhân sự (chỉ dành cho Quản lý) [F4]
 * 
 * Tính năng nâng cao:
 * - Hệ thống phím tắt toàn cục hoạt động 100% (F1-F4, F10, ESC, DEL).
 * - ChangeListener tự động làm mới danh sách sản phẩm khi chuyển về tab Bán hàng (C7).
 */
public class ManHinhChinh_GUI extends JFrame implements ActionListener {
    private NhanVien nhanVien;
    private JTabbedPane tabbedPane;
    private JButton btnDangXuat;

    public ManHinhChinh_GUI(NhanVien nv) {
        this.nhanVien = nv;

        setTitle("HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG - STEPUP POS");
        setSize(1350, 800);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // 1. Header trên cùng
        JPanel pnlHeader = buildHeaderPanel();
        add(pnlHeader, BorderLayout.NORTH);

        // 2. JTabbedPane chứa các phân hệ
        tabbedPane = new JTabbedPane(JTabbedPane.TOP);
        tabbedPane.setFont(new Font("Arial", Font.BOLD, 13));

        // Phân hệ 1: Bán hàng (POS)
        tabbedPane.addTab("🛒 BÁN HÀNG (POS) [F1]", new BanHang_GUI(nhanVien));

        // Phân hệ 2: Quản lý mẫu giày
        tabbedPane.addTab("👟 QUẢN LÝ MẪU GIÀY [F2]", new QuanLySanPham_GUI(nhanVien));

        // Phân hệ 3: Khách hàng
        tabbedPane.addTab("👥 KHÁCH HÀNG & TÍCH ĐIỂM [F3]", new QuanLyKhachHang_GUI(nhanVien));

        // Phân hệ 4 & 5: Nhân sự & Thống kê (Chỉ mở nếu là Quản lý - L06)
        if (nhanVien != null && nhanVien.isQuanLy()) {
            tabbedPane.addTab("👔 QUẢN LÝ NHÂN SỰ [F4]", new QuanLyNhanVien_GUI());
            tabbedPane.addTab("📊 THỐNG KÊ DOANH THU [F5]", new ThongKe_GUI());
        }

        // C7: Khi chuyển tab về Bán hàng (tab 0), tự động đồng bộ lại danh sách sản phẩm mới
        tabbedPane.addChangeListener(e -> {
            if (tabbedPane.getSelectedIndex() == 0) {
                Component comp = tabbedPane.getComponentAt(0);
                if (comp instanceof BanHang_GUI) {
                    ((BanHang_GUI) comp).taiLaiDanhSachSanPham();
                }
            }
        });

        add(tabbedPane, BorderLayout.CENTER);

        // 3. Đăng ký Key Bindings toàn cục trên rootPane cho các phím F1, F2, F3, F4, F10, ESC, DELETE
        registerKeyBindings();

        // 4. Footer dưới cùng
        JPanel pnlFooter = new JPanel(new FlowLayout(FlowLayout.RIGHT, 20, 4));
        pnlFooter.setBackground(new Color(241, 245, 249));
        JLabel lblHotkeys = new JLabel("Phím tắt: [F1] Bán hàng | [F2] Mẫu giày | [F3] Khách hàng | [F4] Nhân sự | [F5] Thống kê | [F10] Thanh toán | [Del] Xóa giỏ");
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

        String hoTen = (nhanVien != null) ? nhanVien.getHoTen() : "Nhân viên";
        String chucVu = (nhanVien != null) ? nhanVien.getChucVu() : "";
        String info = "Nhân viên: " + hoTen + (chucVu.isEmpty() ? "" : " (" + chucVu + ")");
        JLabel lblUser = new JLabel(info);
        lblUser.setFont(new Font("Arial", Font.BOLD, 13));
        lblUser.setForeground(new Color(254, 240, 138)); // Vàng nhạt nổi bật

        btnDangXuat = UIHelper.createDangerBtn("Đăng Xuất", 100, 30);
        btnDangXuat.addActionListener(this);

        pnlUser.add(lblUser);
        pnlUser.add(btnDangXuat);
        pnl.add(pnlUser, BorderLayout.EAST);

        return pnl;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource().equals(btnDangXuat)) {
            int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?", "Đăng xuất", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                this.dispose();
                new DangNhap_GUI().setVisible(true);
            }
        }
    }

    public void dangXuat() {
        btnDangXuat.doClick();
    }

    /**
     * Đăng ký phím tắt toàn cục trên JRootPane (WHEN_IN_FOCUSED_WINDOW).
     * Bất kể con trỏ đang ở ô nhập hay bảng nào trong cửa sổ, các phím đều hoạt động.
     */
    private void registerKeyBindings() {
        JRootPane rp = getRootPane();
        InputMap im = rp.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
        ActionMap am = rp.getActionMap();

        // F1: Chuyển về Tab Bán Hàng
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F1, 0), "KEY_F1");
        am.put("KEY_F1", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getTabCount() > 0) tabbedPane.setSelectedIndex(0);
            }
        });

        // F2: Chuyển sang Tab Quản lý mẫu giày
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F2, 0), "KEY_F2");
        am.put("KEY_F2", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getTabCount() > 1) tabbedPane.setSelectedIndex(1);
            }
        });

        // F3: Chuyển sang Tab Khách hàng
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F3, 0), "KEY_F3");
        am.put("KEY_F3", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getTabCount() > 2) tabbedPane.setSelectedIndex(2);
            }
        });

        // F4: Chuyển sang Tab Nhân sự (nếu có quyền Quản lý)
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F4, 0), "KEY_F4");
        am.put("KEY_F4", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getTabCount() > 3) tabbedPane.setSelectedIndex(3);
            }
        });

        // F5: Chuyển sang Tab Thống kê (nếu có quyền Quản lý)
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F5, 0), "KEY_F5");
        am.put("KEY_F5", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getTabCount() > 4) tabbedPane.setSelectedIndex(4);
            }
        });

        // ESC: Mở hộp thoại xác nhận đăng xuất
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_ESCAPE, 0), "KEY_ESC");
        am.put("KEY_ESC", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                dangXuat();
            }
        });

        // F10: Thực hiện thanh toán đơn hàng (chỉ khi đang ở tab POS - tab 0)
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F10, 0), "KEY_F10");
        am.put("KEY_F10", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getSelectedIndex() == 0) {
                    Component c0 = tabbedPane.getComponentAt(0);
                    if (c0 instanceof BanHang_GUI) {
                        ((BanHang_GUI) c0).thanhToanDonHang();
                    }
                }
            }
        });

        // DELETE: Xóa sản phẩm đang chọn trong giỏ hàng (chỉ khi đang ở tab POS - tab 0)
        im.put(KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_DELETE, 0), "KEY_DELETE");
        am.put("KEY_DELETE", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (tabbedPane.getSelectedIndex() == 0) {
                    Component c0 = tabbedPane.getComponentAt(0);
                    if (c0 instanceof BanHang_GUI) {
                        ((BanHang_GUI) c0).xoaMucKhoiGio();
                    }
                }
            }
        });
    }

    public JTabbedPane getTabbedPane() {
        return tabbedPane;
    }
}

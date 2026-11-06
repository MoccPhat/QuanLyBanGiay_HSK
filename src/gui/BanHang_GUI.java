package gui;

import dao.ChiTietGiay_DAO;
import dao.HoaDon_DAO;
import dao.KhachHang_DAO;
import dao.SanPham_DAO;
import entity.*;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.text.DecimalFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.List;

/**
 * Phân hệ Bán Hàng Tại Quầy (POS - Point of Sale).
 * Được tối ưu hóa toàn diện theo Clean Code:
 * 1. [C1] Hệ thống phím tắt đa tầng: F1 (POS), F2 (Chọn giày), F10 (Thanh toán), DEL (Xóa giỏ), ESC (Đăng xuất).
 * 2. [C3, K6] Cơ chế làm mới đơn hàng lamMoiDonHang() dọn sạch dữ liệu khách cũ sau thanh toán.
 * 3. [C5, K7] Kiểm soát ngoại lệ NumberFormatException khi khách nhập chữ hoặc để trống ô tiền.
 * 4. [C7, K9] Đồng bộ danh sách sản phẩm tức thì qua taiLaiDanhSachSanPham() khi có mẫu giày mới.
 * 5. [B1, B2] Kết nối với HoaDon_DAO thực hiện giao dịch toàn vẹn, bảo toàn tiền chiết khấu và trừ điểm.
 */
public class BanHang_GUI extends JPanel implements ActionListener {
    // Thông tin phiên đăng nhập
    private NhanVien nhanVienDangNhap;
    private KhachHang khachHienTai;

    // DAO
    private SanPham_DAO sanPhamDAO;
    private ChiTietGiay_DAO chiTietGiayDAO;
    private KhachHang_DAO kh_dao;
    private HoaDon_DAO hd_dao;

    // Dữ liệu bộ nhớ tạm
    private List<ChiTietGiay> dsChiTietGiay;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    // Component vùng Chọn Sản Phẩm
    private JComboBox<String> cboSanPham;
    private JComboBox<String> cboSize;
    private JComboBox<String> cboMauSac;
    private JSpinner spnSoLuong;
    private JLabel lblTonKhoVal;
    private JLabel lblDonGiaVal;
    private JButton btnThemGio;

    // Component vùng Giỏ Hàng
    private JTable tableGioHang;
    private DefaultTableModel modelGioHang;
    private JButton btnXoaKhoiGio;
    private JButton btnXoaTrangGio;

    // Component vùng Khách Hàng & Thanh Toán
    private JTextField txtSDTKhach;
    private JButton btnTimKhach;
    private JLabel lblTenKhachVal;
    private JLabel lblHangTheVal;
    private JLabel lblDiemVal;
    private JCheckBox chkDungDiem;

    private JLabel lblTongTienHangVal;
    private JLabel lblChietKhauVal;
    private JLabel lblKhachCanTraVal;

    private JComboBox<String> cboPhuongThuc;
    private JTextField txtTienKhachDua;
    private JLabel lblTienThuaVal;
    private JButton btnThanhToan;

    // Biến tính toán tổng tiền
    private double tongTienGoc = 0;
    private double tongTienGiam = 0;
    private double khachCanTra = 0;

    public BanHang_GUI(NhanVien nv) {
        this.nhanVienDangNhap = nv;
        this.sanPhamDAO = new SanPham_DAO();
        this.chiTietGiayDAO = new ChiTietGiay_DAO();
        this.kh_dao = new KhachHang_DAO();
        this.hd_dao = new HoaDon_DAO();

        loadDataBienThe();

        setLayout(new BorderLayout(8, 8));
        setBackground(new Color(241, 245, 249)); // Màu xám nhạt hiện đại
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));

        // Cột trái: Chọn sản phẩm & Giỏ hàng
        JPanel pnlTrai = new JPanel(new BorderLayout(0, 8));
        pnlTrai.setOpaque(false);
        pnlTrai.add(buildChonSanPhamPanel(), BorderLayout.NORTH);
        pnlTrai.add(buildGioHangPanel(), BorderLayout.CENTER);

        // Cột phải: Thông tin khách hàng & Khung tính tiền
        JPanel pnlPhai = buildThanhToanPanel();
        pnlPhai.setPreferredSize(new Dimension(420, 0));

        add(pnlTrai, BorderLayout.CENTER);
        add(pnlPhai, BorderLayout.EAST);

        // Đăng ký sự kiện và phím tắt đa tầng
        registerEvents();

        // Khởi tạo trạng thái ban đầu: nạp toàn bộ danh mục sản phẩm
        taiLaiDanhSachSanPham();
    }

    private void loadDataBienThe() {
        dsChiTietGiay = chiTietGiayDAO.getAllChiTietGiay();
        if (dsChiTietGiay == null) dsChiTietGiay = new ArrayList<>();
    }

    /**
     * Vùng chọn sản phẩm mẫu, kích cỡ, màu sắc và số lượng mua.
     */
    private JPanel buildChonSanPhamPanel() {
        JPanel pnl = new JPanel(new BorderLayout());
        pnl.setBackground(Color.WHITE);
        pnl.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "1. CHỌN MẪU GIÀY & KÍCH CỠ",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));

        JPanel pnlChon = new JPanel(new GridBagLayout());
        pnlChon.setOpaque(false);
        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(4, 8, 4, 8);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Dòng 1: Mẫu giày
        g.gridx = 0; g.gridy = 0;
        pnlChon.add(new JLabel("Mẫu giày:"), g);

        cboSanPham = new JComboBox<>();
        cboSanPham.setFont(new Font("Arial", Font.PLAIN, 13));
        cboSanPham.setPreferredSize(new Dimension(280, 30));

        g.gridx = 1; g.gridy = 0; g.gridwidth = 3;
        pnlChon.add(cboSanPham, g);

        // Dòng 2: Kích cỡ & Màu sắc
        g.gridwidth = 1;
        g.gridx = 0; g.gridy = 1;
        pnlChon.add(new JLabel("Kích cỡ (Size):"), g);

        cboSize = new JComboBox<>();
        cboSize.setFont(new Font("Arial", Font.BOLD, 13));
        cboSize.setPreferredSize(new Dimension(100, 30));
        g.gridx = 1; g.gridy = 1;
        pnlChon.add(cboSize, g);

        g.gridx = 2; g.gridy = 1;
        pnlChon.add(new JLabel("Màu sắc:"), g);

        cboMauSac = new JComboBox<>();
        cboMauSac.setFont(new Font("Arial", Font.BOLD, 13));
        cboMauSac.setPreferredSize(new Dimension(140, 30));
        g.gridx = 3; g.gridy = 1;
        pnlChon.add(cboMauSac, g);

        // Dòng 3: Tồn kho & Đơn giá
        g.gridx = 0; g.gridy = 2;
        pnlChon.add(new JLabel("Tồn kho hiện có:"), g);

        lblTonKhoVal = new JLabel("0 đôi");
        lblTonKhoVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblTonKhoVal.setForeground(new Color(37, 99, 235));
        g.gridx = 1; g.gridy = 2;
        pnlChon.add(lblTonKhoVal, g);

        g.gridx = 2; g.gridy = 2;
        pnlChon.add(new JLabel("Đơn giá:"), g);

        lblDonGiaVal = new JLabel("0 VNĐ");
        lblDonGiaVal.setFont(new Font("Arial", Font.BOLD, 14));
        lblDonGiaVal.setForeground(new Color(185, 28, 28));
        g.gridx = 3; g.gridy = 2;
        pnlChon.add(lblDonGiaVal, g);

        // Dòng 4: Số lượng mua & Nút thêm giỏ
        g.gridx = 0; g.gridy = 3;
        pnlChon.add(new JLabel("Số lượng mua:"), g);

        spnSoLuong = new JSpinner(new SpinnerNumberModel(1, 1, 100, 1));
        spnSoLuong.setFont(new Font("Arial", Font.BOLD, 13));
        spnSoLuong.setPreferredSize(new Dimension(80, 30));
        g.gridx = 1; g.gridy = 3;
        pnlChon.add(spnSoLuong, g);

        btnThemGio = UIHelper.createPrimaryBtn("+ Thêm Vào Giỏ", 180, 34);
        g.gridx = 2; g.gridy = 3; g.gridwidth = 2;
        pnlChon.add(btnThemGio, g);

        pnl.add(pnlChon, BorderLayout.CENTER);
        return pnl;
    }

    /**
     * Vùng giỏ hàng chứa danh sách sản phẩm khách chọn mua.
     */
    private JPanel buildGioHangPanel() {
        JPanel pnl = new JPanel(new BorderLayout(5, 5));
        pnl.setBackground(Color.WHITE);
        pnl.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "2. GIỎ HÀNG ĐANG CHỜ THANH TOÁN",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));

        String[] headers = {"STT", "Mã SKU", "Tên Giày", "Size", "Màu", "Số Lượng", "Đơn Giá", "Giảm Giá", "Thành Tiền"};
        modelGioHang = new DefaultTableModel(headers, 0) {
            @Override
            public boolean isCellEditable(int row, int column) { return false; }
        };

        tableGioHang = new JTable(modelGioHang);
        tableGioHang.setRowHeight(28);
        tableGioHang.setFont(new Font("Arial", Font.PLAIN, 12));
        tableGioHang.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        tableGioHang.getTableHeader().setBackground(new Color(241, 245, 249));

        DefaultTableCellRenderer center = new DefaultTableCellRenderer();
        center.setHorizontalAlignment(JLabel.CENTER);
        tableGioHang.getColumnModel().getColumn(0).setPreferredWidth(40);
        tableGioHang.getColumnModel().getColumn(0).setCellRenderer(center);
        tableGioHang.getColumnModel().getColumn(3).setCellRenderer(center);
        tableGioHang.getColumnModel().getColumn(5).setCellRenderer(center);

        JScrollPane scroll = new JScrollPane(tableGioHang);
        pnl.add(scroll, BorderLayout.CENTER);

        // Nút thao tác trên giỏ hàng
        JPanel pnlActionGio = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 5));
        pnlActionGio.setBackground(Color.WHITE);

        btnXoaKhoiGio = UIHelper.createSecondaryBtn("Xóa Mục Đang Chọn [Del]", 180, 32);
        btnXoaKhoiGio.setFont(new Font("Arial", Font.BOLD, 12));

        btnXoaTrangGio = UIHelper.createSecondaryBtn("Làm Trống Giỏ", 120, 32);
        btnXoaTrangGio.setFont(new Font("Arial", Font.BOLD, 12));

        pnlActionGio.add(btnXoaKhoiGio);
        pnlActionGio.add(btnXoaTrangGio);
        pnl.add(pnlActionGio, BorderLayout.SOUTH);

        return pnl;
    }

    /**
     * Vùng thông tin khách hàng, chiết khấu và tính toán thanh toán.
     */
    private JPanel buildThanhToanPanel() {
        JPanel pnl = new JPanel(new BorderLayout(8, 8));
        pnl.setBackground(Color.WHITE);
        pnl.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "3. THÔNG TIN KHÁCH HÀNG & THANH TOÁN",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));

        JPanel pnlContent = new JPanel();
        pnlContent.setLayout(new BoxLayout(pnlContent, BoxLayout.Y_AXIS));
        pnlContent.setOpaque(false);
        pnlContent.setBorder(BorderFactory.createEmptyBorder(6, 10, 6, 10));

        // Khối Tra cứu khách hàng
        JPanel pnlKhach = new JPanel(new GridLayout(4, 2, 6, 6));
        pnlKhach.setOpaque(false);
        pnlKhach.setBorder(BorderFactory.createTitledBorder("Thành viên tích điểm"));

        pnlKhach.add(new JLabel("Số điện thoại:"));
        JPanel pnlTim = new JPanel(new BorderLayout(4, 0));
        pnlTim.setOpaque(false);
        txtSDTKhach = new JTextField();
        btnTimKhach = UIHelper.createDarkBtn("Tìm", 65, 28);
        pnlTim.add(txtSDTKhach, BorderLayout.CENTER);
        pnlTim.add(btnTimKhach, BorderLayout.EAST);
        pnlKhach.add(pnlTim);

        pnlKhach.add(new JLabel("Họ tên:"));
        lblTenKhachVal = new JLabel("Khách vãng lai");
        lblTenKhachVal.setFont(new Font("Arial", Font.BOLD, 13));
        pnlKhach.add(lblTenKhachVal);

        pnlKhach.add(new JLabel("Hạng thành viên:"));
        lblHangTheVal = new JLabel("Chưa có");
        lblHangTheVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblHangTheVal.setForeground(new Color(202, 138, 4));
        pnlKhach.add(lblHangTheVal);

        pnlKhach.add(new JLabel("Điểm tích lũy:"));
        JPanel pnlDiem = new JPanel(new FlowLayout(FlowLayout.LEFT, 4, 0));
        pnlDiem.setOpaque(false);
        lblDiemVal = new JLabel("0 điểm");
        lblDiemVal.setFont(new Font("Arial", Font.BOLD, 13));
        chkDungDiem = new JCheckBox("Dùng điểm");
        chkDungDiem.setOpaque(false);
        pnlDiem.add(lblDiemVal);
        pnlDiem.add(chkDungDiem);
        pnlKhach.add(pnlDiem);

        pnlContent.add(pnlKhach);
        pnlContent.add(Box.createVerticalStrut(10));

        // Khối Tính tiền hóa đơn
        JPanel pnlTien = new JPanel(new GridLayout(6, 2, 8, 8));
        pnlTien.setOpaque(false);
        pnlTien.setBorder(BorderFactory.createTitledBorder("Chi tiết thanh toán"));

        pnlTien.add(new JLabel("Tổng tiền hàng:"));
        lblTongTienHangVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblTongTienHangVal.setFont(new Font("Arial", Font.BOLD, 13));
        pnlTien.add(lblTongTienHangVal);

        pnlTien.add(new JLabel("Chiết khấu & Giảm giá:"));
        lblChietKhauVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblChietKhauVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblChietKhauVal.setForeground(new Color(220, 38, 38));
        pnlTien.add(lblChietKhauVal);

        pnlTien.add(new JLabel("KHÁCH CẦN TRẢ:"));
        lblKhachCanTraVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblKhachCanTraVal.setFont(new Font("Arial", Font.BOLD, 16));
        lblKhachCanTraVal.setForeground(new Color(185, 28, 28));
        pnlTien.add(lblKhachCanTraVal);

        pnlTien.add(new JLabel("Hình thức thanh toán:"));
        cboPhuongThuc = new JComboBox<>(new String[]{"Tiền mặt", "Chuyển khoản QR"});
        cboPhuongThuc.setFont(new Font("Arial", Font.PLAIN, 12));
        pnlTien.add(cboPhuongThuc);

        pnlTien.add(new JLabel("Tiền khách đưa:"));
        txtTienKhachDua = new JTextField("");
        txtTienKhachDua.setHorizontalAlignment(JTextField.RIGHT);
        txtTienKhachDua.setFont(new Font("Arial", Font.BOLD, 14));
        pnlTien.add(txtTienKhachDua);

        pnlTien.add(new JLabel("Tiền thừa trả khách:"));
        lblTienThuaVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblTienThuaVal.setFont(new Font("Arial", Font.BOLD, 14));
        lblTienThuaVal.setForeground(new Color(22, 163, 74));
        pnlTien.add(lblTienThuaVal);

        pnlContent.add(pnlTien);
        pnl.add(pnlContent, BorderLayout.CENTER);

        // Nút Thanh Toán lớn
        btnThanhToan = UIHelper.createSuccessBtn("THANH TOÁN & IN HÓA ĐƠN [F10]", 0, 50);
        btnThanhToan.setFont(new Font("Arial", Font.BOLD, 14));
        pnl.add(btnThanhToan, BorderLayout.SOUTH);

        return pnl;
    }

    /**
     * Đăng ký toàn bộ sự kiện và phím tắt đa tầng.
     */
    private void registerEvents() {
        btnThemGio.addActionListener(this);
        btnXoaKhoiGio.addActionListener(this);
        btnXoaTrangGio.addActionListener(this);
        btnTimKhach.addActionListener(this);
        btnThanhToan.addActionListener(this);

        cboSanPham.addActionListener(e -> capNhatDanhSachSizeVaMau());
        cboSize.addActionListener(e -> capNhatThongTinBienThe());
        cboMauSac.addActionListener(e -> capNhatThongTinBienThe());
        chkDungDiem.addActionListener(e -> tinhToanTongTienHoaDon());

        cboPhuongThuc.addActionListener(e -> {
            if ("Chuyển khoản QR".equals(cboPhuongThuc.getSelectedItem())) {
                txtTienKhachDua.setText(String.format("%.0f", khachCanTra));
                txtTienKhachDua.setEditable(false);
                tinhTienThua();
            } else {
                txtTienKhachDua.setEditable(true);
                txtTienKhachDua.setText("");
                tinhTienThua();
                txtTienKhachDua.requestFocus();
            }
        });
        txtSDTKhach.addActionListener(e -> btnTimKhach.doClick());

        // Xử lý ô tiền khách đưa
        txtTienKhachDua.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_F10) {
                    btnThanhToan.doClick();
                }
            }
            @Override
            public void keyReleased(KeyEvent e) {
                tinhTienThua();
            }
        });

        // Phím F10 trên ô tiền khách đưa
        txtTienKhachDua.getInputMap(JComponent.WHEN_FOCUSED).put(KeyStroke.getKeyStroke(KeyEvent.VK_F10, 0), "TXT_F10");
        txtTienKhachDua.getActionMap().put("TXT_F10", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                btnThanhToan.doClick();
            }
        });

        // Bắt phím DELETE trên bảng giỏ hàng
        tableGioHang.getInputMap(JComponent.WHEN_FOCUSED).put(KeyStroke.getKeyStroke(KeyEvent.VK_DELETE, 0), "TBL_DEL");
        tableGioHang.getInputMap(JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke(KeyEvent.VK_DELETE, 0), "TBL_DEL");
        tableGioHang.getActionMap().put("TBL_DEL", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                xoaMucKhoiGio();
            }
        });
        tableGioHang.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_DELETE) {
                    xoaMucKhoiGio();
                }
            }
        });

        // Phím tắt trên toàn bộ Panel POS
        InputMap posIm = this.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
        ActionMap posAm = this.getActionMap();

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_F10, 0), "POS_F10");
        posAm.put("POS_F10", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                btnThanhToan.doClick();
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_DELETE, 0), "POS_DELETE");
        posAm.put("POS_DELETE", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                xoaMucKhoiGio();
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_F1, 0), "POS_F1");
        posAm.put("POS_F1", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                switchTab(0);
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_F2, 0), "POS_F2");
        posAm.put("POS_F2", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                switchTab(1);
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_F3, 0), "POS_F3");
        posAm.put("POS_F3", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                switchTab(2);
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_F4, 0), "POS_F4");
        posAm.put("POS_F4", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                switchTab(3);
            }
        });

        posIm.put(KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0), "POS_ESC");
        posAm.put("POS_ESC", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Window w = SwingUtilities.getWindowAncestor(BanHang_GUI.this);
                if (w instanceof ManHinhChinh_GUI) {
                    ((ManHinhChinh_GUI) w).dangXuat();
                }
            }
        });
    }

    private void switchTab(int index) {
        Window w = SwingUtilities.getWindowAncestor(this);
        if (w instanceof ManHinhChinh_GUI) {
            JTabbedPane tp = (JTabbedPane) ((ManHinhChinh_GUI) w).getContentPane().getComponent(1);
            if (tp.getTabCount() > index) {
                tp.setSelectedIndex(index);
            }
        }
    }

    /**
     * C7, K9: Nạp lại danh sách tất cả mẫu giày đang kinh doanh vào ComboBox.
     */
    public void taiLaiDanhSachSanPham() {
        loadDataBienThe();
        List<SanPham> dsSanPham = sanPhamDAO.getAllSanPham();
        cboSanPham.removeAllItems();

        Set<String> setTenSP = new LinkedHashSet<>();
        // Nạp tất cả sản phẩm đang kinh doanh
        if (dsSanPham != null) {
            for (SanPham sp : dsSanPham) {
                if (sp.isTrangThai()) {
                    setTenSP.add(sp.getTenSanPham());
                }
            }
        }
        if (dsChiTietGiay != null) {
            for (ChiTietGiay ct : dsChiTietGiay) {
                if (ct.getSanPham() != null && ct.getSanPham().isTrangThai()) {
                    setTenSP.add(ct.getSanPham().getTenSanPham());
                }
            }
        }
        for (String ten : setTenSP) {
            cboSanPham.addItem(ten);
        }

        if (cboSanPham.getItemCount() > 0) {
            cboSanPham.setSelectedIndex(0);
            capNhatDanhSachSizeVaMau();
        }
    }

    private void capNhatDanhSachSizeVaMau() {
        if (cboSanPham == null || cboSize == null || cboMauSac == null) return;
        String tenSP = (String) cboSanPham.getSelectedItem();
        if (tenSP == null) return;

        cboSize.removeAllItems();
        cboMauSac.removeAllItems();

        Set<String> setSize = new TreeSet<>();
        Set<String> setMau = new TreeSet<>();

        for (ChiTietGiay ct : dsChiTietGiay) {
            if (ct.getSanPham() != null && ct.getSanPham().getTenSanPham().equalsIgnoreCase(tenSP)) {
                setSize.add(String.valueOf(ct.getKichThuoc()));
                setMau.add(ct.getMauSac());
            }
        }

        for (String s : setSize) cboSize.addItem(s);
        for (String m : setMau) cboMauSac.addItem(m);

        if (cboSize.getItemCount() > 0) cboSize.setSelectedIndex(0);
        if (cboMauSac.getItemCount() > 0) cboMauSac.setSelectedIndex(0);

        capNhatThongTinBienThe();
    }

    private void capNhatThongTinBienThe() {
        ChiTietGiay ct = timChiTietDangChon();
        if (ct != null) {
            lblTonKhoVal.setText(ct.getSoLuongTon() + " đôi");
            lblDonGiaVal.setText(df.format(ct.getSanPham().getGiaBan()));
        } else {
            lblTonKhoVal.setText("0 đôi");
            lblDonGiaVal.setText("0 VNĐ");
        }
    }

    private ChiTietGiay timChiTietDangChon() {
        String tenSP = (String) cboSanPham.getSelectedItem();
        String sizeStr = (String) cboSize.getSelectedItem();
        String mau = (String) cboMauSac.getSelectedItem();

        if (tenSP == null || sizeStr == null || mau == null) return null;
        int size = Integer.parseInt(sizeStr);

        for (ChiTietGiay ct : dsChiTietGiay) {
            if (ct.getSanPham() != null &&
                    ct.getSanPham().getTenSanPham().equalsIgnoreCase(tenSP) &&
                    ct.getKichThuoc() == size &&
                    ct.getMauSac().equalsIgnoreCase(mau)) {
                return ct;
            }
        }
        return null;
    }

    private void tinhToanTongTienHoaDon() {
        tongTienGoc = 0;
        for (int i = 0; i < modelGioHang.getRowCount(); i++) {
            tongTienGoc += (Double) modelGioHang.getValueAt(i, 8);
        }

        // 1. Tính chiết khấu hạng thẻ
        double ptChietKhau = (khachHienTai != null) ? khachHienTai.tinhChietKhau() : 0.0;
        double tienChietKhau = Math.floor(tongTienGoc * ptChietKhau);

        // 2. Tính giảm giá dùng điểm tích lũy (1 điểm = 1.000 VNĐ)
        double tienGiamDiem = 0;
        if (chkDungDiem.isSelected() && khachHienTai != null) {
            int diem = khachHienTai.getDiemTichLuy();
            double toiDaCoTheGiam = Math.max(0, tongTienGoc - tienChietKhau);
            tienGiamDiem = Math.min(diem * 1000.0, toiDaCoTheGiam);
        }

        tongTienGiam = tienChietKhau + tienGiamDiem;
        khachCanTra = Math.max(0, tongTienGoc - tongTienGiam);

        lblTongTienHangVal.setText(df.format(tongTienGoc));
        lblChietKhauVal.setText(df.format(tongTienGiam));
        lblKhachCanTraVal.setText(df.format(khachCanTra));

        tinhTienThua();
    }

    private void tinhTienThua() {
        try {
            String str = txtTienKhachDua.getText().replace(",", "").replace(".", "").trim();
            double tienDua = str.isEmpty() ? 0 : Double.parseDouble(str);
            double tienThua = Math.max(0, tienDua - khachCanTra);
            lblTienThuaVal.setText(df.format(tienThua));
        } catch (NumberFormatException ex) {
            lblTienThuaVal.setText("0 VNĐ");
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();

        if (o.equals(btnThemGio)) {
            ChiTietGiay ct = timChiTietDangChon();
            if (ct == null) {
                JOptionPane.showMessageDialog(this, "Sản phẩm hoặc biến thể này hiện không khả dụng!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                return;
            }

            int slMua = (Integer) spnSoLuong.getValue();
            if (slMua > ct.getSoLuongTon()) {
                JOptionPane.showMessageDialog(this, "Tồn kho không đủ! Chỉ còn " + ct.getSoLuongTon() + " đôi.", "Cảnh báo hết hàng", JOptionPane.WARNING_MESSAGE);
                return;
            }

            // Kiểm tra số lượng đã có trong giỏ hàng
            int daCoTrongGio = 0;
            int rowDaCo = -1;
            for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                if (modelGioHang.getValueAt(i, 1).equals(ct.getMaChiTietGiay())) {
                    daCoTrongGio = (Integer) modelGioHang.getValueAt(i, 5);
                    rowDaCo = i;
                    break;
                }
            }

            if (daCoTrongGio + slMua > ct.getSoLuongTon()) {
                JOptionPane.showMessageDialog(this, "Tổng số lượng trong giỏ (" + (daCoTrongGio + slMua) + ") vượt quá tồn kho (" + ct.getSoLuongTon() + ")!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                return;
            }

            double donGia = ct.getSanPham().getGiaBan();
            if (rowDaCo >= 0) {
                int tongSL = daCoTrongGio + slMua;
                modelGioHang.setValueAt(tongSL, rowDaCo, 5);
                modelGioHang.setValueAt(tongSL * donGia, rowDaCo, 8);
            } else {
                int stt = modelGioHang.getRowCount() + 1;
                double thanhTien = slMua * donGia;
                modelGioHang.addRow(new Object[]{
                        stt, ct.getMaChiTietGiay(), ct.getSanPham().getTenSanPham(),
                        ct.getKichThuoc(), ct.getMauSac(), slMua, donGia, 0.0, thanhTien
                });
            }

            tinhToanTongTienHoaDon();

        } else if (o.equals(btnXoaKhoiGio)) {
            xoaMucKhoiGio();

        } else if (o.equals(btnXoaTrangGio)) {
            if (modelGioHang.getRowCount() > 0) {
                int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc chắn muốn xóa toàn bộ sản phẩm trong giỏ hàng?", "Xác nhận làm trống", JOptionPane.YES_NO_OPTION);
                if (opt == JOptionPane.YES_OPTION) {
                    modelGioHang.setRowCount(0);
                    tinhToanTongTienHoaDon();
                }
            }

        } else if (o.equals(btnTimKhach)) {
            String sdt = txtSDTKhach.getText().trim();
            if (sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập số điện thoại cần tìm!", "Lỗi", JOptionPane.WARNING_MESSAGE);
                return;
            }
            if (!sdt.matches("^0[35789]\\d{8}$")) {
                JOptionPane.showMessageDialog(this, "Số điện thoại không hợp lệ! Phải gồm 10 chữ số và bắt đầu bằng 03, 05, 07, 08, 09.", "Lỗi định dạng", JOptionPane.WARNING_MESSAGE);
                return;
            }
            KhachHang kh = kh_dao.timTheoSoDienThoai(sdt);
            if (kh != null) {
                khachHienTai = kh;
                lblTenKhachVal.setText(kh.getHoTen());
                lblHangTheVal.setText(kh.getHangThanhVien() + " (Giảm " + (int)(kh.tinhChietKhau()*100) + "%)");
                lblDiemVal.setText(kh.getDiemTichLuy() + " điểm");
                tinhToanTongTienHoaDon();
            } else {
                int opt = JOptionPane.showConfirmDialog(this, "Không tìm thấy khách hàng với SĐT này! Bạn có muốn thêm mới thành viên?", "Khách hàng mới", JOptionPane.YES_NO_OPTION);
                if (opt == JOptionPane.YES_OPTION) {
                    String tenMoi = JOptionPane.showInputDialog(this, "Nhập họ tên khách hàng mới:");
                    if (tenMoi != null && !tenMoi.trim().isEmpty()) {
                        String maMoi = kh_dao.sinhMaKhachHangMoi();
                        KhachHang khMoi = new KhachHang(maMoi, tenMoi.trim(), sdt, null, true, null, null, 0, "Đồng");
                        if (kh_dao.themKhachHang(khMoi)) {
                            khachHienTai = khMoi;
                            lblTenKhachVal.setText(khMoi.getHoTen());
                            lblHangTheVal.setText("Đồng");
                            lblDiemVal.setText("0 điểm");
                            tinhToanTongTienHoaDon();
                        } else {
                            String err = kh_dao.getLastError();
                            JOptionPane.showMessageDialog(this, "Không thể tạo khách hàng mới: " + (err.isEmpty() ? "Lỗi cơ sở dữ liệu!" : err), "Lỗi", JOptionPane.ERROR_MESSAGE);
                        }
                    }
                }
            }

        } else if (o.equals(btnThanhToan)) {
            thucHienThanhToan();
        }
    }

    /**
     * C1: Xóa dòng sản phẩm đang chọn trong giỏ hàng.
     */
    public void xoaMucKhoiGio() {
        int row = tableGioHang.getSelectedRow();
        if (row >= 0 && row < modelGioHang.getRowCount()) {
            modelGioHang.removeRow(row);
            for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                modelGioHang.setValueAt(i + 1, i, 0);
            }
            tinhToanTongTienHoaDon();
        } else {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn dòng cần xóa trong giỏ hàng!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
        }
    }

    /**
     * Xử lý thanh toán hóa đơn an toàn, kiểm tra nhập liệu chặt chẽ (C5, K7, B1, B2).
     */
    private void thucHienThanhToan() {
        if (modelGioHang.getRowCount() == 0) {
            JOptionPane.showMessageDialog(this, "Giỏ hàng đang trống! Vui lòng thêm sản phẩm trước khi thanh toán.", "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }

        double canTra = khachCanTra;
        double tienDua = 0;
        String strDua = txtTienKhachDua.getText().replace(",", "").replace(".", "").trim();

        try {
            if ("Chuyển khoản QR".equals(cboPhuongThuc.getSelectedItem())) {
                tienDua = canTra;
            } else {
                if (strDua.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "Vui lòng nhập số tiền khách đưa!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    txtTienKhachDua.requestFocus();
                    return;
                }
                tienDua = Double.parseDouble(strDua);
            }
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Tiền khách đưa không hợp lệ! Vui lòng nhập số.", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
            txtTienKhachDua.requestFocus();
            return;
        }

        if (cboPhuongThuc.getSelectedItem().equals("Tiền mặt") && tienDua < canTra) {
            JOptionPane.showMessageDialog(this, "Tiền khách đưa chưa đủ để thanh toán!", "Lỗi thanh toán", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Tạo đối tượng HoaDon với đầy đủ các số liệu tài chính đã chiết khấu
        String maHD = "HD" + String.format("%06d", System.currentTimeMillis() % 1000000);
        double tienThua = Math.max(0, tienDua - canTra);

        HoaDon hd = new HoaDon(maHD, LocalDateTime.now(), nhanVienDangNhap, khachHienTai, canTra,
                (String) cboPhuongThuc.getSelectedItem(), tienDua, tienThua);

        int diemToiDa = (int) Math.floor((tongTienGoc - (khachHienTai != null ? Math.floor(tongTienGoc * khachHienTai.tinhChietKhau()) : 0)) / 1000.0);
        int diemDung = (chkDungDiem.isSelected() && khachHienTai != null) ? Math.min(khachHienTai.getDiemTichLuy(), diemToiDa) : 0;
        double tienGiamDiem = diemDung * 1000.0;
        double chietKhauHang = Math.max(0, tongTienGiam - tienGiamDiem);

        hd.setTongTienHang(tongTienGoc);
        hd.setChietKhau(chietKhauHang);
        hd.setDiemSuDung(diemDung);
        hd.setTienGiamDiem(tienGiamDiem);
        hd.setTongTien(canTra);
        hd.setDiemCong((int) Math.floor(canTra / 100000.0));

        // Thêm chi tiết các sản phẩm trong giỏ
        for (int i = 0; i < modelGioHang.getRowCount(); i++) {
            String maCTG = (String) modelGioHang.getValueAt(i, 1);
            int sl = (Integer) modelGioHang.getValueAt(i, 5);
            double donGia = (Double) modelGioHang.getValueAt(i, 6);
            double giam = (Double) modelGioHang.getValueAt(i, 7);
            double thanhTien = (Double) modelGioHang.getValueAt(i, 8);

            ChiTietGiay ctg = new ChiTietGiay(maCTG);
            ChiTietHoaDon cthd = new ChiTietHoaDon(hd, ctg, sl, donGia, giam, thanhTien);
            hd.themChiTiet(cthd);
        }

        // Gọi DAO lưu trong Transaction ACID
        boolean thanhCong = hd_dao.themHoaDon(hd);
        if (thanhCong) {
            // Hiển thị hóa đơn bán lẻ K80 chuẩn hóa khoảng cách và độ rộng
            StringBuilder bill = new StringBuilder();
            bill.append("=============================================\n");
            bill.append("            STEPUP FOOTWEAR STORE            \n");
            bill.append("      12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM      \n\n");
            bill.append("               HÓA ĐƠN BÁN LẺ                \n\n");
            bill.append("Mã HĐ: ").append(hd.getMaHoaDon()).append("\n");
            bill.append("Ngày: ").append(LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm"))).append("\n");
            bill.append("Thu ngân: ").append((nhanVienDangNhap != null) ? nhanVienDangNhap.getHoTen() : "Thu ngân").append("\n");
            bill.append("Khách hàng: ").append(khachHienTai != null ? khachHienTai.getHoTen() : "Khách vãng lai").append("\n");
            bill.append("---------------------------------------------\n");
            for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                bill.append(modelGioHang.getValueAt(i, 2)).append(" (Size ").append(modelGioHang.getValueAt(i, 3)).append(")\n");
                bill.append("  ").append(modelGioHang.getValueAt(i, 5)).append(" x ").append(df.format(modelGioHang.getValueAt(i, 6)))
                        .append(" = ").append(df.format(modelGioHang.getValueAt(i, 8))).append("\n");
            }
            bill.append("---------------------------------------------\n");
            bill.append(String.format("%-24s %18s\n", "Tổng tiền hàng:", df.format(hd.getTongTienHang())));
            bill.append(String.format("%-24s %18s\n", "Chiết khấu hạng thẻ:", (hd.getChietKhau() > 0 ? "-" : "") + df.format(hd.getChietKhau())));
            bill.append(String.format("%-24s %18s\n", "Tiền giảm từ điểm:", (hd.getTienGiamDiem() > 0 ? "-" : "") + df.format(hd.getTienGiamDiem())));
            bill.append(String.format("%-24s %18s\n", "CẦN THANH TOÁN:", df.format(hd.getTongTien())));
            bill.append(String.format("%-24s %18s\n", "Khách đưa:", df.format(tienDua)));
            bill.append(String.format("%-24s %18s\n", "Tiền thừa:", df.format(tienThua)));
            bill.append(String.format("%-24s %18s\n", "Điểm cộng mới:", "+" + hd.getDiemCong() + " điểm"));
            bill.append(String.format("%-24s %18s\n", "Hình thức:", cboPhuongThuc.getSelectedItem()));
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

            JOptionPane.showMessageDialog(this, scrollBill, "THANH TOÁN THÀNH CÔNG - HÓA ĐƠN K80", JOptionPane.INFORMATION_MESSAGE);

            // C3, K6: Làm mới đơn hàng sạch sẽ hoàn toàn cho giao dịch tiếp theo
            lamMoiDonHang();
        } else {
            String msg = hd_dao.getLastErrorMessage();
            if (msg == null || msg.trim().isEmpty()) {
                msg = "Lỗi khi lưu giao dịch vào CSDL!";
            }
            JOptionPane.showMessageDialog(this, msg, "Lỗi giao dịch", JOptionPane.ERROR_MESSAGE);
        }
    }

    /**
     * C3, K6: Làm mới đơn hàng, xóa sạch khách cũ và tiền thừa sau thanh toán.
     */
    public void lamMoiDonHang() {
        khachHienTai = null;
        txtSDTKhach.setText("");
        lblTenKhachVal.setText("Khách vãng lai");
        lblHangTheVal.setText("Chưa có");
        lblDiemVal.setText("0 điểm");
        chkDungDiem.setSelected(false);
        modelGioHang.setRowCount(0);
        txtTienKhachDua.setText("");
        lblTienThuaVal.setText("0 VNĐ");
        tongTienGoc = 0;
        tongTienGiam = 0;
        khachCanTra = 0;
        lblTongTienHangVal.setText("0 VNĐ");
        lblChietKhauVal.setText("0 VNĐ");
        lblKhachCanTraVal.setText("0 VNĐ");
        cboPhuongThuc.setSelectedIndex(0);

        loadDataBienThe();
        capNhatThongTinBienThe();
    }

    public void thanhToanDonHang() {
        btnThanhToan.doClick();
    }

    public DefaultTableModel getModelGioHang() {
        return modelGioHang;
    }
}

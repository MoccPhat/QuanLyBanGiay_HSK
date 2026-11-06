package gui;

import dao.ChiTietGiay_DAO;
import dao.HoaDon_DAO;
import dao.KhachHang_DAO;
import dao.SanPham_DAO;
import entity.*;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.text.DecimalFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class BanHang_GUI extends JPanel implements ActionListener {
    private NhanVien nhanVienDangNhap;

    // DAOs
    private SanPham_DAO sp_dao;
    private ChiTietGiay_DAO ctg_dao;
    private KhachHang_DAO kh_dao;
    private HoaDon_DAO hd_dao;

    // Cache dữ liệu
    private List<ChiTietGiay> dsChiTietGiay;
    private KhachHang khachHienTai = null;

    // Components - Tra cứu & Chọn giày
    private JComboBox<String> cboSanPham;
    private JComboBox<String> cboSize;
    private JComboBox<String> cboMauSac;
    private JLabel lblTonKhoVal;
    private JLabel lblDonGiaVal;
    private JSpinner spnSoLuong;
    private JButton btnThemGio;
    private JButton btnXoaKhoiGio;
    private JButton btnXoaTrangGio;

    // Components - Giỏ hàng
    private JTable tableGioHang;
    private DefaultTableModel modelGioHang;

    // Components - Thanh toán
    private JTextField txtSDTKhach;
    private JButton btnTimKhach;
    private JLabel lblTenKhachVal;
    private JLabel lblHangTheVal;
    private JLabel lblDiemVal;
    private JCheckBox chkDungDiem;

    private JLabel lblTongTienHangVal;
    private JLabel lblChietKhauVal;
    private JLabel lblKhachCanTraVal;
    private JTextField txtTienKhachDua;
    private JLabel lblTienThuaVal;
    private JComboBox<String> cboPhuongThuc;
    private JButton btnThanhToan;

    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    public BanHang_GUI(NhanVien nv) {
        this.nhanVienDangNhap = nv;
        this.sp_dao = new SanPham_DAO();
        this.ctg_dao = new ChiTietGiay_DAO();
        this.kh_dao = new KhachHang_DAO();
        this.hd_dao = new HoaDon_DAO();

        setLayout(new BorderLayout(12, 12));
        setBackground(UIHelper.BG_GRAY);
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));

        loadDataBienThe();

        JPanel pnlLeft = buildLeftPanel();
        JPanel pnlRight = buildRightPanel();

        add(pnlLeft, BorderLayout.CENTER);
        add(pnlRight, BorderLayout.EAST);

        registerEvents();
        capNhatThongTinBienThe();
    }

    private void loadDataBienThe() {
        dsChiTietGiay = ctg_dao.getAllChiTietGiay();
        if (dsChiTietGiay == null || dsChiTietGiay.isEmpty()) {
            dsChiTietGiay = new ArrayList<>();
            SanPham sp1 = new SanPham("SP0001", "Nike Air Force 1 07 Low", "Sneaker", "Nike", 1800000, 2600000, "Da thật", true);
            SanPham sp2 = new SanPham("SP0002", "Adidas Ultraboost Light 23", "Chạy bộ", "Adidas", 2400000, 3500000, "Primeknit", true);
            SanPham sp3 = new SanPham("SP0003", "Vans Old Skool Classic", "Sneaker", "Vans", 1100000, 1750000, "Canvas", true);

            dsChiTietGiay.add(new ChiTietGiay("CTG0001", sp1, 39, "Trắng", 15, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0002", sp1, 40, "Trắng", 20, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0003", sp1, 41, "Trắng", 18, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0006", sp2, 40, "Đen Phối Trắng", 12, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0007", sp2, 41, "Đen Phối Trắng", 14, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0010", sp3, 39, "Đen Sọc Trắng", 22, ""));
            dsChiTietGiay.add(new ChiTietGiay("CTG0011", sp3, 40, "Đen Sọc Trắng", 25, ""));
        }
    }

    private JPanel buildLeftPanel() {
        JPanel pnl = new JPanel(new BorderLayout(10, 10));
        pnl.setOpaque(false);

        // 1. KHUNG CHỌN SẢN PHẨM & BIẾN THỂ SIZE/MÀU
        JPanel pnlChon = UIHelper.createTitledPanel("1. CHỌN MẪU GIÀY & BIẾN THỂ SIZE / MÀU", UIHelper.PRIMARY_BLUE);
        pnlChon.setLayout(new GridBagLayout());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 8, 6, 8);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Dòng 1: Mẫu giày
        JLabel lblSP = new JLabel("Mẫu giày:");
        lblSP.setFont(new Font("Arial", Font.BOLD, 13));
        g.gridx = 0; g.gridy = 0; g.weightx = 0;
        pnlChon.add(lblSP, g);

        cboSanPham = new JComboBox<>();
        UIHelper.styleComboBox(cboSanPham);
        cboSanPham.setPreferredSize(new Dimension(300, 32));
        List<String> listTenSP = new ArrayList<>();
        for (ChiTietGiay ct : dsChiTietGiay) {
            String ten = ct.getSanPham().getTenSanPham();
            if (!listTenSP.contains(ten)) listTenSP.add(ten);
        }
        for (String ten : listTenSP) cboSanPham.addItem(ten);

        g.gridx = 1; g.gridy = 0; g.gridwidth = 3; g.weightx = 1.0;
        pnlChon.add(cboSanPham, g);

        // Dòng 2: Size & Màu sắc
        g.gridwidth = 1; g.weightx = 0;
        g.gridx = 0; g.gridy = 1;
        JLabel lblSz = new JLabel("Kích cỡ (Size):");
        lblSz.setFont(new Font("Arial", Font.BOLD, 13));
        pnlChon.add(lblSz, g);

        cboSize = new JComboBox<>();
        UIHelper.styleComboBox(cboSize);
        cboSize.setPreferredSize(new Dimension(100, 32));
        g.gridx = 1; g.gridy = 1;
        pnlChon.add(cboSize, g);

        g.gridx = 2; g.gridy = 1;
        JLabel lblMau = new JLabel("Màu sắc:");
        lblMau.setFont(new Font("Arial", Font.BOLD, 13));
        pnlChon.add(lblMau, g);

        cboMauSac = new JComboBox<>();
        UIHelper.styleComboBox(cboMauSac);
        cboMauSac.setPreferredSize(new Dimension(140, 32));
        g.gridx = 3; g.gridy = 1;
        pnlChon.add(cboMauSac, g);

        // Dòng 3: Tồn kho & Đơn giá
        g.gridx = 0; g.gridy = 2;
        pnlChon.add(new JLabel("Tồn kho hiện có:"), g);

        lblTonKhoVal = new JLabel("0 đôi");
        lblTonKhoVal.setFont(new Font("Arial", Font.BOLD, 15));
        lblTonKhoVal.setForeground(UIHelper.SUCCESS_GREEN);
        g.gridx = 1; g.gridy = 2;
        pnlChon.add(lblTonKhoVal, g);

        g.gridx = 2; g.gridy = 2;
        pnlChon.add(new JLabel("Đơn giá niêm yết:"), g);

        lblDonGiaVal = new JLabel("0 VNĐ");
        lblDonGiaVal.setFont(new Font("Arial", Font.BOLD, 15));
        lblDonGiaVal.setForeground(UIHelper.DANGER_RED);
        g.gridx = 3; g.gridy = 2;
        pnlChon.add(lblDonGiaVal, g);

        // Dòng 4: Số lượng bán & Nút Thêm Vào Giỏ
        g.gridx = 0; g.gridy = 3;
        JLabel lblSL = new JLabel("Số lượng mua:");
        lblSL.setFont(new Font("Arial", Font.BOLD, 13));
        pnlChon.add(lblSL, g);

        spnSoLuong = new JSpinner(new SpinnerNumberModel(1, 1, 100, 1));
        spnSoLuong.setFont(new Font("Arial", Font.BOLD, 14));
        spnSoLuong.setPreferredSize(new Dimension(90, 34));
        g.gridx = 1; g.gridy = 3;
        pnlChon.add(spnSoLuong, g);

        btnThemGio = UIHelper.createButton("+ THÊM VÀO GIỎ [F2]", UIHelper.ACCENT_BLUE, Color.WHITE, 200, 38);
        g.gridx = 2; g.gridy = 3; g.gridwidth = 2;
        pnlChon.add(btnThemGio, g);

        pnl.add(pnlChon, BorderLayout.NORTH);

        // 2. KHUNG GIỎ HÀNG (JTABLE)
        JPanel pnlGio = UIHelper.createTitledPanel("2. GIỎ HÀNG ĐANG CHỜ THANH TOÁN", UIHelper.PRIMARY_BLUE);
        pnlGio.setLayout(new BorderLayout(8, 8));

        String[] headers = {"STT", "Mã SKU", "Tên Giày", "Size", "Màu", "Số Lượng", "Đơn Giá", "Giảm Giá", "Thành Tiền"};
        modelGioHang = new DefaultTableModel(headers, 0) {
            @Override
            public boolean isCellEditable(int r, int c) { return false; }
        };

        tableGioHang = new JTable(modelGioHang);
        UIHelper.styleTable(tableGioHang);

        DefaultTableCellRenderer center = new DefaultTableCellRenderer();
        center.setHorizontalAlignment(JLabel.CENTER);
        tableGioHang.getColumnModel().getColumn(3).setCellRenderer(center);
        tableGioHang.getColumnModel().getColumn(4).setCellRenderer(center);
        tableGioHang.getColumnModel().getColumn(5).setCellRenderer(center);

        JScrollPane scroll = new JScrollPane(tableGioHang);
        scroll.setBorder(BorderFactory.createLineBorder(UIHelper.BORDER_GRAY, 1));
        pnlGio.add(scroll, BorderLayout.CENTER);

        // Nút thao tác giỏ hàng
        JPanel pnlActionGio = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 4));
        pnlActionGio.setOpaque(false);

        btnXoaKhoiGio = UIHelper.createDangerBtn("Xóa Khỏi Giỏ [Del]", 170, 34);
        btnXoaTrangGio = UIHelper.createSecondaryBtn("Làm Trống Giỏ", 130, 34);

        pnlActionGio.add(btnXoaKhoiGio);
        pnlActionGio.add(btnXoaTrangGio);
        pnlGio.add(pnlActionGio, BorderLayout.SOUTH);

        pnl.add(pnlGio, BorderLayout.CENTER);
        return pnl;
    }

    private JPanel buildRightPanel() {
        JPanel pnl = UIHelper.createTitledPanel("3. THÔNG TIN KHÁCH HÀNG & HÓA ĐƠN", UIHelper.DANGER_RED);
        pnl.setLayout(new BorderLayout(10, 10));
        pnl.setPreferredSize(new Dimension(400, 0));

        JPanel pnlContent = new JPanel();
        pnlContent.setLayout(new BoxLayout(pnlContent, BoxLayout.Y_AXIS));
        pnlContent.setOpaque(false);

        // THÔNG TIN KHÁCH HÀNG
        JPanel pnlKhach = new JPanel(new GridBagLayout());
        pnlKhach.setBackground(new Color(241, 245, 249));
        pnlKhach.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(UIHelper.BORDER_GRAY, 1, true),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(4, 6, 4, 6);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Dòng SĐT + Nút Tìm
        g.gridx = 0; g.gridy = 0; g.weightx = 0.3;
        JLabel lblSDT = new JLabel("SĐT Khách:");
        lblSDT.setFont(new Font("Arial", Font.BOLD, 12));
        pnlKhach.add(lblSDT, g);

        JPanel pnlSearch = new JPanel(new BorderLayout(6, 0));
        pnlSearch.setOpaque(false);
        txtSDTKhach = new JTextField("0938111222");
        UIHelper.styleTextField(txtSDTKhach);
        btnTimKhach = UIHelper.createButton("Tìm", UIHelper.PRIMARY_BLUE, Color.WHITE, 65, 30);
        pnlSearch.add(txtSDTKhach, BorderLayout.CENTER);
        pnlSearch.add(btnTimKhach, BorderLayout.EAST);

        g.gridx = 1; g.gridy = 0; g.weightx = 0.7;
        pnlKhach.add(pnlSearch, g);

        // Họ tên
        g.gridx = 0; g.gridy = 1;
        pnlKhach.add(new JLabel("Họ tên:"), g);
        lblTenKhachVal = new JLabel("Khách vãng lai");
        lblTenKhachVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblTenKhachVal.setForeground(new Color(30, 41, 59));
        g.gridx = 1; g.gridy = 1;
        pnlKhach.add(lblTenKhachVal, g);

        // Hạng thẻ
        g.gridx = 0; g.gridy = 2;
        pnlKhach.add(new JLabel("Hạng thẻ:"), g);
        lblHangTheVal = new JLabel("Chưa có");
        lblHangTheVal.setFont(new Font("Arial", Font.PLAIN, 12));
        g.gridx = 1; g.gridy = 2;
        pnlKhach.add(lblHangTheVal, g);

        // Điểm tích lũy
        g.gridx = 0; g.gridy = 3;
        pnlKhach.add(new JLabel("Điểm tích lũy:"), g);
        lblDiemVal = new JLabel("0 điểm");
        lblDiemVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblDiemVal.setForeground(UIHelper.SUCCESS_GREEN);
        g.gridx = 1; g.gridy = 3;
        pnlKhach.add(lblDiemVal, g);

        pnlContent.add(pnlKhach);
        pnlContent.add(Box.createVerticalStrut(10));

        // DÙNG ĐIỂM
        chkDungDiem = new JCheckBox("Quy đổi điểm thưởng (1 điểm = 1.000 VNĐ)");
        chkDungDiem.setFont(new Font("Arial", Font.PLAIN, 12));
        chkDungDiem.setOpaque(false);
        pnlContent.add(chkDungDiem);
        pnlContent.add(Box.createVerticalStrut(10));

        // TÍNH TIỀN
        JPanel pnlTien = new JPanel(new GridLayout(6, 2, 8, 8));
        pnlTien.setOpaque(false);

        pnlTien.add(new JLabel("Tổng tiền hàng:"));
        lblTongTienHangVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblTongTienHangVal.setFont(new Font("Arial", Font.BOLD, 14));
        pnlTien.add(lblTongTienHangVal);

        pnlTien.add(new JLabel("Giảm giá / Ưu đãi:"));
        lblChietKhauVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblChietKhauVal.setFont(new Font("Arial", Font.BOLD, 13));
        lblChietKhauVal.setForeground(UIHelper.DANGER_RED);
        pnlTien.add(lblChietKhauVal);

        JLabel lblCanTra = new JLabel("KHÁCH CẦN TRẢ:");
        lblCanTra.setFont(new Font("Arial", Font.BOLD, 14));
        lblCanTra.setForeground(UIHelper.PRIMARY_BLUE);
        pnlTien.add(lblCanTra);

        lblKhachCanTraVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblKhachCanTraVal.setFont(new Font("Arial", Font.BOLD, 18));
        lblKhachCanTraVal.setForeground(UIHelper.DANGER_RED);
        pnlTien.add(lblKhachCanTraVal);

        pnlTien.add(new JLabel("Phương thức:"));
        cboPhuongThuc = new JComboBox<>(new String[]{"Tiền mặt", "Chuyển khoản QR"});
        UIHelper.styleComboBox(cboPhuongThuc);
        pnlTien.add(cboPhuongThuc);

        pnlTien.add(new JLabel("Tiền khách đưa:"));
        txtTienKhachDua = new JTextField("0");
        UIHelper.styleTextField(txtTienKhachDua);
        txtTienKhachDua.setHorizontalAlignment(JTextField.RIGHT);
        txtTienKhachDua.setFont(new Font("Arial", Font.BOLD, 14));
        pnlTien.add(txtTienKhachDua);

        pnlTien.add(new JLabel("Tiền thừa trả khách:"));
        lblTienThuaVal = new JLabel("0 VNĐ", JLabel.RIGHT);
        lblTienThuaVal.setFont(new Font("Arial", Font.BOLD, 15));
        lblTienThuaVal.setForeground(UIHelper.SUCCESS_GREEN);
        pnlTien.add(lblTienThuaVal);

        pnlContent.add(pnlTien);
        pnl.add(pnlContent, BorderLayout.CENTER);

        // NÚT THANH TOÁN (To, xanh, siêu nổi bật)
        btnThanhToan = UIHelper.createButton("THANH TOÁN & IN HÓA ĐƠN [F10]", UIHelper.SUCCESS_GREEN, Color.WHITE, 0, 52);
        btnThanhToan.setFont(new Font("Arial", Font.BOLD, 15));
        pnl.add(btnThanhToan, BorderLayout.SOUTH);

        return pnl;
    }

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

        txtTienKhachDua.addKeyListener(new KeyAdapter() {
            @Override
            public void keyReleased(KeyEvent e) {
                tinhTienThua();
            }
        });

        capNhatDanhSachSizeVaMau();
    }

    private void capNhatDanhSachSizeVaMau() {
        String tenSP = (String) cboSanPham.getSelectedItem();
        if (tenSP == null) return;

        cboSize.removeAllItems();
        cboMauSac.removeAllItems();

        List<Integer> sizes = new ArrayList<>();
        List<String> mauSacs = new ArrayList<>();

        for (ChiTietGiay ct : dsChiTietGiay) {
            if (ct.getSanPham().getTenSanPham().equalsIgnoreCase(tenSP)) {
                if (!sizes.contains(ct.getKichThuoc())) sizes.add(ct.getKichThuoc());
                if (!mauSacs.contains(ct.getMauSac())) mauSacs.add(ct.getMauSac());
            }
        }

        for (int s : sizes) cboSize.addItem(String.valueOf(s));
        for (String m : mauSacs) cboMauSac.addItem(m);

        capNhatThongTinBienThe();
    }

    private ChiTietGiay layBienTheDangChon() {
        String tenSP = (String) cboSanPham.getSelectedItem();
        String sizeStr = (String) cboSize.getSelectedItem();
        String mau = (String) cboMauSac.getSelectedItem();

        if (tenSP == null || sizeStr == null || mau == null) return null;
        int size = Integer.parseInt(sizeStr);

        for (ChiTietGiay ct : dsChiTietGiay) {
            if (ct.getSanPham().getTenSanPham().equalsIgnoreCase(tenSP) &&
                ct.getKichThuoc() == size &&
                ct.getMauSac().equalsIgnoreCase(mau)) {
                return ct;
            }
        }
        return null;
    }

    private void capNhatThongTinBienThe() {
        ChiTietGiay ct = layBienTheDangChon();
        if (ct != null) {
            lblTonKhoVal.setText(ct.getSoLuongTon() + " đôi");
            lblDonGiaVal.setText(df.format(ct.getSanPham().getGiaBan()));
        } else {
            lblTonKhoVal.setText("0 đôi");
            lblDonGiaVal.setText("0 VNĐ");
        }
    }

    private void tinhToanTongTienHoaDon() {
        double tongHang = 0;
        for (int i = 0; i < modelGioHang.getRowCount(); i++) {
            tongHang += (Double) modelGioHang.getValueAt(i, 8);
        }
        lblTongTienHangVal.setText(df.format(tongHang));

        double chietKhau = 0;
        if (khachHienTai != null) {
            chietKhau += tongHang * khachHienTai.tinhChietKhau();
            if (chkDungDiem.isSelected() && khachHienTai.getDiemTichLuy() > 0) {
                double tienDiem = khachHienTai.getDiemTichLuy() * 1000.0;
                chietKhau += Math.min(tienDiem, tongHang - chietKhau);
            }
        }
        lblChietKhauVal.setText(df.format(chietKhau));

        double khachCanTra = Math.max(0, tongHang - chietKhau);
        lblKhachCanTraVal.setText(df.format(khachCanTra));

        tinhTienThua();
    }

    private void tinhTienThua() {
        try {
            String str = txtTienKhachDua.getText().replace(",", "").replace(".", "").trim();
            double tienDua = str.isEmpty() ? 0 : Double.parseDouble(str);
            double canTra = Double.parseDouble(lblKhachCanTraVal.getText().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
            double thua = Math.max(0, tienDua - canTra);
            lblTienThuaVal.setText(df.format(thua));
        } catch (NumberFormatException e) {
            lblTienThuaVal.setText("0 VNĐ");
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();

        if (o.equals(btnThemGio)) {
            ChiTietGiay ct = layBienTheDangChon();
            if (ct == null) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn mẫu giày, size và màu hợp lệ!", "Lỗi", JOptionPane.WARNING_MESSAGE);
                return;
            }
            int slMua = (Integer) spnSoLuong.getValue();
            if (slMua > ct.getSoLuongTon()) {
                JOptionPane.showMessageDialog(this, "Tồn kho không đủ! Chỉ còn " + ct.getSoLuongTon() + " đôi.", "Cảnh báo hết hàng", JOptionPane.WARNING_MESSAGE);
                return;
            }

            int foundRow = -1;
            for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                if (modelGioHang.getValueAt(i, 1).equals(ct.getMaChiTietGiay())) {
                    foundRow = i;
                    break;
                }
            }

            if (foundRow >= 0) {
                int slCu = (Integer) modelGioHang.getValueAt(foundRow, 5);
                int slMoi = slCu + slMua;
                if (slMoi > ct.getSoLuongTon()) {
                    JOptionPane.showMessageDialog(this, "Tổng số lượng trong giỏ (" + slMoi + ") vượt quá tồn kho (" + ct.getSoLuongTon() + ")!", "Lỗi", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                modelGioHang.setValueAt(slMoi, foundRow, 5);
                double ttMoi = slMoi * ct.getSanPham().getGiaBan();
                modelGioHang.setValueAt(ttMoi, foundRow, 8);
            } else {
                int stt = modelGioHang.getRowCount() + 1;
                double donGia = ct.getSanPham().getGiaBan();
                double thanhTien = slMua * donGia;
                modelGioHang.addRow(new Object[]{
                        stt, ct.getMaChiTietGiay(), ct.getSanPham().getTenSanPham(),
                        ct.getKichThuoc(), ct.getMauSac(), slMua, donGia, 0.0, thanhTien
                });
            }

            tinhToanTongTienHoaDon();

        } else if (o.equals(btnXoaKhoiGio)) {
            int row = tableGioHang.getSelectedRow();
            if (row >= 0) {
                modelGioHang.removeRow(row);
                for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                    modelGioHang.setValueAt(i + 1, i, 0);
                }
                tinhToanTongTienHoaDon();
            } else {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn dòng cần xóa trong giỏ hàng!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
            }

        } else if (o.equals(btnXoaTrangGio)) {
            modelGioHang.setRowCount(0);
            tinhToanTongTienHoaDon();

        } else if (o.equals(btnTimKhach)) {
            String sdt = txtSDTKhach.getText().trim();
            if (sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập số điện thoại cần tìm!", "Lỗi", JOptionPane.WARNING_MESSAGE);
                return;
            }
            KhachHang kh = kh_dao.timTheoSoDienThoai(sdt);
            if (kh != null) {
                khachHienTai = kh;
                lblTenKhachVal.setText(kh.getHoTen());
                lblHangTheVal.setText(kh.getHangThanhVien() + " (Chiết khấu " + (int)(kh.tinhChietKhau()*100) + "%)");
                lblDiemVal.setText(kh.getDiemTichLuy() + " điểm");
                tinhToanTongTienHoaDon();
            } else {
                int opt = JOptionPane.showConfirmDialog(this, "Không tìm thấy khách hàng với SĐT này! Bạn có muốn thêm mới thành viên?", "Khách hàng mới", JOptionPane.YES_NO_OPTION);
                if (opt == JOptionPane.YES_OPTION) {
                    String tenMoi = JOptionPane.showInputDialog(this, "Nhập họ tên khách hàng mới:");
                    if (tenMoi != null && !tenMoi.trim().isEmpty()) {
                        String maMoi = "KH" + System.currentTimeMillis() % 10000;
                        KhachHang khMoi = new KhachHang(maMoi, tenMoi.trim(), sdt, null, true, "", "", 0, "Đồng");
                        kh_dao.themKhachHang(khMoi);
                        khachHienTai = khMoi;
                        lblTenKhachVal.setText(khMoi.getHoTen());
                        lblHangTheVal.setText("Đồng");
                        lblDiemVal.setText("0 điểm");
                        tinhToanTongTienHoaDon();
                    }
                }
            }

        } else if (o.equals(btnThanhToan)) {
            if (modelGioHang.getRowCount() == 0) {
                JOptionPane.showMessageDialog(this, "Giỏ hàng đang trống! Vui lòng thêm sản phẩm trước khi thanh toán.", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            double canTra = Double.parseDouble(lblKhachCanTraVal.getText().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
            String strDua = txtTienKhachDua.getText().replace(",", "").replace(".", "").trim();
            double tienDua = strDua.isEmpty() ? 0 : Double.parseDouble(strDua);

            if (cboPhuongThuc.getSelectedItem().equals("Tiền mặt") && tienDua < canTra) {
                JOptionPane.showMessageDialog(this, "Tiền khách đưa chưa đủ để thanh toán!", "Lỗi thanh toán", JOptionPane.ERROR_MESSAGE);
                return;
            }

            String maHD = "HD" + String.format("%06d", System.currentTimeMillis() % 1000000);
            HoaDon hd = new HoaDon(maHD, LocalDateTime.now(), nhanVienDangNhap, khachHienTai, canTra,
                    (String) cboPhuongThuc.getSelectedItem(), tienDua, Math.max(0, tienDua - canTra));

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

            boolean thanhCong = hd_dao.themHoaDon(hd);
            if (thanhCong) {
                StringBuilder bill = new StringBuilder();
                bill.append("=========================================\n");
                bill.append("       STEPUP FOOTWEAR STORE             \n");
                bill.append("  12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM      \n");
                bill.append("           HÓA ĐƠN BÁN LẺ                \n");
                bill.append("Mã HĐ: ").append(maHD).append("\n");
                bill.append("Ngày: ").append(LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm"))).append("\n");
                bill.append("Thu ngân: ").append(nhanVienDangNhap.getHoTen()).append("\n");
                bill.append("Khách hàng: ").append(khachHienTai != null ? khachHienTai.getHoTen() : "Khách vãng lai").append("\n");
                bill.append("-----------------------------------------\n");
                for (int i = 0; i < modelGioHang.getRowCount(); i++) {
                    bill.append(modelGioHang.getValueAt(i, 2)).append(" (Size ").append(modelGioHang.getValueAt(i, 3)).append(")\n");
                    bill.append("  ").append(modelGioHang.getValueAt(i, 5)).append(" x ").append(df.format(modelGioHang.getValueAt(i, 6)))
                            .append(" = ").append(df.format(modelGioHang.getValueAt(i, 8))).append("\n");
                }
                bill.append("-----------------------------------------\n");
                bill.append("TỔNG TIỀN:    ").append(lblKhachCanTraVal.getText()).append("\n");
                bill.append("Khách đưa:    ").append(df.format(tienDua)).append("\n");
                bill.append("Tiền thừa:    ").append(lblTienThuaVal.getText()).append("\n");
                bill.append("Hình thức:    ").append(cboPhuongThuc.getSelectedItem()).append("\n");
                bill.append("=========================================\n");
                bill.append("   CẢM ƠN QUÝ KHÁCH & HẸN GẶP LẠI!       \n");

                JTextArea area = new JTextArea(bill.toString(), 22, 35);
                area.setFont(new Font("Monospaced", Font.PLAIN, 12));
                area.setEditable(false);
                JOptionPane.showMessageDialog(this, new JScrollPane(area), "THANH TOÁN THÀNH CÔNG - HÓA ĐƠN K80", JOptionPane.INFORMATION_MESSAGE);

                modelGioHang.setRowCount(0);
                loadDataBienThe();
                capNhatThongTinBienThe();
                tinhToanTongTienHoaDon();
                txtTienKhachDua.setText("0");
            } else {
                JOptionPane.showMessageDialog(this, "Lỗi khi lưu giao dịch vào CSDL!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}

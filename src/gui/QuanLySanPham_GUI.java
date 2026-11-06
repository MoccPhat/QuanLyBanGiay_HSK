package gui;

import dao.ChiTietGiay_DAO;
import dao.SanPham_DAO;
import entity.ChiTietGiay;
import entity.NhanVien;
import entity.SanPham;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.text.DecimalFormat;
import java.util.List;

/**
 * Phân hệ Quản lý danh mục mẫu giày (StepUp POS).
 * - Cung cấp giao diện CRUD mẫu giày cho Quản lý.
 * - Kiểm tra chặt chẽ tính hợp lệ của dữ liệu trước khi gửi xuống DAO/CSDL (C6, K8).
 * - Tự động tạo biến thể khởi tạo (Size 40, Đen, Tồn 20) để sản phẩm mới có thể bán được ngay (C7, K9).
 * - Sử dụng cả ListSelectionListener và MouseListener để hỗ trợ phím mũi tên và click chuột (C8).
 */
public class QuanLySanPham_GUI extends JPanel implements ActionListener, MouseListener {
    private JTextField txtMaSP;
    private JTextField txtTenSP;
    private JComboBox<String> cboLoai;
    private JComboBox<String> cboThuongHieu;
    private JTextField txtGiaNhap;
    private JTextField txtGiaBan;
    private JTextField txtChatLieu;
    private JTextField txtTimKiem;

    private JButton btnThem;
    private JButton btnXoa;
    private JButton btnSua;
    private JButton btnXoaTrang;
    private JButton btnTim;

    private JTable tableSP;
    private DefaultTableModel modelSP;

    private NhanVien nhanVien;
    private SanPham_DAO sp_dao;
    private ChiTietGiay_DAO ctg_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    public QuanLySanPham_GUI() {
        this(null);
    }

    public QuanLySanPham_GUI(NhanVien nv) {
        this.nhanVien = nv;
        this.sp_dao = new SanPham_DAO();
        this.ctg_dao = new ChiTietGiay_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(245, 247, 250));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // 1. TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ DANH MỤC SẢN PHẨM GIÀY DÉP", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(new Color(30, 58, 138));
        add(lblHeader, BorderLayout.NORTH);

        // 2. VÙNG NHẬP LIỆU (FORM)
        JPanel pnlForm = new JPanel(new GridBagLayout());
        pnlForm.setBackground(Color.WHITE);
        pnlForm.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "Thông Tin Sản Phẩm Mẫu",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 10, 6, 10);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        g.gridx = 0; g.gridy = 0; pnlForm.add(new JLabel("Mã sản phẩm:"), g);
        txtMaSP = new JTextField(15);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaSP, g);

        g.gridx = 0; g.gridy = 1; pnlForm.add(new JLabel("Tên sản phẩm:"), g);
        txtTenSP = new JTextField(15);
        g.gridx = 1; g.gridy = 1; pnlForm.add(txtTenSP, g);

        g.gridx = 0; g.gridy = 2; pnlForm.add(new JLabel("Phân loại:"), g);
        cboLoai = new JComboBox<>(new String[]{"Sneaker", "Chạy bộ", "Sandal", "Giày Da", "Tập gym"});
        g.gridx = 1; g.gridy = 2; pnlForm.add(cboLoai, g);

        g.gridx = 0; g.gridy = 3; pnlForm.add(new JLabel("Thương hiệu:"), g);
        cboThuongHieu = new JComboBox<>(new String[]{"Nike", "Adidas", "Vans", "Converse", "Biti's", "Puma"});
        g.gridx = 1; g.gridy = 3; pnlForm.add(cboThuongHieu, g);

        // Cột 2
        g.gridx = 2; g.gridy = 0; pnlForm.add(new JLabel("Giá nhập (VNĐ):"), g);
        txtGiaNhap = new JTextField(15);
        g.gridx = 3; g.gridy = 0; pnlForm.add(txtGiaNhap, g);

        g.gridx = 2; g.gridy = 1; pnlForm.add(new JLabel("Giá bán niêm yết:"), g);
        txtGiaBan = new JTextField(15);
        g.gridx = 3; g.gridy = 1; pnlForm.add(txtGiaBan, g);

        g.gridx = 2; g.gridy = 2; pnlForm.add(new JLabel("Chất liệu:"), g);
        txtChatLieu = new JTextField(15);
        g.gridx = 3; g.gridy = 2; pnlForm.add(txtChatLieu, g);

        // Tìm kiếm
        g.gridx = 2; g.gridy = 3; pnlForm.add(new JLabel("Tìm kiếm (Tên/Mã):"), g);
        JPanel pnlTim = new JPanel(new BorderLayout(4, 0));
        pnlTim.setOpaque(false);
        txtTimKiem = new JTextField(10);
        btnTim = UIHelper.createDarkBtn("Tìm", 65, 28);
        pnlTim.add(txtTimKiem, BorderLayout.CENTER);
        pnlTim.add(btnTim, BorderLayout.EAST);
        g.gridx = 3; g.gridy = 3; pnlForm.add(pnlTim, g);

        // 3. NÚT CHỨC NĂNG
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        pnlButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Mới", 115, 34);
        btnXoa = UIHelper.createDangerBtn("Xóa Sản Phẩm", 130, 34);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 115, 34);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng Form", 130, 34);

        pnlButtons.add(btnThem);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnXoaTrang);

        JPanel pnlTop = new JPanel(new BorderLayout());
        pnlTop.add(pnlForm, BorderLayout.CENTER);
        pnlTop.add(pnlButtons, BorderLayout.SOUTH);
        add(pnlTop, BorderLayout.NORTH);

        // 4. BẢNG HIỂN THỊ JTABLE
        String[] headers = {"STT", "Mã Sản Phẩm", "Tên Sản Phẩm", "Phân Loại", "Thương Hiệu", "Giá Nhập", "Giá Bán", "Chất Liệu"};
        modelSP = new DefaultTableModel(headers, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };
        tableSP = new JTable(modelSP);
        tableSP.setRowHeight(26);
        tableSP.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        tableSP.getTableHeader().setBackground(new Color(241, 245, 249));

        JScrollPane scroll = new JScrollPane(tableSP);
        scroll.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "Danh Sách Mẫu Giày Hiện Có Trong Hệ Thống",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));
        add(scroll, BorderLayout.CENTER);

        // Đăng ký sự kiện
        btnThem.addActionListener(this);
        btnXoa.addActionListener(this);
        btnSua.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        btnTim.addActionListener(this);
        txtTimKiem.addActionListener(this);
        tableSP.addMouseListener(this);

        // C8: Thêm ListSelectionListener để điều hướng bàn phím mũi tên cũng nạp dữ liệu lên form
        tableSP.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                int row = tableSP.getSelectedRow();
                if (row >= 0) {
                    hienThiThongTinLenForm(row);
                }
            }
        });

        // Phân quyền: Nhân viên bán hàng chỉ được xem, không được thêm/sửa/xóa
        if (nhanVien != null && !nhanVien.isQuanLy()) {
            btnThem.setEnabled(false);
            btnSua.setEnabled(false);
            btnXoa.setEnabled(false);
            btnThem.setToolTipText("Chỉ Quản lý mới có quyền Thêm sản phẩm");
            btnSua.setToolTipText("Chỉ Quản lý mới có quyền Sửa sản phẩm");
            btnXoa.setToolTipText("Chỉ Quản lý mới có quyền Xóa sản phẩm");
        }

        // Đổ dữ liệu vào bảng
        DocDuLieuDatabaseVaoTable();
    }

    public void DocDuLieuDatabaseVaoTable() {
        modelSP.setRowCount(0);
        List<SanPham> list = sp_dao.getAllSanPham();
        if (list == null || list.isEmpty()) return;

        int stt = 1;
        for (SanPham sp : list) {
            modelSP.addRow(new Object[]{
                    stt++,
                    sp.getMaSanPham(),
                    sp.getTenSanPham(),
                    sp.getLoaiGiay(),
                    sp.getThuongHieu(),
                    df.format(sp.getGiaNhap()),
                    df.format(sp.getGiaBan()),
                    sp.getChatLieu()
            });
        }
    }

    private void hienThiThongTinLenForm(int row) {
        if (row < 0 || row >= modelSP.getRowCount()) return;
        txtMaSP.setText(modelSP.getValueAt(row, 1).toString());
        txtMaSP.setEditable(false); // Khóa ô mã khi đang chọn sản phẩm để sửa
        txtTenSP.setText(modelSP.getValueAt(row, 2).toString());
        cboLoai.setSelectedItem(modelSP.getValueAt(row, 3).toString());
        cboThuongHieu.setSelectedItem(modelSP.getValueAt(row, 4).toString());
        txtGiaNhap.setText(modelSP.getValueAt(row, 5).toString().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
        txtGiaBan.setText(modelSP.getValueAt(row, 6).toString().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
        Object cl = modelSP.getValueAt(row, 7);
        txtChatLieu.setText(cl != null ? cl.toString() : "");
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();

        // Kiểm tra phân quyền: Chỉ Quản lý mới được Thêm / Sửa / Xóa mẫu giày
        if (o.equals(btnThem) || o.equals(btnXoa) || o.equals(btnSua)) {
            if (nhanVien != null && !nhanVien.isQuanLy()) {
                JOptionPane.showMessageDialog(this, "Chỉ Quản lý mới có quyền Thêm, Sửa hoặc Xóa sản phẩm!", "Phân quyền", JOptionPane.WARNING_MESSAGE);
                return;
            }
        }

        if (o.equals(btnThem)) {
            String ma = txtMaSP.getText().trim();
            String ten = txtTenSP.getText().trim();
            String loai = (String) cboLoai.getSelectedItem();
            String hang = (String) cboThuongHieu.getSelectedItem();
            String chatLieu = txtChatLieu.getText().trim();

            if (ma.isEmpty() || ten.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập Mã và Tên sản phẩm!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (!ma.matches("^SP\\d{4}$")) {
                JOptionPane.showMessageDialog(this, "Mã sản phẩm phải có định dạng SPxxxx (Ví dụ: SP0001)!", "Lỗi định dạng", JOptionPane.ERROR_MESSAGE);
                txtMaSP.requestFocus();
                return;
            }

            if (sp_dao.kiemTraTrungMa(ma)) {
                JOptionPane.showMessageDialog(this, "Mã sản phẩm '" + ma + "' đã tồn tại trong hệ thống!", "Trùng dữ liệu", JOptionPane.ERROR_MESSAGE);
                txtMaSP.requestFocus();
                return;
            }

            try {
                double giaNhap = Double.parseDouble(txtGiaNhap.getText().replace(",", "").replace(".", "").trim());
                double giaBan = Double.parseDouble(txtGiaBan.getText().replace(",", "").replace(".", "").trim());

                if (giaNhap <= 0 || giaBan <= 0) {
                    JOptionPane.showMessageDialog(this, "Giá nhập và Giá bán phải lớn hơn 0!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                if (giaBan < giaNhap) {
                    JOptionPane.showMessageDialog(this, "Giá bán phải lớn hơn hoặc bằng giá nhập!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                SanPham sp = new SanPham(ma, ten, loai, hang, giaNhap, giaBan, chatLieu, true);
                if (sp_dao.themSanPham(sp)) {
                    // C7, K9: Tự động khởi tạo 1 biến thể cơ bản để sản phẩm mới có thể bán được ngay trên POS
                    String maCTG = ctg_dao.sinhMaChiTietGiayMoi();
                    ChiTietGiay ctg = new ChiTietGiay(maCTG, sp, 40, "Đen", 20, "default_shoe.png");
                    ctg_dao.themChiTietGiay(ctg);

                    JOptionPane.showMessageDialog(this, "Thêm sản phẩm mới thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    DocDuLieuDatabaseVaoTable();
                    xoaTrang();
                } else {
                    String err = sp_dao.getLastError();
                    JOptionPane.showMessageDialog(this, (err != null && !err.isEmpty()) ? err : "Không thể thêm sản phẩm!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Giá nhập và Giá bán phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
            }

        } else if (o.equals(btnXoa)) {
            int row = tableSP.getSelectedRow();
            if (row < 0) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn sản phẩm cần xóa trên bảng!", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }
            String ma = (String) modelSP.getValueAt(row, 1);
            int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc muốn ngừng kinh doanh mẫu giày " + ma + "?", "Xác nhận xóa", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                if (sp_dao.xoaSanPham(ma)) {
                    JOptionPane.showMessageDialog(this, "Đã ngừng kinh doanh mẫu giày " + ma + "!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    DocDuLieuDatabaseVaoTable();
                    xoaTrang();
                } else {
                    String err = sp_dao.getLastError();
                    JOptionPane.showMessageDialog(this, (err != null && !err.isEmpty()) ? err : "Không thể ngừng kinh doanh sản phẩm!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            }

        } else if (o.equals(btnSua)) {
            String ma = txtMaSP.getText().trim();
            String ten = txtTenSP.getText().trim();
            String loai = (String) cboLoai.getSelectedItem();
            String hang = (String) cboThuongHieu.getSelectedItem();
            String chatLieu = txtChatLieu.getText().trim();

            if (ma.isEmpty() || ten.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập Mã và Tên sản phẩm!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            try {
                double giaNhap = Double.parseDouble(txtGiaNhap.getText().replace(",", "").replace(".", "").trim());
                double giaBan = Double.parseDouble(txtGiaBan.getText().replace(",", "").replace(".", "").trim());

                if (giaNhap <= 0 || giaBan <= 0) {
                    JOptionPane.showMessageDialog(this, "Giá nhập và Giá bán phải lớn hơn 0!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                if (giaBan < giaNhap) {
                    JOptionPane.showMessageDialog(this, "Giá bán phải lớn hơn hoặc bằng giá nhập!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                SanPham sp = new SanPham(ma, ten, loai, hang, giaNhap, giaBan, chatLieu, true);
                if (sp_dao.capNhatSanPham(sp)) {
                    JOptionPane.showMessageDialog(this, "Cập nhật sản phẩm thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    DocDuLieuDatabaseVaoTable();
                    xoaTrang();
                } else {
                    String err = sp_dao.getLastError();
                    JOptionPane.showMessageDialog(this, (err != null && !err.isEmpty()) ? err : "Cập nhật sản phẩm thất bại!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Giá nhập và Giá bán phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi cập nhật dữ liệu: " + ex.getMessage(), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }

        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();

        } else if (o.equals(btnTim) || o.equals(txtTimKiem)) {
            String key = txtTimKiem.getText().trim().toLowerCase();
            if (key.isEmpty()) {
                DocDuLieuDatabaseVaoTable();
                return;
            }
            modelSP.setRowCount(0);
            List<SanPham> list = sp_dao.getAllSanPham();
            int stt = 1;
            for (SanPham sp : list) {
                if (sp.getMaSanPham().toLowerCase().contains(key) || sp.getTenSanPham().toLowerCase().contains(key)) {
                    modelSP.addRow(new Object[]{
                            stt++, sp.getMaSanPham(), sp.getTenSanPham(), sp.getLoaiGiay(),
                            sp.getThuongHieu(), df.format(sp.getGiaNhap()), df.format(sp.getGiaBan()), sp.getChatLieu()
                    });
                }
            }
        }
    }

    private void xoaTrang() {
        txtMaSP.setText("");
        txtMaSP.setEditable(true);
        txtTenSP.setText("");
        txtGiaNhap.setText("");
        txtGiaBan.setText("");
        txtChatLieu.setText("");
        txtTimKiem.setText("");
        tableSP.clearSelection();
        txtMaSP.requestFocus();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableSP.getSelectedRow();
        if (row >= 0) {
            hienThiThongTinLenForm(row);
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

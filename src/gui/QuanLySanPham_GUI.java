package gui;

import dao.SanPham_DAO;
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

    private SanPham_DAO sp_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    public QuanLySanPham_GUI() {
        sp_dao = new SanPham_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(245, 247, 250));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // 1. TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ DANH MỤC SẢN PHẨM GIÀY DÉP", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(new Color(30, 58, 138));
        add(lblHeader, BorderLayout.NORTH);

        // 2. VÙNG NHẬP LIỆU (FORM)
        JPanel pnlForm = UIHelper.createTitledPanel("Thông Tin Mẫu Giày Đang Chọn", UIHelper.PRIMARY_BLUE);
        pnlForm.setLayout(new GridBagLayout());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        JLabel lblMa = new JLabel("Mã sản phẩm:");
        lblMa.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 0; pnlForm.add(lblMa, g);
        txtMaSP = new JTextField(15);
        UIHelper.styleTextField(txtMaSP);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaSP, g);

        JLabel lblTen = new JLabel("Tên sản phẩm:");
        lblTen.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 1; pnlForm.add(lblTen, g);
        txtTenSP = new JTextField(15);
        UIHelper.styleTextField(txtTenSP);
        g.gridx = 1; g.gridy = 1; pnlForm.add(txtTenSP, g);

        JLabel lblLoai = new JLabel("Phân loại:");
        lblLoai.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 2; pnlForm.add(lblLoai, g);
        cboLoai = new JComboBox<>(new String[]{"Sneaker", "Chạy bộ", "Sandal", "Giày Da", "Tập gym"});
        UIHelper.styleComboBox(cboLoai);
        g.gridx = 1; g.gridy = 2; pnlForm.add(cboLoai, g);

        JLabel lblTH = new JLabel("Thương hiệu:");
        lblTH.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 3; pnlForm.add(lblTH, g);
        cboThuongHieu = new JComboBox<>(new String[]{"Nike", "Adidas", "Vans", "Converse", "Biti's", "Puma"});
        UIHelper.styleComboBox(cboThuongHieu);
        g.gridx = 1; g.gridy = 3; pnlForm.add(cboThuongHieu, g);

        // Cột 2
        JLabel lblGN = new JLabel("Giá nhập (VNĐ):");
        lblGN.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 0; pnlForm.add(lblGN, g);
        txtGiaNhap = new JTextField(15);
        UIHelper.styleTextField(txtGiaNhap);
        g.gridx = 3; g.gridy = 0; pnlForm.add(txtGiaNhap, g);

        JLabel lblGB = new JLabel("Giá bán niêm yết:");
        lblGB.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 1; pnlForm.add(lblGB, g);
        txtGiaBan = new JTextField(15);
        UIHelper.styleTextField(txtGiaBan);
        g.gridx = 3; g.gridy = 1; pnlForm.add(txtGiaBan, g);

        JLabel lblCL = new JLabel("Chất liệu:");
        lblCL.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 2; pnlForm.add(lblCL, g);
        txtChatLieu = new JTextField(15);
        UIHelper.styleTextField(txtChatLieu);
        g.gridx = 3; g.gridy = 2; pnlForm.add(txtChatLieu, g);

        // Tìm kiếm
        JLabel lblTK = new JLabel("Tìm kiếm (Tên/Mã):");
        lblTK.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 3; pnlForm.add(lblTK, g);
        JPanel pnlTim = new JPanel(new BorderLayout(6, 0));
        pnlTim.setOpaque(false);
        txtTimKiem = new JTextField(10);
        UIHelper.styleTextField(txtTimKiem);
        btnTim = UIHelper.createDarkBtn("Tìm", 65, 30);
        pnlTim.add(txtTimKiem, BorderLayout.CENTER);
        pnlTim.add(btnTim, BorderLayout.EAST);
        g.gridx = 3; g.gridy = 3; pnlForm.add(pnlTim, g);

        // 3. NÚT CHỨC NĂNG (Màu sắc chuẩn, chữ trắng nổi bật hoặc đen sắc nét)
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        pnlButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Mới", 125, 36);
        btnXoa = UIHelper.createDangerBtn("Xóa Sản Phẩm", 135, 36);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 125, 36);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng Form", 135, 36);

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
        UIHelper.styleTable(tableSP);

        JScrollPane scroll = new JScrollPane(tableSP);
        scroll.setBorder(UIHelper.createTitledPanel("Danh Sách Mẫu Giày Hiện Có Trong Cửa Hàng", UIHelper.PRIMARY_BLUE).getBorder());
        add(scroll, BorderLayout.CENTER);

        // Đăng ký sự kiện
        btnThem.addActionListener(this);
        btnXoa.addActionListener(this);
        btnSua.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        btnTim.addActionListener(this);
        tableSP.addMouseListener(this);

        // Đổ dữ liệu vào bảng
        DocDuLieuDatabaseVaoTable();
    }

    public void DocDuLieuDatabaseVaoTable() {
        modelSP.setRowCount(0);
        List<SanPham> list = sp_dao.getAllSanPham();
        if (list == null || list.isEmpty()) {
            // Demo fallback
            modelSP.addRow(new Object[]{1, "SP0001", "Nike Air Force 1 07 Low", "Sneaker", "Nike", "1,800,000 VNĐ", "2,600,000 VNĐ", "Da thật"});
            modelSP.addRow(new Object[]{2, "SP0002", "Adidas Ultraboost Light 23", "Chạy bộ", "Adidas", "2,400,000 VNĐ", "3,500,000 VNĐ", "Primeknit"});
            modelSP.addRow(new Object[]{3, "SP0003", "Vans Old Skool Classic", "Sneaker", "Vans", "1,100,000 VNĐ", "1,750,000 VNĐ", "Canvas"});
            return;
        }

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

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
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

            try {
                double giaNhap = Double.parseDouble(txtGiaNhap.getText().replace(",", "").replace(".", "").trim());
                double giaBan = Double.parseDouble(txtGiaBan.getText().replace(",", "").replace(".", "").trim());

                SanPham sp = new SanPham(ma, ten, loai, hang, giaNhap, giaBan, chatLieu, true);
                if (sp_dao.themSanPham(sp)) {
                    JOptionPane.showMessageDialog(this, "Thêm sản phẩm mới thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    DocDuLieuDatabaseVaoTable();
                    xoaTrang();
                } else {
                    JOptionPane.showMessageDialog(this, "Không thể thêm sản phẩm (Trùng mã)!", "Lỗi", JOptionPane.ERROR_MESSAGE);
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
                sp_dao.xoaSanPham(ma);
                DocDuLieuDatabaseVaoTable();
                xoaTrang();
            }

        } else if (o.equals(btnSua)) {
            String ma = txtMaSP.getText().trim();
            String ten = txtTenSP.getText().trim();
            String loai = (String) cboLoai.getSelectedItem();
            String hang = (String) cboThuongHieu.getSelectedItem();
            String chatLieu = txtChatLieu.getText().trim();

            try {
                double giaNhap = Double.parseDouble(txtGiaNhap.getText().replace(",", "").replace(".", "").trim());
                double giaBan = Double.parseDouble(txtGiaBan.getText().replace(",", "").replace(".", "").trim());

                SanPham sp = new SanPham(ma, ten, loai, hang, giaNhap, giaBan, chatLieu, true);
                if (sp_dao.capNhatSanPham(sp)) {
                    JOptionPane.showMessageDialog(this, "Cập nhật sản phẩm thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    DocDuLieuDatabaseVaoTable();
                }
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi cập nhật dữ liệu!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }

        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();

        } else if (o.equals(btnTim)) {
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
        txtTenSP.setText("");
        txtGiaNhap.setText("");
        txtGiaBan.setText("");
        txtChatLieu.setText("");
        txtTimKiem.setText("");
        txtMaSP.requestFocus();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableSP.getSelectedRow();
        if (row >= 0) {
            txtMaSP.setText(modelSP.getValueAt(row, 1).toString());
            txtTenSP.setText(modelSP.getValueAt(row, 2).toString());
            cboLoai.setSelectedItem(modelSP.getValueAt(row, 3).toString());
            cboThuongHieu.setSelectedItem(modelSP.getValueAt(row, 4).toString());
            txtGiaNhap.setText(modelSP.getValueAt(row, 5).toString().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
            txtGiaBan.setText(modelSP.getValueAt(row, 6).toString().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
            txtChatLieu.setText(modelSP.getValueAt(row, 7).toString());
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

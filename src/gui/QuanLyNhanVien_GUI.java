package gui;

import dao.NhanVien_DAO;
import entity.NhanVien;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.text.DecimalFormat;
import java.time.LocalDate;
import java.util.List;

public class QuanLyNhanVien_GUI extends JPanel implements ActionListener, MouseListener {
    private JTextField txtMaNV, txtHoTen, txtSDT, txtDiaChi, txtLuong, txtCaLam;
    private JComboBox<String> cboChucVu;
    private JRadioButton radNam, radNu;
    private JButton btnThem, btnXoa, btnSua, btnXoaTrang;
    private JTable tableNV;
    private DefaultTableModel modelNV;
    private NhanVien_DAO nv_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    public QuanLyNhanVien_GUI() {
        nv_dao = new NhanVien_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(245, 247, 250));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ DANH SÁCH NHÂN SỰ CỬA HÀNG", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(new Color(30, 58, 138));
        add(lblHeader, BorderLayout.NORTH);

        // FORM NHẬP LIỆU
        JPanel pnlForm = UIHelper.createTitledPanel("Thông Tin Chi Tiết Nhân Viên", UIHelper.PRIMARY_BLUE);
        pnlForm.setLayout(new GridBagLayout());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        JLabel lblMa = new JLabel("Mã nhân viên:");
        lblMa.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 0; pnlForm.add(lblMa, g);
        txtMaNV = new JTextField(15);
        UIHelper.styleTextField(txtMaNV);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaNV, g);

        JLabel lblTen = new JLabel("Họ và tên:");
        lblTen.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 1; pnlForm.add(lblTen, g);
        txtHoTen = new JTextField(15);
        UIHelper.styleTextField(txtHoTen);
        g.gridx = 1; g.gridy = 1; pnlForm.add(txtHoTen, g);

        JLabel lblSDT = new JLabel("Số điện thoại:");
        lblSDT.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 2; pnlForm.add(lblSDT, g);
        txtSDT = new JTextField(15);
        UIHelper.styleTextField(txtSDT);
        g.gridx = 1; g.gridy = 2; pnlForm.add(txtSDT, g);

        JLabel lblGT = new JLabel("Giới tính:");
        lblGT.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 3; pnlForm.add(lblGT, g);
        JPanel pnlGioiTinh = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        pnlGioiTinh.setOpaque(false);
        radNam = new JRadioButton("Nam", true);
        radNu = new JRadioButton("Nữ");
        radNam.setFont(new Font("Arial", Font.PLAIN, 12));
        radNu.setFont(new Font("Arial", Font.PLAIN, 12));
        radNam.setOpaque(false); radNu.setOpaque(false);
        ButtonGroup bg = new ButtonGroup();
        bg.add(radNam); bg.add(radNu);
        pnlGioiTinh.add(radNam); pnlGioiTinh.add(radNu);
        g.gridx = 1; g.gridy = 3; pnlForm.add(pnlGioiTinh, g);

        JLabel lblCV = new JLabel("Chức vụ:");
        lblCV.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 0; pnlForm.add(lblCV, g);
        cboChucVu = new JComboBox<>(new String[]{"Nhân viên bán hàng", "Quản lý"});
        UIHelper.styleComboBox(cboChucVu);
        g.gridx = 3; g.gridy = 0; pnlForm.add(cboChucVu, g);

        JLabel lblL = new JLabel("Lương cơ bản (VNĐ):");
        lblL.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 1; pnlForm.add(lblL, g);
        txtLuong = new JTextField("6500000", 15);
        UIHelper.styleTextField(txtLuong);
        g.gridx = 3; g.gridy = 1; pnlForm.add(txtLuong, g);

        JLabel lblCa = new JLabel("Ca làm việc:");
        lblCa.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 2; pnlForm.add(lblCa, g);
        txtCaLam = new JTextField("Ca sáng", 15);
        UIHelper.styleTextField(txtCaLam);
        g.gridx = 3; g.gridy = 2; pnlForm.add(txtCaLam, g);

        JLabel lblDC = new JLabel("Địa chỉ:");
        lblDC.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 3; pnlForm.add(lblDC, g);
        txtDiaChi = new JTextField("Gò Vấp, TP.HCM", 15);
        UIHelper.styleTextField(txtDiaChi);
        g.gridx = 3; g.gridy = 3; pnlForm.add(txtDiaChi, g);

        // Nút chức năng
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        pnlButtons.setBackground(Color.WHITE);
        btnThem = UIHelper.createSuccessBtn("Thêm Mới", 130, 36);
        btnXoa = UIHelper.createDangerBtn("Nghỉ Việc / Xóa", 150, 36);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 130, 36);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 130, 36);

        pnlButtons.add(btnThem);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnXoaTrang);

        JPanel pnlTop = new JPanel(new BorderLayout());
        pnlTop.add(pnlForm, BorderLayout.CENTER);
        pnlTop.add(pnlButtons, BorderLayout.SOUTH);
        add(pnlTop, BorderLayout.NORTH);

        // BẢNG NHÂN VIÊN
        String[] headers = {"STT", "Mã NV", "Họ Tên", "Giới Tính", "Số Điện Thoại", "Chức Vụ", "Lương Cơ Bản", "Ca Làm Việc"};
        modelNV = new DefaultTableModel(headers, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };
        tableNV = new JTable(modelNV);
        UIHelper.styleTable(tableNV);

        JScrollPane scroll = new JScrollPane(tableNV);
        scroll.setBorder(UIHelper.createTitledPanel("Danh Sách Nhân Sự Đang Hoạt Động", UIHelper.PRIMARY_BLUE).getBorder());
        add(scroll, BorderLayout.CENTER);

        btnThem.addActionListener(this);
        btnXoa.addActionListener(this);
        btnSua.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        tableNV.addMouseListener(this);

        docDuLieuVaoTable();
    }

    public void docDuLieuVaoTable() {
        modelNV.setRowCount(0);
        List<NhanVien> list = nv_dao.getAllNhanVien();
        int stt = 1;
        for (NhanVien nv : list) {
            modelNV.addRow(new Object[]{
                    stt++, nv.getMaNhanVien(), nv.getHoTen(), nv.isGioiTinh() ? "Nam" : "Nữ",
                    nv.getSoDienThoai(), nv.getChucVu(), df.format(nv.getLuongCoBan()), nv.getCaLamViec()
            });
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnThem)) {
            String ma = txtMaNV.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String chucVu = (String) cboChucVu.getSelectedItem();
            String ca = txtCaLam.getText().trim();
            String dc = txtDiaChi.getText().trim();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ thông tin nhân viên!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            try {
                double luong = Double.parseDouble(txtLuong.getText().replace(",", "").replace(".", "").trim());
                NhanVien nv = new NhanVien(ma, ten, sdt, LocalDate.of(2000, 1, 1), radNam.isSelected(), dc, "", chucVu, luong, ca, "123456", true);
                if (nv_dao.themNhanVien(nv)) {
                    JOptionPane.showMessageDialog(this, "Thêm nhân viên mới thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                } else {
                    JOptionPane.showMessageDialog(this, "Thêm thất bại (Trùng mã nhân viên)!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Lương cơ bản phải là số hợp lệ!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoa)) {
            int row = tableNV.getSelectedRow();
            String ma = (row >= 0) ? (String) modelNV.getValueAt(row, 1) : txtMaNV.getText().trim();
            if (ma.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn nhân viên cần xóa/cho thôi việc trên bảng!", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }
            if (ma.equalsIgnoreCase("NV0001")) {
                JOptionPane.showMessageDialog(this, "Không thể xóa tài khoản Quản Lý Trưởng!", "Cảnh báo bảo mật", JOptionPane.WARNING_MESSAGE);
                return;
            }
            int opt = JOptionPane.showConfirmDialog(this, "Xác nhận chuyển trạng thái nhân viên " + ma + " sang [Đã nghỉ việc]?", "Xác nhận xóa", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                if (nv_dao.xoaNhanVien(ma)) {
                    JOptionPane.showMessageDialog(this, "Đã cập nhật trạng thái nhân viên sang Đã nghỉ việc thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                    xoaTrang();
                } else {
                    JOptionPane.showMessageDialog(this, "Thao tác thất bại!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else if (o.equals(btnSua)) {
            String ma = txtMaNV.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String chucVu = (String) cboChucVu.getSelectedItem();
            String ca = txtCaLam.getText().trim();
            String dc = txtDiaChi.getText().trim();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn nhân viên và nhập đầy đủ thông tin!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            try {
                double luong = Double.parseDouble(txtLuong.getText().replace(",", "").replace(".", "").trim());
                NhanVien nv = new NhanVien(ma, ten, sdt, LocalDate.of(2000, 1, 1), radNam.isSelected(), dc, "", chucVu, luong, ca, "123456", true);
                if (nv_dao.capNhatNhanVien(nv)) {
                    JOptionPane.showMessageDialog(this, "Cập nhật thông tin nhân viên thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                } else {
                    JOptionPane.showMessageDialog(this, "Cập nhật nhân viên thất bại!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Lương cơ bản phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();
        }
    }

    private void xoaTrang() {
        txtMaNV.setText("");
        txtHoTen.setText("");
        txtSDT.setText("");
        txtLuong.setText("6500000");
        txtCaLam.setText("Ca sáng");
        txtDiaChi.setText("");
        radNam.setSelected(true);
        cboChucVu.setSelectedIndex(0);
        tableNV.clearSelection();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int r = tableNV.getSelectedRow();
        if (r >= 0) {
            txtMaNV.setText(modelNV.getValueAt(r, 1).toString());
            txtHoTen.setText(modelNV.getValueAt(r, 2).toString());
            boolean isNam = modelNV.getValueAt(r, 3).toString().equalsIgnoreCase("Nam");
            radNam.setSelected(isNam);
            radNu.setSelected(!isNam);
            txtSDT.setText(modelNV.getValueAt(r, 4).toString());
            cboChucVu.setSelectedItem(modelNV.getValueAt(r, 5).toString());
            txtLuong.setText(modelNV.getValueAt(r, 6).toString().replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
            txtCaLam.setText(modelNV.getValueAt(r, 7).toString());
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

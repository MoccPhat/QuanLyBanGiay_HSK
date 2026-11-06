package gui;

import dao.KhachHang_DAO;
import entity.KhachHang;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.List;

public class QuanLyKhachHang_GUI extends JPanel implements ActionListener, MouseListener {
    private JTextField txtMaKH, txtHoTen, txtSDT, txtDiaChi, txtEmail, txtDiem;
    private JComboBox<String> cboHang;
    private JButton btnThem, btnXoa, btnSua, btnXoaTrang, btnTim;
    private JTextField txtTimSDT;
    private JTable tableKH;
    private DefaultTableModel modelKH;
    private KhachHang_DAO kh_dao;

    public QuanLyKhachHang_GUI() {
        kh_dao = new KhachHang_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(245, 247, 250));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ HỒ SƠ KHÁCH HÀNG & TÍCH ĐIỂM", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(new Color(30, 58, 138));
        add(lblHeader, BorderLayout.NORTH);

        // FORM NHẬP LIỆU
        JPanel pnlForm = UIHelper.createTitledPanel("Thông Tin Khách Hàng & Thẻ Thành Viên", UIHelper.PRIMARY_BLUE);
        pnlForm.setLayout(new GridBagLayout());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        JLabel lblMa = new JLabel("Mã khách hàng:");
        lblMa.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 0; g.gridy = 0; pnlForm.add(lblMa, g);
        txtMaKH = new JTextField(15);
        UIHelper.styleTextField(txtMaKH);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaKH, g);

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

        JLabel lblDC = new JLabel("Địa chỉ:");
        lblDC.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 0; pnlForm.add(lblDC, g);
        txtDiaChi = new JTextField(15);
        UIHelper.styleTextField(txtDiaChi);
        g.gridx = 3; g.gridy = 0; pnlForm.add(txtDiaChi, g);

        JLabel lblDiem = new JLabel("Điểm tích lũy:");
        lblDiem.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 1; pnlForm.add(lblDiem, g);
        txtDiem = new JTextField("0", 15);
        txtDiem.setEditable(false);
        UIHelper.styleTextField(txtDiem);
        txtDiem.setForeground(UIHelper.SUCCESS_GREEN);
        txtDiem.setFont(new Font("Arial", Font.BOLD, 13));
        g.gridx = 3; g.gridy = 1; pnlForm.add(txtDiem, g);

        JLabel lblHang = new JLabel("Hạng thành viên:");
        lblHang.setFont(new Font("Arial", Font.BOLD, 12));
        g.gridx = 2; g.gridy = 2; pnlForm.add(lblHang, g);
        cboHang = new JComboBox<>(new String[]{"Đồng", "Bạc", "Vàng", "Kim Cương"});
        UIHelper.styleComboBox(cboHang);
        g.gridx = 3; g.gridy = 2; pnlForm.add(cboHang, g);

        // Nút bấm
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 12, 10));
        pnlButtons.setBackground(Color.WHITE);
        btnThem = UIHelper.createSuccessBtn("Thêm Mới", 110, 36);
        btnXoa = UIHelper.createDangerBtn("Xóa Khách", 110, 36);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 110, 36);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 110, 36);

        JLabel lblTraCuu = new JLabel("Tra cứu SĐT:");
        lblTraCuu.setFont(new Font("Arial", Font.BOLD, 12));
        txtTimSDT = new JTextField(12);
        UIHelper.styleTextField(txtTimSDT);
        btnTim = UIHelper.createDarkBtn("Tìm Kiếm", 90, 32);

        pnlButtons.add(btnThem);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnXoaTrang);
        pnlButtons.add(Box.createHorizontalStrut(10));
        pnlButtons.add(lblTraCuu);
        pnlButtons.add(txtTimSDT);
        pnlButtons.add(btnTim);

        JPanel pnlTop = new JPanel(new BorderLayout());
        pnlTop.add(pnlForm, BorderLayout.CENTER);
        pnlTop.add(pnlButtons, BorderLayout.SOUTH);
        add(pnlTop, BorderLayout.NORTH);

        // BẢNG DỮ LIỆU
        String[] headers = {"STT", "Mã KH", "Họ Tên", "Số Điện Thoại", "Địa Chỉ", "Điểm Tích Lũy", "Hạng Thành Viên"};
        modelKH = new DefaultTableModel(headers, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };
        tableKH = new JTable(modelKH);
        UIHelper.styleTable(tableKH);

        JScrollPane scroll = new JScrollPane(tableKH);
        scroll.setBorder(UIHelper.createTitledPanel("Danh Sách Khách Hàng & Lịch Sử Tích Điểm", UIHelper.PRIMARY_BLUE).getBorder());
        add(scroll, BorderLayout.CENTER);

        btnThem.addActionListener(this);
        btnXoa.addActionListener(this);
        btnSua.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        btnTim.addActionListener(this);
        tableKH.addMouseListener(this);

        docDuLieuVaoTable();
    }

    public void docDuLieuVaoTable() {
        modelKH.setRowCount(0);
        List<KhachHang> list = kh_dao.getAllKhachHang();
        int stt = 1;
        for (KhachHang kh : list) {
            modelKH.addRow(new Object[]{
                    stt++, kh.getMaKhachHang(), kh.getHoTen(), kh.getSoDienThoai(),
                    kh.getDiaChi(), kh.getDiemTichLuy(), kh.getHangThanhVien()
            });
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnThem)) {
            String ma = txtMaKH.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String dc = txtDiaChi.getText().trim();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ Mã, Họ tên và Số điện thoại!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            KhachHang kh = new KhachHang(ma, ten, sdt, null, true, dc, "", 0, (String) cboHang.getSelectedItem());
            if (kh_dao.themKhachHang(kh)) {
                JOptionPane.showMessageDialog(this, "Thêm khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                docDuLieuVaoTable();
            } else {
                JOptionPane.showMessageDialog(this, "Thêm thất bại (Trùng mã hoặc SĐT)!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoa)) {
            int row = tableKH.getSelectedRow();
            String ma = (row >= 0) ? (String) modelKH.getValueAt(row, 1) : txtMaKH.getText().trim();
            if (ma.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn khách hàng cần xóa từ bảng!", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }
            int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc muốn xóa khách hàng " + ma + "?", "Xác nhận xóa", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                if (kh_dao.xoaKhachHang(ma)) {
                    JOptionPane.showMessageDialog(this, "Xóa khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                    xoaTrang();
                } else {
                    JOptionPane.showMessageDialog(this, "Không thể xóa khách hàng này (Có thể đã có lịch sử hóa đơn liên kết)!", "Lỗi ràng buộc", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else if (o.equals(btnSua)) {
            String ma = txtMaKH.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String dc = txtDiaChi.getText().trim();
            String hang = (String) cboHang.getSelectedItem();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn khách hàng và nhập đầy đủ thông tin!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            int diem = 0;
            try {
                diem = Integer.parseInt(txtDiem.getText().trim());
            } catch (NumberFormatException ex) {}

            KhachHang kh = new KhachHang(ma, ten, sdt, null, true, dc, "", diem, hang);
            if (kh_dao.capNhatKhachHang(kh)) {
                JOptionPane.showMessageDialog(this, "Cập nhật thông tin khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                docDuLieuVaoTable();
            } else {
                JOptionPane.showMessageDialog(this, "Cập nhật thất bại!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();
        } else if (o.equals(btnTim)) {
            String sdt = txtTimSDT.getText().trim();
            if (sdt.isEmpty()) {
                docDuLieuVaoTable();
                return;
            }
            KhachHang kh = kh_dao.timTheoSoDienThoai(sdt);
            modelKH.setRowCount(0);
            if (kh != null) {
                modelKH.addRow(new Object[]{1, kh.getMaKhachHang(), kh.getHoTen(), kh.getSoDienThoai(), kh.getDiaChi(), kh.getDiemTichLuy(), kh.getHangThanhVien()});
            } else {
                JOptionPane.showMessageDialog(this, "Không tìm thấy khách hàng nào có SĐT: " + sdt, "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
            }
        }
    }

    private void xoaTrang() {
        txtMaKH.setText("");
        txtHoTen.setText("");
        txtSDT.setText("");
        txtDiaChi.setText("");
        txtDiem.setText("0");
        txtTimSDT.setText("");
        tableKH.clearSelection();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int r = tableKH.getSelectedRow();
        if (r >= 0) {
            txtMaKH.setText(modelKH.getValueAt(r, 1).toString());
            txtHoTen.setText(modelKH.getValueAt(r, 2).toString());
            txtSDT.setText(modelKH.getValueAt(r, 3).toString());
            txtDiaChi.setText(modelKH.getValueAt(r, 4).toString());
            txtDiem.setText(modelKH.getValueAt(r, 5).toString());
            cboHang.setSelectedItem(modelKH.getValueAt(r, 6).toString());
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

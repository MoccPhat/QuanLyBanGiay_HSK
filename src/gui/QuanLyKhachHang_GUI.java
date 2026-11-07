package gui;

import dao.KhachHang_DAO;
import entity.KhachHang;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.List;

/**
 * Phân hệ Quản lý khách hàng & Chương trình tích điểm thành viên (StepUp POS).
 * - Quản lý hồ sơ khách hàng, phân hạng thẻ (Đồng, Bạc, Vàng, Kim Cương).
 * - Kiểm tra dữ liệu: SĐT 10 chữ số bắt đầu bằng số 0 (C6).
 * - Sử dụng ListSelectionListener để điều hướng bàn phím mũi tên hiển thị dữ liệu form (C8).
 * - Khóa ô Mã khách hàng khi sửa.
 */
public class QuanLyKhachHang_GUI extends JPanel implements ActionListener, MouseListener {
    private JTextField txtMaKH;
    private JTextField txtHoTen;
    private JTextField txtSDT;
    private JTextField txtDiaChi;
    private JComboBox<String> cboHang;
    private JTextField txtDiem;
    private JTextField txtTimSDT;
    private JButton btnThem, btnXoa, btnSua, btnXoaTrang, btnTim;

    private JTable tableKH;
    private DefaultTableModel modelKH;
    private KhachHang_DAO kh_dao;
    private entity.NhanVien nhanVienDangNhap;

    public QuanLyKhachHang_GUI() {
        this(null);
    }

    public QuanLyKhachHang_GUI(entity.NhanVien nhanVien) {
        this.nhanVienDangNhap = nhanVien;
        kh_dao = new KhachHang_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(UIHelper.BG_MAIN);
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ THÔNG TIN KHÁCH HÀNG & CHƯƠNG TRÌNH TÍCH ĐIỂM", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(UIHelper.PRIMARY_BLUE);
        add(lblHeader, BorderLayout.NORTH);

        // FORM NHẬP LIỆU
        JPanel pnlForm = new JPanel(new GridBagLayout());
        pnlForm.setBackground(Color.WHITE);
        pnlForm.setBorder(UIHelper.createTitledPanel("Thông Tin Thành Viên", UIHelper.PRIMARY_BLUE).getBorder());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        g.gridx = 0; g.gridy = 0; pnlForm.add(new JLabel("Mã khách hàng:"), g);
        txtMaKH = new JTextField(15);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaKH, g);

        g.gridx = 0; g.gridy = 1; pnlForm.add(new JLabel("Họ và tên:"), g);
        txtHoTen = new JTextField(15);
        g.gridx = 1; g.gridy = 1; pnlForm.add(txtHoTen, g);

        g.gridx = 0; g.gridy = 2; pnlForm.add(new JLabel("Số điện thoại:"), g);
        txtSDT = new JTextField(15);
        g.gridx = 1; g.gridy = 2; pnlForm.add(txtSDT, g);

        // Cột 2
        g.gridx = 2; g.gridy = 0; pnlForm.add(new JLabel("Địa chỉ:"), g);
        txtDiaChi = new JTextField(15);
        g.gridx = 3; g.gridy = 0; pnlForm.add(txtDiaChi, g);

        g.gridx = 2; g.gridy = 1; pnlForm.add(new JLabel("Hạng thành viên:"), g);
        cboHang = new JComboBox<>(new String[]{"Đồng", "Bạc", "Vàng", "Kim Cương"});
        cboHang.setEnabled(false); // Khóa hạng thẻ, hệ thống tự động tính theo điểm tích lũy (chống gian lận VIP)
        g.gridx = 3; g.gridy = 1; pnlForm.add(cboHang, g);

        g.gridx = 2; g.gridy = 2; pnlForm.add(new JLabel("Điểm tích lũy:"), g);
        txtDiem = new JTextField("0", 15);
        txtDiem.setEditable(false);
        g.gridx = 3; g.gridy = 2; pnlForm.add(txtDiem, g);

        // NÚT CHỨC NĂNG
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 8));
        pnlButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Khách Hàng", 150, 34);
        btnXoa = UIHelper.createDangerBtn("Xóa Khách", 110, 34);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 110, 34);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 110, 34);

        JLabel lblTraCuu = new JLabel("Tìm SĐT:");
        lblTraCuu.setFont(new Font("Arial", Font.BOLD, 12));
        txtTimSDT = new JTextField(11);
        btnTim = UIHelper.createDarkBtn("Tìm", 65, 28);

        pnlButtons.add(btnThem);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnXoaTrang);
        pnlButtons.add(Box.createHorizontalStrut(20));
        pnlButtons.add(lblTraCuu);
        pnlButtons.add(txtTimSDT);
        pnlButtons.add(btnTim);

        // L14: Phân quyền - Thu ngân không được phép xóa khách hàng
        if (nhanVienDangNhap != null && !nhanVienDangNhap.isQuanLy()) {
            btnXoa.setEnabled(false);
            btnXoa.setToolTipText("Chỉ Quản lý mới có quyền xóa khách hàng!");
        }

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
        txtTimSDT.addActionListener(this);
        tableKH.addMouseListener(this);

        // C8: ListSelectionListener để điều hướng bàn phím mũi tên cũng nạp dữ liệu lên form
        tableKH.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                int row = tableKH.getSelectedRow();
                if (row >= 0) {
                    hienThiThongTinLenForm(row);
                }
            }
        });

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

    private void hienThiThongTinLenForm(int row) {
        if (row < 0 || row >= modelKH.getRowCount()) return;
        txtMaKH.setText((String) modelKH.getValueAt(row, 1));
        txtMaKH.setEditable(false); // Khóa ô mã khách hàng khi sửa
        txtHoTen.setText((String) modelKH.getValueAt(row, 2));
        txtSDT.setText((String) modelKH.getValueAt(row, 3));
        txtDiaChi.setText((String) modelKH.getValueAt(row, 4));
        txtDiem.setText(String.valueOf(modelKH.getValueAt(row, 5)));
        cboHang.setSelectedItem((String) modelKH.getValueAt(row, 6));
        cboHang.setEnabled(false);
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

            if (!ma.matches("^KH\\d{4}$")) {
                JOptionPane.showMessageDialog(this, "Mã khách hàng không đúng định dạng (phải là KHxxxx với 4 chữ số, ví dụ: KH0001)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtMaKH.requestFocus();
                return;
            }

            // Kiểm tra định dạng số điện thoại chuẩn khớp ràng buộc CK_KhachHang_sdt
            if (!sdt.matches("^0[35789]\\d{8}$")) {
                JOptionPane.showMessageDialog(this, "Số điện thoại không hợp lệ (phải gồm 10 chữ số, bắt đầu bằng 03, 05, 07, 08 hoặc 09)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            if (kh_dao.kiemTraTrungMa(ma)) {
                JOptionPane.showMessageDialog(this, "Mã khách hàng '" + ma + "' đã tồn tại trong hệ thống!", "Trùng mã khách hàng", JOptionPane.WARNING_MESSAGE);
                txtMaKH.requestFocus();
                return;
            }

            if (kh_dao.kiemTraTrungSDT(sdt, null)) {
                JOptionPane.showMessageDialog(this, "Số điện thoại '" + sdt + "' đã được đăng ký bởi khách hàng khác!", "Trùng số điện thoại", JOptionPane.WARNING_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            KhachHang kh = new KhachHang(ma, ten, sdt, null, true, dc.isEmpty() ? null : dc, null, 0, (String) cboHang.getSelectedItem());
            if (kh_dao.themKhachHang(kh)) {
                JOptionPane.showMessageDialog(this, "Thêm khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                docDuLieuVaoTable();
                xoaTrang();
            } else {
                String errMsg = kh_dao.getLastError();
                JOptionPane.showMessageDialog(this, "Thêm thất bại: " + (errMsg.isEmpty() ? "Lỗi cơ sở dữ liệu!" : errMsg), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoa)) {
            int row = tableKH.getSelectedRow();
            String ma = (row >= 0) ? (String) modelKH.getValueAt(row, 1) : txtMaKH.getText().trim();
            if (ma.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn khách hàng cần xóa từ bảng!", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }
            int opt = JOptionPane.showConfirmDialog(this, "Bạn có chắc chắn muốn xóa khách hàng " + ma + "?", "Xác nhận xóa", JOptionPane.YES_NO_OPTION);
            if (opt == JOptionPane.YES_OPTION) {
                if (kh_dao.xoaKhachHang(ma, nhanVienDangNhap)) {
                    JOptionPane.showMessageDialog(this, "Đã xóa khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                    xoaTrang();
                } else {
                    String errMsg = kh_dao.getLastError();
                    JOptionPane.showMessageDialog(this, "Không thể xóa: " + (errMsg == null || errMsg.isEmpty() ? "Lỗi hệ thống!" : errMsg), "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else if (o.equals(btnSua)) {
            String ma = txtMaKH.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String dc = txtDiaChi.getText().trim();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ Mã, Họ tên và Số điện thoại!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (!sdt.matches("^0[35789]\\d{8}$")) {
                JOptionPane.showMessageDialog(this, "Số điện thoại không hợp lệ (phải gồm 10 chữ số, bắt đầu bằng 03, 05, 07, 08 hoặc 09)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            if (!kh_dao.kiemTraTrungMa(ma)) {
                JOptionPane.showMessageDialog(this, "Khách hàng có mã '" + ma + "' không tồn tại trong hệ thống!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                return;
            }

            if (kh_dao.kiemTraTrungSDT(sdt, ma)) {
                JOptionPane.showMessageDialog(this, "Số điện thoại '" + sdt + "' đã được đăng ký bởi khách hàng khác!", "Trùng số điện thoại", JOptionPane.WARNING_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            int diem = 0;
            try {
                diem = Integer.parseInt(txtDiem.getText().trim());
            } catch (Exception ex) {
                diem = 0;
            }

            // L12: Bảo toàn ngaySinh, gioiTinh, email khi cập nhật từ giao diện
            KhachHang khCu = kh_dao.getKhachHangTheoMa(ma);
            java.time.LocalDate ns = (khCu != null) ? khCu.getNgaySinh() : null;
            boolean gt = (khCu != null) ? khCu.isGioiTinh() : true;
            String em = (khCu != null) ? khCu.getEmail() : null;

            KhachHang kh = new KhachHang(ma, ten, sdt, ns, gt, dc.isEmpty() ? null : dc, em, diem, "Đồng");
            kh.capNhatHang(); // Tự động đồng bộ hạng thẻ theo điểm tích lũy, không cho phép can thiệp thủ công
            cboHang.setSelectedItem(kh.getHangThanhVien());
            cboHang.setEnabled(false);
            if (kh_dao.capNhatKhachHang(kh)) {
                JOptionPane.showMessageDialog(this, "Cập nhật thông tin khách hàng thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                xoaTrang();
            } else {
                String errMsg = kh_dao.getLastError();
                JOptionPane.showMessageDialog(this, "Cập nhật thất bại: " + (errMsg.isEmpty() ? "Lỗi hệ thống!" : errMsg), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();
        } else if (o.equals(btnTim) || o.equals(txtTimSDT)) {
            String sdt = txtTimSDT.getText().trim();
            if (sdt.isEmpty()) {
                docDuLieuVaoTable();
                return;
            }
            KhachHang kh = kh_dao.timTheoSoDienThoai(sdt);
            modelKH.setRowCount(0);
            if (kh != null) {
                modelKH.addRow(new Object[]{
                        1, kh.getMaKhachHang(), kh.getHoTen(), kh.getSoDienThoai(),
                        kh.getDiaChi(), kh.getDiemTichLuy(), kh.getHangThanhVien()
                });
            } else {
                JOptionPane.showMessageDialog(this, "Không tìm thấy khách hàng với SĐT này!", "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
                docDuLieuVaoTable();
                txtTimSDT.selectAll();
                txtTimSDT.requestFocus();
            }
        }
    }

    private void xoaTrang() {
        txtMaKH.setText("");
        txtMaKH.setEditable(true);
        txtHoTen.setText("");
        txtSDT.setText("");
        txtDiaChi.setText("");
        txtDiem.setText("0");
        cboHang.setSelectedIndex(0);
        cboHang.setEnabled(false);
        txtTimSDT.setText("");
        tableKH.clearSelection();
        docDuLieuVaoTable();
        txtMaKH.requestFocus();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableKH.getSelectedRow();
        if (row >= 0) {
            hienThiThongTinLenForm(row);
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

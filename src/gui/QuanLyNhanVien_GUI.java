package gui;

import dao.NhanVien_DAO;
import entity.NhanVien;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.text.DecimalFormat;
import java.time.LocalDate;
import java.util.List;

/**
 * Phân hệ Quản lý nhân sự cửa hàng (StepUp POS).
 * - Dành riêng cho Quản lý.
 * - Kiểm tra dữ liệu đầu vào: Lương > 0, SĐT 10 chữ số đúng định dạng (C6).
 * - Sử dụng ListSelectionListener hỗ trợ chọn nhân viên bằng bàn phím (C8).
 * - Khóa ô Mã nhân viên khi cập nhật thông tin.
 */
public class QuanLyNhanVien_GUI extends JPanel implements ActionListener, MouseListener {
    private JTextField txtMaNV;
    private JTextField txtHoTen;
    private JTextField txtSDT;
    private JTextField txtDiaChi;
    private JTextField txtNgaySinh;
    private JTextField txtEmail;
    private JTextField txtLuong;
    private JPasswordField txtMatKhau;
    private JComboBox<String> cboCaLam;
    private JComboBox<String> cboChucVu;
    private JRadioButton radNam, radNu;
    private JButton btnThem, btnXoa, btnSua, btnDoiMatKhau, btnXoaTrang;

    private JTable tableNV;
    private DefaultTableModel modelNV;
    private NhanVien_DAO nv_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    public QuanLyNhanVien_GUI() {
        nv_dao = new NhanVien_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(UIHelper.BG_MAIN);
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // TIÊU ĐỀ
        JLabel lblHeader = new JLabel("QUẢN LÝ DANH SÁCH NHÂN SỰ & PHÂN QUYỀN HỆ THỐNG", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(UIHelper.PRIMARY_BLUE);
        add(lblHeader, BorderLayout.NORTH);

        // FORM NHẬP LIỆU
        JPanel pnlForm = new JPanel(new GridBagLayout());
        pnlForm.setBackground(Color.WHITE);
        pnlForm.setBorder(UIHelper.createTitledPanel("Thông Tin Chi Tiết Nhân Viên", UIHelper.PRIMARY_BLUE).getBorder());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        g.gridx = 0; g.gridy = 0; pnlForm.add(new JLabel("Mã nhân viên:"), g);
        txtMaNV = new JTextField(15);
        g.gridx = 1; g.gridy = 0; pnlForm.add(txtMaNV, g);

        g.gridx = 0; g.gridy = 1; pnlForm.add(new JLabel("Họ và tên:"), g);
        txtHoTen = new JTextField(15);
        g.gridx = 1; g.gridy = 1; pnlForm.add(txtHoTen, g);

        g.gridx = 0; g.gridy = 2; pnlForm.add(new JLabel("Số điện thoại:"), g);
        txtSDT = new JTextField(15);
        g.gridx = 1; g.gridy = 2; pnlForm.add(txtSDT, g);

        g.gridx = 0; g.gridy = 3; pnlForm.add(new JLabel("Giới tính:"), g);
        JPanel pnlGender = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        pnlGender.setOpaque(false);
        radNam = new JRadioButton("Nam", true);
        radNu = new JRadioButton("Nữ");
        ButtonGroup bgGender = new ButtonGroup();
        bgGender.add(radNam); bgGender.add(radNu);
        pnlGender.add(radNam); pnlGender.add(radNu);
        g.gridx = 1; g.gridy = 3; pnlForm.add(pnlGender, g);

        g.gridx = 0; g.gridy = 4; pnlForm.add(new JLabel("Ngày sinh (dd/MM/yyyy):"), g);
        txtNgaySinh = new JTextField("01/01/2000", 15);
        g.gridx = 1; g.gridy = 4; pnlForm.add(txtNgaySinh, g);

        g.gridx = 0; g.gridy = 5; pnlForm.add(new JLabel("Mật khẩu khởi tạo:"), g);
        txtMatKhau = new JPasswordField(15);
        g.gridx = 1; g.gridy = 5; pnlForm.add(txtMatKhau, g);

        // Cột 2
        g.gridx = 2; g.gridy = 0; pnlForm.add(new JLabel("Chức vụ:"), g);
        cboChucVu = new JComboBox<>(new String[]{"Nhân viên bán hàng", "Quản lý"});
        g.gridx = 3; g.gridy = 0; pnlForm.add(cboChucVu, g);

        g.gridx = 2; g.gridy = 1; pnlForm.add(new JLabel("Lương cơ bản (VNĐ):"), g);
        txtLuong = new JTextField(15);
        g.gridx = 3; g.gridy = 1; pnlForm.add(txtLuong, g);

        g.gridx = 2; g.gridy = 2; pnlForm.add(new JLabel("Ca làm việc:"), g);
        cboCaLam = new JComboBox<>(new String[]{"Toàn thời gian", "Ca sáng", "Ca chiều", "Ca tối"});
        g.gridx = 3; g.gridy = 2; pnlForm.add(cboCaLam, g);

        g.gridx = 2; g.gridy = 3; pnlForm.add(new JLabel("Địa chỉ:"), g);
        txtDiaChi = new JTextField(15);
        g.gridx = 3; g.gridy = 3; pnlForm.add(txtDiaChi, g);

        g.gridx = 2; g.gridy = 4; pnlForm.add(new JLabel("Email:"), g);
        txtEmail = new JTextField(15);
        g.gridx = 3; g.gridy = 4; pnlForm.add(txtEmail, g);

        // NÚT CHỨC NĂNG
        JPanel pnlButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 8));
        pnlButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Nhân Viên", 150, 34);
        btnXoa = UIHelper.createDangerBtn("Thôi Việc (Xóa)", 130, 34);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 110, 34);
        btnDoiMatKhau = UIHelper.createButton("Đổi Mật Khẩu", UIHelper.WARN_AMBER, Color.WHITE, 130, 34);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 110, 34);

        pnlButtons.add(btnThem);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnDoiMatKhau);
        pnlButtons.add(btnXoaTrang);

        JPanel pnlTop = new JPanel(new BorderLayout());
        pnlTop.add(pnlForm, BorderLayout.CENTER);
        pnlTop.add(pnlButtons, BorderLayout.SOUTH);
        add(pnlTop, BorderLayout.NORTH);

        // BẢNG NHÂN VIÊN
        String[] headers = {"STT", "Mã NV", "Họ Tên", "Giới Tính", "Số Điện Thoại", "Chức Vụ", "Lương Cơ Bản", "Ca Làm Việc", "Địa Chỉ"};
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
        btnDoiMatKhau.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        tableNV.addMouseListener(this);

        // C8: ListSelectionListener để điều hướng bàn phím mũi tên cũng nạp dữ liệu lên form
        tableNV.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                int row = tableNV.getSelectedRow();
                if (row >= 0) {
                    hienThiThongTinLenForm(row);
                }
            }
        });

        docDuLieuVaoTable();
    }

    public void docDuLieuVaoTable() {
        modelNV.setRowCount(0);
        List<NhanVien> list = nv_dao.getAllNhanVien();
        int stt = 1;
        for (NhanVien nv : list) {
            modelNV.addRow(new Object[]{
                    stt++, nv.getMaNhanVien(), nv.getHoTen(), nv.isGioiTinh() ? "Nam" : "Nữ",
                    nv.getSoDienThoai(), nv.getChucVu(), df.format(nv.getLuongCoBan()), nv.getCaLamViec(), nv.getDiaChi()
            });
        }
    }

    private void hienThiThongTinLenForm(int row) {
        if (row < 0 || row >= modelNV.getRowCount()) return;
        String ma = (String) modelNV.getValueAt(row, 1);
        txtMaNV.setText(ma);
        txtMaNV.setEditable(false); // Khóa mã nhân viên khi sửa
        txtHoTen.setText((String) modelNV.getValueAt(row, 2));
        String gt = (String) modelNV.getValueAt(row, 3);
        if ("Nam".equalsIgnoreCase(gt)) radNam.setSelected(true);
        else radNu.setSelected(true);
        txtSDT.setText((String) modelNV.getValueAt(row, 4));
        cboChucVu.setSelectedItem((String) modelNV.getValueAt(row, 5));
        txtLuong.setText(String.valueOf(modelNV.getValueAt(row, 6)).replace(" VNĐ", "").replace(",", "").replace(".", "").trim());
        String ca = (String) modelNV.getValueAt(row, 7);
        if (ca != null) cboCaLam.setSelectedItem(ca);
        Object dc = modelNV.getValueAt(row, 8);
        txtDiaChi.setText(dc != null ? dc.toString() : "");

        NhanVien nv = nv_dao.getNhanVienTheoMa(ma);
        if (nv != null) {
            if (nv.getNgaySinh() != null) {
                txtNgaySinh.setText(nv.getNgaySinh().format(java.time.format.DateTimeFormatter.ofPattern("dd/MM/yyyy")));
            } else {
                txtNgaySinh.setText("01/01/2000");
            }
            txtEmail.setText(nv.getEmail() != null ? nv.getEmail() : "");
        }
        txtMatKhau.setText("");
        txtMatKhau.setEditable(false);
    }

    private LocalDate parseNgaySinh(String text) {
        if (text == null || text.trim().isEmpty()) return null;
        text = text.trim();
        String[] patterns = {"dd/MM/yyyy", "d/M/yyyy", "yyyy-MM-dd", "yyyy/MM/dd"};
        for (String pattern : patterns) {
            try {
                return LocalDate.parse(text, java.time.format.DateTimeFormatter.ofPattern(pattern));
            } catch (Exception ignored) {}
        }
        return null;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnThem)) {
            String ma = txtMaNV.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String chucVu = (String) cboChucVu.getSelectedItem();
            String ca = (String) cboCaLam.getSelectedItem();
            String dc = txtDiaChi.getText().trim();
            String em = txtEmail.getText().trim();
            String nsStr = txtNgaySinh.getText().trim();
            String pwd = new String(txtMatKhau.getPassword()).trim();

            if (ma.isEmpty() || ten.isEmpty() || sdt.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ Mã, Họ tên và Số điện thoại!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (!ma.matches("^NV\\d{4}$")) {
                JOptionPane.showMessageDialog(this, "Mã nhân viên phải theo định dạng NVxxxx (ví dụ: NV0005)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtMaNV.requestFocus();
                return;
            }

            // Kiểm tra định dạng số điện thoại chuẩn khớp ràng buộc CK_NhanVien_sdt
            if (!sdt.matches("^0[35789]\\d{8}$")) {
                JOptionPane.showMessageDialog(this, "Số điện thoại không hợp lệ (phải gồm 10 chữ số bắt đầu bằng 03, 05, 07, 08, 09)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            LocalDate ngaySinh = parseNgaySinh(nsStr);
            if (ngaySinh == null) {
                JOptionPane.showMessageDialog(this, "Ngày sinh không hợp lệ (định dạng dd/MM/yyyy, ví dụ: 20/08/1998)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
                return;
            }

            // Kiểm tra độ tuổi theo ràng buộc CK_NhanVien_tuoi (>= 18 tuổi)
            int tuoi = java.time.Period.between(ngaySinh, LocalDate.now()).getYears();
            if (tuoi < 18) {
                JOptionPane.showMessageDialog(this, "Nhân viên phải từ 18 tuổi trở lên!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
                return;
            }

            if (!em.isEmpty() && !em.matches("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$")) {
                JOptionPane.showMessageDialog(this, "Email không đúng định dạng (ví dụ: nhanvien@stepup.vn)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtEmail.requestFocus();
                return;
            }

            if (pwd.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập mật khẩu khởi tạo cho nhân viên mới!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtMatKhau.requestFocus();
                return;
            }
            if (pwd.length() < 6) {
                JOptionPane.showMessageDialog(this, "Mật khẩu khởi tạo phải từ 6 ký tự trở lên!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtMatKhau.requestFocus();
                return;
            }

            if (nv_dao.kiemTraTrungMa(ma)) {
                JOptionPane.showMessageDialog(this, "Mã nhân viên '" + ma + "' đã tồn tại trong hệ thống!", "Trùng mã", JOptionPane.WARNING_MESSAGE);
                txtMaNV.requestFocus();
                return;
            }

            if (nv_dao.kiemTraTrungSDT(sdt, null)) {
                JOptionPane.showMessageDialog(this, "Số điện thoại '" + sdt + "' đã được sử dụng bởi nhân viên khác!", "Trùng số điện thoại", JOptionPane.WARNING_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            try {
                double luong = Double.parseDouble(txtLuong.getText().replace(",", "").replace(".", "").trim());
                if (luong <= 0) {
                    JOptionPane.showMessageDialog(this, "Lương cơ bản phải lớn hơn 0!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                NhanVien nv = new NhanVien(ma, ten, sdt, ngaySinh, radNam.isSelected(), dc.isEmpty() ? null : dc, em.isEmpty() ? null : em, chucVu, luong, ca, pwd, true);
                if (nv_dao.themNhanVien(nv)) {
                    JOptionPane.showMessageDialog(this, "Thêm nhân viên mới thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                    xoaTrang();
                } else {
                    String err = nv_dao.getLastError();
                    JOptionPane.showMessageDialog(this, "Thêm thất bại: " + (err.isEmpty() ? "Vui lòng kiểm tra lại thông tin!" : err), "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Lương cơ bản phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
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
                    String err = nv_dao.getLastError();
                    JOptionPane.showMessageDialog(this, "Thao tác thất bại: " + (err.isEmpty() ? "Lỗi cơ sở dữ liệu!" : err), "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else if (o.equals(btnSua)) {
            String ma = txtMaNV.getText().trim();
            String ten = txtHoTen.getText().trim();
            String sdt = txtSDT.getText().trim();
            String chucVu = (String) cboChucVu.getSelectedItem();
            String ca = (String) cboCaLam.getSelectedItem();
            String dc = txtDiaChi.getText().trim();
            String em = txtEmail.getText().trim();
            String nsStr = txtNgaySinh.getText().trim();

            if (ma.isEmpty() || ten.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn nhân viên và nhập đầy đủ thông tin!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (!sdt.matches("^0[35789]\\d{8}$")) {
                JOptionPane.showMessageDialog(this, "Số điện thoại không hợp lệ (phải gồm 10 chữ số bắt đầu bằng 03, 05, 07, 08, 09)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            LocalDate ngaySinh = parseNgaySinh(nsStr);
            if (ngaySinh == null) {
                JOptionPane.showMessageDialog(this, "Ngày sinh không hợp lệ (định dạng dd/MM/yyyy, ví dụ: 20/08/1998)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
                return;
            }

            int tuoi = java.time.Period.between(ngaySinh, LocalDate.now()).getYears();
            if (tuoi < 18) {
                JOptionPane.showMessageDialog(this, "Nhân viên phải từ 18 tuổi trở lên!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
                return;
            }

            if (!em.isEmpty() && !em.matches("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$")) {
                JOptionPane.showMessageDialog(this, "Email không đúng định dạng (ví dụ: nhanvien@stepup.vn)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtEmail.requestFocus();
                return;
            }

            if (nv_dao.kiemTraTrungSDT(sdt, ma)) {
                JOptionPane.showMessageDialog(this, "Số điện thoại '" + sdt + "' đã được sử dụng bởi nhân viên khác!", "Trùng số điện thoại", JOptionPane.WARNING_MESSAGE);
                txtSDT.requestFocus();
                return;
            }

            try {
                double luong = Double.parseDouble(txtLuong.getText().replace(",", "").replace(".", "").trim());
                if (luong <= 0) {
                    JOptionPane.showMessageDialog(this, "Lương cơ bản phải lớn hơn 0!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                NhanVien nv = new NhanVien(ma, ten, sdt, ngaySinh, radNam.isSelected(), dc.isEmpty() ? null : dc, em.isEmpty() ? null : em, chucVu, luong, ca, "", true);
                if (nv_dao.capNhatNhanVien(nv)) {
                    JOptionPane.showMessageDialog(this, "Cập nhật thông tin nhân viên thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                    docDuLieuVaoTable();
                    xoaTrang();
                } else {
                    String err = nv_dao.getLastError();
                    JOptionPane.showMessageDialog(this, "Cập nhật thất bại: " + (err.isEmpty() ? "Lỗi cập nhật CSDL!" : err), "Lỗi", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Lương cơ bản phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
            }
        } else if (o.equals(btnDoiMatKhau)) {
            hienThiDialogDoiMatKhau();
        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();
        }
    }

    private void hienThiDialogDoiMatKhau() {
        int row = tableNV.getSelectedRow();
        String ma = (row >= 0) ? (String) modelNV.getValueAt(row, 1) : txtMaNV.getText().trim();
        if (ma.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn nhân viên cần đổi mật khẩu từ bảng danh sách!", "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Window parentWindow = SwingUtilities.getWindowAncestor(this);
        JDialog dlg = new JDialog((Frame) (parentWindow instanceof Frame ? parentWindow : null), "Đổi Mật Khẩu - " + ma, true);
        dlg.setLayout(new BorderLayout(10, 10));
        dlg.setSize(380, 240);
        dlg.setLocationRelativeTo(this);

        JPanel pnlContent = new JPanel(new GridBagLayout());
        pnlContent.setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));
        pnlContent.setBackground(Color.WHITE);

        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(5, 5, 5, 5);
        gc.fill = GridBagConstraints.HORIZONTAL;

        gc.gridx = 0; gc.gridy = 0; pnlContent.add(new JLabel("Mã nhân viên:"), gc);
        JTextField txtMaDlg = new JTextField(ma, 15);
        txtMaDlg.setEditable(false);
        gc.gridx = 1; gc.gridy = 0; pnlContent.add(txtMaDlg, gc);

        gc.gridx = 0; gc.gridy = 1; pnlContent.add(new JLabel("Mật khẩu cũ:"), gc);
        JPasswordField txtOldPass = new JPasswordField(15);
        gc.gridx = 1; gc.gridy = 1; pnlContent.add(txtOldPass, gc);

        gc.gridx = 0; gc.gridy = 2; pnlContent.add(new JLabel("Mật khẩu mới:"), gc);
        JPasswordField txtNewPass = new JPasswordField(15);
        gc.gridx = 1; gc.gridy = 2; pnlContent.add(txtNewPass, gc);

        gc.gridx = 0; gc.gridy = 3; pnlContent.add(new JLabel("Xác nhận MK mới:"), gc);
        JPasswordField txtConfirmPass = new JPasswordField(15);
        gc.gridx = 1; gc.gridy = 3; pnlContent.add(txtConfirmPass, gc);

        JPanel pnlBtn = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
        JButton btnSave = UIHelper.createSuccessBtn("Lưu Thay Đổi", 120, 32);
        JButton btnCancel = UIHelper.createSecondaryBtn("Đóng", 80, 32);
        pnlBtn.add(btnSave);
        pnlBtn.add(btnCancel);

        btnSave.addActionListener(ev -> {
            String oldP = new String(txtOldPass.getPassword()).trim();
            String newP = new String(txtNewPass.getPassword()).trim();
            String confP = new String(txtConfirmPass.getPassword()).trim();

            if (oldP.isEmpty()) {
                JOptionPane.showMessageDialog(dlg, "Vui lòng nhập mật khẩu cũ!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                txtOldPass.requestFocus();
                return;
            }
            if (newP.length() < 6) {
                JOptionPane.showMessageDialog(dlg, "Mật khẩu mới phải từ 6 ký tự trở lên!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                txtNewPass.requestFocus();
                return;
            }
            if (!newP.equals(confP)) {
                JOptionPane.showMessageDialog(dlg, "Mật khẩu xác nhận không khớp với mật khẩu mới!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                txtConfirmPass.requestFocus();
                return;
            }

            if (nv_dao.doiMatKhau(ma, oldP, newP)) {
                JOptionPane.showMessageDialog(dlg, "Đổi mật khẩu cho nhân viên '" + ma + "' thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
                dlg.dispose();
            } else {
                String err = nv_dao.getLastError();
                JOptionPane.showMessageDialog(dlg, "Đổi mật khẩu thất bại: " + (err.isEmpty() ? "Lỗi hệ thống!" : err), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });

        btnCancel.addActionListener(ev -> dlg.dispose());

        dlg.add(pnlContent, BorderLayout.CENTER);
        dlg.add(pnlBtn, BorderLayout.SOUTH);
        dlg.setVisible(true);
    }

    private void xoaTrang() {
        txtMaNV.setText("");
        txtMaNV.setEditable(true);
        txtHoTen.setText("");
        txtSDT.setText("");
        txtDiaChi.setText("");
        txtNgaySinh.setText("01/01/2000");
        txtEmail.setText("");
        txtLuong.setText("");
        txtMatKhau.setText("");
        txtMatKhau.setEditable(true);
        cboCaLam.setSelectedIndex(0);
        radNam.setSelected(true);
        cboChucVu.setSelectedIndex(0);
        tableNV.clearSelection();
        txtMaNV.requestFocus();
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableNV.getSelectedRow();
        if (row >= 0) {
            hienThiThongTinLenForm(row);
        }
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}

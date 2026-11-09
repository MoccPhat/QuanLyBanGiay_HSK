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
import java.util.ArrayList;
import java.util.List;

/**
 * Phân hệ Quản lý nhân sự cửa hàng và phân quyền tài khoản người dùng.
 * Thuộc tầng Presentation (GUI) trong kiến trúc 3 tầng, tiếp nhận các thao tác CRUD nhân viên và phân quyền qua NhanVien_DAO.
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
    private JButton btnThem, btnXoa, btnSua, btnXemChiTiet, btnXoaTrang, btnTimNV;
    private JTextField txtTimNV;

    private JTable tableNV;
    private DefaultTableModel modelNV;
    private NhanVien_DAO nv_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    /**
     * Khởi tạo giao diện quản lý nhân sự với các trường nhập liệu thông tin cá nhân, chức vụ, ca làm việc và bảng danh sách.
     */
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
        JPanel pForm = new JPanel(new GridBagLayout());
        pForm.setBackground(Color.WHITE);
        pForm.setBorder(UIHelper.createTitledPanel("Thông Tin Chi Tiết Nhân Viên", UIHelper.PRIMARY_BLUE).getBorder());

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 12, 6, 12);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        g.gridx = 0; g.gridy = 0; pForm.add(new JLabel("Mã nhân viên:"), g);
        txtMaNV = new JTextField(15);
        g.gridx = 1; g.gridy = 0; pForm.add(txtMaNV, g);

        g.gridx = 0; g.gridy = 1; pForm.add(new JLabel("Họ và tên:"), g);
        txtHoTen = new JTextField(15);
        g.gridx = 1; g.gridy = 1; pForm.add(txtHoTen, g);

        g.gridx = 0; g.gridy = 2; pForm.add(new JLabel("Số điện thoại:"), g);
        txtSDT = new JTextField(15);
        g.gridx = 1; g.gridy = 2; pForm.add(txtSDT, g);

        g.gridx = 0; g.gridy = 3; pForm.add(new JLabel("Giới tính:"), g);
        JPanel pGender = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        pGender.setOpaque(false);
        radNam = new JRadioButton("Nam", true);
        radNu = new JRadioButton("Nữ");
        ButtonGroup bgGender = new ButtonGroup();
        bgGender.add(radNam); bgGender.add(radNu);
        pGender.add(radNam); pGender.add(radNu);
        g.gridx = 1; g.gridy = 3; pForm.add(pGender, g);

        g.gridx = 0; g.gridy = 4; pForm.add(new JLabel("Ngày sinh (dd/MM/yyyy):"), g);
        txtNgaySinh = new JTextField(15);
        txtNgaySinh.setToolTipText("dd/MM/yyyy");
        g.gridx = 1; g.gridy = 4; pForm.add(txtNgaySinh, g);

        g.gridx = 0; g.gridy = 5; pForm.add(new JLabel("Mật khẩu khởi tạo:"), g);
        txtMatKhau = new JPasswordField(15);
        g.gridx = 1; g.gridy = 5; pForm.add(txtMatKhau, g);

        // Cột 2
        g.gridx = 2; g.gridy = 0; pForm.add(new JLabel("Chức vụ:"), g);
        cboChucVu = new JComboBox<>(new String[]{"Nhân viên bán hàng", "Quản lý"});
        g.gridx = 3; g.gridy = 0; pForm.add(cboChucVu, g);

        g.gridx = 2; g.gridy = 1; pForm.add(new JLabel("Lương cơ bản (VNĐ):"), g);
        txtLuong = new JTextField(15);
        g.gridx = 3; g.gridy = 1; pForm.add(txtLuong, g);

        g.gridx = 2; g.gridy = 2; pForm.add(new JLabel("Ca làm việc:"), g);
        cboCaLam = new JComboBox<>(new String[]{"Toàn thời gian", "Ca sáng", "Ca chiều", "Ca tối"});
        g.gridx = 3; g.gridy = 2; pForm.add(cboCaLam, g);

        g.gridx = 2; g.gridy = 3; pForm.add(new JLabel("Địa chỉ:"), g);
        txtDiaChi = new JTextField(15);
        g.gridx = 3; g.gridy = 3; pForm.add(txtDiaChi, g);

        g.gridx = 2; g.gridy = 4; pForm.add(new JLabel("Email:"), g);
        txtEmail = new JTextField(15);
        g.gridx = 3; g.gridy = 4; pForm.add(txtEmail, g);

        // NÚT CHỨC NĂNG
        JPanel pButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 8));
        pButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Nhân Viên", 140, 34);
        btnXoa = UIHelper.createDangerBtn("Thôi Việc", 100, 34);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 95, 34);
        btnXemChiTiet = UIHelper.createButton("Xem Chi Tiết", UIHelper.PRIMARY_BLUE, Color.WHITE, 115, 34);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 95, 34);

        JLabel lblTim = new JLabel("Tìm NV:");
        lblTim.setFont(new Font("Arial", Font.BOLD, 12));
        txtTimNV = new JTextField(9);
        btnTimNV = UIHelper.createDarkBtn("Tìm", 60, 28);

        pButtons.add(btnThem);
        pButtons.add(btnXoa);
        pButtons.add(btnSua);
        pButtons.add(btnXemChiTiet);
        pButtons.add(btnXoaTrang);
        pButtons.add(Box.createHorizontalStrut(10));
        pButtons.add(lblTim);
        pButtons.add(txtTimNV);
        pButtons.add(btnTimNV);

        JPanel pTop = new JPanel(new BorderLayout());
        pTop.add(pForm, BorderLayout.CENTER);
        pTop.add(pButtons, BorderLayout.SOUTH);
        add(pTop, BorderLayout.NORTH);

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
        btnXemChiTiet.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        btnTimNV.addActionListener(this);
        txtTimNV.addActionListener(this);
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

    /**
     * Nạp toàn bộ danh sách nhân viên từ cơ sở dữ liệu lên bảng hiển thị JTable.
     */
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

    /**
     * Hiển thị thông tin chi tiết của nhân viên được chọn trên bảng lên các trường nhập liệu của form.
     *
     * @param row chỉ số dòng đang được chọn trong bảng nhân viên
     */
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
                txtNgaySinh.setText("");
            }
            txtEmail.setText(nv.getEmail() != null ? nv.getEmail() : "");
        }
        txtMatKhau.setText("");
        txtMatKhau.setEditable(false);
    }

    /**
     * Chuyển đổi chuỗi ngày sinh theo định dạng linh hoạt (dd/MM/yyyy hoặc chuỗi số 8 ký tự ddMMyyyy) sang LocalDate.
     *
     * @param text chuỗi văn bản chứa thông tin ngày sinh do người dùng nhập
     * @return đối tượng LocalDate tương ứng hoặc ném ngoại lệ nếu định dạng không hợp lệ
     */
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

    /**
     * Xử lý các sự kiện hành động trên form: Thêm nhân viên, Cập nhật thông tin, Xóa/Nghỉ việc, Xóa trắng form, Tìm kiếm hoặc Lọc chức vụ.
     *
     * @param e sự kiện hành động của người dùng
     */
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

            if (nsStr == null || nsStr.trim().isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập ngày sinh (dd/MM/yyyy)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
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
                JOptionPane.showMessageDialog(this, "Email không đúng định dạng (ví dụ: nhanvien@gmail.com)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
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

            if (nsStr == null || nsStr.trim().isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập ngày sinh (dd/MM/yyyy)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                txtNgaySinh.requestFocus();
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
                JOptionPane.showMessageDialog(this, "Email không đúng định dạng (ví dụ: nhanvien@gmail.com)!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
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
        } else if (o.equals(btnXemChiTiet)) {
            int row = tableNV.getSelectedRow();
            if (row < 0) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn một nhân viên trong bảng để xem chi tiết hồ sơ!", "Chưa chọn nhân viên", JOptionPane.WARNING_MESSAGE);
                return;
            }
            String maNV = (String) modelNV.getValueAt(row, 1);
            hienThiChiTietNhanVien(maNV);
        } else if (o.equals(btnTimNV) || o.equals(txtTimNV)) {
            String tuKhoa = txtTimNV.getText().trim();
            if (tuKhoa.isEmpty()) {
                docDuLieuVaoTable();
                return;
            }
            ArrayList<NhanVien> ketQua = nv_dao.timKiemNhanVien(tuKhoa);
            modelNV.setRowCount(0);
            if (ketQua.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Không tìm thấy nhân viên nào khớp với từ khóa '" + tuKhoa + "'!", "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
                docDuLieuVaoTable();
                txtTimNV.selectAll();
                txtTimNV.requestFocus();
            } else {
                int stt = 1;
                for (NhanVien nv : ketQua) {
                    modelNV.addRow(new Object[]{
                        stt++, nv.getMaNhanVien(), nv.getHoTen(), nv.isGioiTinh() ? "Nam" : "Nữ",
                        nv.getSoDienThoai(), nv.getChucVu(), df.format(nv.getLuongCoBan()),
                        nv.getCaLamViec(), nv.getDiaChi()
                    });
                }
            }
        } else if (o.equals(btnXoaTrang)) {
            xoaTrang();
        }
    }

    /**
     * Hiển thị hộp thoại chi tiết nhân sự gồm mã, họ tên, chức vụ, lương cơ bản, ca làm việc và ngày vào làm.
     *
     * @param maNV mã định danh của nhân viên cần xem chi tiết
     */
    private void hienThiChiTietNhanVien(String maNV) {
        NhanVien nv = nv_dao.getNhanVienTheoMa(maNV);
        if (nv == null) {
            JOptionPane.showMessageDialog(this, "Không tìm thấy thông tin nhân viên: " + maNV, "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Window parentWindow = SwingUtilities.getWindowAncestor(this);
        JDialog dlg = new JDialog((Frame) (parentWindow instanceof Frame ? parentWindow : null), "Chi Tiết Hồ Sơ Nhân Viên - " + maNV, true);
        dlg.setLayout(new BorderLayout(10, 10));
        dlg.setSize(680, 520);
        dlg.setLocationRelativeTo(this);

        JPanel pInfo = new JPanel(new GridLayout(6, 2, 10, 6));
        pInfo.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createTitledBorder("Thông Tin Nhân Viên"),
            BorderFactory.createEmptyBorder(8, 12, 8, 12)
        ));
        pInfo.setBackground(Color.WHITE);

        pInfo.add(new JLabel("Mã nhân viên: " + nv.getMaNhanVien()));
        pInfo.add(new JLabel("Họ và tên: " + nv.getHoTen()));
        pInfo.add(new JLabel("Giới tính: " + (nv.isGioiTinh() ? "Nam" : "Nữ")));
        pInfo.add(new JLabel("Ngày sinh: " + (nv.getNgaySinh() != null ? nv.getNgaySinh().format(java.time.format.DateTimeFormatter.ofPattern("dd/MM/yyyy")) : "Chưa rõ")));
        pInfo.add(new JLabel("Số điện thoại: " + nv.getSoDienThoai()));
        pInfo.add(new JLabel("Email: " + (nv.getEmail() != null ? nv.getEmail() : "Chưa cập nhật")));
        pInfo.add(new JLabel("Địa chỉ: " + (nv.getDiaChi() != null ? nv.getDiaChi() : "Chưa cập nhật")));
        pInfo.add(new JLabel("Chức vụ: " + nv.getChucVu()));
        pInfo.add(new JLabel("Ca làm việc: " + (nv.getCaLamViec() != null ? nv.getCaLamViec() : "Toàn thời gian")));
        pInfo.add(new JLabel("Lương cơ bản: " + df.format(nv.getLuongCoBan()) + " VNĐ"));
        pInfo.add(new JLabel("Trạng thái: " + (nv.isTrangThai() ? "Đang làm việc" : "Đã nghỉ việc")));
        pInfo.add(new JLabel("Vai trò hệ thống: " + (nv.isQuanLy() ? "Quản lý cấp cao" : "Nhân viên bán hàng")));

        // Bảng hóa đơn do nhân viên đã lập
        dao.HoaDon_DAO hd_dao = new dao.HoaDon_DAO();
        ArrayList<entity.HoaDon> allHD = hd_dao.getAllHoaDon();
        String[] headers = {"STT", "Mã HĐ", "Thời Gian Lập", "Khách Hàng", "Tổng Tiền", "Phương Thức"};
        DefaultTableModel modelHD = new DefaultTableModel(headers, 0) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        };
        int stt = 1;
        java.text.DecimalFormat dfTien = new java.text.DecimalFormat("#,### VNĐ");
        for (entity.HoaDon h : allHD) {
            if (h.getNhanVien() != null && nv.getMaNhanVien().equals(h.getNhanVien().getMaNhanVien())) {
                modelHD.addRow(new Object[]{
                    stt++,
                    h.getMaHoaDon(),
                    h.getNgayLap().format(java.time.format.DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm")),
                    (h.getKhachHang() != null ? h.getKhachHang().getHoTen() : "Khách lẻ"),
                    dfTien.format(h.getTongTien()),
                    h.getPhuongThucTT()
                });
            }
        }
        JTable tableHD = new JTable(modelHD);
        tableHD.setRowHeight(24);
        JScrollPane scrollHD = new JScrollPane(tableHD);
        scrollHD.setBorder(BorderFactory.createTitledBorder("Doanh Số Đã Lập (" + (stt - 1) + " hóa đơn)"));

        JPanel pBot = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton btnDong = UIHelper.createSecondaryBtn("Đóng", 90, 32);
        btnDong.addActionListener(e -> dlg.dispose());
        pBot.add(btnDong);

        dlg.add(pInfo, BorderLayout.NORTH);
        dlg.add(scrollHD, BorderLayout.CENTER);
        dlg.add(pBot, BorderLayout.SOUTH);
        dlg.setVisible(true);
    }

    /**
     * Xóa trắng các trường nhập liệu trên form và thiết lập lại các lựa chọn mặc định ban đầu.
     */
    private void xoaTrang() {
        txtMaNV.setText("");
        txtMaNV.setEditable(true);
        txtHoTen.setText("");
        txtSDT.setText("");
        txtDiaChi.setText("");
        txtNgaySinh.setText("");
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

    /**
     * Xử lý sự kiện click chuột trên bảng nhân viên: 1 click để hiển thị form, 2 click để xem hộp thoại chi tiết nhân sự.
     *
     * @param e sự kiện thao tác chuột của người dùng
     */
    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableNV.getSelectedRow();
        if (row >= 0) {
            hienThiThongTinLenForm(row);
            if (e.getClickCount() == 2) {
                String maNV = (String) modelNV.getValueAt(row, 1);
                hienThiChiTietNhanVien(maNV);
            }
        }
    }

    /**
     * Xử lý sự kiện nhấn chuột trên bảng nhân viên (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mousePressed(MouseEvent e) {}

    /**
     * Xử lý sự kiện nhả chuột trên bảng nhân viên (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseReleased(MouseEvent e) {}

    /**
     * Xử lý sự kiện chuột đi vào vùng bảng nhân viên (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseEntered(MouseEvent e) {}

    /**
     * Xử lý sự kiện chuột rời khỏi vùng bảng nhân viên (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseExited(MouseEvent e) {}
}

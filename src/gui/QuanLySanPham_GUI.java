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
import java.util.ArrayList;
import java.util.List;

/**
 * Phân hệ Quản lý danh mục mẫu giày dép và biến thể kích thước, màu sắc, tồn kho.
 * Thuộc tầng Presentation (GUI) trong kiến trúc 3 tầng, tiếp nhận các thao tác CRUD sản phẩm và biến thể qua SanPham_DAO và ChiTietGiay_DAO.
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
    private JButton btnXemChiTiet;
    private JComboBox<String> cboLocThuongHieu;
    private JTextField txtLocGiaTu, txtLocGiaDen;
    private JButton btnLocNangCao, btnBoLoc;

    private JTable tableSP;
    private DefaultTableModel modelSP;

    private NhanVien nhanVien;
    private SanPham_DAO sp_dao;
    private ChiTietGiay_DAO ctg_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");

    /**
     * Khởi tạo giao diện quản lý mẫu giày mặc định không phân quyền nhân viên cụ thể.
     */
    public QuanLySanPham_GUI() {
        this(null);
    }

    /**
     * Khởi tạo giao diện quản lý mẫu giày với thông tin nhân viên đăng nhập để phân quyền thao tác (khóa nút nếu là thu ngân).
     *
     * @param nv đối tượng nhân viên đang đăng nhập vào hệ thống
     */
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
        JPanel pForm = new JPanel(new GridBagLayout());
        pForm.setBackground(Color.WHITE);
        pForm.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "Thông Tin Sản Phẩm Mẫu",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));

        GridBagConstraints g = new GridBagConstraints();
        g.insets = new Insets(6, 10, 6, 10);
        g.fill = GridBagConstraints.HORIZONTAL;

        // Cột 1
        g.gridx = 0; g.gridy = 0; pForm.add(new JLabel("Mã sản phẩm:"), g);
        txtMaSP = new JTextField(15);
        g.gridx = 1; g.gridy = 0; pForm.add(txtMaSP, g);

        g.gridx = 0; g.gridy = 1; pForm.add(new JLabel("Tên sản phẩm:"), g);
        txtTenSP = new JTextField(15);
        g.gridx = 1; g.gridy = 1; pForm.add(txtTenSP, g);

        g.gridx = 0; g.gridy = 2; pForm.add(new JLabel("Phân loại:"), g);
        cboLoai = new JComboBox<>(new String[]{"Sneaker", "Chạy bộ", "Sandal", "Giày Da", "Tập gym"});
        g.gridx = 1; g.gridy = 2; pForm.add(cboLoai, g);

        g.gridx = 0; g.gridy = 3; pForm.add(new JLabel("Thương hiệu:"), g);
        cboThuongHieu = new JComboBox<>(new String[]{"Nike", "Adidas", "Vans", "Converse", "Biti's", "Puma"});
        g.gridx = 1; g.gridy = 3; pForm.add(cboThuongHieu, g);

        // Cột 2
        g.gridx = 2; g.gridy = 0; pForm.add(new JLabel("Giá nhập (VNĐ):"), g);
        txtGiaNhap = new JTextField(15);
        g.gridx = 3; g.gridy = 0; pForm.add(txtGiaNhap, g);

        g.gridx = 2; g.gridy = 1; pForm.add(new JLabel("Giá bán niêm yết:"), g);
        txtGiaBan = new JTextField(15);
        g.gridx = 3; g.gridy = 1; pForm.add(txtGiaBan, g);

        g.gridx = 2; g.gridy = 2; pForm.add(new JLabel("Chất liệu:"), g);
        txtChatLieu = new JTextField(15);
        g.gridx = 3; g.gridy = 2; pForm.add(txtChatLieu, g);

        // Tìm kiếm
        g.gridx = 2; g.gridy = 3; pForm.add(new JLabel("Tìm kiếm (Tên/Mã):"), g);
        JPanel pTim = new JPanel(new BorderLayout(4, 0));
        pTim.setOpaque(false);
        txtTimKiem = new JTextField(10);
        btnTim = UIHelper.createDarkBtn("Tìm", 65, 28);
        pTim.add(txtTimKiem, BorderLayout.CENTER);
        pTim.add(btnTim, BorderLayout.EAST);
        g.gridx = 3; g.gridy = 3; pForm.add(pTim, g);

        // 3. THANH LỌC NÂNG CAO INLINE
        JPanel pLoc = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 4));
        pLoc.setBackground(new Color(241, 245, 249));
        pLoc.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "Lọc Nâng Cao Sản Phẩm",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 12), new Color(30, 58, 138)
        ));
        pLoc.add(new JLabel("Thương hiệu:"));
        ArrayList<String> dsHang = sp_dao.getAllThuongHieu();
        dsHang.add(0, "Tất cả");
        cboLocThuongHieu = new JComboBox<>(dsHang.toArray(new String[0]));
        pLoc.add(cboLocThuongHieu);
        pLoc.add(new JLabel("Giá từ:"));
        txtLocGiaTu = new JTextField(8);
        pLoc.add(txtLocGiaTu);
        pLoc.add(new JLabel("Đến:"));
        txtLocGiaDen = new JTextField(8);
        pLoc.add(txtLocGiaDen);
        btnLocNangCao = UIHelper.createPrimaryBtn("Lọc", 75, 28);
        btnBoLoc = UIHelper.createSecondaryBtn("Bỏ Lọc", 75, 28);
        pLoc.add(btnLocNangCao);
        pLoc.add(btnBoLoc);

        // 4. NÚT CHỨC NĂNG
        JPanel pButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));
        pButtons.setBackground(Color.WHITE);

        btnThem = UIHelper.createSuccessBtn("Thêm Mới", 110, 34);
        btnXoa = UIHelper.createDangerBtn("Xóa (Ngừng)", 115, 34);
        btnSua = UIHelper.createPrimaryBtn("Cập Nhật", 105, 34);
        btnXemChiTiet = UIHelper.createButton("Xem Chi Tiết", UIHelper.PRIMARY_BLUE, Color.WHITE, 120, 34);
        btnXoaTrang = UIHelper.createSecondaryBtn("Xóa Trắng", 100, 34);

        pButtons.add(btnThem);
        pButtons.add(btnXoa);
        pButtons.add(btnSua);
        pButtons.add(btnXemChiTiet);
        pButtons.add(btnXoaTrang);

        JPanel pTop = new JPanel();
        pTop.setLayout(new BoxLayout(pTop, BoxLayout.Y_AXIS));
        pTop.add(pForm);
        pTop.add(pLoc);
        pTop.add(pButtons);
        add(pTop, BorderLayout.NORTH);

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
        btnXemChiTiet.addActionListener(this);
        btnXoaTrang.addActionListener(this);
        btnTim.addActionListener(this);
        txtTimKiem.addActionListener(this);
        btnLocNangCao.addActionListener(this);
        btnBoLoc.addActionListener(this);
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

    /**
     * Nạp toàn bộ danh sách sản phẩm cùng tổng tồn kho các biến thể từ cơ sở dữ liệu lên bảng hiển thị JTable.
     */
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

    /**
     * Hiển thị thông tin chi tiết của mẫu giày được chọn trên bảng lên các trường nhập liệu của form.
     *
     * @param row chỉ số dòng đang được chọn trong bảng sản phẩm
     */
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

    /**
     * Xử lý các sự kiện hành động trên form: Thêm mẫu giày, Cập nhật thông tin, Xóa sản phẩm, Xóa trắng form, Tìm kiếm hoặc Lọc nâng cao.
     *
     * @param e sự kiện hành động của người dùng
     */
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

        } else if (o.equals(btnLocNangCao)) {
            String hang = cboLocThuongHieu.getSelectedItem().toString();
            Double giaTu = null;
            Double giaDen = null;
            try {
                String strTu = txtLocGiaTu.getText().trim();
                if (!strTu.isEmpty()) giaTu = Double.parseDouble(strTu);
                String strDen = txtLocGiaDen.getText().trim();
                if (!strDen.isEmpty()) giaDen = Double.parseDouble(strDen);
            } catch (NumberFormatException nfe) {
                JOptionPane.showMessageDialog(this, "Giá bán tìm kiếm phải là số hợp lệ!", "Lỗi nhập liệu", JOptionPane.ERROR_MESSAGE);
                return;
            }
            ArrayList<SanPham> ketQua = sp_dao.timKiemNangCao(hang, giaTu, giaDen, "Tất cả", null);
            if (ketQua.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Không tìm thấy sản phẩm nào khớp với tiêu chí lọc nâng cao!", "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
            } else {
                modelSP.setRowCount(0);
                int stt = 1;
                for (SanPham sp : ketQua) {
                    modelSP.addRow(new Object[]{
                        stt++, sp.getMaSanPham(), sp.getTenSanPham(), sp.getLoaiGiay(),
                        sp.getThuongHieu(), df.format(sp.getGiaNhap()), df.format(sp.getGiaBan()), sp.getChatLieu()
                    });
                }
            }
        } else if (o.equals(btnBoLoc)) {
            cboLocThuongHieu.setSelectedIndex(0);
            txtLocGiaTu.setText("");
            txtLocGiaDen.setText("");
            txtTimKiem.setText("");
            DocDuLieuDatabaseVaoTable();

        } else if (o.equals(btnXemChiTiet)) {
            int row = tableSP.getSelectedRow();
            if (row < 0) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn một sản phẩm trong bảng để xem chi tiết biến thể!", "Chưa chọn sản phẩm", JOptionPane.WARNING_MESSAGE);
                return;
            }
            String maSP = modelSP.getValueAt(row, 1).toString();
            hienThiChiTietSanPham(maSP);

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
            if (modelSP.getRowCount() == 0) {
                JOptionPane.showMessageDialog(this, "Không tìm thấy sản phẩm nào khớp với từ khóa '" + key + "'!", "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
                DocDuLieuDatabaseVaoTable();
            }
        }
    }

    /**
     * Hiển thị hộp thoại chi tiết sản phẩm gồm danh sách các biến thể kích cỡ, màu sắc, số lượng tồn kho và cho phép cập nhật tồn kho.
     *
     * @param maSP mã định danh của sản phẩm cần xem chi tiết
     */
    private void hienThiChiTietSanPham(String maSP) {
        SanPham sp = sp_dao.getSanPhamTheoMa(maSP);
        if (sp == null) {
            JOptionPane.showMessageDialog(this, "Không tìm thấy thông tin sản phẩm!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            return;
        }
        java.util.ArrayList<ChiTietGiay> listCTG = ctg_dao.getChiTietTheoSanPham(maSP);

        JDialog dlg = new JDialog(SwingUtilities.getWindowAncestor(this), "CHI TIẾT SẢN PHẨM & BIẾN THỂ SKU: " + sp.getMaSanPham(), Dialog.ModalityType.APPLICATION_MODAL);
        dlg.setLayout(new BorderLayout(10, 10));
        dlg.setSize(650, 420);
        dlg.setLocationRelativeTo(this);

        JPanel pInfo = new JPanel(new GridLayout(4, 2, 8, 4));
        pInfo.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createEmptyBorder(10, 10, 10, 10),
            BorderFactory.createTitledBorder("Thông Tin Chung Mẫu Giày")
        ));
        pInfo.add(new JLabel("Mã sản phẩm: " + sp.getMaSanPham()));
        pInfo.add(new JLabel("Tên sản phẩm: " + sp.getTenSanPham()));
        pInfo.add(new JLabel("Phân loại: " + sp.getLoaiGiay()));
        pInfo.add(new JLabel("Thương hiệu: " + sp.getThuongHieu()));
        pInfo.add(new JLabel("Giá nhập: " + df.format(sp.getGiaNhap())));
        pInfo.add(new JLabel("Giá bán: " + df.format(sp.getGiaBan())));
        pInfo.add(new JLabel("Chất liệu: " + (sp.getChatLieu() != null ? sp.getChatLieu() : "Đang cập nhật")));
        pInfo.add(new JLabel("Trạng thái: " + (sp.isTrangThai() ? "Đang kinh doanh" : "Ngừng kinh doanh")));

        String[] headers = {"STT", "Mã SKU (CTG)", "Size", "Màu Sắc", "Tồn Kho", "Tình Trạng Kho"};
        DefaultTableModel modelCTG = new DefaultTableModel(headers, 0) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        };
        int stt = 1;
        for (ChiTietGiay ctg : listCTG) {
            modelCTG.addRow(new Object[]{
                stt++,
                ctg.getMaChiTietGiay(),
                ctg.getKichThuoc(),
                ctg.getMauSac(),
                ctg.getSoLuongTon(),
                (ctg.getSoLuongTon() > 0 ? "Còn hàng (" + ctg.getSoLuongTon() + " đôi)" : "Hết hàng")
            });
        }
        JTable tableCTG = new JTable(modelCTG);
        tableCTG.setRowHeight(24);
        JScrollPane scrollCTG = new JScrollPane(tableCTG);
        scrollCTG.setBorder(BorderFactory.createTitledBorder("Danh Sách Biến Thể Kích Thước & Màu Sắc (SKU)"));

        JPanel pBot = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton btnDong = UIHelper.createSecondaryBtn("Đóng", 90, 32);
        btnDong.addActionListener(e -> dlg.dispose());
        pBot.add(btnDong);

        dlg.add(pInfo, BorderLayout.NORTH);
        dlg.add(scrollCTG, BorderLayout.CENTER);
        dlg.add(pBot, BorderLayout.SOUTH);
        dlg.setVisible(true);
    }

    /**
     * Xóa trắng các trường nhập liệu trên form và thiết lập lại các lựa chọn mặc định ban đầu.
     */
    private void xoaTrang() {
        txtMaSP.setText("");
        txtMaSP.setEditable(true);
        txtTenSP.setText("");
        txtGiaNhap.setText("");
        txtGiaBan.setText("");
        txtChatLieu.setText("");
        txtTimKiem.setText("");
        tableSP.clearSelection();
        DocDuLieuDatabaseVaoTable();
        txtMaSP.requestFocus();
    }

    /**
     * Xử lý sự kiện click chuột trên bảng sản phẩm: 1 click để hiển thị form, 2 click để xem hộp thoại chi tiết biến thể kích cỡ/màu sắc.
     *
     * @param e sự kiện thao tác chuột của người dùng
     */
    @Override
    public void mouseClicked(MouseEvent e) {
        int row = tableSP.getSelectedRow();
        if (row >= 0) {
            hienThiThongTinLenForm(row);
            if (e.getClickCount() == 2) {
                String maSP = modelSP.getValueAt(row, 1).toString();
                hienThiChiTietSanPham(maSP);
            }
        }
    }

    /**
     * Xử lý sự kiện nhấn chuột trên bảng sản phẩm (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mousePressed(MouseEvent e) {}

    /**
     * Xử lý sự kiện nhả chuột trên bảng sản phẩm (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseReleased(MouseEvent e) {}

    /**
     * Xử lý sự kiện chuột đi vào vùng bảng sản phẩm (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseEntered(MouseEvent e) {}

    /**
     * Xử lý sự kiện chuột rời khỏi vùng bảng sản phẩm (không sử dụng).
     *
     * @param e sự kiện chuột
     */
    @Override public void mouseExited(MouseEvent e) {}
}

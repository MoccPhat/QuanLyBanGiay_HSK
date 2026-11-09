package gui;

import dao.NhanVien_DAO;
import entity.NhanVien;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class DangNhap_GUI extends JFrame implements ActionListener {
    private JTextField txtMaNV;
    private JPasswordField txtMatKhau;
    private JButton btnDangNhap;
    private JButton btnThoat;
    private NhanVien_DAO nv_dao;

    public DangNhap_GUI() {
        setTitle("HỆ THỐNG QUẢN LÝ BÁN HÀNG GIÀY DÉP - ĐĂNG NHẬP");
        setSize(480, 320);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setResizable(false);

        nv_dao = new NhanVien_DAO();

        // Panel chính
        JPanel panelMain = new JPanel(new BorderLayout(10, 10));
        panelMain.setBackground(Color.WHITE);
        panelMain.setBorder(BorderFactory.createEmptyBorder(20, 30, 20, 30));

        // Tiêu đề
        JPanel pTitle = new JPanel(new GridLayout(2, 1));
        pTitle.setBackground(Color.WHITE);
        JLabel lblTitle = new JLabel("HỆ THỐNG QUẢN LÝ BÁN HÀNG GIÀY DÉP", JLabel.CENTER);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 20));
        lblTitle.setForeground(new Color(185, 28, 28)); // Đỏ rượu phong cách shop giày

        JLabel lblSub = new JLabel("ĐĂNG NHẬP HỆ THỐNG BÁN HÀNG", JLabel.CENTER);
        lblSub.setFont(new Font("Arial", Font.PLAIN, 12));
        lblSub.setForeground(Color.GRAY);

        pTitle.add(lblTitle);
        pTitle.add(lblSub);
        panelMain.add(pTitle, BorderLayout.NORTH);

        // Form nhập liệu
        JPanel pForm = new JPanel(new GridBagLayout());
        pForm.setBackground(Color.WHITE);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel lblMaNV = new JLabel("Mã nhân viên:");
        lblMaNV.setFont(new Font("Arial", Font.BOLD, 13));
        gbc.gridx = 0; gbc.gridy = 0;
        pForm.add(lblMaNV, gbc);

        txtMaNV = new JTextField(15);
        txtMaNV.setText("NV0001"); // Mặc định quản lý mẫu
        txtMaNV.setFont(new Font("Arial", Font.PLAIN, 13));
        gbc.gridx = 1; gbc.gridy = 0;
        pForm.add(txtMaNV, gbc);

        JLabel lblMatKhau = new JLabel("Mật khẩu:");
        lblMatKhau.setFont(new Font("Arial", Font.BOLD, 13));
        gbc.gridx = 0; gbc.gridy = 1;
        pForm.add(lblMatKhau, gbc);

        txtMatKhau = new JPasswordField(15);
        txtMatKhau.setText("123456");
        txtMatKhau.setFont(new Font("Arial", Font.PLAIN, 13));
        gbc.gridx = 1; gbc.gridy = 1;
        pForm.add(txtMatKhau, gbc);

        panelMain.add(pForm, BorderLayout.CENTER);

        // Nút bấm
        JPanel pButtons = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
        pButtons.setBackground(Color.WHITE);

        btnDangNhap = UIHelper.createPrimaryBtn("Đăng Nhập", 130, 36);
        btnThoat = UIHelper.createSecondaryBtn("Thoát", 100, 36);

        pButtons.add(btnDangNhap);
        pButtons.add(btnThoat);
        panelMain.add(pButtons, BorderLayout.SOUTH);

        add(panelMain);

        btnDangNhap.addActionListener(this);
        btnThoat.addActionListener(this);

        // Phím Enter để đăng nhập nhanh
        KeyAdapter enterKey = new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    btnDangNhap.doClick();
                }
            }
        };
        txtMaNV.addKeyListener(enterKey);
        txtMatKhau.addKeyListener(enterKey);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnThoat)) {
            System.exit(0);
        } else if (o.equals(btnDangNhap)) {
            String maNV = txtMaNV.getText().trim();
            String matKhau = new String(txtMatKhau.getPassword()).trim();

            if (maNV.isEmpty() || matKhau.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ Mã nhân viên và Mật khẩu!", "Cảnh báo", JOptionPane.WARNING_MESSAGE);
                return;
            }

            NhanVien nv = nv_dao.dangNhap(maNV, matKhau);
            if (nv != null) {
                JOptionPane.showMessageDialog(this, "Đăng nhập thành công!\nChào mừng " + nv.getHoTen() + " (" + nv.getChucVu() + ")", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
                this.dispose();
                new ManHinhChinh_GUI(nv).setVisible(true);
            } else {
                String err = nv_dao.getLastError();
                if (err == null || err.isEmpty()) {
                    err = "Sai Mã nhân viên hoặc Mật khẩu!";
                }
                String title = err.startsWith("Không kết nối") ? "Lỗi kết nối cơ sở dữ liệu" : "Lỗi đăng nhập";
                JOptionPane.showMessageDialog(this, err, title, JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {}
        SwingUtilities.invokeLater(() -> new DangNhap_GUI().setVisible(true));
    }
}

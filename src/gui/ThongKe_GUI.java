package gui;

import javax.swing.border.TitledBorder;

import dao.HoaDon_DAO;
import entity.ChiTietHoaDon;
import entity.HoaDon;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.text.DecimalFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

public class ThongKe_GUI extends JPanel implements ActionListener {
    private JLabel lblTongDoanhThuVal;
    private JLabel lblTongDonHangVal;
    private JLabel lblTongSoLuongVal;
    private JLabel lblKhachHangVal;

    private JButton btnLamMoi;
    private JButton btnXuatBaoCao;

    private JTextField txtTimKiemHD;
    private JButton btnTimHD;
    private JButton btnXemChiTietHD;

    private JTable tableHoaDon;
    private DefaultTableModel modelHoaDon;



    private HoaDon_DAO hd_dao;
    private DecimalFormat df = new DecimalFormat("#,### VNĐ");
    private DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    public ThongKe_GUI() {
        hd_dao = new HoaDon_DAO();

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(245, 247, 250));
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));

        // 1. TIÊU ĐỀ
        JLabel lblHeader = new JLabel("BÁO CÁO THỐNG KÊ DOANH THU & HIỆU SUẤT BÁN HÀNG", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 18));
        lblHeader.setForeground(UIHelper.PRIMARY_BLUE);
        add(lblHeader, BorderLayout.NORTH);

        // 2. KHUNG TRUNG TÂM (KPI CARDS + FILTER + TABLES)
        JPanel pCenter = new JPanel(new BorderLayout(10, 10));
        pCenter.setOpaque(false);

        // A. Thẻ KPI (Bento Cards)
        JPanel pKPI = new JPanel(new GridLayout(1, 4, 12, 0));
        pKPI.setOpaque(false);

        lblTongDoanhThuVal = new JLabel("0 VNĐ", JLabel.CENTER);
        lblTongDonHangVal  = new JLabel("0 đơn", JLabel.CENTER);
        lblTongSoLuongVal  = new JLabel("0 đôi", JLabel.CENTER);
        lblKhachHangVal    = new JLabel("4 khách", JLabel.CENTER);

        pKPI.add(createKPICard("TỔNG DOANH THU", lblTongDoanhThuVal, UIHelper.SUCCESS_GREEN, new Color(240, 253, 244)));
        pKPI.add(createKPICard("SỐ HÓA ĐƠN ĐÃ LẬP", lblTongDonHangVal, UIHelper.ACCENT_BLUE, new Color(239, 246, 255)));
        pKPI.add(createKPICard("SẢN PHẨM ĐÃ BÁN", lblTongSoLuongVal, UIHelper.PRIMARY_BLUE, new Color(241, 245, 249)));
        pKPI.add(createKPICard("KHÁCH HÀNG THÀNH VIÊN", lblKhachHangVal, UIHelper.WARN_AMBER, new Color(254, 243, 199)));

        // B. Thanh lọc dữ liệu
        JPanel pFilterBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 12, 8));
        pFilterBar.setBackground(Color.WHITE);
        pFilterBar.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(UIHelper.BORDER_GRAY, 1, true),
                BorderFactory.createEmptyBorder(4, 8, 4, 8)
        ));

        btnLamMoi = UIHelper.createSecondaryBtn("Làm Mới", 100, 34);
        btnXuatBaoCao = UIHelper.createSuccessBtn("Xuất Báo Cáo [Excel]", 180, 34);

        txtTimKiemHD = new JTextField(10);
        txtTimKiemHD.setPreferredSize(new Dimension(130, 32));
        txtTimKiemHD.setToolTipText("Nhập mã HĐ, tên thu ngân hoặc khách hàng");
        btnTimHD = UIHelper.createPrimaryBtn("Tìm HĐ", 85, 34);
        btnXemChiTietHD = UIHelper.createSecondaryBtn("Xem Chi Tiết", 115, 34);

        pFilterBar.add(btnLamMoi);
        pFilterBar.add(Box.createHorizontalStrut(12));
        pFilterBar.add(new JLabel("Tìm:"));
        pFilterBar.add(txtTimKiemHD);
        pFilterBar.add(btnTimHD);
        pFilterBar.add(btnXemChiTietHD);
        pFilterBar.add(Box.createHorizontalStrut(12));
        pFilterBar.add(btnXuatBaoCao);

        // Ghép KPI + Toolbar vào TopCenter
        JPanel pTopCenter = new JPanel(new BorderLayout(0, 10));
        pTopCenter.setOpaque(false);
        pTopCenter.add(pKPI, BorderLayout.NORTH);
        pTopCenter.add(pFilterBar, BorderLayout.SOUTH);
        pCenter.add(pTopCenter, BorderLayout.NORTH);

        // C. Bảng hiển thị danh sách hóa đơn
        String[] headersHD = {"STT", "Mã Hóa Đơn", "Thời Gian Lập", "Thu Ngân Bán Hàng", "Khách Hàng", "Tổng Thanh Toán", "Phương Thức"};
        modelHoaDon = new DefaultTableModel(headersHD, 0) {
            @Override
            public boolean isCellEditable(int r, int c) { return false; }
        };
        tableHoaDon = new JTable(modelHoaDon);
        UIHelper.styleTable(tableHoaDon);
        tableHoaDon.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    int row = tableHoaDon.getSelectedRow();
                    if (row >= 0) {
                        String maHD = (String) modelHoaDon.getValueAt(row, 1);
                        hienThiChiTietHoaDon(maHD);
                    }
                }
            }
        });
        JScrollPane scrollHD = new JScrollPane(tableHoaDon);
        scrollHD.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(203, 213, 225)),
                "Danh Sách Hóa Đơn Bán Hàng",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), new Color(30, 58, 138)
        ));
        pCenter.add(scrollHD, BorderLayout.CENTER);
        add(pCenter, BorderLayout.CENTER);

        // Đăng ký sự kiện
        btnLamMoi.addActionListener(this);
        btnXuatBaoCao.addActionListener(this);
        btnTimHD.addActionListener(this);
        txtTimKiemHD.addActionListener(this);
        btnXemChiTietHD.addActionListener(this);

        // Nạp dữ liệu
        napDuLieuThongKe();
    }

    private JPanel createKPICard(String title, JLabel lblValue, Color primaryColor, Color bgColor) {
        JPanel card = new JPanel(new BorderLayout(0, 6));
        card.setBackground(bgColor);
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(primaryColor.brighter(), 1, true),
                BorderFactory.createEmptyBorder(12, 14, 12, 14)
        ));

        JLabel lblTitle = new JLabel(title, JLabel.CENTER);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 11));
        lblTitle.setForeground(new Color(71, 85, 105));

        lblValue.setFont(new Font("Arial", Font.BOLD, 20));
        lblValue.setForeground(primaryColor);

        card.add(lblTitle, BorderLayout.NORTH);
        card.add(lblValue, BorderLayout.CENTER);
        return card;
    }

    public static class ThongKeData {
        public ArrayList<HoaDon> dsHD;
        public int tongSL;
        public int tongKH;
    }

    /**
     * Nạp dữ liệu thống kê ngoài luồng sự kiện (Off-EDT) bằng SwingWorker (L27).
     * Tránh treo giao diện người dùng khi cơ sở dữ liệu có lượng hóa đơn lớn.
     */
    public ThongKeData loadThongKeData() {
        ThongKeData data = new ThongKeData();
        data.dsHD = hd_dao.getAllHoaDon();
        data.tongSL = hd_dao.getTongSoLuongBanRa();
        data.tongKH = hd_dao.getTongKhachHang();
        return data;
    }

    /**
     * Nạp dữ liệu thống kê ngoài luồng sự kiện (Off-EDT) bằng SwingWorker (L27).
     * Tránh treo giao diện người dùng khi cơ sở dữ liệu có lượng hóa đơn lớn.
     */
    public void napDuLieuThongKe() {
        
        if (btnLamMoi != null) btnLamMoi.setEnabled(false);

        SwingWorker<ThongKeData, Void> worker = new SwingWorker<>() {
            @Override
            protected ThongKeData doInBackground() {
                return loadThongKeData();
            }

            @Override
            protected void done() {
                try {
                    ThongKeData data = get();
                    capNhatGiaoDienThongKe(data);
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    
                    if (btnLamMoi != null) btnLamMoi.setEnabled(true);
                }
            }
        };

        if (SwingUtilities.isEventDispatchThread()) {
            worker.execute();
        } else {
            try {
                ThongKeData data = loadThongKeData();
                capNhatGiaoDienThongKe(data);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void capNhatGiaoDienThongKe(ThongKeData data) {
        modelHoaDon.setRowCount(0);

        ArrayList<HoaDon> dsHD = data.dsHD;
        double tongDoanhThu = 0;
        int stt = 1;
        int countDon = 0;

        if (dsHD != null && !dsHD.isEmpty()) {
            for (HoaDon hd : dsHD) {
                tongDoanhThu += hd.getTongTien();
                countDon++;
                String tenKH = (hd.getKhachHang() != null && hd.getKhachHang().getHoTen() != null)
                        ? hd.getKhachHang().getHoTen()
                        : "Khách lẻ vãng lai";
                String tenNV = (hd.getNhanVien() != null && hd.getNhanVien().getHoTen() != null)
                        ? hd.getNhanVien().getHoTen()
                        : (hd.getNhanVien() != null ? hd.getNhanVien().getMaNhanVien() : "NV0001");

                modelHoaDon.addRow(new Object[]{
                        stt++,
                        hd.getMaHoaDon(),
                        (hd.getNgayLap() != null) ? dtf.format(hd.getNgayLap()) : "",
                        tenNV,
                        tenKH,
                        df.format(hd.getTongTien()),
                        hd.getPhuongThucTT()
                });
            }

            lblTongDoanhThuVal.setText(df.format(tongDoanhThu));
            lblTongDonHangVal.setText(countDon + " đơn");
            lblTongSoLuongVal.setText(data.tongSL + " đôi");
        } else {
            lblTongDoanhThuVal.setText("0 VNĐ");
            lblTongDonHangVal.setText("0 đơn");
            lblTongSoLuongVal.setText("0 đôi");
        }

        lblKhachHangVal.setText(data.tongKH + " khách");
    }

    public String taoNoiDungHoaDon(HoaDon hd) {
        StringBuilder bill = new StringBuilder();
        bill.append("=============================================\n");
        bill.append("              CỬA HÀNG GIÀY DÉP              \n");
        bill.append("      12 Nguyễn Văn Bảo, Gò Vấp, TP.HCM      \n\n");
        bill.append("               HÓA ĐƠN BÁN LẺ                \n\n");
        bill.append("Mã HĐ: ").append(hd.getMaHoaDon()).append("\n");
        bill.append("Ngày: ").append((hd.getNgayLap() != null) ? dtf.format(hd.getNgayLap()) : "").append("\n");
        bill.append("Thu ngân: ").append((hd.getNhanVien() != null && hd.getNhanVien().getHoTen() != null) ? hd.getNhanVien().getHoTen() : (hd.getNhanVien() != null ? hd.getNhanVien().getMaNhanVien() : "")).append("\n");
        bill.append("Khách hàng: ").append((hd.getKhachHang() != null && hd.getKhachHang().getHoTen() != null) ? hd.getKhachHang().getHoTen() : "Khách lẻ vãng lai").append("\n");
        bill.append("---------------------------------------------\n");
        if (hd.getDanhSachChiTiet() != null) {
            for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                String tenGiay = (ct.getChiTietGiay() != null && ct.getChiTietGiay().getSanPham() != null)
                        ? ct.getChiTietGiay().getSanPham().getTenSanPham()
                        : "Sản phẩm";
                int size = (ct.getChiTietGiay() != null) ? ct.getChiTietGiay().getKichThuoc() : 0;
                bill.append(tenGiay).append(" (Size ").append(size).append(")\n");
                bill.append("  ").append(ct.getSoLuong()).append(" x ").append(df.format(ct.getDonGia()))
                    .append(" = ").append(df.format(ct.getThanhTien())).append("\n");
            }
        }
        bill.append("---------------------------------------------\n");
        bill.append(String.format("%-24s %18s\n", "Tổng tiền hàng:", df.format(hd.getTongTienHang())));
        bill.append(String.format("%-24s %18s\n", "Chiết khấu hạng thẻ:", (hd.getChietKhau() > 0 ? "-" : "") + df.format(hd.getChietKhau())));
        bill.append(String.format("%-24s %18s\n", "Tiền giảm từ điểm:", (hd.getTienGiamDiem() > 0 ? "-" : "") + df.format(hd.getTienGiamDiem())));
        bill.append(String.format("%-24s %18s\n", "CẦN THANH TOÁN:", df.format(hd.getTongTien())));
        bill.append(String.format("%-24s %18s\n", "Khách đưa:", df.format(hd.getTienKhachDua())));
        bill.append(String.format("%-24s %18s\n", "Tiền thừa:", df.format(hd.getTienThua())));
        bill.append(String.format("%-24s %18s\n", "Điểm cộng mới:", "+" + hd.getDiemCong() + " điểm"));
        bill.append(String.format("%-24s %18s\n", "Hình thức:", (hd.getPhuongThucTT() != null ? hd.getPhuongThucTT() : "Tiền mặt")));
        bill.append("=============================================\n");
        bill.append("       CẢM ƠN QUÝ KHÁCH & HẸN GẶP LẠI!       \n");
        return bill.toString();
    }

    public void hienThiChiTietHoaDon(String maHD) {
        HoaDon hd = hd_dao.getHoaDonTheoMa(maHD);
        if (hd == null) {
            JOptionPane.showMessageDialog(this, "Không tìm thấy chi tiết hóa đơn: " + maHD, "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Window parentWindow = SwingUtilities.getWindowAncestor(this);
        JDialog dlg = new JDialog((Frame) (parentWindow instanceof Frame ? parentWindow : null), "Chi Tiết Hóa Đơn - " + maHD, true);
        dlg.setLayout(new BorderLayout(10, 10));
        dlg.setSize(760, 560);
        dlg.setLocationRelativeTo(this);

        JPanel pInfo = new JPanel(new GridLayout(6, 2, 10, 6));
        pInfo.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createTitledBorder("Thông Tin Hóa Đơn & Thanh Toán"),
            BorderFactory.createEmptyBorder(8, 12, 8, 12)
        ));
        pInfo.setBackground(Color.WHITE);

        String tenNV = (hd.getNhanVien() != null && hd.getNhanVien().getHoTen() != null) ? hd.getNhanVien().getHoTen() : (hd.getNhanVien() != null ? hd.getNhanVien().getMaNhanVien() : "N/A");
        String tenKH = (hd.getKhachHang() != null && hd.getKhachHang().getHoTen() != null) ? hd.getKhachHang().getHoTen() : "Khách lẻ vãng lai";

        pInfo.add(new JLabel("Mã hóa đơn: " + hd.getMaHoaDon()));
        pInfo.add(new JLabel("Thời gian lập: " + ((hd.getNgayLap() != null) ? dtf.format(hd.getNgayLap()) : "")));
        pInfo.add(new JLabel("Thu ngân lập đơn: " + tenNV));
        pInfo.add(new JLabel("Khách hàng: " + tenKH));
        pInfo.add(new JLabel("Tổng tiền hàng: " + df.format(hd.getTongTienHang())));
        pInfo.add(new JLabel("Chiết khấu hạng thẻ: " + (hd.getChietKhau() > 0 ? "-" : "") + df.format(hd.getChietKhau())));
        pInfo.add(new JLabel("Điểm sử dụng: " + hd.getDiemSuDung() + " điểm"));
        pInfo.add(new JLabel("Tiền giảm từ điểm: " + (hd.getTienGiamDiem() > 0 ? "-" : "") + df.format(hd.getTienGiamDiem())));
        pInfo.add(new JLabel("Tổng thanh toán: " + df.format(hd.getTongTien())));
        pInfo.add(new JLabel("Phương thức thanh toán: " + (hd.getPhuongThucTT() != null ? hd.getPhuongThucTT() : "Tiền mặt")));
        pInfo.add(new JLabel("Tiền khách đưa / Tiền thừa: " + df.format(hd.getTienKhachDua()) + " / " + df.format(hd.getTienThua())));
        pInfo.add(new JLabel("Điểm thưởng tích lũy thêm: +" + hd.getDiemCong() + " điểm"));

        String[] headers = {"STT", "Mã Chi Tiết", "Tên Sản Phẩm", "Size", "Màu Sắc", "Số Lượng", "Đơn Giá", "Thành Tiền"};
        DefaultTableModel modelCT = new DefaultTableModel(headers, 0) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        };

        int stt = 1;
        if (hd.getDanhSachChiTiet() != null) {
            for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                String maCTG = (ct.getChiTietGiay() != null) ? ct.getChiTietGiay().getMaChiTietGiay() : "";
                String tenSP = (ct.getChiTietGiay() != null && ct.getChiTietGiay().getSanPham() != null)
                        ? ct.getChiTietGiay().getSanPham().getTenSanPham() : "Sản phẩm";
                int sz = (ct.getChiTietGiay() != null) ? ct.getChiTietGiay().getKichThuoc() : 0;
                String mau = (ct.getChiTietGiay() != null) ? ct.getChiTietGiay().getMauSac() : "";

                modelCT.addRow(new Object[]{
                    stt++, maCTG, tenSP, sz, mau, ct.getSoLuong(), df.format(ct.getDonGia()), df.format(ct.getThanhTien())
                });
            }
        }
        JTable tableCT = new JTable(modelCT);
        tableCT.setRowHeight(24);
        JScrollPane scrollCT = new JScrollPane(tableCT);
        scrollCT.setBorder(BorderFactory.createTitledBorder("Danh Sách Sản Phẩm Mua (" + (stt - 1) + " mặt hàng)"));

        JPanel pBot = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 8));
        JButton btnXuat = UIHelper.createSuccessBtn("📄 Xuất File Hóa Đơn", 160, 34);
        JButton btnDong = UIHelper.createSecondaryBtn("Đóng", 90, 34);

        final String billText = taoNoiDungHoaDon(hd);
        btnXuat.addActionListener(ev -> {
            File f = BanHang_GUI.xuatHoaDonRaFile(hd.getMaHoaDon(), billText);
            if (f != null) {
                JOptionPane.showMessageDialog(dlg, "Đã xuất hóa đơn thành công tại:\n" + f.getAbsolutePath(), "Xuất hóa đơn", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(dlg, "Lỗi khi ghi file hóa đơn!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnDong.addActionListener(ev -> dlg.dispose());

        pBot.add(btnXuat);
        pBot.add(btnDong);

        dlg.add(pInfo, BorderLayout.NORTH);
        dlg.add(scrollCT, BorderLayout.CENTER);
        dlg.add(pBot, BorderLayout.SOUTH);
        dlg.setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnLamMoi)) {
            txtTimKiemHD.setText("");
            napDuLieuThongKe();
            JOptionPane.showMessageDialog(this,
                    "Đã làm mới và cập nhật toàn bộ số liệu thống kê doanh thu!",
                    "Thông Báo Thống Kê", JOptionPane.INFORMATION_MESSAGE);
        } else if (o.equals(btnXuatBaoCao)) {
            JOptionPane.showMessageDialog(this,
                    "Tính năng xuất Excel đang được hoàn thiện trong phiên bản nâng cấp tiếp theo!",
                    "Thông Báo", JOptionPane.INFORMATION_MESSAGE);
        } else if (o.equals(btnTimHD) || o.equals(txtTimKiemHD)) {
            String tuKhoa = txtTimKiemHD.getText().trim();
            if (tuKhoa.isEmpty()) {
                napDuLieuThongKe();
                return;
            }
            ArrayList<HoaDon> ketQua = hd_dao.timKiemHoaDon(tuKhoa);
            modelHoaDon.setRowCount(0);
            if (ketQua.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Không tìm thấy hóa đơn nào khớp với từ khóa '" + tuKhoa + "'!", "Kết quả tìm kiếm", JOptionPane.INFORMATION_MESSAGE);
                napDuLieuThongKe();
                txtTimKiemHD.selectAll();
                txtTimKiemHD.requestFocus();
            } else {
                int stt = 1;
                double tongTienTimDuoc = 0;
                for (HoaDon hd : ketQua) {
                    tongTienTimDuoc += hd.getTongTien();
                    String tenKH = (hd.getKhachHang() != null && hd.getKhachHang().getHoTen() != null)
                            ? hd.getKhachHang().getHoTen() : "Khách lẻ vãng lai";
                    String tenNV = (hd.getNhanVien() != null && hd.getNhanVien().getHoTen() != null)
                            ? hd.getNhanVien().getHoTen() : (hd.getNhanVien() != null ? hd.getNhanVien().getMaNhanVien() : "");

                    modelHoaDon.addRow(new Object[]{
                        stt++,
                        hd.getMaHoaDon(),
                        (hd.getNgayLap() != null) ? dtf.format(hd.getNgayLap()) : "",
                        tenNV,
                        tenKH,
                        df.format(hd.getTongTien()),
                        hd.getPhuongThucTT()
                    });
                }
                lblTongDoanhThuVal.setText(df.format(tongTienTimDuoc));
                lblTongDonHangVal.setText(ketQua.size() + " đơn (lọc)");
            }
        } else if (o.equals(btnXemChiTietHD)) {
            int row = tableHoaDon.getSelectedRow();
            if (row < 0) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn một hóa đơn trong bảng để xem chi tiết!", "Chưa chọn hóa đơn", JOptionPane.WARNING_MESSAGE);
                return;
            }
            String maHD = (String) modelHoaDon.getValueAt(row, 1);
            hienThiChiTietHoaDon(maHD);
        }
    }
}

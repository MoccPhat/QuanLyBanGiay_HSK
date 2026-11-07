package gui;

import dao.HoaDon_DAO;
import entity.HoaDon;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.DecimalFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

public class ThongKe_GUI extends JPanel implements ActionListener {
    private JLabel lblTongDoanhThuVal;
    private JLabel lblTongDonHangVal;
    private JLabel lblTongSoLuongVal;
    private JLabel lblKhachHangVal;

    private JComboBox<String> cboThoiGian;
    private JButton btnLoc;
    private JButton btnLamMoi;
    private JButton btnXuatBaoCao;

    private JTable tableHoaDon;
    private DefaultTableModel modelHoaDon;

    private JTable tableTopSP;
    private DefaultTableModel modelTopSP;

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
        JPanel pnlCenter = new JPanel(new BorderLayout(10, 10));
        pnlCenter.setOpaque(false);

        // A. Thẻ KPI (Bento Cards)
        JPanel pnlKPI = new JPanel(new GridLayout(1, 4, 12, 0));
        pnlKPI.setOpaque(false);

        lblTongDoanhThuVal = new JLabel("0 VNĐ", JLabel.CENTER);
        lblTongDonHangVal  = new JLabel("0 đơn", JLabel.CENTER);
        lblTongSoLuongVal  = new JLabel("0 đôi", JLabel.CENTER);
        lblKhachHangVal    = new JLabel("4 khách", JLabel.CENTER);

        pnlKPI.add(createKPICard("TỔNG DOANH THU", lblTongDoanhThuVal, UIHelper.SUCCESS_GREEN, new Color(240, 253, 244)));
        pnlKPI.add(createKPICard("SỐ HÓA ĐƠN ĐÃ LẬP", lblTongDonHangVal, UIHelper.ACCENT_BLUE, new Color(239, 246, 255)));
        pnlKPI.add(createKPICard("SẢN PHẨM ĐÃ BÁN", lblTongSoLuongVal, UIHelper.PRIMARY_BLUE, new Color(241, 245, 249)));
        pnlKPI.add(createKPICard("KHÁCH HÀNG THÀNH VIÊN", lblKhachHangVal, UIHelper.WARN_AMBER, new Color(254, 243, 199)));

        // B. Thanh lọc dữ liệu
        JPanel pnlFilterBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 12, 8));
        pnlFilterBar.setBackground(Color.WHITE);
        pnlFilterBar.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(UIHelper.BORDER_GRAY, 1, true),
                BorderFactory.createEmptyBorder(4, 8, 4, 8)
        ));

        JLabel lblKy = new JLabel("Kỳ thống kê:");
        lblKy.setFont(new Font("Arial", Font.BOLD, 13));
        LocalDate today = LocalDate.now();
        int curThang = today.getMonthValue();
        int curNam = today.getYear();
        String strThang = (curThang < 10 ? "0" + curThang : "" + curThang) + "/" + curNam;
        cboThoiGian = new JComboBox<>(new String[]{
                "Toàn bộ thời gian", "Hôm nay", "Tháng này (" + strThang + ")", "Năm " + curNam
        });
        UIHelper.styleComboBox(cboThoiGian);
        cboThoiGian.setPreferredSize(new Dimension(190, 32));

        btnLoc = UIHelper.createPrimaryBtn("Lọc Dữ Liệu", 120, 34);
        btnLamMoi = UIHelper.createSecondaryBtn("Làm Mới", 100, 34);
        btnXuatBaoCao = UIHelper.createSuccessBtn("Xuất Báo Cáo [Excel]", 180, 34);

        pnlFilterBar.add(lblKy);
        pnlFilterBar.add(cboThoiGian);
        pnlFilterBar.add(btnLoc);
        pnlFilterBar.add(btnLamMoi);
        pnlFilterBar.add(Box.createHorizontalStrut(20));
        pnlFilterBar.add(btnXuatBaoCao);

        // Ghép KPI + Filter vào TopCenter
        JPanel pnlTopCenter = new JPanel(new BorderLayout(0, 10));
        pnlTopCenter.setOpaque(false);
        pnlTopCenter.add(pnlKPI, BorderLayout.NORTH);
        pnlTopCenter.add(pnlFilterBar, BorderLayout.SOUTH);
        pnlCenter.add(pnlTopCenter, BorderLayout.NORTH);

        // C. Bảng hiển thị chi tiết (Tabbed: Hóa đơn & Top sản phẩm)
        JTabbedPane tabTables = new JTabbedPane();
        tabTables.setFont(new Font("Arial", Font.BOLD, 12));

        // Tab 1: Danh sách hóa đơn
        String[] headersHD = {"STT", "Mã Hóa Đơn", "Thời Gian Lập", "Thu Ngân Bán Hàng", "Khách Hàng", "Tổng Thanh Toán", "Phương Thức"};
        modelHoaDon = new DefaultTableModel(headersHD, 0) {
            @Override
            public boolean isCellEditable(int r, int c) { return false; }
        };
        tableHoaDon = new JTable(modelHoaDon);
        UIHelper.styleTable(tableHoaDon);
        JScrollPane scrollHD = new JScrollPane(tableHoaDon);
        scrollHD.setBorder(BorderFactory.createEmptyBorder());
        tabTables.addTab("📋 Danh Sách Hóa Đơn Bán Hàng", scrollHD);

        // Tab 2: Top sản phẩm bán chạy
        String[] headersTop = {"Hạng", "Mã Sản Phẩm", "Tên Mẫu Giày", "Thương Hiệu", "Số Lượng Bán (Đôi)", "Doanh Thu Đóng Góp", "Tỷ Lệ Doanh Thu"};
        modelTopSP = new DefaultTableModel(headersTop, 0) {
            @Override
            public boolean isCellEditable(int r, int c) { return false; }
        };
        tableTopSP = new JTable(modelTopSP);
        UIHelper.styleTable(tableTopSP);
        JScrollPane scrollTop = new JScrollPane(tableTopSP);
        scrollTop.setBorder(BorderFactory.createEmptyBorder());
        tabTables.addTab("🏆 Top Sản Phẩm Bán Chạy Nhất", scrollTop);

        pnlCenter.add(tabTables, BorderLayout.CENTER);
        add(pnlCenter, BorderLayout.CENTER);

        // Đăng ký sự kiện
        btnLoc.addActionListener(this);
        btnLamMoi.addActionListener(this);
        btnXuatBaoCao.addActionListener(this);

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

    public void napDuLieuThongKe() {
        modelHoaDon.setRowCount(0);
        modelTopSP.setRowCount(0);

        ArrayList<HoaDon> dsHD = hd_dao.getAllHoaDon();
        double tongDoanhThu = 0;
        int stt = 1;
        int countDon = 0;

        int filterIdx = (cboThoiGian != null) ? cboThoiGian.getSelectedIndex() : 0;
        LocalDate now = LocalDate.now();

        if (dsHD != null && !dsHD.isEmpty()) {
            for (HoaDon hd : dsHD) {
                if (hd.getNgayLap() != null) {
                    LocalDate ngayLapDate = hd.getNgayLap().toLocalDate();
                    if (filterIdx == 1 && !ngayLapDate.isEqual(now)) {
                        continue; // Hôm nay
                    } else if (filterIdx == 2 && (ngayLapDate.getYear() != now.getYear() || ngayLapDate.getMonthValue() != now.getMonthValue())) {
                        continue; // Tháng này
                    } else if (filterIdx == 3 && ngayLapDate.getYear() != now.getYear()) {
                        continue; // Năm nay
                    }
                }

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
            int tongSL = hd_dao.getTongSoLuongBanRa();
            lblTongSoLuongVal.setText(tongSL + " đôi");
        } else {
            lblTongDoanhThuVal.setText("0 VNĐ");
            lblTongDonHangVal.setText("0 đơn");
            lblTongSoLuongVal.setText("0 đôi");
        }

        int tongKH = hd_dao.getTongKhachHang();
        lblKhachHangVal.setText(tongKH + " khách");

        // L06: Bảng Top Sản Phẩm Bán Chạy từ CSDL thật (HoaDon_DAO.getTopSanPhamBanChay)
        ArrayList<Object[]> topList = hd_dao.getTopSanPhamBanChay(5);
        if (topList != null && !topList.isEmpty()) {
            for (Object[] row : topList) {
                int sl = (row[4] instanceof Number) ? ((Number) row[4]).intValue() : 0;
                double dt = (row[5] instanceof Number) ? ((Number) row[5]).doubleValue() : 0.0;
                String tyLe = (tongDoanhThu > 0) ? String.format(java.util.Locale.US, "%.1f%%", (dt / tongDoanhThu) * 100) : "0.0%";
                modelTopSP.addRow(new Object[]{
                    row[0], row[1], row[2], row[3], sl, df.format(dt), tyLe
                });
            }
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object o = e.getSource();
        if (o.equals(btnLoc) || o.equals(btnLamMoi)) {
            napDuLieuThongKe();
            JOptionPane.showMessageDialog(this,
                    "Đã làm mới và cập nhật toàn bộ số liệu thống kê doanh thu theo: " + cboThoiGian.getSelectedItem(),
                    "Thông Báo Thống Kê", JOptionPane.INFORMATION_MESSAGE);
        } else if (o.equals(btnXuatBaoCao)) {
            JOptionPane.showMessageDialog(this,
                    "Tính năng xuất Excel đang được hoàn thiện trong phiên bản nâng cấp tiếp theo!",
                    "Thông Báo", JOptionPane.INFORMATION_MESSAGE);
        }
    }
}

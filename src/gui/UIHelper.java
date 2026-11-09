package gui;

import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;

/**
 * Lớp tiện ích giao diện (GUI Helper) cung cấp bảng màu chuẩn, kiểu nút bấm phẳng, định dạng bảng và các thành phần giao diện đồ họa.
 */
public class UIHelper {

    // Bảng màu chuẩn đồ họa hiện đại
    public static final Color PRIMARY_BLUE = new Color(30, 58, 138);   // Xanh Navy đậm IUH
    public static final Color ACCENT_BLUE  = new Color(37, 99, 235);   // Xanh dương nổi bật
    public static final Color SUCCESS_GREEN= new Color(22, 163, 74);   // Xanh lá thanh toán
    public static final Color DANGER_RED   = new Color(220, 38, 38);   // Đỏ xóa / hủy
    public static final Color WARN_AMBER   = new Color(217, 119, 6);   // Vàng cam cảnh báo
    public static final Color BG_GRAY      = new Color(248, 250, 252); // Xám nền nhẹ
    public static final Color BG_MAIN      = BG_GRAY;
    public static final Color INFO_BLUE    = ACCENT_BLUE;
    public static final Color BORDER_GRAY  = new Color(203, 213, 225); // Xám viền

    public static final Color TEXT_DARK    = new Color(15, 23, 42);    // Chữ màu tối chuẩn sắc nét
    public static final Color BTN_LIGHT_BG = new Color(241, 245, 249); // Nền nút xám sáng

    /**
     * Tạo nút bấm với kích thước mặc định (100x32px), màu nền và màu chữ tùy chọn.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param bgColor màu nền của nút
     * @param fgColor màu chữ của nút
     * @return đối tượng JButton tùy biến
     */
    public static JButton createButton(String text, Color bgColor, Color fgColor) {
        return createButton(text, bgColor, fgColor, 100, 32);
    }

    /**
     * Tạo nút bấm tùy biến đảm bảo 100% hiển thị màu nền và chữ sắc nét trên mọi hệ điều hành.
     * Tự vẽ nền và chữ bằng Graphics2D để ngăn Look & Feel của Windows làm mờ hoặc đổi màu chữ.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param bgColor màu nền của nút
     * @param fgColor màu chữ của nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton tùy biến
     */
    public static JButton createButton(String text, Color bgColor, Color fgColor, int minW, int minH) {
        JButton btn = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_LCD_HRGB);

                // 0. Xử lý khi nút bị vô hiệu hóa (Disabled)
                if (!isEnabled()) {
                    g2.setColor(new Color(226, 232, 240));
                    g2.fillRoundRect(0, 0, getWidth(), getHeight(), 8, 8);
                    g2.setColor(new Color(203, 213, 225));
                    g2.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 8, 8);
                    g2.setFont(getFont());
                    g2.setColor(new Color(148, 163, 184));
                    FontMetrics fm = g2.getFontMetrics();
                    int textX = (getWidth() - fm.stringWidth(getText())) / 2;
                    int textY = (getHeight() - fm.getHeight()) / 2 + fm.getAscent();
                    g2.drawString(getText(), textX, textY);
                    g2.dispose();
                    return;
                }

                // 1. Vẽ nền nút bo góc
                if (getModel().isPressed()) {
                    g2.setColor(bgColor.darker());
                } else if (getModel().isRollover()) {
                    g2.setColor(new Color(
                        Math.min(255, bgColor.getRed() + 20),
                        Math.min(255, bgColor.getGreen() + 20),
                        Math.min(255, bgColor.getBlue() + 20)
                    ));
                } else {
                    g2.setColor(bgColor);
                }
                g2.fillRoundRect(0, 0, getWidth(), getHeight(), 8, 8);

                // 2. Viền phân tách thanh lịch
                if (fgColor.equals(TEXT_DARK) || bgColor.equals(BTN_LIGHT_BG)) {
                    g2.setColor(BORDER_GRAY); // Viền xám cho nút sáng
                } else {
                    g2.setColor(new Color(0, 0, 0, 35));
                }
                g2.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 8, 8);

                // 3. Vẽ chữ sắc nét, căn giữa hoàn hảo
                g2.setFont(getFont());
                g2.setColor(fgColor);
                FontMetrics fm = g2.getFontMetrics();
                int textX = (getWidth() - fm.stringWidth(getText())) / 2;
                int textY = (getHeight() - fm.getHeight()) / 2 + fm.getAscent();
                g2.drawString(getText(), textX, textY);

                g2.dispose();
            }
        };

        btn.setFont(new Font("Arial", Font.BOLD, 13));
        btn.setForeground(fgColor);
        btn.setContentAreaFilled(false);
        btn.setFocusPainted(false);
        btn.setBorderPainted(false);
        btn.setOpaque(false);
        btn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        if (minW > 0 && minH > 0) {
            btn.setPreferredSize(new Dimension(minW, minH));
        }
        return btn;
    }

    /**
     * Tạo nút bấm chính (Primary) màu xanh dương nổi bật với kích thước chuẩn (110x34px).
     *
     * @param text tiêu đề hiển thị trên nút
     * @return đối tượng JButton kiểu Primary
     */
    public static JButton createPrimaryBtn(String text) {
        return createPrimaryBtn(text, 110, 34);
    }

    /**
     * Tạo nút bấm chính (Primary) màu xanh dương nổi bật với kích thước tùy biến.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton kiểu Primary
     */
    public static JButton createPrimaryBtn(String text, int minW, int minH) {
        return createButton(text, ACCENT_BLUE, Color.WHITE, minW, minH);
    }

    /**
     * Tạo nút bấm thành công (Success) màu xanh lá cây với kích thước chuẩn (110x34px).
     *
     * @param text tiêu đề hiển thị trên nút
     * @return đối tượng JButton kiểu Success
     */
    public static JButton createSuccessBtn(String text) {
        return createSuccessBtn(text, 110, 34);
    }

    /**
     * Tạo nút bấm thành công (Success) màu xanh lá cây với kích thước tùy biến.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton kiểu Success
     */
    public static JButton createSuccessBtn(String text, int minW, int minH) {
        return createButton(text, SUCCESS_GREEN, Color.WHITE, minW, minH);
    }

    /**
     * Tạo nút bấm cảnh báo nguy hiểm (Danger) màu đỏ với kích thước chuẩn (110x34px).
     *
     * @param text tiêu đề hiển thị trên nút
     * @return đối tượng JButton kiểu Danger
     */
    public static JButton createDangerBtn(String text) {
        return createDangerBtn(text, 110, 34);
    }

    /**
     * Tạo nút bấm cảnh báo nguy hiểm (Danger) màu đỏ với kích thước tùy biến.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton kiểu Danger
     */
    public static JButton createDangerBtn(String text, int minW, int minH) {
        return createButton(text, DANGER_RED, Color.WHITE, minW, minH);
    }

    /**
     * Tạo nút bấm tối màu (Dark) xanh navy đậm với kích thước chuẩn (65x30px).
     *
     * @param text tiêu đề hiển thị trên nút
     * @return đối tượng JButton kiểu Dark
     */
    public static JButton createDarkBtn(String text) {
        return createDarkBtn(text, 65, 30);
    }

    /**
     * Tạo nút bấm tối màu (Dark) xanh navy đậm với kích thước tùy biến.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton kiểu Dark
     */
    public static JButton createDarkBtn(String text, int minW, int minH) {
        return createButton(text, PRIMARY_BLUE, Color.WHITE, minW, minH);
    }

    /**
     * Tạo nút bấm phụ (Secondary) màu xám sáng với kích thước chuẩn (120x34px).
     *
     * @param text tiêu đề hiển thị trên nút
     * @return đối tượng JButton kiểu Secondary
     */
    public static JButton createSecondaryBtn(String text) {
        return createSecondaryBtn(text, 120, 34);
    }

    /**
     * Tạo nút bấm phụ (Secondary) màu xám sáng với kích thước tùy biến.
     *
     * @param text tiêu đề hiển thị trên nút
     * @param minW chiều rộng tối thiểu của nút (px)
     * @param minH chiều cao tối thiểu của nút (px)
     * @return đối tượng JButton kiểu Secondary
     */
    public static JButton createSecondaryBtn(String text, int minW, int minH) {
        return createButton(text, BTN_LIGHT_BG, TEXT_DARK, minW, minH);
    }

    /**
     * Định dạng trường nhập liệu có viền mềm và hiệu ứng đổi màu viền khi nhận/mất tiêu điểm.
     *
     * @param txt trường nhập liệu JTextField cần định dạng
     */
    public static void styleTextField(JTextField txt) {
        txt.setFont(new Font("Arial", Font.PLAIN, 13));
        txt.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER_GRAY, 1, true),
                BorderFactory.createEmptyBorder(6, 10, 6, 10)
        ));
        txt.addFocusListener(new FocusAdapter() {
            @Override
            public void focusGained(FocusEvent e) {
                txt.setBorder(BorderFactory.createCompoundBorder(
                        BorderFactory.createLineBorder(ACCENT_BLUE, 2, true),
                        BorderFactory.createEmptyBorder(5, 9, 5, 9)
                ));
            }
            @Override
            public void focusLost(FocusEvent e) {
                txt.setBorder(BorderFactory.createCompoundBorder(
                        BorderFactory.createLineBorder(BORDER_GRAY, 1, true),
                        BorderFactory.createEmptyBorder(6, 10, 6, 10)
                ));
            }
        });
    }

    /**
     * Định dạng ComboBox phẳng và dễ đọc.
     *
     * @param cbo hộp chọn JComboBox cần định dạng
     */
    public static void styleComboBox(JComboBox<?> cbo) {
        cbo.setFont(new Font("Arial", Font.PLAIN, 13));
        cbo.setBackground(Color.WHITE);
        cbo.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER_GRAY, 1, true),
                BorderFactory.createEmptyBorder(2, 4, 2, 4)
        ));
    }

    /**
     * Định dạng bảng JTable chuẩn doanh nghiệp: hàng cao 32px, tiêu đề xanh navy sang trọng, căn giữa cột đầu tiên.
     *
     * @param table bảng JTable cần định dạng
     */
    public static void styleTable(JTable table) {
        table.setRowHeight(30);
        table.setFont(new Font("Arial", Font.PLAIN, 12));
        table.setSelectionBackground(new Color(224, 231, 255));
        table.setSelectionForeground(new Color(30, 58, 138));
        table.setGridColor(new Color(241, 245, 249));

        JTableHeader header = table.getTableHeader();
        header.setFont(new Font("Arial", Font.BOLD, 12));
        header.setBackground(new Color(241, 245, 249));
        header.setForeground(new Color(30, 41, 59));
        header.setPreferredSize(new Dimension(0, 36));

        DefaultTableCellRenderer center = new DefaultTableCellRenderer();
        center.setHorizontalAlignment(JLabel.CENTER);
        table.getColumnModel().getColumn(0).setPreferredWidth(45);
        table.getColumnModel().getColumn(0).setCellRenderer(center);
    }

    /**
     * Tạo Panel có khung TitledBorder chuẩn đồng bộ và tiêu đề màu tùy chọn.
     *
     * @param title tiêu đề hiển thị trên khung viền
     * @param titleColor màu sắc của chữ tiêu đề
     * @return đối tượng JPanel có khung viền TitledBorder
     */
    public static JPanel createTitledPanel(String title, Color titleColor) {
        JPanel p = new JPanel();
        p.setBackground(Color.WHITE);
        Border line = BorderFactory.createLineBorder(BORDER_GRAY, 1, true);
        TitledBorder border = BorderFactory.createTitledBorder(
                line, " " + title + " ",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), titleColor
        );
        p.setBorder(BorderFactory.createCompoundBorder(
                border, BorderFactory.createEmptyBorder(8, 12, 8, 12)
        ));
        return p;
    }
}

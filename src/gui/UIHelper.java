package gui;

import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;

public class UIHelper {

    // Bảng màu chuẩn đồ họa hiện đại
    public static final Color PRIMARY_BLUE = new Color(30, 58, 138);   // Xanh Navy đậm IUH
    public static final Color ACCENT_BLUE  = new Color(37, 99, 235);   // Xanh dương nổi bật
    public static final Color SUCCESS_GREEN= new Color(22, 163, 74);   // Xanh lá thanh toán
    public static final Color DANGER_RED   = new Color(220, 38, 38);   // Đỏ xóa / hủy
    public static final Color WARN_AMBER   = new Color(217, 119, 6);   // Vàng cam cảnh báo
    public static final Color BG_GRAY      = new Color(248, 250, 252); // Xám nền nhẹ
    public static final Color BORDER_GRAY  = new Color(203, 213, 225); // Xám viền

    public static final Color TEXT_DARK    = new Color(15, 23, 42);    // Chữ màu tối chuẩn sắc nét
    public static final Color BTN_LIGHT_BG = new Color(241, 245, 249); // Nền nút xám sáng

    /**
     * Tạo nút bấm tùy biến đảm bảo 100% hiển thị màu nền và chữ sắc nét trên mọi hệ điều hành.
     * Vẽ trực tiếp chữ bằng Graphics2D để ngăn Look & Feel của Windows làm mờ hoặc đổi màu chữ.
     */
    public static JButton createButton(String text, Color bgColor, Color fgColor, int minW, int minH) {
        JButton btn = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_LCD_HRGB);

                // 1. Vẽ nền nút bo góc
                if (getModel().isPressed()) {
                    g2.setColor(bgColor.darker());
                } else if (getModel().isRollover()) {
                    g2.setColor(bgColor.brighter());
                } else {
                    g2.setColor(bgColor);
                }
                g2.fillRoundRect(0, 0, getWidth(), getHeight(), 8, 8);

                // 2. Viền phân tách thanh lịch
                g2.setColor(new Color(0, 0, 0, 25));
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

    public static JButton createPrimaryBtn(String text, int minW, int minH) {
        return createButton(text, ACCENT_BLUE, Color.WHITE, minW, minH);
    }

    public static JButton createSuccessBtn(String text, int minW, int minH) {
        return createButton(text, SUCCESS_GREEN, Color.WHITE, minW, minH);
    }

    public static JButton createDangerBtn(String text, int minW, int minH) {
        return createButton(text, DANGER_RED, Color.WHITE, minW, minH);
    }

    public static JButton createDarkBtn(String text, int minW, int minH) {
        return createButton(text, PRIMARY_BLUE, Color.WHITE, minW, minH);
    }

    public static JButton createSecondaryBtn(String text, int minW, int minH) {
        return createButton(text, BTN_LIGHT_BG, TEXT_DARK, minW, minH);
    }

    /**
     * Định dạng trường nhập liệu có viền mềm và hiệu ứng khi focus
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
     * Định dạng ComboBox phẳng và dễ đọc
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
     * Định dạng bảng JTable chuẩn doanh nghiệp: hàng cao 32px, tiêu đề xanh navy sang trọng
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
     * Tạo Panel có khung TitledBorder chuẩn đồng bộ
     */
    public static JPanel createTitledPanel(String title, Color titleColor) {
        JPanel pnl = new JPanel();
        pnl.setBackground(Color.WHITE);
        Border line = BorderFactory.createLineBorder(BORDER_GRAY, 1, true);
        TitledBorder border = BorderFactory.createTitledBorder(
                line, " " + title + " ",
                TitledBorder.LEFT, TitledBorder.TOP,
                new Font("Arial", Font.BOLD, 13), titleColor
        );
        pnl.setBorder(BorderFactory.createCompoundBorder(
                border, BorderFactory.createEmptyBorder(8, 12, 8, 12)
        ));
        return pnl;
    }
}

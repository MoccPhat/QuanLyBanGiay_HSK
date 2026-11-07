"""
Script: generate_analysis_diagrams.py
Mục đích:
  - Sinh 3 sơ đồ phân tích còn thiếu cho L21:
    1. Sơ đồ Use Case tổng thể -> diagram_usecase_shoe.png & SoDoUseCase_QuanLyBanGiay.drawio
    2. Sơ đồ Tuần tự (Sequence Diagram) luồng thanh toán POS -> diagram_sequence_shoe.png & SoDoSequence_QuanLyBanGiay.drawio
    3. Sơ đồ Kiến trúc 3 tầng (Architecture Diagram) -> diagram_architecture_shoe.png & SoDoKienTruc_QuanLyBanGiay.drawio
  - Độ phân giải >= 1600px width (300 DPI), font rõ nét, chuẩn UML.
"""

import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'


# ==============================================================================
# 1. SƠ ĐỒ USE CASE TỔNG THỂ
# ==============================================================================

def generate_usecase_diagram():
    print(">>> Đang vẽ Sơ đồ Use Case tổng thể...")
    fig, ax = plt.subplots(figsize=(19, 13), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Title
    ax.text(800, 1060, "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG (SYSTEM USE CASE DIAGRAM)", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(800, 1030, "HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG (STEPUP POS SYSTEM)", 
            ha='center', va='center', fontsize=11, color='#475569')

    # System boundary box
    sys_box = patches.FancyBboxPatch((360, 60), 960, 930, boxstyle="round,pad=10,rounding_size=20", 
                                    facecolor='#F8FAFC', edgecolor='#0284C7', linewidth=2, zorder=1)
    ax.add_patch(sys_box)
    ax.text(840, 965, "HỆ THỐNG POS STEPUP FOOTWEAR", ha='center', va='center', 
            fontsize=13, fontweight='bold', color='#0369A1', zorder=2)

    # Helper vẽ Stick Figure Actor
    def draw_actor(x, y, label):
        head = patches.Circle((x, y + 40), 16, edgecolor='#0F172A', facecolor='#FEF3C7', linewidth=1.8, zorder=3)
        ax.add_patch(head)
        ax.plot([x, x], [y + 24, y - 16], color='#0F172A', lw=1.8, zorder=3) # Body
        ax.plot([x - 22, x + 22], [y + 12, y + 12], color='#0F172A', lw=1.8, zorder=3) # Arms
        ax.plot([x, x - 18], [y - 16, y - 50], color='#0F172A', lw=1.8, zorder=3) # Left leg
        ax.plot([x, x + 18], [y - 16, y - 50], color='#0F172A', lw=1.8, zorder=3) # Right leg
        ax.text(x, y - 72, label, ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A', zorder=3)

    # Vẽ 2 Actors
    # Actor 1: Thu ngân (trên trái)
    draw_actor(160, 720, "Nhân viên thu ngân\n(Cashier / Staff)")
    # Actor 2: Quản lý (dưới trái)
    draw_actor(160, 260, "Người quản lý\n(Store Manager / Admin)")

    # Kế thừa Actor: Quản lý extends Thu ngân
    ax.plot([160, 160], [330, 620], color='#0F172A', lw=1.5, ls='--', zorder=2)
    tri_act = patches.Polygon([[152, 605], [168, 605], [160, 620]], closed=True, 
                              edgecolor='#0F172A', facecolor='#FFFFFF', lw=1.5, zorder=4)
    ax.add_patch(tri_act)
    ax.text(175, 475, "kế thừa", fontsize=9, style='italic', color='#64748B', va='center')

    # Helper vẽ Oval Use Case
    def draw_usecase(x, y, w, h, text, code, color='#EFF6FF', border='#3B82F6'):
        oval = patches.Ellipse((x, y), w, h, facecolor=color, edgecolor=border, lw=1.4, zorder=3)
        ax.add_patch(oval)
        ax.text(x, y + 8, f"[{code}]", ha='center', va='center', fontsize=8.5, fontweight='bold', color=border, zorder=4)
        ax.text(x, y - 9, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A', zorder=4)
        return (x, y)

    # Use cases
    # Common Use Cases
    uc_dn = draw_usecase(540, 890, 260, 65, "Đăng nhập hệ thống", "UC01", '#FEF3C7', '#D97706')
    uc_dx = draw_usecase(540, 800, 260, 65, "Đăng xuất & Thoát", "UC02", '#F1F5F9', '#64748B')
    uc_pos = draw_usecase(540, 680, 270, 75, "Bán hàng tại quầy (POS)", "UC03", '#DCFCE7', '#16A34A')
    uc_kh = draw_usecase(540, 560, 260, 65, "Quản lý khách hàng", "UC04", '#DCFCE7', '#16A34A')

    # Sub-use cases included/extended in POS
    uc_ton = draw_usecase(960, 780, 280, 65, "Tra cứu tồn kho theo size/màu", "UC03.1", '#F0FDFA', '#0D9488')
    uc_pay = draw_usecase(960, 680, 280, 65, "Trừ tồn kho & Thanh toán ACID", "UC03.2", '#F0FDFA', '#0D9488')
    uc_point = draw_usecase(960, 580, 280, 65, "Tích điểm & Giảm giá thành viên", "UC03.3", '#F0FDFA', '#0D9488')

    # Manager-only Use Cases
    uc_sp = draw_usecase(620, 420, 290, 70, "Quản lý mẫu giày & Biến thể", "UC05", '#EDE9FE', '#7C3AED')
    uc_nv = draw_usecase(620, 310, 290, 70, "Quản lý nhân sự & Băm mật khẩu", "UC06", '#EDE9FE', '#7C3AED')
    uc_tk = draw_usecase(620, 200, 290, 70, "Báo cáo doanh thu & Thống kê", "UC07", '#FEE2E2', '#DC2626')
    uc_note = draw_usecase(1040, 200, 240, 60, "(Định hướng mở rộng)", "MÔ ĐUN", '#FFF1F2', '#E11D48')

    # Connectors Actor -> Use Case
    def connect_actor(x_act, y_act, x_uc, y_uc):
        ax.plot([x_act, x_uc], [y_act, y_uc], color='#0F172A', lw=1.2, zorder=2)

    # Thu ngân nối UC chung
    connect_actor(185, 730, 410, 890)
    connect_actor(185, 720, 410, 800)
    connect_actor(185, 710, 405, 680)
    connect_actor(185, 690, 410, 560)

    # Quản lý nối UC quản lý
    connect_actor(185, 280, 475, 420)
    connect_actor(185, 260, 475, 310)
    connect_actor(185, 240, 475, 200)

    # Include & Extend relationships
    def draw_dashed_arrow(x1, y1, x2, y2, label="<<include>>"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#0284C7', lw=1.3, ls='--', shrinkA=4, shrinkB=4))
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 6, label, fontsize=8.5, style='italic', color='#0369A1', ha='center',
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

    draw_dashed_arrow(675, 700, 820, 765, "<<include>>")
    draw_dashed_arrow(675, 680, 820, 680, "<<include>>")
    draw_dashed_arrow(675, 660, 820, 600, "<<extend>>")
    draw_dashed_arrow(765, 200, 920, 200, "<<include>>")

    # Legend / Note at bottom right
    leg = patches.FancyBboxPatch((970, 70), 330, 80, boxstyle="round,pad=6,rounding_size=8", 
                                facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1, zorder=2)
    ax.add_patch(leg)
    ax.text(980, 125, "Chú thích phân quyền:", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(980, 103, "• Màu xanh lá/vàng: Thu ngân & Quản lý cùng dùng", fontsize=8.5, color='#15803D')
    ax.text(980, 83, "• Màu tím/đỏ: Đặc quyền Người quản lý (Admin)", fontsize=8.5, color='#7C3AED')

    plt.tight_layout()
    out = os.path.join(os.getcwd(), 'diagram_usecase_shoe.png')
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f" [PASS] Đã tạo thành công Sơ đồ Use Case: {out}")


# ==============================================================================
# 2. SƠ ĐỒ TUẦN TỰ (SEQUENCE DIAGRAM) CHO LUỒNG THANH TOÁN POS
# ==============================================================================

def generate_sequence_diagram():
    print(">>> Đang vẽ Sơ đồ Tuần tự (Sequence Diagram) luồng thanh toán POS...")
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1250)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Title
    ax.text(800, 1210, "SƠ ĐỒ TUẦN TỰ: GIAO DỊCH THANH TOÁN TẠI QUẦY POS (TRANSACTION ACID)", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(800, 1180, "LUỒNG TƯƠNG TÁC GIỮA THU NGÂN, GIAO DIỆN SWING, DAO VÀ HỆ QUẢN TRỊ SQL SERVER", 
            ha='center', va='center', fontsize=11, color='#475569')

    # Lifeline objects
    lifelines = [
        ("Thu ngân\n(Cashier)", 150, '#FEF3C7', '#D97706'),
        ("BanHang_GUI\n(Giao diện POS)", 450, '#E0F2FE', '#0284C7'),
        ("HoaDon_DAO\n(Xử lý giao dịch)", 800, '#EDE9FE', '#7C3AED'),
        ("ChiTietGiay_DAO\n(Kiểm soát kho)", 1150, '#FFEDD5', '#EA580C'),
        ("SQL Server DB\n(QuanLyBanGiay)", 1450, '#FCE7F3', '#DB2777'),
    ]

    top_y = 1110
    bot_y = 70

    # Draw Lifelines & Headers
    for name, x, bg, border in lifelines:
        # Header Box
        box = patches.FancyBboxPatch((x - 85, top_y - 25), 170, 50, boxstyle="round,pad=4,rounding_size=6",
                                    facecolor=bg, edgecolor=border, lw=1.4, zorder=3)
        ax.add_patch(box)
        ax.text(x, top_y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A', zorder=4)

        # Dashed line
        ax.plot([x, x], [top_y - 25, bot_y], color='#94A3B8', lw=1.2, ls='--', zorder=1)

    # Helper Message Arrow
    def draw_msg(x1, x2, y, text, is_async=False, is_return=False, color='#0F172A'):
        style = "->"
        ls = "--" if is_return else "-"
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.4, ls=ls, shrinkA=2, shrinkB=2))
        mx = (x1 + x2) / 2
        va = 'bottom' if not is_return else 'top'
        ax.text(mx, y + (5 if not is_return else -12), text, ha='center', va='center', 
                fontsize=9.2, fontweight='bold', color=color,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

    # Activation Bar Helper
    def draw_act(x, y1, y2, bg='#E2E8F0', border='#475569'):
        h = abs(y1 - y2)
        ymin = min(y1, y2)
        rect = patches.Rectangle((x - 7, ymin), 14, h, facecolor=bg, edgecolor=border, lw=1, zorder=2)
        ax.add_patch(rect)

    draw_act(150, 1020, 160)
    draw_act(450, 1020, 190)
    draw_act(800, 970, 250)
    draw_act(1450, 930, 270)

    # Messages sequence
    y = 1020
    draw_msg(150, 450, y, "1. Nhấn [F10] hoặc click 'THANH TOÁN' (tiền khách đưa)")
    
    y -= 50
    # Self call validate
    ax.plot([450, 490, 490, 450], [y + 10, y + 10, y - 15, y - 15], color='#0284C7', lw=1.3)
    ax.text(500, y - 3, "validateForm(): kiểm tra giỏ hàng, tiền đưa >= tổng", fontsize=8.5, color='#0284C7', va='center')

    y -= 50
    draw_msg(450, 800, y, "2. themHoaDon(hoaDon) -> bắt đầu Transaction", color='#7C3AED')

    y -= 45
    draw_msg(800, 1450, y, "3. setAutoCommit(false) -> Khởi tạo giao dịch ACID", color='#7C3AED')

    y -= 45
    draw_msg(800, 1450, y, "4. SELECT MAX(maHoaDon)+1 WITH (UPDLOCK, HOLDLOCK)", color='#0F172A')

    y -= 40
    draw_msg(1450, 800, y, "5. Trả về mã HD mới (ví dụ 'HD000003')", is_return=True)

    y -= 45
    draw_msg(800, 1450, y, "6. INSERT INTO HoaDon (13 cột tài chính/điểm)")

    y -= 45
    draw_msg(800, 1450, y, "7. Lặp INSERT INTO ChiTietHoaDon (từng dòng hàng)")

    y -= 55
    draw_msg(800, 1450, y, "8. UPDATE ChiTietGiay SET soLuongTon -= ? WHERE soLuongTon >= ?", color='#B45309')

    # Frame ALT (Kiểm tra tồn kho thành công hoặc thất bại)
    y_alt_top = y - 25
    y_alt_bot = y_alt_top - 330
    alt_box = patches.Rectangle((400, y_alt_bot), 1100, 330, facecolor='#F0FDF4', edgecolor='#16A34A', lw=1.4, zorder=1)
    ax.add_patch(alt_box)
    ax.text(415, y_alt_top - 15, "[alt] THÀNH CÔNG: Kho đủ tồn (rowsUpdated > 0)", fontsize=9.5, fontweight='bold', color='#15803D')

    y -= 60
    draw_msg(800, 1450, y, "9.1. UPDATE KhachHang SET diemTichLuy..., hangThanhVien...", color='#16A34A')

    y -= 45
    draw_msg(800, 1450, y, "9.2. con.commit() -> Ghi nhận vĩnh viễn vào CSDL", color='#16A34A')

    y -= 45
    draw_msg(800, 450, y, "9.3. Trả về true (thanh toán hoàn tất)", is_return=True, color='#16A34A')

    y -= 45
    draw_msg(450, 150, y, "9.4. Hiển thị JDialog Hóa đơn K80, in phiếu & làm mới giỏ hàng", color='#16A34A')

    # Divider line in ALT box
    y_div = y - 30
    ax.plot([400, 1500], [y_div, y_div], color='#DC2626', lw=1.2, ls=':', zorder=2)
    ax.text(415, y_div - 15, "[else] THẤT BẠI: Kho không đủ (rowsUpdated == 0)", fontsize=9.5, fontweight='bold', color='#DC2626')

    y = y_div - 45
    draw_msg(800, 1450, y, "10.1. con.rollback() -> Hoàn tác 100% mọi thay đổi", color='#DC2626')

    y -= 40
    draw_msg(800, 450, y, "10.2. Ném ngoại lệ / Trả về false ('Tồn kho không đủ')", is_return=True, color='#DC2626')

    y -= 40
    draw_msg(450, 150, y, "10.3. Hiện JOptionPane lỗi, giữ nguyên giỏ hàng để thu ngân xử lý", color='#DC2626')

    # Bottom note
    ax.text(800, 30, "Nguyên lý toàn vẹn: Tầng DAO đảm bảo tính ACID; không có trigger ngầm; kiểm soát xung đột qua UPDLOCK & HOLDLOCK.", 
            ha='center', va='center', fontsize=9.5, style='italic', color='#475569')

    plt.tight_layout()
    out = os.path.join(os.getcwd(), 'diagram_sequence_shoe.png')
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f" [PASS] Đã tạo thành công Sơ đồ Tuần tự: {out}")


# ==============================================================================
# 3. SƠ ĐỒ KIẾN TRÚC 3 TẦNG (ARCHITECTURE DIAGRAM)
# ==============================================================================

def generate_architecture_diagram():
    print(">>> Đang vẽ Sơ đồ Kiến trúc 3 tầng...")
    fig, ax = plt.subplots(figsize=(19, 13), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Title
    ax.text(800, 1060, "SƠ ĐỒ KIẾN TRÚC HỆ THỐNG 3 TẦNG (3-TIER ARCHITECTURE DIAGRAM)", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(800, 1030, "MÔ HÌNH PHÂN TẦNG: GIAO DIỆN SWING (GUI) - TRUY CẬP DỮ LIỆU (DAO) - CƠ SỞ DỮ LIỆU (SQL SERVER)", 
            ha='center', va='center', fontsize=11, color='#475569')

    # Helper vẽ Tier Container Box
    def draw_tier_box(x, y, w, h, title, subtitle, bg_color, border_color):
        shadow = patches.FancyBboxPatch((x + 5, y - 5), w, h, boxstyle="round,pad=6,rounding_size=12",
                                        facecolor='#E2E8F0', edgecolor='none', zorder=1)
        ax.add_patch(shadow)
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=6,rounding_size=12",
                                    facecolor=bg_color, edgecolor=border_color, lw=1.6, zorder=2)
        ax.add_patch(box)
        ax.text(x + 20, y + h - 25, title, fontsize=12, fontweight='bold', color=border_color, zorder=3)
        ax.text(x + 20, y + h - 45, subtitle, fontsize=9.5, style='italic', color='#64748B', zorder=3)
        return box

    # 1. TẦNG 1: GUI (Trên)
    draw_tier_box(80, 710, 1440, 270, 
                  "TẦNG TRÌNH DIỄN (PRESENTATION LAYER - GUI & USER INTERFACE)",
                  "Công nghệ: Java Swing, AWT, Event-Driven Programming, UIHelper, KeyBindings",
                  '#F8FAFC', '#0284C7')

    # Helper Component Card
    def draw_card(x, y, w, h, title, desc, bg='#FFFFFF', border='#CBD5E1'):
        c = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=1.2, zorder=3)
        ax.add_patch(c)
        ax.text(x + w/2, y + h - 18, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0F172A', zorder=4)
        ax.text(x + 12, y + h/2 - 8, desc, ha='left', va='center', fontsize=8.5, color='#475569', zorder=4)

    draw_card(110, 730, 240, 170, "DangNhap_GUI", "• Xác thực tài khoản\n• Băm SHA-256 đối chiếu\n• Phân luồng Admin/Staff")
    draw_card(380, 730, 270, 170, "BanHang_GUI (POS)", "• Phím tắt F1, F10, DEL, ESC\n• Chọn size/màu & hiện SoLuongTon\n• Tích điểm & hóa đơn K80")
    draw_card(680, 730, 260, 170, "QuanLySanPham_GUI", "• CRUD Mẫu giày & SKU\n• Validate giaBan >= giaNhap\n• Xóa mềm (trangThai = 0)")
    draw_card(970, 730, 260, 170, "QuanLyKhachHang_GUI", "• CRUD khách hàng\n• Regex SĐT: ^0[35789]\\d{8}$\n• Tự tính hạng thành viên")
    draw_card(1260, 730, 230, 170, "QuanLyNhanVien_GUI", "• CRUD nhân viên\n• Chặn < 18 tuổi\n• Khóa tài khoản nghỉ")

    # 2. TẦNG 2: DAO & ENTITY (Giữa)
    draw_tier_box(80, 360, 1440, 280, 
                  "TẦNG TRUY CẬP DỮ LIỆU & THỰC THỂ (DATA ACCESS LAYER - DAO & ENTITY)",
                  "Công nghệ: JDBC PreparedStatement, Transaction ACID (con.setAutoCommit(false)), Domain Models",
                  '#F8FAFC', '#7C3AED')

    # Left: DAO Modules
    draw_card(110, 380, 260, 185, "HoaDon_DAO", "• Transaction thêm HĐ & CTHĐ\n• Trừ kho có điều kiện\n• Rollback an toàn khi thiếu tồn\n• Sinh mã UPDLOCK, HOLDLOCK", '#EDE9FE', '#7C3AED')
    draw_card(400, 380, 260, 185, "SanPham_DAO & ChiTietGiay_DAO", "• Truy vấn tồn kho tức thời\n• Cập nhật thông tin mẫu giày\n• Sinh mã SKU biến thể tự động\n• Bảo toàn lịch sử bán", '#EDE9FE', '#7C3AED')
    draw_card(690, 380, 240, 185, "KhachHang_DAO & NhanVien_DAO", "• Cập nhật điểm & nâng hạng\n• Quản lý hồ sơ nhân sự\n• Xác thực đăng nhập SHA-256\n• Bắt lỗi vi phạm CHECK/UQ", '#EDE9FE', '#7C3AED')

    # Right: Domain Entities box
    ent_box = patches.Rectangle((960, 380), 530, 185, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2, zorder=3)
    ax.add_patch(ent_box)
    ax.text(1225, 545, "7 LỚP THỰC THỂ HƯỚNG ĐỐI TƯỢNG (OOP ENTITIES)", ha='center', fontsize=10.5, fontweight='bold', color='#B45309', zorder=4)
    ax.text(980, 485, "• Nguoi (Abstract: hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email)\n"
                      "• NhanVien (extends Nguoi, matKhau, isQuanLy, tinhLuong)\n"
                      "• KhachHang (extends Nguoi, diemTichLuy, hangThanhVien, tinhChietKhau)\n"
                      "• SanPham <>-- ChiTietGiay (Composition: 1 Mẫu giày sở hữu n biến thể)\n"
                      "• HoaDon <>-- ChiTietHoaDon (Composition: 1 Hóa đơn sở hữu n dòng hàng)", 
            fontsize=8.8, color='#0F172A', zorder=4)

    # 3. TẦNG 3: CSDL (Dưới)
    draw_tier_box(80, 60, 1440, 230, 
                  "TẦNG CƠ SỞ DỮ LIỆU QUAN HỆ (DATABASE LAYER - SQL SERVER)",
                  "Công nghệ: Microsoft SQL Server, Chuẩn 3NF, 33 CHECK Constraints, 5 Foreign Keys, 3 Unique Keys",
                  '#F8FAFC', '#BE185D')

    draw_card(110, 80, 320, 145, "Bảng Tài Chính & Bán Hàng", "• HoaDon (13 cột, DECIMAL(18,0))\n• ChiTietHoaDon (PK phức hợp, CASCADE)\n• Ràng buộc tiền thừa & chiết khấu", '#FCE7F3', '#BE185D')
    draw_card(460, 80, 320, 145, "Bảng Sản Phẩm & Biến Thể SKU", "• SanPham (giaBan >= giaNhap > 0)\n• ChiTietGiay (UQ size/màu/mã SP)\n• Kiểm soát tồn kho không âm", '#FCE7F3', '#BE185D')
    draw_card(810, 80, 320, 145, "Bảng Khách Hàng & Nhân Sự", "• NhanVien (CHAR(64) SHA-256)\n• KhachHang (UQ SĐT, CHECK điểm)\n• Ràng buộc độ tuổi lao động >= 18", '#FCE7F3', '#BE185D')
    draw_card(1160, 80, 330, 145, "Cơ Chế Toàn Vẹn & Đồng Thời", "• JDBC Transaction (ACID)\n• Khóa chống trùng mã: UPDLOCK, HOLDLOCK\n• Xóa mềm SanPham.trangThai\n• 33 ràng buộc CHECK bảo vệ dữ liệu", '#FCE7F3', '#BE185D')

    # Big Connection Arrows between Tiers
    # Tier 1 -> Tier 2
    ax.annotate('', xy=(800, 640), xytext=(800, 710),
                arrowprops=dict(arrowstyle="<->", color='#0284C7', lw=2.5, shrinkA=4, shrinkB=4))
    ax.text(815, 675, "Lời gọi phương thức nghiệp vụ & Nhận kết quả đối tượng Entity", 
            fontsize=9.5, fontweight='bold', color='#0369A1', va='center')

    # Tier 2 -> Tier 3
    ax.annotate('', xy=(800, 290), xytext=(800, 360),
                arrowprops=dict(arrowstyle="<->", color='#7C3AED', lw=2.5, shrinkA=4, shrinkB=4))
    ax.text(815, 325, "Câu lệnh T-SQL (PreparedStatement) & Nhận tập kết quả ResultSet qua JDBC", 
            fontsize=9.5, fontweight='bold', color='#6D28D9', va='center')

    plt.tight_layout()
    out = os.path.join(os.getcwd(), 'diagram_architecture_shoe.png')
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f" [PASS] Đã tạo thành công Sơ đồ Kiến trúc 3 tầng: {out}")


# ==============================================================================
# 4. TẠO CÁC FILE NGUỒN DRAW.IO TƯƠNG ỨNG
# ==============================================================================

def generate_drawio_source_files():
    print(">>> Đang xuất các file nguồn Draw.io...")
    
    # 1. SoDoUseCase_QuanLyBanGiay.drawio
    uc_drawio = """<?xml version='1.0' encoding='utf-8'?>
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="UseCase_POS" name="SoDoUseCase_QuanLyBanGiay">
    <mxGraphModel dx="1422" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="box" value="HỆ THỐNG POS STEPUP FOOTWEAR" style="swimlane;startSize=30;fillColor=#F8FAFC;strokeColor=#0284C7;fontColor=#0369A1;fontStyle=1;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="360" y="80" width="960" height="920" as="geometry" />
        </mxCell>
        <!-- Actors -->
        <mxCell id="act_cashier" value="Nhân viên thu ngân" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#FEF3C7;strokeColor=#0F172A;" vertex="1" parent="1">
          <mxGeometry x="140" y="320" width="40" height="80" as="geometry" />
        </mxCell>
        <mxCell id="act_manager" value="Người quản lý" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#FEF3C7;strokeColor=#0F172A;" vertex="1" parent="1">
          <mxGeometry x="140" y="680" width="40" height="80" as="geometry" />
        </mxCell>
        <mxCell id="rel_act" value="kế thừa" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;dashed=1;strokeColor=#0F172A;" edge="1" parent="1" source="act_manager" target="act_cashier">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- Use cases -->
        <mxCell id="uc1" value="[UC01] Đăng nhập hệ thống" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="50" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="uc2" value="[UC02] Đăng xuất &amp; Thoát" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#64748B;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="140" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="uc3" value="[UC03] Bán hàng tại quầy (POS)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#16A34A;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="90" y="240" width="240" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc4" value="[UC04] Quản lý khách hàng" style="ellipse;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#16A34A;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="350" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="uc5" value="[UC05] Quản lý mẫu giày &amp; SKU" style="ellipse;whiteSpace=wrap;html=1;fillColor=#EDE9FE;strokeColor=#7C3AED;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="470" width="240" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc6" value="[UC06] Quản lý nhân sự" style="ellipse;whiteSpace=wrap;html=1;fillColor=#EDE9FE;strokeColor=#7C3AED;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="580" width="240" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc7" value="[UC07] Báo cáo doanh thu" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;" vertex="1" parent="box">
          <mxGeometry x="100" y="690" width="240" height="70" as="geometry" />
        </mxCell>
        <!-- Sub use cases -->
        <mxCell id="uc3_1" value="[UC03.1] Tra cứu tồn kho" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F0FDFA;strokeColor=#0D9488;" vertex="1" parent="box">
          <mxGeometry x="500" y="180" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="uc3_2" value="[UC03.2] Trừ tồn kho &amp; Thanh toán ACID" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F0FDFA;strokeColor=#0D9488;" vertex="1" parent="box">
          <mxGeometry x="500" y="270" width="240" height="65" as="geometry" />
        </mxCell>
        <mxCell id="uc3_3" value="[UC03.3] Tích điểm thành viên" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F0FDFA;strokeColor=#0D9488;" vertex="1" parent="box">
          <mxGeometry x="500" y="360" width="220" height="60" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open('SoDoUseCase_QuanLyBanGiay.drawio', 'w', encoding='utf-8') as f:
        f.write(uc_drawio)
    print(" [PASS] Đã tạo SoDoUseCase_QuanLyBanGiay.drawio")

    # 2. SoDoSequence_QuanLyBanGiay.drawio
    seq_drawio = """<?xml version='1.0' encoding='utf-8'?>
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="Seq_Checkout" name="SoDoSequence_QuanLyBanGiay">
    <mxGraphModel dx="1422" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1250" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Lifelines -->
        <mxCell id="ll_cashier" value="Thu ngân" style="shape=umlLifeline;participant=umlActor;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;verticalAlign=top;spacingTop=36;outlineConnect=0;" vertex="1" parent="1">
          <mxGeometry x="140" y="80" width="40" height="800" as="geometry" />
        </mxCell>
        <mxCell id="ll_gui" value="BanHang_GUI" style="shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;verticalAlign=top;spacingTop=36;outlineConnect=0;fillColor=#E0F2FE;strokeColor=#0284C7;" vertex="1" parent="1">
          <mxGeometry x="400" y="80" width="120" height="800" as="geometry" />
        </mxCell>
        <mxCell id="ll_dao" value="HoaDon_DAO" style="shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;verticalAlign=top;spacingTop=36;outlineConnect=0;fillColor=#EDE9FE;strokeColor=#7C3AED;" vertex="1" parent="1">
          <mxGeometry x="750" y="80" width="120" height="800" as="geometry" />
        </mxCell>
        <mxCell id="ll_db" value="SQL Server DB" style="shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;verticalAlign=top;spacingTop=36;outlineConnect=0;fillColor=#FCE7F3;strokeColor=#DB2777;" vertex="1" parent="1">
          <mxGeometry x="1350" y="80" width="120" height="800" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open('SoDoSequence_QuanLyBanGiay.drawio', 'w', encoding='utf-8') as f:
        f.write(seq_drawio)
    print(" [PASS] Đã tạo SoDoSequence_QuanLyBanGiay.drawio")

    # 3. SoDoKienTruc_QuanLyBanGiay.drawio
    arch_drawio = """<?xml version='1.0' encoding='utf-8'?>
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="Arch_3Tier" name="SoDoKienTruc_QuanLyBanGiay">
    <mxGraphModel dx="1422" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="tier1" value="TẦNG TRÌNH DIỄN (GUI - JAVA SWING)" style="swimlane;startSize=30;fillColor=#F8FAFC;strokeColor=#0284C7;fontStyle=1;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="80" width="1440" height="240" as="geometry" />
        </mxCell>
        <mxCell id="tier2" value="TẦNG TRUY CẬP DỮ LIỆU &amp; THỰC THỂ (DAO &amp; ENTITY)" style="swimlane;startSize=30;fillColor=#F8FAFC;strokeColor=#7C3AED;fontStyle=1;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="380" width="1440" height="250" as="geometry" />
        </mxCell>
        <mxCell id="tier3" value="TẦNG CƠ SỞ DỮ LIỆU (MICROSOFT SQL SERVER)" style="swimlane;startSize=30;fillColor=#F8FAFC;strokeColor=#BE185D;fontStyle=1;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="690" width="1440" height="220" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open('SoDoKienTruc_QuanLyBanGiay.drawio', 'w', encoding='utf-8') as f:
        f.write(arch_drawio)
    print(" [PASS] Đã tạo SoDoKienTruc_QuanLyBanGiay.drawio")


if __name__ == '__main__':
    generate_usecase_diagram()
    generate_sequence_diagram()
    generate_architecture_diagram()
    generate_drawio_source_files()
    print("=== TẤT CẢ 3 SƠ ĐỒ PHÂN TÍCH ĐÃ ĐƯỢC TẠO THÀNH CÔNG ===")

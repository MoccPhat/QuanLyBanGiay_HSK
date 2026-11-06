import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Setup clean crisp figure
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
ax.set_xlim(0, 1500)
ax.set_ylim(0, 1150)
ax.axis('off')

# Background
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Helper to draw UML Class with guaranteed text padding
def draw_class(x, y, w, title, attrs, methods, is_abstract=False):
    header_h = 44 if is_abstract else 34
    line_h = 19
    pad = 14
    
    attr_lines = attrs.strip().split('\n')
    meth_lines = methods.strip().split('\n')
    
    attr_h = len(attr_lines) * line_h + pad
    meth_h = len(meth_lines) * line_h + pad
    total_h = header_h + attr_h + 1 + meth_h
    
    # Outer box
    rect = patches.Rectangle((x, y), w, total_h, linewidth=1.5, edgecolor='#000000', facecolor='#ffffff', zorder=2)
    ax.add_patch(rect)
    
    # Title box
    title_rect = patches.Rectangle((x, y + total_h - header_h), w, header_h, linewidth=1.2, edgecolor='#000000', facecolor='#f8f9fa', zorder=3)
    ax.add_patch(title_rect)
    
    if is_abstract:
        ax.text(x + w/2, y + total_h - 14, "<<abstract>>", ha='center', va='center', fontsize=9.5, style='italic', color='#000000', zorder=4)
        ax.text(x + w/2, y + total_h - 30, title, ha='center', va='center', fontsize=12, fontweight='bold', color='#000000', zorder=4)
    else:
        ax.text(x + w/2, y + total_h - header_h/2, title, ha='center', va='center', fontsize=12, fontweight='bold', color='#000000', zorder=4)
        
    # Text attributes
    attr_start_y = y + total_h - header_h - 15
    for i, line in enumerate(attr_lines):
        ax.text(x + 12, attr_start_y - i * line_h, line, ha='left', va='center', fontsize=9.5, family='monospace', color='#000000', zorder=4)
        
    # Divider line
    div_y = y + meth_h + 1
    ax.plot([x, x + w], [div_y, div_y], color='#000000', linewidth=1.0, zorder=3)
    
    # Text methods
    meth_start_y = div_y - 15
    for i, line in enumerate(meth_lines):
        ax.text(x + 12, meth_start_y - i * line_h, line, ha='left', va='center', fontsize=9.5, family='monospace', color='#000000', zorder=4)
        
    return total_h

# --- VẼ 7 CLASS VỚI BỐ CỤC 3 CỘT KHÔNG BAO GIỜ BỊ CẮT CHÉO DÂY ---
# CỘT 1 (BÊN TRÁI): NGUOI (TRÊN) -> NHANVIEN & KHACHHANG (GIỮA) -> HOADON (DƯỚI)
# 1. Nguoi (Abstract)
h_ng = draw_class(
    x=210, y=810, w=330,
    title='Nguoi',
    attrs=(
        '- hoTen : String\n'
        '- soDienThoai : String\n'
        '- ngaySinh : LocalDate\n'
        '- gioiTinh : boolean\n'
        '- diaChi : String\n'
        '- email : String'
    ),
    methods=(
        '+ Nguoi()\n'
        '+ getHoTen() : String\n'
        '+ getSoDienThoai() : String\n'
        '+ {abstract} getThongTin() : String'
    ),
    is_abstract=True
)

# 2. NhanVien
h_nv = draw_class(
    x=50, y=490, w=290,
    title='NhanVien',
    attrs=(
        '- maNhanVien : String\n'
        '- chucVu : String\n'
        '- luongCoBan : double\n'
        '- caLamViec : String\n'
        '- trangThai : boolean'
    ),
    methods=(
        '+ NhanVien()\n'
        '+ tinhLuong() : double\n'
        '+ isQuanLy() : boolean\n'
        '+ getThongTin() : String'
    )
)

# 3. KhachHang
h_kh = draw_class(
    x=410, y=520, w=290,
    title='KhachHang',
    attrs=(
        '- maKhachHang : String\n'
        '- diemTichLuy : int\n'
        '- hangThanhVien : String'
    ),
    methods=(
        '+ KhachHang()\n'
        '+ tinhChietKhau() : double\n'
        '+ congDiem(diem : int) : void\n'
        '+ getThongTin() : String'
    )
)

# 4. HoaDon
h_hd = draw_class(
    x=190, y=110, w=330,
    title='HoaDon',
    attrs=(
        '- maHoaDon : String\n'
        '- ngayLap : LocalDateTime\n'
        '- tongTien : double\n'
        '- phuongThucTT : String\n'
        '- tienKhachDua : double\n'
        '- tienThua : double'
    ),
    methods=(
        '+ HoaDon()\n'
        '+ tinhTongTien() : double\n'
        '+ tinhTienThua() : double\n'
        '+ inHoaDon() : void'
    )
)

# CỘT 2 (GIỮA DƯỚI): CHI TIẾT HÓA ĐƠN
# 5. ChiTietHoaDon
h_cthd = draw_class(
    x=640, y=170, w=270,
    title='ChiTietHoaDon',
    attrs=(
        '- soLuong : int\n'
        '- donGia : double\n'
        '- giamGia : double\n'
        '- thanhTien : double'
    ),
    methods=(
        '+ ChiTietHoaDon()\n'
        '+ tinhThanhTien() : double'
    )
)

# CỘT 3 (BÊN PHẢI): CHI TIẾT GIÀY (DƯỚI) VÀ SẢN PHẨM (TRÊN)
# 6. ChiTietGiay
h_ctg = draw_class(
    x=1050, y=140, w=320,
    title='ChiTietGiay',
    attrs=(
        '- maChiTietGiay : String\n'
        '- kichThuoc : int\n'
        '- mauSac : String\n'
        '- soLuongTon : int\n'
        '- hinhAnh : String'
    ),
    methods=(
        '+ ChiTietGiay()\n'
        '+ kiemTraTonKho(sl : int) : boolean\n'
        '+ giamTonKho(sl : int) : void\n'
        '+ tangTonKho(sl : int) : void'
    )
)

# 7. SanPham
h_sp = draw_class(
    x=1050, y=510, w=320,
    title='SanPham',
    attrs=(
        '- maSanPham : String\n'
        '- tenSanPham : String\n'
        '- loaiGiay : String\n'
        '- thuongHieu : String\n'
        '- giaNhap : double\n'
        '- giaBan : double\n'
        '- chatLieu : String'
    ),
    methods=(
        '+ SanPham()\n'
        '+ getGiaBan() : double\n'
        '+ capNhatGia(giaMoi : double) : void\n'
        '+ toString() : String'
    )
)

# --- CÁC ĐƯỜNG NỐI CHUẨN UML ĐẸP MẮT, KHÔNG CHỒNG CHÉO ---
# 1. Kế thừa: NhanVien (top=710) -> Nguoi (bottom=810)
ax.plot([195, 195, 300, 300], [490 + h_nv, 760, 760, 810], color='#000000', linewidth=1.5, zorder=1)
tri1 = patches.Polygon([[293, 796], [307, 796], [300, 810]], closed=True, edgecolor='#000000', facecolor='#ffffff', linewidth=1.5, zorder=5)
ax.add_patch(tri1)
ax.text(235, 768, "extends", fontsize=9.5, style='italic', ha='center', va='bottom', color='#000000')

# 2. Kế thừa: KhachHang (top=710) -> Nguoi (bottom=810)
ax.plot([555, 555, 450, 450], [520 + h_kh, 760, 760, 810], color='#000000', linewidth=1.5, zorder=1)
tri2 = patches.Polygon([[443, 796], [457, 796], [450, 810]], closed=True, edgecolor='#000000', facecolor='#ffffff', linewidth=1.5, zorder=5)
ax.add_patch(tri2)
ax.text(515, 768, "extends", fontsize=9.5, style='italic', ha='center', va='bottom', color='#000000')

# 3. Liên kết: NhanVien (bottom=490) -> HoaDon (top=110+h_hd=356)
ax.plot([195, 195, 270, 270], [490, 410, 410, 110 + h_hd], color='#000000', linewidth=1.5, zorder=1)
ax.text(180, 470, "1", fontsize=9.5, fontweight='bold', ha='right')
ax.text(255, 110 + h_hd + 15, "0..*", fontsize=9.5, fontweight='bold', ha='right')
ax.text(230, 416, "lập", fontsize=9, style='italic', ha='center', va='bottom')

# 4. Liên kết: KhachHang (bottom=520) -> HoaDon (top=110+h_hd=356)
ax.plot([555, 555, 440, 440], [520, 410, 410, 110 + h_hd], color='#000000', linewidth=1.5, zorder=1)
ax.text(570, 500, "0..1", fontsize=9.5, fontweight='bold', ha='left')
ax.text(455, 110 + h_hd + 15, "0..*", fontsize=9.5, fontweight='bold', ha='left')
ax.text(500, 416, "mua", fontsize=9, style='italic', ha='center', va='bottom')

# 5. Tổng thành (Composition): HoaDon -> ChiTietHoaDon (Đường ngang cực đẹp)
y_conn_hd = 240
ax.plot([190 + 330, 640], [y_conn_hd, y_conn_hd], color='#000000', linewidth=1.5, zorder=1)
# Black diamond at (520, y_conn_hd)
dia1 = patches.Polygon([[520, y_conn_hd], [530, y_conn_hd + 6], [540, y_conn_hd], [530, y_conn_hd - 6]], closed=True, edgecolor='#000000', facecolor='#000000', zorder=5)
ax.add_patch(dia1)
ax.text(548, y_conn_hd + 6, "1", fontsize=9.5, fontweight='bold')
ax.text(620, y_conn_hd + 6, "1..*", fontsize=9.5, fontweight='bold')
ax.text(580, y_conn_hd - 16, "chứa", fontsize=9, style='italic', ha='center')

# 6. Liên kết: ChiTietHoaDon -> ChiTietGiay (Đường ngang cực đẹp)
y_conn_ct = 240
ax.plot([640 + 270, 1050], [y_conn_ct, y_conn_ct], color='#000000', linewidth=1.5, zorder=1)
ax.text(925, y_conn_ct + 6, "0..*", fontsize=9.5, fontweight='bold')
ax.text(1030, y_conn_ct + 6, "1", fontsize=9.5, fontweight='bold')
ax.text(980, y_conn_ct - 16, "bán", fontsize=9, style='italic', ha='center')

# 7. Tổng thành (Composition): SanPham -> ChiTietGiay (Đường dọc cực đẹp)
x_conn_sp = 1210
ax.plot([x_conn_sp, x_conn_sp], [510, 140 + h_ctg], color='#000000', linewidth=1.5, zorder=1)
# Black diamond at (1210, 510)
dia2 = patches.Polygon([[x_conn_sp, 510], [x_conn_sp + 6, 500], [x_conn_sp, 490], [x_conn_sp - 6, 500]], closed=True, edgecolor='#000000', facecolor='#000000', zorder=5)
ax.add_patch(dia2)
ax.text(x_conn_sp + 12, 480, "1", fontsize=9.5, fontweight='bold')
ax.text(x_conn_sp + 12, 140 + h_ctg + 20, "1..*", fontsize=9.5, fontweight='bold')
ax.text(x_conn_sp - 12, 420, "gồm", fontsize=9, style='italic', ha='right', va='center')

# --- TIÊU ĐỀ RÕ RÀNG, KHÔNG VA CHẠM ---
ax.text(750, 1110, "SƠ ĐỒ LỚP THỰC THỂ HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)", ha='center', va='center', fontsize=15, fontweight='bold', color='#000000')
ax.text(750, 1078, "HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG", ha='center', va='center', fontsize=11, color='#444444')

plt.tight_layout()
plt.savefig(r'e:\Project_HSK\SoDoLop_QuanLyBanGiay.png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
plt.savefig(r'e:\Project_HSK\diagram_class_shoe.png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
print("Successfully generated balanced & clean OOP PNG diagram without any legend box!")

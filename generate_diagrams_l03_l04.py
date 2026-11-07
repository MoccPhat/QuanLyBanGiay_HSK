"""
Script: generate_diagrams_l03_l04.py
Mục đích:
  - Vẽ lại ERD 6 bảng CSDL chuẩn SQL Server (L03) -> diagram_erd_shoe.png
  - Vẽ lại Sơ đồ lớp 7 lớp OOP chuẩn src/entity (L04) -> SoDoLop_QuanLyBanGiay.png, diagram_class_shoe.png
  - Sinh đồng bộ 2 file .drawio: SoDoERD_QuanLyBanGiay.drawio và SoDoLop_QuanLyBanGiay.drawio
  - Độ phân giải >= 1600px width (300 DPI), font rõ nét, chuẩn UML/ERD, không chồng chéo, không cắt chữ.
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

# Ensure Arial or Segoe UI font
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'


# ==============================================================================
# PHẦN 1: VẼ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM - 7 LỚP)
# ==============================================================================

def generate_oop_class_diagram():
    print(">>> Đang vẽ Sơ đồ lớp thực thể OOP (7 lớp)...")
    fig, ax = plt.subplots(figsize=(19, 14), dpi=300)
    ax.set_xlim(0, 1650)
    ax.set_ylim(0, 1300)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Helper vẽ box UML Class
    def draw_uml_class(x, y, w, title, attrs, methods, is_abstract=False, header_bg='#F1F5F9', border_color='#0F172A'):
        header_h = 44 if is_abstract else 34
        line_h = 18
        pad_top = 10
        pad_bot = 10
        
        attr_lines = [l for l in attrs.strip().split('\n') if l.strip()]
        meth_lines = [l for l in methods.strip().split('\n') if l.strip()]
        
        attr_h = len(attr_lines) * line_h + pad_top + pad_bot
        meth_h = len(meth_lines) * line_h + pad_top + pad_bot
        total_h = header_h + attr_h + meth_h
        
        # Shadow box for modern look
        shadow = patches.Rectangle((x + 4, y - 4), w, total_h, facecolor='#E2E8F0', edgecolor='none', zorder=1)
        ax.add_patch(shadow)

        # Main box
        rect = patches.Rectangle((x, y), w, total_h, linewidth=1.4, edgecolor=border_color, facecolor='#FFFFFF', zorder=2)
        ax.add_patch(rect)
        
        # Header rect
        hdr_rect = patches.Rectangle((x, y + total_h - header_h), w, header_h, linewidth=1.4, 
                                     edgecolor=border_color, facecolor=header_bg, zorder=3)
        ax.add_patch(hdr_rect)
        
        if is_abstract:
            ax.text(x + w/2, y + total_h - 13, "<<abstract>>", ha='center', va='center', 
                    fontsize=9.5, style='italic', color='#1E293B', fontweight='bold', zorder=4)
            ax.text(x + w/2, y + total_h - 29, title, ha='center', va='center', 
                    fontsize=12, fontweight='bold', color='#0F172A', zorder=4)
        else:
            ax.text(x + w/2, y + total_h - header_h/2, title, ha='center', va='center', 
                    fontsize=12, fontweight='bold', color='#0F172A', zorder=4)
            
        # Divider 1 (Header -> Attr)
        ax.plot([x, x + w], [y + total_h - header_h, y + total_h - header_h], color=border_color, linewidth=1.2, zorder=3)

        # Draw Attributes
        attr_y = y + total_h - header_h - pad_top - 7
        for line in attr_lines:
            ax.text(x + 12, attr_y, line, ha='left', va='center', fontsize=9.2, family='monospace', color='#1E293B', zorder=4)
            attr_y -= line_h

        # Divider 2 (Attr -> Meth)
        div2_y = y + meth_h
        ax.plot([x, x + w], [div2_y, div2_y], color=border_color, linewidth=1.0, zorder=3)

        # Draw Methods
        meth_y = div2_y - pad_top - 7
        for line in meth_lines:
            ax.text(x + 12, meth_y, line, ha='left', va='center', fontsize=9.2, family='monospace', color='#0369A1', zorder=4)
            meth_y -= line_h
            
        return total_h

    # --- ĐẶT TỌA ĐỘ VÀ VẼ 7 CLASS ---
    # 1. Nguoi (Abstract) - Giữa Trên
    h_ng = draw_uml_class(
        x=240, y=860, w=350,
        title='Nguoi',
        attrs=(
            '# hoTen : String\n'
            '# soDienThoai : String\n'
            '# ngaySinh : LocalDate\n'
            '# gioiTinh : boolean\n'
            '# diaChi : String\n'
            '# email : String'
        ),
        methods=(
            '+ Nguoi()\n'
            '+ getHoTen() : String\n'
            '+ getSoDienThoai() : String\n'
            '+ {abstract} getThongTin() : String\n'
            '+ toString() : String'
        ),
        is_abstract=True,
        header_bg='#FEF3C7',
        border_color='#B45309'
    )

    # 2. NhanVien (Bên trái giữa)
    h_nv = draw_uml_class(
        x=40, y=490, w=340,
        title='NhanVien',
        attrs=(
            '- maNhanVien : String\n'
            '- chucVu : String\n'
            '- luongCoBan : double\n'
            '- caLamViec : String\n'
            '- matKhau : String\n'
            '- trangThai : boolean'
        ),
        methods=(
            '+ NhanVien()\n'
            '+ isQuanLy() : boolean\n'
            '+ tinhLuong() : double\n'
            '+ getThongTin() : String\n'
            '+ equals(obj : Object) : boolean\n'
            '+ hashCode() : int'
        ),
        header_bg='#E0F2FE',
        border_color='#0284C7'
    )

    # 3. KhachHang (Giữa bên phải của NhanVien)
    h_kh = draw_uml_class(
        x=430, y=510, w=340,
        title='KhachHang',
        attrs=(
            '- maKhachHang : String\n'
            '- diemTichLuy : int\n'
            '- hangThanhVien : String'
        ),
        methods=(
            '+ KhachHang()\n'
            '+ congDiem(diem : int) : void\n'
            '+ capNhatHang() : void\n'
            '+ tinhChietKhau() : double\n'
            '+ getThongTin() : String\n'
            '+ equals(obj : Object) : boolean\n'
            '+ hashCode() : int'
        ),
        header_bg='#DCFCE7',
        border_color='#16A34A'
    )

    # 4. HoaDon (Dưới cùng bên trái)
    h_hd = draw_uml_class(
        x=40, y=30, w=440,
        title='HoaDon',
        attrs=(
            '- maHoaDon : String\n'
            '- ngayLap : LocalDateTime\n'
            '- nhanVien : NhanVien\n'
            '- khachHang : KhachHang\n'
            '- tongTienHang : double\n'
            '- chietKhau : double\n'
            '- diemSuDung : int\n'
            '- tienGiamDiem : double\n'
            '- tongTien : double\n'
            '- phuongThucTT : String\n'
            '- tienKhachDua : double\n'
            '- tienThua : double\n'
            '- diemCong : int\n'
            '- danhSachChiTiet : List<ChiTietHoaDon>'
        ),
        methods=(
            '+ HoaDon()\n'
            '+ themChiTiet(ct : ChiTietHoaDon) : void\n'
            '+ tinhTongTien() : double\n'
            '+ tinhTienThua() : double'
        ),
        header_bg='#EDE9FE',
        border_color='#7C3AED'
    )

    # 5. ChiTietHoaDon (Dưới cùng ở giữa)
    h_cthd = draw_uml_class(
        x=570, y=110, w=340,
        title='ChiTietHoaDon',
        attrs=(
            '- hoaDon : HoaDon\n'
            '- chiTietGiay : ChiTietGiay\n'
            '- soLuong : int\n'
            '- donGia : double\n'
            '- giamGia : double\n'
            '- thanhTien : double'
        ),
        methods=(
            '+ ChiTietHoaDon()\n'
            '+ tinhThanhTien() : double'
        ),
        header_bg='#FCE7F3',
        border_color='#DB2777'
    )

    # 6. SanPham (Cột phải trên)
    h_sp = draw_uml_class(
        x=1120, y=660, w=380,
        title='SanPham',
        attrs=(
            '- maSanPham : String\n'
            '- tenSanPham : String\n'
            '- loaiGiay : String\n'
            '- thuongHieu : String\n'
            '- giaNhap : double\n'
            '- giaBan : double\n'
            '- chatLieu : String\n'
            '- trangThai : boolean'
        ),
        methods=(
            '+ SanPham()\n'
            '+ getMaSanPham() : String\n'
            '+ getGiaBan() : double\n'
            '+ getTrangThai() : boolean\n'
            '+ equals(obj : Object) : boolean\n'
            '+ hashCode() : int\n'
            '+ toString() : String'
        ),
        header_bg='#E0E7FF',
        border_color='#4F46E5'
    )

    # 7. ChiTietGiay (Cột phải dưới)
    h_ctg = draw_uml_class(
        x=1120, y=170, w=380,
        title='ChiTietGiay',
        attrs=(
            '- maChiTietGiay : String\n'
            '- sanPham : SanPham\n'
            '- kichThuoc : int\n'
            '- mauSac : String\n'
            '- soLuongTon : int\n'
            '- hinhAnh : String'
        ),
        methods=(
            '+ ChiTietGiay()\n'
            '+ kiemTraTonKho(sl : int) : boolean\n'
            '+ giamTonKho(sl : int) : void\n'
            '+ tangTonKho(sl : int) : void\n'
            '+ toString() : String'
        ),
        header_bg='#FFEDD5',
        border_color='#EA580C'
    )

    # --- CÁC ĐƯỜNG NỐI QUAN HỆ UML ---
    # 1. Kế thừa: NhanVien (top) -> Nguoi (bottom)
    top_nv = 490 + h_nv
    ax.plot([210, 210, 330, 330], [top_nv, 815, 815, 860], color='#0F172A', linewidth=1.5, zorder=3)
    tri1 = patches.Polygon([[322, 846], [338, 846], [330, 860]], closed=True, 
                           edgecolor='#0F172A', facecolor='#FFFFFF', linewidth=1.5, zorder=5)
    ax.add_patch(tri1)
    ax.text(260, 822, "extends", fontsize=9.5, style='italic', color='#475569', ha='center')

    # 2. Kế thừa: KhachHang (top) -> Nguoi (bottom)
    top_kh = 510 + h_kh
    ax.plot([600, 600, 480, 480], [top_kh, 815, 815, 860], color='#0F172A', linewidth=1.5, zorder=3)
    tri2 = patches.Polygon([[472, 846], [488, 846], [480, 860]], closed=True, 
                           edgecolor='#0F172A', facecolor='#FFFFFF', linewidth=1.5, zorder=5)
    ax.add_patch(tri2)
    ax.text(540, 822, "extends", fontsize=9.5, style='italic', color='#475569', ha='center')

    # 3. Liên kết: NhanVien (1) -> HoaDon (0..*)
    top_hd = 30 + h_hd
    ax.plot([140, 140], [490, top_hd], color='#0F172A', linewidth=1.5, zorder=3)
    ax.text(152, 470, "1", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(152, top_hd + 12, "0..*", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(130, (490 + top_hd)/2, "lập [nhanVien]", fontsize=9, style='italic', color='#475569', ha='right')

    # 4. Liên kết: KhachHang (0..1) -> HoaDon (0..*)
    ax.plot([530, 530, 360, 360], [510, 460, 460, top_hd], color='#0F172A', linewidth=1.5, zorder=3)
    ax.text(542, 490, "0..1", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(372, top_hd + 12, "0..*", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(445, 468, "mua [khachHang]", fontsize=9, style='italic', color='#475569', ha='center')

    # 5. Tổng thành (Composition): HoaDon (1) ◆── (1..*) ChiTietHoaDon
    y_hd_ct = 220
    ax.plot([480, 570], [y_hd_ct, y_hd_ct], color='#0F172A', linewidth=1.6, zorder=3)
    dia_hd = patches.Polygon([[480, y_hd_ct], [492, y_hd_ct + 7], [504, y_hd_ct], [492, y_hd_ct - 7]], 
                             closed=True, edgecolor='#0F172A', facecolor='#0F172A', zorder=5)
    ax.add_patch(dia_hd)
    ax.text(510, y_hd_ct + 8, "1", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(545, y_hd_ct + 8, "1..*", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(525, y_hd_ct - 18, "chứa", fontsize=9, style='italic', color='#475569', ha='center')

    # 6. Liên kết: ChiTietHoaDon (0..*) ── (1) ChiTietGiay
    ax.plot([910, 1120], [y_hd_ct, y_hd_ct], color='#0F172A', linewidth=1.5, zorder=3)
    ax.text(925, y_hd_ct + 8, "0..*", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(1095, y_hd_ct + 8, "1", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(1015, y_hd_ct - 18, "bán [chiTietGiay]", fontsize=9, style='italic', color='#475569', ha='center')

    # 7. Tổng thành (Composition): SanPham (1) ◆── (1..*) ChiTietGiay
    x_sp_ctg = 1310
    top_ctg = 170 + h_ctg
    ax.plot([x_sp_ctg, x_sp_ctg], [660, top_ctg], color='#0F172A', linewidth=1.6, zorder=3)
    dia_sp = patches.Polygon([[x_sp_ctg, 660], [x_sp_ctg + 7, 648], [x_sp_ctg, 636], [x_sp_ctg - 7, 648]], 
                             closed=True, edgecolor='#0F172A', facecolor='#0F172A', zorder=5)
    ax.add_patch(dia_sp)
    ax.text(x_sp_ctg + 12, 625, "1", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(x_sp_ctg + 12, top_ctg + 12, "1..*", fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(x_sp_ctg - 12, (660 + top_ctg)/2, "gồm [sanPham]", fontsize=9, style='italic', color='#475569', ha='right', va='center')

    # Header Title Banner (Có khoảng cách an toàn rộng rãi phía trên)
    ax.text(825, 1260, "SƠ ĐỒ LỚP THỰC THỂ HƯỚNG ĐỐI TƯỢNG (OOP ENTITY CLASS DIAGRAM)", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(825, 1228, "HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG (STEPUP POS SYSTEM)", 
            ha='center', va='center', fontsize=11, color='#475569')

    plt.tight_layout()
    out1 = os.path.join(os.getcwd(), 'SoDoLop_QuanLyBanGiay.png')
    out2 = os.path.join(os.getcwd(), 'diagram_class_shoe.png')
    plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f" [PASS] Đã tạo thành công Sơ đồ lớp: {out1} & {out2}")


# ==============================================================================
# PHẦN 2: VẼ SƠ ĐỒ CƠ SỞ DỮ LIỆU QUAN HỆ (DATABASE ERD - 6 BẢNG)
# ==============================================================================

def generate_erd_diagram():
    print(">>> Đang vẽ Sơ đồ cơ sở dữ liệu quan hệ ERD (6 bảng)...")
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 1750)
    ax.set_ylim(0, 1300)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Helper vẽ Table Box cho ERD
    def draw_erd_table(x, y, w, table_name, pk_cols, fk_cols, uq_cols, normal_cols, header_color='#1E40AF'):
        header_h = 36
        line_h = 20
        pad_top = 10
        pad_bot = 10

        all_rows = []
        for c in pk_cols:
            all_rows.append(("[PK]", c, '#B91C1C'))
        for c in fk_cols:
            all_rows.append(("[FK]", c, '#2563EB'))
        for c in uq_cols:
            all_rows.append(("[UQ]", c, '#0D9488'))
        for c in normal_cols:
            all_rows.append(("", c, '#334155'))

        body_h = len(all_rows) * line_h + pad_top + pad_bot
        total_h = header_h + body_h

        # Shadow box
        shadow = patches.Rectangle((x + 4, y - 4), w, total_h, facecolor='#E2E8F0', edgecolor='none', zorder=1)
        ax.add_patch(shadow)

        # Outer border
        rect = patches.Rectangle((x, y), w, total_h, linewidth=1.4, edgecolor='#1E293B', facecolor='#FFFFFF', zorder=2)
        ax.add_patch(rect)

        # Header box
        hdr_rect = patches.Rectangle((x, y + total_h - header_h), w, header_h, linewidth=1.4, 
                                     edgecolor='#1E293B', facecolor=header_color, zorder=3)
        ax.add_patch(hdr_rect)
        ax.text(x + w/2, y + total_h - header_h/2, table_name, ha='center', va='center', 
                color='#FFFFFF', fontweight='bold', fontsize=12, zorder=4)

        # Divider line
        ax.plot([x, x + w], [y + total_h - header_h, y + total_h - header_h], color='#1E293B', linewidth=1.2, zorder=3)

        # Render Columns
        row_y = y + total_h - header_h - pad_top - 8
        for tag, col_text, col_color in all_rows:
            if tag:
                ax.text(x + 10, row_y, tag, ha='left', va='center', fontsize=8.8, fontweight='bold', color=col_color, zorder=4)
                ax.text(x + 48, row_y, col_text, ha='left', va='center', fontsize=9.0, family='monospace', color='#0F172A', zorder=4)
            else:
                ax.text(x + 48, row_y, col_text, ha='left', va='center', fontsize=9.0, family='monospace', color=col_color, zorder=4)
            row_y -= line_h

        return total_h

    # --- BỐ CỤC 3 CỘT KHÔNG BAO GIỜ CHỒNG CHÉO ---
    # CỘT 1 (TRÁI): NhanVien (Trên) & KhachHang (Dưới)
    h_nv = draw_erd_table(
        x=50, y=600, w=380,
        table_name='NhanVien',
        pk_cols=['maNhanVien VARCHAR(10)'],
        fk_cols=[],
        uq_cols=['soDienThoai VARCHAR(10)'],
        normal_cols=[
            'hoTen NVARCHAR(50)',
            'ngaySinh DATE',
            'gioiTinh BIT',
            'diaChi NVARCHAR(200)',
            'email VARCHAR(100)',
            'chucVu NVARCHAR(30)',
            'luongCoBan DECIMAL(18,0)',
            'caLamViec NVARCHAR(20)',
            'matKhau CHAR(64)',
            'trangThai BIT'
        ],
        header_color='#1E3A8A'
    )

    h_kh = draw_erd_table(
        x=50, y=160, w=380,
        table_name='KhachHang',
        pk_cols=['maKhachHang VARCHAR(10)'],
        fk_cols=[],
        uq_cols=['soDienThoai VARCHAR(10)'],
        normal_cols=[
            'hoTen NVARCHAR(50)',
            'ngaySinh DATE',
            'gioiTinh BIT',
            'diaChi NVARCHAR(200)',
            'email VARCHAR(100)',
            'diemTichLuy INT',
            'hangThanhVien NVARCHAR(20)'
        ],
        header_color='#047857'
    )

    # CỘT 2 (GIỮA): HoaDon (Trái giữa) & ChiTietHoaDon (Phải giữa)
    h_hd = draw_erd_table(
        x=520, y=360, w=430,
        table_name='HoaDon',
        pk_cols=['maHoaDon VARCHAR(10)'],
        fk_cols=[
            'maNhanVien VARCHAR(10)',
            'maKhachHang VARCHAR(10) (NULL)'
        ],
        uq_cols=[],
        normal_cols=[
            'ngayLap DATETIME',
            'tongTienHang DECIMAL(18,0)',
            'chietKhau DECIMAL(18,0)',
            'diemSuDung INT',
            'tienGiamDiem DECIMAL(18,0)',
            'tongTien DECIMAL(18,0)',
            'phuongThucTT NVARCHAR(30)',
            'tienKhachDua DECIMAL(18,0)',
            'tienThua DECIMAL(18,0)',
            'diemCong INT'
        ],
        header_color='#6D28D9'
    )

    h_cthd = draw_erd_table(
        x=1030, y=420, w=400,
        table_name='ChiTietHoaDon',
        pk_cols=[
            'maHoaDon VARCHAR(10)',
            'maChiTietGiay VARCHAR(10)'
        ],
        fk_cols=[],
        uq_cols=[],
        normal_cols=[
            'soLuong INT',
            'donGia DECIMAL(18,0)',
            'giamGia DECIMAL(18,0)',
            'thanhTien DECIMAL(18,0)'
        ],
        header_color='#BE185D'
    )

    # CỘT 3 (PHẢI): SanPham (Trên) & ChiTietGiay (Dưới)
    h_sp = draw_erd_table(
        x=1330, y=690, w=380,
        table_name='SanPham',
        pk_cols=['maSanPham VARCHAR(10)'],
        fk_cols=[],
        uq_cols=[],
        normal_cols=[
            'tenSanPham NVARCHAR(100)',
            'loaiGiay NVARCHAR(50)',
            'thuongHieu NVARCHAR(50)',
            'giaNhap DECIMAL(18,0)',
            'giaBan DECIMAL(18,0)',
            'chatLieu NVARCHAR(50)',
            'trangThai BIT'
        ],
        header_color='#2563EB'
    )

    h_ctg = draw_erd_table(
        x=1330, y=160, w=380,
        table_name='ChiTietGiay',
        pk_cols=['maChiTietGiay VARCHAR(10)'],
        fk_cols=['maSanPham VARCHAR(10)'],
        uq_cols=['(maSanPham, kichThuoc, mauSac)'],
        normal_cols=[
            'kichThuoc INT',
            'mauSac NVARCHAR(30)',
            'soLuongTon INT',
            'hinhAnh NVARCHAR(255)'
        ],
        header_color='#C2410C'
    )

    # Helper vẽ ký hiệu Crow's Foot
    def draw_crows_foot(x_end, y_end, direction='left', size=11):
        if direction == 'left':
            ax.plot([x_end, x_end + size], [y_end, y_end + size/1.5], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end, x_end + size], [y_end, y_end - size/1.5], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end + size, x_end + size], [y_end - size/1.5, y_end + size/1.5], color='#1E293B', lw=1.4, zorder=5)
        elif direction == 'right':
            ax.plot([x_end, x_end - size], [y_end, y_end + size/1.5], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end, x_end - size], [y_end, y_end - size/1.5], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end - size, x_end - size], [y_end - size/1.5, y_end + size/1.5], color='#1E293B', lw=1.4, zorder=5)
        elif direction == 'up':
            ax.plot([x_end, x_end - size/1.5], [y_end, y_end - size], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end, x_end + size/1.5], [y_end, y_end - size], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end - size/1.5, x_end + size/1.5], [y_end - size, y_end - size], color='#1E293B', lw=1.4, zorder=5)
        elif direction == 'down':
            ax.plot([x_end, x_end - size/1.5], [y_end, y_end + size], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end, x_end + size/1.5], [y_end, y_end + size], color='#1E293B', lw=1.4, zorder=5)
            ax.plot([x_end - size/1.5, x_end + size/1.5], [y_end + size, y_end + size], color='#1E293B', lw=1.4, zorder=5)

    # 1. NhanVien (1) ── (0..*) HoaDon [FK_HoaDon_NhanVien]
    y_nv_hd = 700
    ax.plot([430, 475, 475, 520], [y_nv_hd, y_nv_hd, 580, 580], color='#1E293B', linewidth=1.5, zorder=3)
    ax.plot([445, 445], [y_nv_hd - 8, y_nv_hd + 8], color='#1E293B', linewidth=1.8, zorder=5)
    draw_crows_foot(520, 580, direction='left', size=11)
    ax.text(450, y_nv_hd + 8, "1", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(500, 588, "0..*", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(475, 640, "FK_HoaDon_NhanVien", fontsize=8.5, style='italic', color='#334155', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", lw=0.8, alpha=0.9))

    # 2. KhachHang (0..1) ── (0..*) HoaDon [FK_HoaDon_KhachHang]
    y_kh_hd = 280
    ax.plot([430, 475, 475, 520], [y_kh_hd, y_kh_hd, 440, 440], color='#1E293B', linewidth=1.5, zorder=3)
    circle = patches.Circle((448, y_kh_hd), 4, facecolor='#FFFFFF', edgecolor='#1E293B', lw=1.3, zorder=5)
    ax.add_patch(circle)
    ax.plot([456, 456], [y_kh_hd - 7, y_kh_hd + 7], color='#1E293B', linewidth=1.5, zorder=5)
    draw_crows_foot(520, 440, direction='left', size=11)
    ax.text(438, y_kh_hd + 8, "0..1", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(500, 448, "0..*", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(475, 360, "FK_HoaDon_KhachHang", fontsize=8.5, style='italic', color='#334155', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", lw=0.8, alpha=0.9))

    # 3. HoaDon (1) ── (1..*) ChiTietHoaDon [FK_ChiTietHoaDon_HoaDon (ON DELETE CASCADE)]
    y_hd_cthd = 508
    ax.plot([950, 1030], [y_hd_cthd, y_hd_cthd], color='#1E293B', linewidth=1.6, zorder=3)
    ax.plot([965, 965], [y_hd_cthd - 8, y_hd_cthd + 8], color='#1E293B', linewidth=1.8, zorder=5)
    draw_crows_foot(1030, y_hd_cthd, direction='left', size=11)
    ax.text(970, y_hd_cthd + 8, "1", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(1005, y_hd_cthd + 8, "1..*", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(990, y_hd_cthd - 18, "CASCADE", fontsize=8.5, fontweight='bold', color='#B91C1C', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FEE2E2", ec="#F87171", lw=0.8))

    # 4. SanPham (1) ── (1..*) ChiTietGiay [FK_ChiTietGiay_SanPham]
    x_sp_ctg = 1520
    top_ctg = 160 + h_ctg
    ax.plot([x_sp_ctg, x_sp_ctg], [690, top_ctg], color='#1E293B', linewidth=1.6, zorder=3)
    ax.plot([x_sp_ctg - 8, x_sp_ctg + 8], [675, 675], color='#1E293B', linewidth=1.8, zorder=5)
    draw_crows_foot(x_sp_ctg, top_ctg, direction='down', size=11)
    ax.text(x_sp_ctg + 12, 665, "1", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(x_sp_ctg + 12, top_ctg + 15, "1..*", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(x_sp_ctg - 12, (690 + top_ctg)/2, "FK_ChiTietGiay_SanPham", fontsize=8.5, style='italic', color='#334155', ha='right', va='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", lw=0.8, alpha=0.9))

    # 5. ChiTietGiay (1) ── (0..*) ChiTietHoaDon [FK_ChiTietHoaDon_ChiTietGiay]
    y_ctg_cthd = 260
    ax.plot([1330, 1240, 1240], [y_ctg_cthd, y_ctg_cthd, 420], color='#1E293B', linewidth=1.5, zorder=3)
    ax.plot([1315, 1315], [y_ctg_cthd - 8, y_ctg_cthd + 8], color='#1E293B', linewidth=1.8, zorder=5)
    draw_crows_foot(1240, 420, direction='up', size=11)
    ax.text(1290, y_ctg_cthd + 8, "1", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(1252, 402, "0..*", fontsize=10, fontweight='bold', color='#1E293B')
    ax.text(1225, 340, "FK_ChiTietHoaDon_ChiTietGiay", fontsize=8.5, style='italic', color='#334155', ha='right', va='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", lw=0.8, alpha=0.9))

    # Header Title Banner (Có khoảng cách an toàn rộng rãi phía trên)
    ax.text(875, 1260, "SƠ ĐỒ CƠ SỞ DỮ LIỆU QUAN HỆ (DATABASE ERD - 6 BẢNG CHUẨN 3NF)", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(875, 1228, "MICROSOFT SQL SERVER - QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG", 
            ha='center', va='center', fontsize=11, color='#475569')

    # Legend at top
    leg_x, leg_y = 50, 1190
    ax.text(leg_x, leg_y, "[PK] Khóa chính", fontsize=9, fontweight='bold', color='#B91C1C')
    ax.text(leg_x + 130, leg_y, "[FK] Khóa ngoại", fontsize=9, fontweight='bold', color='#2563EB')
    ax.text(leg_x + 260, leg_y, "[UQ] Ràng buộc duy nhất", fontsize=9, fontweight='bold', color='#0D9488')
    ax.text(leg_x + 460, leg_y, "-|<- Bội số Crow's Foot (1 - N)", fontsize=9, style='italic', color='#1E293B')

    plt.tight_layout()
    out = os.path.join(os.getcwd(), 'diagram_erd_shoe.png')
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f" [PASS] Đã tạo thành công Sơ đồ ERD: {out}")


# ==============================================================================
# PHẦN 3: XUẤT CÁC FILE NGUỒN DRAW.IO TƯƠNG ỨNG
# ==============================================================================

def generate_drawio_files():
    print(">>> Đang cập nhật và sinh các file nguồn .drawio...")
    
    # 1. SoDoLop_QuanLyBanGiay.drawio (7 lớp OOP)
    drawio_oop_content = """<?xml version='1.0' encoding='utf-8'?>
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="ClassDiagram_ShoePOS_OOP" name="SoDoLop_OOP_QuanLyBanGiay">
    <mxGraphModel dx="1422" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1650" pageHeight="1300" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Nguoi (Abstract) -->
        <mxCell id="10" value="&amp;lt;&amp;lt;abstract&amp;gt;&amp;gt;&amp;#10;&amp;lt;b&amp;gt;Nguoi&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=36;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#B45309;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="240" y="50" width="350" height="260" as="geometry" />
        </mxCell>
        <mxCell id="10_attr" value="# hoTen : String&#10;# soDienThoai : String&#10;# ngaySinh : LocalDate&#10;# gioiTinh : boolean&#10;# diaChi : String&#10;# email : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="10">
          <mxGeometry y="36" width="350" height="120" as="geometry" />
        </mxCell>
        <mxCell id="10_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#B45309;" vertex="1" parent="10">
          <mxGeometry y="156" width="350" height="8" as="geometry" />
        </mxCell>
        <mxCell id="10_meth" value="+ Nguoi()&#10;+ getHoTen() : String&#10;+ getSoDienThoai() : String&#10;+ {abstract} getThongTin() : String&#10;+ toString() : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="10">
          <mxGeometry y="164" width="350" height="96" as="geometry" />
        </mxCell>

        <!-- NhanVien -->
        <mxCell id="20" value="&amp;lt;b&amp;gt;NhanVien&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#0284C7;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="40" y="380" width="340" height="260" as="geometry" />
        </mxCell>
        <mxCell id="20_attr" value="- maNhanVien : String&#10;- chucVu : String&#10;- luongCoBan : double&#10;- caLamViec : String&#10;- matKhau : String&#10;- trangThai : boolean" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="20">
          <mxGeometry y="28" width="340" height="114" as="geometry" />
        </mxCell>
        <mxCell id="20_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#0284C7;" vertex="1" parent="20">
          <mxGeometry y="142" width="340" height="8" as="geometry" />
        </mxCell>
        <mxCell id="20_meth" value="+ NhanVien()&#10;+ isQuanLy() : boolean&#10;+ tinhLuong() : double&#10;+ getThongTin() : String&#10;+ equals(obj : Object) : boolean&#10;+ hashCode() : int" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="20">
          <mxGeometry y="150" width="340" height="110" as="geometry" />
        </mxCell>

        <!-- KhachHang -->
        <mxCell id="30" value="&amp;lt;b&amp;gt;KhachHang&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#16A34A;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="430" y="380" width="340" height="235" as="geometry" />
        </mxCell>
        <mxCell id="30_attr" value="- maKhachHang : String&#10;- diemTichLuy : int&#10;- hangThanhVien : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="30">
          <mxGeometry y="28" width="340" height="66" as="geometry" />
        </mxCell>
        <mxCell id="30_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#16A34A;" vertex="1" parent="30">
          <mxGeometry y="94" width="340" height="8" as="geometry" />
        </mxCell>
        <mxCell id="30_meth" value="+ KhachHang()&#10;+ congDiem(diem : int) : void&#10;+ capNhatHang() : void&#10;+ tinhChietKhau() : double&#10;+ getThongTin() : String&#10;+ equals(obj : Object) : boolean&#10;+ hashCode() : int" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="30">
          <mxGeometry y="102" width="340" height="133" as="geometry" />
        </mxCell>

        <!-- HoaDon -->
        <mxCell id="40" value="&amp;lt;b&amp;gt;HoaDon&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#EDE9FE;strokeColor=#7C3AED;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="40" y="730" width="440" height="380" as="geometry" />
        </mxCell>
        <mxCell id="40_attr" value="- maHoaDon : String&#10;- ngayLap : LocalDateTime&#10;- nhanVien : NhanVien&#10;- khachHang : KhachHang&#10;- tongTienHang : double&#10;- chietKhau : double&#10;- diemSuDung : int&#10;- tienGiamDiem : double&#10;- tongTien : double&#10;- phuongThucTT : String&#10;- tienKhachDua : double&#10;- tienThua : double&#10;- diemCong : int&#10;- danhSachChiTiet : List&amp;lt;ChiTietHoaDon&amp;gt;" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="40">
          <mxGeometry y="28" width="440" height="260" as="geometry" />
        </mxCell>
        <mxCell id="40_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#7C3AED;" vertex="1" parent="40">
          <mxGeometry y="288" width="440" height="8" as="geometry" />
        </mxCell>
        <mxCell id="40_meth" value="+ HoaDon()&#10;+ themChiTiet(ct : ChiTietHoaDon) : void&#10;+ tinhTongTien() : double&#10;+ tinhTienThua() : double" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="40">
          <mxGeometry y="296" width="440" height="84" as="geometry" />
        </mxCell>

        <!-- ChiTietHoaDon -->
        <mxCell id="50" value="&amp;lt;b&amp;gt;ChiTietHoaDon&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#FCE7F3;strokeColor=#DB2777;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="570" y="810" width="340" height="210" as="geometry" />
        </mxCell>
        <mxCell id="50_attr" value="- hoaDon : HoaDon&#10;- chiTietGiay : ChiTietGiay&#10;- soLuong : int&#10;- donGia : double&#10;- giamGia : double&#10;- thanhTien : double" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="50">
          <mxGeometry y="28" width="340" height="120" as="geometry" />
        </mxCell>
        <mxCell id="50_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#DB2777;" vertex="1" parent="50">
          <mxGeometry y="148" width="340" height="8" as="geometry" />
        </mxCell>
        <mxCell id="50_meth" value="+ ChiTietHoaDon()&#10;+ tinhThanhTien() : double" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="50">
          <mxGeometry y="156" width="340" height="54" as="geometry" />
        </mxCell>

        <!-- SanPham -->
        <mxCell id="70" value="&amp;lt;b&amp;gt;SanPham&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#E0E7FF;strokeColor=#4F46E5;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1120" y="240" width="380" height="310" as="geometry" />
        </mxCell>
        <mxCell id="70_attr" value="- maSanPham : String&#10;- tenSanPham : String&#10;- loaiGiay : String&#10;- thuongHieu : String&#10;- giaNhap : double&#10;- giaBan : double&#10;- chatLieu : String&#10;- trangThai : boolean" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="70">
          <mxGeometry y="28" width="380" height="152" as="geometry" />
        </mxCell>
        <mxCell id="70_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#4F46E5;" vertex="1" parent="70">
          <mxGeometry y="180" width="380" height="8" as="geometry" />
        </mxCell>
        <mxCell id="70_meth" value="+ SanPham()&#10;+ getMaSanPham() : String&#10;+ getGiaBan() : double&#10;+ getTrangThai() : boolean&#10;+ equals(obj : Object) : boolean&#10;+ hashCode() : int&#10;+ toString() : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="70">
          <mxGeometry y="188" width="380" height="122" as="geometry" />
        </mxCell>

        <!-- ChiTietGiay -->
        <mxCell id="60" value="&amp;lt;b&amp;gt;ChiTietGiay&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#FFEDD5;strokeColor=#EA580C;fontColor=#0F172A;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1120" y="750" width="380" height="270" as="geometry" />
        </mxCell>
        <mxCell id="60_attr" value="- maChiTietGiay : String&#10;- sanPham : SanPham&#10;- kichThuoc : int&#10;- mauSac : String&#10;- soLuongTon : int&#10;- hinhAnh : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#1E293B;fontSize=11;fontFamily=monospace;" vertex="1" parent="60">
          <mxGeometry y="28" width="380" height="120" as="geometry" />
        </mxCell>
        <mxCell id="60_line" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#EA580C;" vertex="1" parent="60">
          <mxGeometry y="148" width="380" height="8" as="geometry" />
        </mxCell>
        <mxCell id="60_meth" value="+ ChiTietGiay()&#10;+ kiemTraTonKho(sl : int) : boolean&#10;+ giamTonKho(sl : int) : void&#10;+ tangTonKho(sl : int) : void&#10;+ toString() : String" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0369A1;fontSize=11;fontFamily=monospace;" vertex="1" parent="60">
          <mxGeometry y="156" width="380" height="114" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="80" value="extends" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.5;startArrow=none;endArrow=block;endFill=0;exitX=0.5;exitY=0;entryX=0.25;entryY=1;" edge="1" parent="1" source="20" target="10">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="81" value="extends" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.5;startArrow=none;endArrow=block;endFill=0;exitX=0.5;exitY=0;entryX=0.75;entryY=1;" edge="1" parent="1" source="30" target="10">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="82" value="1          lập           0..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.5;startArrow=none;endArrow=none;exitX=0.35;exitY=1;entryX=0.25;entryY=0;" edge="1" parent="1" source="20" target="40">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="83" value="0..1       mua           0..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.5;startArrow=none;endArrow=none;exitX=0.5;exitY=1;entryX=0.75;entryY=0;" edge="1" parent="1" source="30" target="40">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="84" value="1          chứa          1..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.6;startArrow=diamond;startFill=1;endArrow=none;exitX=1;exitY=0.45;entryX=0;entryY=0.45;" edge="1" parent="1" source="40" target="50">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="85" value="0..*       bán           1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.5;startArrow=none;endArrow=none;exitX=1;exitY=0.45;entryX=0;entryY=0.45;" edge="1" parent="1" source="50" target="60">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="86" value="1          gồm           1..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=1.6;startArrow=diamond;startFill=1;endArrow=none;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="70" target="60">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open('SoDoLop_QuanLyBanGiay.drawio', 'w', encoding='utf-8') as f:
        f.write(drawio_oop_content)
    print(" [PASS] Đã tạo SoDoLop_QuanLyBanGiay.drawio")

    # 2. SoDoERD_QuanLyBanGiay.drawio (6 bảng CSDL)
    drawio_erd_content = """<?xml version='1.0' encoding='utf-8'?>
<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="ERD_ShoePOS_DB" name="SoDoERD_QuanLyBanGiay">
    <mxGraphModel dx="1422" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1750" pageHeight="1300" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- NhanVien -->
        <mxCell id="t_nv" value="&amp;lt;b&amp;gt;NhanVien&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#1E3A8A;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="50" y="80" width="380" height="280" as="geometry" />
        </mxCell>
        <mxCell id="t_nv_cols" value="[PK] maNhanVien VARCHAR(10)&#10;[UQ] soDienThoai VARCHAR(10)&#10;     hoTen NVARCHAR(50)&#10;     ngaySinh DATE&#10;     gioiTinh BIT&#10;     diaChi NVARCHAR(200)&#10;     email VARCHAR(100)&#10;     chucVu NVARCHAR(30)&#10;     luongCoBan DECIMAL(18,0)&#10;     caLamViec NVARCHAR(20)&#10;     matKhau CHAR(64)&#10;     trangThai BIT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_nv">
          <mxGeometry y="28" width="380" height="252" as="geometry" />
        </mxCell>

        <!-- KhachHang -->
        <mxCell id="t_kh" value="&amp;lt;b&amp;gt;KhachHang&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#047857;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="50" y="440" width="380" height="200" as="geometry" />
        </mxCell>
        <mxCell id="t_kh_cols" value="[PK] maKhachHang VARCHAR(10)&#10;[UQ] soDienThoai VARCHAR(10)&#10;     hoTen NVARCHAR(50)&#10;     ngaySinh DATE&#10;     gioiTinh BIT&#10;     diaChi NVARCHAR(200)&#10;     email VARCHAR(100)&#10;     diemTichLuy INT&#10;     hangThanhVien NVARCHAR(20)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_kh">
          <mxGeometry y="28" width="380" height="172" as="geometry" />
        </mxCell>

        <!-- HoaDon -->
        <mxCell id="t_hd" value="&amp;lt;b&amp;gt;HoaDon&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#6D28D9;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="520" y="220" width="430" height="300" as="geometry" />
        </mxCell>
        <mxCell id="t_hd_cols" value="[PK] maHoaDon VARCHAR(10)&#10;[FK] maNhanVien VARCHAR(10)&#10;[FK] maKhachHang VARCHAR(10) (NULL)&#10;     ngayLap DATETIME&#10;     tongTienHang DECIMAL(18,0)&#10;     chietKhau DECIMAL(18,0)&#10;     diemSuDung INT&#10;     tienGiamDiem DECIMAL(18,0)&#10;     tongTien DECIMAL(18,0)&#10;     phuongThucTT NVARCHAR(30)&#10;     tienKhachDua DECIMAL(18,0)&#10;     tienThua DECIMAL(18,0)&#10;     diemCong INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_hd">
          <mxGeometry y="28" width="430" height="272" as="geometry" />
        </mxCell>

        <!-- ChiTietHoaDon -->
        <mxCell id="t_cthd" value="&amp;lt;b&amp;gt;ChiTietHoaDon&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#BE185D;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1030" y="270" width="400" height="170" as="geometry" />
        </mxCell>
        <mxCell id="t_cthd_cols" value="[PK][FK] maHoaDon VARCHAR(10)&#10;[PK][FK] maChiTietGiay VARCHAR(10)&#10;         soLuong INT&#10;         donGia DECIMAL(18,0)&#10;         giamGia DECIMAL(18,0)&#10;         thanhTien DECIMAL(18,0)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_cthd">
          <mxGeometry y="28" width="400" height="142" as="geometry" />
        </mxCell>

        <!-- SanPham -->
        <mxCell id="t_sp" value="&amp;lt;b&amp;gt;SanPham&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#2563EB;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1330" y="80" width="380" height="220" as="geometry" />
        </mxCell>
        <mxCell id="t_sp_cols" value="[PK] maSanPham VARCHAR(10)&#10;     tenSanPham NVARCHAR(100)&#10;     loaiGiay NVARCHAR(50)&#10;     thuongHieu NVARCHAR(50)&#10;     giaNhap DECIMAL(18,0)&#10;     giaBan DECIMAL(18,0)&#10;     chatLieu NVARCHAR(50)&#10;     trangThai BIT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_sp">
          <mxGeometry y="28" width="380" height="192" as="geometry" />
        </mxCell>

        <!-- ChiTietGiay -->
        <mxCell id="t_ctg" value="&amp;lt;b&amp;gt;ChiTietGiay&amp;lt;/b&amp;gt;" style="swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#C2410C;strokeColor=#1E293B;fontColor=#FFFFFF;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1330" y="420" width="380" height="200" as="geometry" />
        </mxCell>
        <mxCell id="t_ctg_cols" value="[PK] maChiTietGiay VARCHAR(10)&#10;[FK] maSanPham VARCHAR(10)&#10;[UQ] (maSanPham, kichThuoc, mauSac)&#10;     kichThuoc INT&#10;     mauSac NVARCHAR(30)&#10;     soLuongTon INT&#10;     hinhAnh NVARCHAR(255)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#0F172A;fontSize=11;fontFamily=monospace;" vertex="1" parent="t_ctg">
          <mxGeometry y="28" width="380" height="172" as="geometry" />
        </mxCell>

        <!-- Foreign Keys -->
        <mxCell id="e_nv_hd" value="1             0..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E293B;strokeWidth=1.5;startArrow=none;endArrow=ERmany;exitX=1;exitY=0.4;entryX=0;entryY=0.3;" edge="1" parent="1" source="t_nv" target="t_hd">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_kh_hd" value="0..1          0..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E293B;strokeWidth=1.5;startArrow=none;endArrow=ERmany;exitX=1;exitY=0.4;entryX=0;entryY=0.8;" edge="1" parent="1" source="t_kh" target="t_hd">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_hd_cthd" value="1             1..* (CASCADE)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E293B;strokeWidth=1.6;startArrow=none;endArrow=ERmany;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t_hd" target="t_cthd">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_sp_ctg" value="1             1..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E293B;strokeWidth=1.6;startArrow=none;endArrow=ERmany;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="t_sp" target="t_ctg">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_ctg_cthd" value="1             0..*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E293B;strokeWidth=1.5;startArrow=none;endArrow=ERmany;exitX=0;exitY=0.5;entryX=0.75;entryY=1;" edge="1" parent="1" source="t_ctg" target="t_cthd">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open('SoDoERD_QuanLyBanGiay.drawio', 'w', encoding='utf-8') as f:
        f.write(drawio_erd_content)
    print(" [PASS] Đã tạo SoDoERD_QuanLyBanGiay.drawio")


if __name__ == '__main__':
    generate_oop_class_diagram()
    generate_erd_diagram()
    generate_drawio_files()
    print("=== TẤT CẢ SƠ ĐỒ ĐÃ ĐƯỢC SINH THÀNH CÔNG VỚI CHUẨN ĐỒ HỌA CAO NHẤT ===")

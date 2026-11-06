import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set figure style
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=200)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Helper to draw a class box
    def draw_class(x, y, w, h, title, attrs, methods, header_bg='#1E3A8A'):
        # Header
        rect_hdr = patches.FancyBboxPatch((x, y + h - 0.4), w, 0.4, boxstyle="round,pad=0.02,rounding_size=0.08", 
                                          facecolor=header_bg, edgecolor='#1E293B', linewidth=1.2)
        ax.add_patch(rect_hdr)
        ax.text(x + w/2, y + h - 0.2, title, ha='center', va='center', color='white', weight='bold', fontsize=9.5)
        
        # Body
        rect_body = patches.FancyBboxPatch((x, y), w, h - 0.4, boxstyle="round,pad=0.02,rounding_size=0.08", 
                                           facecolor='white', edgecolor='#94A3B8', linewidth=1)
        ax.add_patch(rect_body)
        
        # Attributes
        curr_y = y + h - 0.55
        for a in attrs:
            ax.text(x + 0.1, curr_y, a, ha='left', va='center', color='#334155', fontsize=8, family='monospace')
            curr_y -= 0.2
            
        # Divider line
        ax.plot([x, x + w], [curr_y + 0.08, curr_y + 0.08], color='#E2E8F0', lw=0.8)
        curr_y -= 0.12
        
        # Methods
        for m in methods:
            ax.text(x + 0.1, curr_y, m, ha='left', va='center', color='#0F766E', fontsize=7.8, family='monospace')
            curr_y -= 0.2

    # Draw classes
    # Row 1: LoaiGiay, ThuongHieu, TaiKhoan
    draw_class(0.5, 6.2, 2.5, 2.2, "LoaiGiay", 
               ["- maLoai: String", "- tenLoai: String", "- moTa: String"], 
               ["+ getMaLoai()", "+ setMaLoai()", "+ getTenLoai()"], '#3B82F6')
    
    draw_class(3.5, 6.2, 2.8, 2.2, "ThuongHieu", 
               ["- maThuongHieu: String", "- tenThuongHieu: String", "- quocGia: String"], 
               ["+ getMaThuongHieu()", "+ setTenThuongHieu()"], '#3B82F6')
               
    draw_class(7.0, 6.2, 3.2, 2.3, "NhanVien", 
               ["- maNhanVien: String", "- hoTen: String", "- sdt: String", "- chucVu: String"], 
               ["+ isQuanLy(): boolean", "+ getMaNV()"], '#1E3A8A')

    draw_class(10.7, 6.2, 2.8, 2.3, "TaiKhoan", 
               ["- tenDangNhap: String", "- matKhau: String", "- quyenHan: String"], 
               ["+ xacThuc(pw): bool", "+ getQuyen()"], '#475569')

    # Row 2: SanPham & ChiTietGiay, HoaDon, KhachHang
    draw_class(1.5, 3.0, 3.2, 2.6, "SanPham", 
               ["- maSP: String", "- tenSP: String", "- loai: LoaiGiay", "- hang: ThuongHieu", "- giaBan: double"], 
               ["+ getMaSP()", "+ setGiaBan()"], '#1E3A8A')
               
    draw_class(5.2, 3.0, 3.2, 2.6, "ChiTietGiay (SKU)", 
               ["- maChiTiet: String", "- sanPham: SanPham", "- kichThuoc: int (35-44)", "- mauSac: String", "- soLuongTon: int"], 
               ["+ giamTonKho(qty)", "+ tangTonKho(qty)"], '#D97706')

    draw_class(9.0, 3.0, 3.2, 2.6, "KhachHang", 
               ["- maKH: String", "- hoTen: String", "- soDienThoai: String", "- diemTichLuy: int"], 
               ["+ congDiem(d)", "+ truDiem(d)"], '#059669')

    # Row 3: ChiTietHoaDon, HoaDon
    draw_class(3.5, 0.4, 3.8, 2.1, "ChiTietHoaDon", 
               ["- hoaDon: HoaDon", "- chiTietGiay: ChiTietGiay", "- soLuong: int", "- donGia: double", "- thanhTien: double"], 
               ["+ tinhThanhTien(): double"], '#D97706')

    draw_class(8.0, 0.4, 3.8, 2.2, "HoaDon", 
               ["- maHD: String", "- ngayLap: LocalDateTime", "- nhanVien: NhanVien", "- khachHang: KhachHang", "- tongTien: double"], 
               ["+ tinhTongTien()", "+ inHoaDon()"], '#1E3A8A')

    # Connectors
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2, shrinkA=3, shrinkB=3))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.08, label, fontsize=7.5, color='#1E293B', ha='center', weight='semibold',
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

    draw_arrow(1.7, 6.2, 2.5, 5.6, "1..*")
    draw_arrow(4.8, 6.2, 3.8, 5.6, "1..*")
    draw_arrow(4.7, 4.3, 5.2, 4.3, "1 - n (Variants)")
    draw_arrow(10.7, 7.3, 10.2, 7.3, "1 - 1")
    draw_arrow(8.6, 6.2, 9.5, 2.6, "lapBoi")
    draw_arrow(10.5, 3.0, 10.2, 2.6, "muaBoi")
    draw_arrow(8.0, 1.4, 7.3, 1.4, "1 - n")
    draw_arrow(5.5, 3.0, 5.5, 2.5, "xuatBan")

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    plt.title("HÌNH 1: SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (UML CLASS DIAGRAM) - HỆ THỐNG QUẢN LÝ BÁN GIÀY", 
              fontsize=11.5, weight='bold', color='#0F172A', pad=15)
    plt.tight_layout()
    plt.savefig('diagram_class_shoe.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Class diagram generated: diagram_class_shoe.png")

def generate_erd_diagram():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=200)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    
    def draw_table(x, y, w, h, table_name, pk_list, fk_list, cols, color='#1E40AF'):
        # Table Header
        rect_hdr = patches.FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0.02,rounding_size=0.06", 
                                          facecolor=color, edgecolor='#0F172A', linewidth=1.1)
        ax.add_patch(rect_hdr)
        ax.text(x + w/2, y + h - 0.18, table_name, ha='center', va='center', color='white', weight='bold', fontsize=9)
        
        # Table Body
        rect_body = patches.FancyBboxPatch((x, y), w, h - 0.35, boxstyle="round,pad=0.02,rounding_size=0.06", 
                                           facecolor='white', edgecolor='#94A3B8', linewidth=0.9)
        ax.add_patch(rect_body)
        
        curr_y = y + h - 0.5
        for pk in pk_list:
            ax.text(x + 0.1, curr_y, "[PK] " + pk, ha='left', va='center', color='#B91C1C', fontsize=7.5, weight='bold', family='monospace')
            curr_y -= 0.18
        for fk in fk_list:
            ax.text(x + 0.1, curr_y, "[FK] " + fk, ha='left', va='center', color='#2563EB', fontsize=7.5, weight='bold', family='monospace')
            curr_y -= 0.18
        for c in cols:
            ax.text(x + 0.1, curr_y, "     " + c, ha='left', va='center', color='#334155', fontsize=7.3, family='monospace')
            curr_y -= 0.18

    # Tables layout
    draw_table(0.5, 6.2, 2.6, 2.0, "LoaiGiay", ["MaLoai VARCHAR(10)"], [], ["TenLoai NVARCHAR(50)", "MoTa NVARCHAR(255)"], '#2563EB')
    draw_table(3.4, 6.2, 2.8, 2.0, "ThuongHieu", ["MaThuongHieu VARCHAR(10)"], [], ["TenThuongHieu NVARCHAR(50)", "QuocGia NVARCHAR(50)"], '#2563EB')
    draw_table(7.0, 6.2, 3.2, 2.3, "NhanVien", ["MaNhanVien VARCHAR(10)"], [], ["HoTen NVARCHAR(50)", "SoDienThoai VARCHAR(10)", "ChucVu NVARCHAR(30)"], '#1E3A8A')
    draw_table(10.7, 6.2, 2.8, 2.0, "TaiKhoan", ["TenDangNhap VARCHAR(10)"], ["MaNhanVien VARCHAR(10)"], ["MatKhau VARCHAR(100)", "QuyenHan VARCHAR(20)"], '#475569')

    draw_table(1.5, 2.8, 3.2, 2.7, "SanPham", ["MaSanPham VARCHAR(10)"], ["MaLoai VARCHAR(10)", "MaThuongHieu VARCHAR(10)"], 
               ["TenSanPham NVARCHAR(100)", "GiaNhap DECIMAL(18,2)", "GiaBan DECIMAL(18,2)", "TrangThai BIT"], '#1E3A8A')
               
    draw_table(5.2, 2.8, 3.3, 2.7, "ChiTietGiay", ["MaChiTietGiay VARCHAR(10)"], ["MaSanPham VARCHAR(10)"], 
               ["KichThuoc INT (35-45)", "MauSac NVARCHAR(30)", "SoLuongTon INT", "TrangThai BIT"], '#B45309')

    draw_table(9.0, 2.8, 3.2, 2.4, "KhachHang", ["MaKhachHang VARCHAR(10)"], [], 
               ["HoTen NVARCHAR(50)", "SoDienThoai VARCHAR(10)", "DiemTichLuy INT"], '#047857')

    draw_table(3.5, 0.3, 3.8, 2.1, "ChiTietHoaDon", ["MaHoaDon VARCHAR(10)", "MaChiTietGiay VARCHAR(10)"], 
               ["MaHoaDon", "MaChiTietGiay"], ["SoLuong INT", "DonGia DECIMAL(18,2)", "ThanhTien DECIMAL(18,2)"], '#B45309')

    draw_table(8.0, 0.3, 3.8, 2.2, "HoaDon", ["MaHoaDon VARCHAR(10)"], ["MaNhanVien VARCHAR(10)", "MaKhachHang VARCHAR(10)"], 
               ["NgayLap DATETIME", "TongTien DECIMAL(18,2)", "TienKhachDua", "TienThua"], '#1E3A8A')

    # Lines & relationships
    ax.annotate('', xy=(2.5, 5.5), xytext=(1.5, 6.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1))
    ax.annotate('', xy=(3.5, 5.5), xytext=(4.2, 6.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1))
    ax.annotate('', xy=(5.2, 4.1), xytext=(4.7, 4.1), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.3))
    ax.annotate('', xy=(10.2, 7.3), xytext=(10.7, 7.3), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1))
    ax.annotate('', xy=(8.6, 2.5), xytext=(8.6, 6.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1))
    ax.annotate('', xy=(10.2, 2.5), xytext=(10.2, 2.8), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1))
    ax.annotate('', xy=(7.3, 1.3), xytext=(8.0, 1.3), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))
    ax.annotate('', xy=(5.5, 2.4), xytext=(5.5, 2.8), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.2))

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    plt.title("HÌNH 2: SƠ ĐỒ CƠ SỞ DỮ LIỆU QUAN HỆ TRÊN SQL SERVER (DATABASE ERD)", 
              fontsize=11.5, weight='bold', color='#0F172A', pad=15)
    plt.tight_layout()
    plt.savefig('diagram_erd_shoe.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("ERD diagram generated: diagram_erd_shoe.png")

def generate_revenue_analytics():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    
    # Chart 1: Doanh thu theo thang
    months = ['T5', 'T6', 'T7', 'T8', 'T9', 'T10']
    rev = [125, 140, 168, 155, 192, 215] # Trieu dong
    ax1.bar(months, rev, color='#2563EB', width=0.55, edgecolor='#1D4ED8', zorder=3)
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax1.set_title("DOANH THU 6 THÁNG GẦN NHẤT (TRIỆU ĐỒNG)", fontsize=10, weight='bold', color='#1E293B', pad=10)
    ax1.set_ylabel("Triệu VNĐ", fontsize=9)
    for i, v in enumerate(rev):
        ax1.text(i, v + 4, f"{v} tr", ha='center', fontsize=8.5, weight='bold', color='#1E3A8A')
    ax1.set_ylim(0, 250)

    # Chart 2: Top giay ban chay
    models = ['Nike Air Force 1', 'Adidas Samba OG', "Biti's Hunter Street", 'MLB Chunky Liner', 'Vans Old Skool']
    pct = [32, 26, 18, 14, 10]
    colors = ['#1E3A8A', '#2563EB', '#F59E0B', '#10B981', '#64748B']
    wedges, texts, autotexts = ax2.pie(pct, labels=models, autopct='%1.0f%%', startangle=140, 
                                       colors=colors, textprops=dict(color='#1E293B', fontsize=8.5, weight='medium'))
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    ax2.set_title("TOP 5 MẪU GIÀY BÁN CHẠY NHẤT THÁNG", fontsize=10, weight='bold', color='#1E293B', pad=10)

    plt.suptitle("HÌNH 3: MINH HỌA THỐNG KÊ DOANH THU & TOP SẢN PHẨM BÁN CHẠY TẠI CỬA HÀNG", 
                 fontsize=11.5, weight='bold', color='#0F172A', y=1.02)
    plt.tight_layout()
    plt.savefig('diagram_chart_shoe.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Chart generated: diagram_chart_shoe.png")

if __name__ == '__main__':
    generate_class_diagram()
    generate_erd_diagram()
    generate_revenue_analytics()
    print("All assets generated successfully!")

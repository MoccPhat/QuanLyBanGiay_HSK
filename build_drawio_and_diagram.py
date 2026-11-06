import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# 1. DRAW.IO XML GENERATION (app.diagrams.net compatible)
# ==============================================================================
def create_drawio_file(filename="SoDoLop_QuanLyBanGiay.drawio"):
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Mozilla/5.0", version="21.6.8")
    diagram = ET.SubElement(mxfile, "diagram", id="class_diagram", name="Sơ đồ lớp - Quản lý bán giày")
    model = ET.SubElement(diagram, "mxGraphModel", dx="1400", dy="1100", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="1400", math="0", shadow="0")
    root = ET.SubElement(model, "root")
    
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    cell_id = 10
    def add_uml_class(parent, x, y, w, h, name, attrs, methods):
        nonlocal cell_id
        cid = str(cell_id)
        cell_id += 1
        attr_text = "<br>".join([f"- {a}" for a in attrs])
        method_text = "<br>".join([f"+ {m}" for m in methods])
        value = f"<b>{name}</b><hr size=\"1\"/><div style=\"text-align: left; margin-left: 4px;\">{attr_text}</div><hr size=\"1\"/><div style=\"text-align: left; margin-left: 4px;\">{method_text}</div>"
        style = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;rounded=0;"
        cell = ET.SubElement(parent, "mxCell", id=cid, value=value, style=style, vertex="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), as_="geometry")
        return cid

    def add_uml_enum(parent, x, y, w, h, name, values):
        nonlocal cell_id
        cid = str(cell_id)
        cell_id += 1
        val_text = "<br>".join([f"&lt;&lt;Constant&gt;&gt; - {v}" for v in values])
        value = f"&lt;&lt;enumeration&gt;&gt;<br><b>{name}</b><hr size=\"1\"/><div style=\"text-align: left; margin-left: 4px;\">{val_text}</div>"
        style = "swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=36;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;rounded=0;"
        cell = ET.SubElement(parent, "mxCell", id=cid, value=value, style=style, vertex="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), as_="geometry")
        return cid

    def add_edge(parent, source_id, target_id, start_arrow="none", end_arrow="none", start_fill="0", style_extra="", label=""):
        nonlocal cell_id
        eid = str(cell_id)
        cell_id += 1
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1;startArrow={start_arrow};endArrow={end_arrow};startFill={start_fill};{style_extra}"
        edge = ET.SubElement(parent, "mxCell", id=eid, value=label, style=style, edge="1", source=source_id, target=target_id)
        ET.SubElement(edge, "mxGeometry", relative="1", as_="geometry")
        return eid

    # Coordinates
    c_lg = add_uml_class(root, 60, 40, 240, 120, "LOAI_GIAY", 
                         ["maLoai : String", "tenLoai : String", "moTa : String"], 
                         ["LOAI_GIAY()", "getMaLoai() : String"])

    c_th = add_uml_class(root, 420, 40, 260, 130, "THUONG_HIEU", 
                         ["maThuongHieu : String", "tenThuongHieu : String", "quocGia : String", "website : String"], 
                         ["THUONG_HIEU()", "getMaThuongHieu() : String"])

    c_sp = add_uml_class(root, 60, 230, 280, 200, "SAN_PHAM", 
                         ["maSanPham : String", "tenSanPham : String", "xuatXu : String", "chatLieu : String", "giaNhap : double", "giaBan : double", "hinhAnh : String", "trangThai : boolean"], 
                         ["SAN_PHAM()", "getMaSanPham() : String", "setGiaBan(giaBan : double)"])

    c_ctg = add_uml_class(root, 460, 230, 260, 180, "CHI_TIET_GIAY", 
                          ["maChiTietGiay : String", "kichThuoc : int", "mauSac : String", "soLuongTon : int", "hinhAnhBienThe : String", "trangThai : boolean"], 
                          ["CHI_TIET_GIAY()", "giamTonKho(qty) : bool", "tangTonKho(qty) : void"])

    c_hd = add_uml_class(root, 60, 490, 280, 210, "HOA_DON", 
                         ["maHoaDon : String", "ngayLap : LocalDateTime", "tongTien : double", "phuongThucThanhToan : String", "tienKhachDua : double", "tienThua : double", "ghiChu : String", "trangThai : String"], 
                         ["HOA_DON()", "tinhTongTien() : double", "tinhTienThua() : double"])

    c_cthd = add_uml_class(root, 460, 490, 260, 160, "CHI_TIET_HOA_DON", 
                           ["soLuong : int", "donGia : double", "giamGia : double", "thanhTien : double"], 
                           ["CHI_TIET_HOA_DON()", "tinhThanhTien() : double"])

    c_nv = add_uml_class(root, 60, 770, 280, 190, "NHAN_VIEN", 
                         ["maNhanVien : String", "hoTen : String", "ngaySinh : LocalDate", "gioiTinh : boolean", "soDienThoai : String", "chucVu : String", "luongCoBan : double", "trangThai : boolean"], 
                         ["NHAN_VIEN()", "isQuanLy() : boolean"])

    c_kh = add_uml_class(root, 460, 770, 260, 170, "KHACH_HANG", 
                         ["maKhachHang : String", "hoTen : String", "soDienThoai : String", "email : String", "diaChi : String", "diemTichLuy : int"], 
                         ["KHACH_HANG()", "congDiem(diem : int) : void"])

    c_tk = add_uml_class(root, 60, 1020, 280, 150, "TAI_KHOAN", 
                         ["tenDangNhap : String", "matKhau : String", "quyenHan : Role", "ngayTao : LocalDate", "trangThai : boolean"], 
                         ["TAI_KHOAN()", "xacThuc(matKhau) : bool"])

    c_role = add_uml_enum(root, 460, 1020, 180, 100, "ROLE", ["ADMIN", "STAFF"])

    # Connectors
    add_edge(root, c_lg, c_sp, label="-loaiGiay [*]")
    add_edge(root, c_th, c_sp, label="-thuongHieu [*]")
    add_edge(root, c_sp, c_ctg, start_arrow="diamond", start_fill="1", label="-chiTietGiay [1..*]")
    add_edge(root, c_hd, c_cthd, start_arrow="diamond", start_fill="1", label="-danhSachChiTiet [1..*]")
    add_edge(root, c_cthd, c_ctg, label="-chiTietGiay [1]")
    add_edge(root, c_nv, c_hd, label="-nhanVien [1]")
    add_edge(root, c_kh, c_hd, label="-khachHang [0..1]")
    add_edge(root, c_nv, c_tk, label="-nhanVien [1]")
    add_edge(root, c_tk, c_role, end_arrow="open", style_extra="dashed=1;", label="&lt;&lt;use&gt;&gt;")

    tree = ET.ElementTree(mxfile)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Draw.io XML successfully saved to: {filename}")


# ==============================================================================
# 2. ACCURATE MONOCHROME UML RENDERING (High Quality Draw.io Style)
# ==============================================================================
def render_clean_drawio_diagram(output_path="diagram_class_shoe.png"):
    fig, ax = plt.subplots(figsize=(13.0, 14.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Draw standard Draw.io UML Box
    def draw_box(x, y, w, h_title, h_attr, h_meth, title, attrs, methods, is_enum=False):
        total_h = h_title + h_attr + h_meth
        y_bot = y - total_h
        
        # Border box
        rect = patches.Rectangle((x, y_bot), w, total_h, lw=1.2, edgecolor='#000000', facecolor='#FFFFFF', zorder=2)
        ax.add_patch(rect)
        
        # Line below title
        y_line1 = y - h_title
        ax.plot([x, x + w], [y_line1, y_line1], color='#000000', lw=1.1, zorder=3)
        
        # Title text
        if is_enum:
            ax.text(x + w/2, y - 0.16, "<<enumeration>>", ha='center', va='center', fontsize=8, family='sans-serif', zorder=4)
            ax.text(x + w/2, y - 0.38, title, ha='center', va='center', fontsize=9.5, weight='bold', family='sans-serif', zorder=4)
        else:
            ax.text(x + w/2, y - h_title/2, title, ha='center', va='center', fontsize=9.5, weight='bold', family='sans-serif', zorder=4)
            
        # Line below attrs
        y_line2 = y_line1 - h_attr
        ax.plot([x, x + w], [y_line2, y_line2], color='#000000', lw=1.1, zorder=3)
        
        # Attrs
        curr_y = y_line1 - 0.18
        for a in attrs:
            ax.text(x + 0.12, curr_y, a, ha='left', va='center', fontsize=8, family='sans-serif', zorder=4)
            curr_y -= 0.22
            
        # Methods
        curr_y = y_line2 - 0.18
        for m in methods:
            ax.text(x + 0.12, curr_y, m, ha='left', va='center', fontsize=8, family='sans-serif', zorder=4)
            curr_y -= 0.22

        return {'x': x, 'y': y, 'w': w, 'h': total_h, 'bot': y_bot, 'top': y, 'mid_x': x + w/2, 'mid_y': y - total_h/2}

    # 1. Row 1 (Top): LOAI_GIAY & THUONG_HIEU
    b_lg = draw_box(0.8, 14.0, 3.8, 0.45, 0.85, 0.65, "LOAI_GIAY",
                    ["- maLoai : String", "- tenLoai : String", "- moTa : String"],
                    ["+ LOAI_GIAY()", "+ LOAI_GIAY(maLoai, tenLoai)"])

    b_th = draw_box(5.8, 14.0, 4.4, 0.45, 1.05, 0.65, "THUONG_HIEU",
                    ["- maThuongHieu : String", "- tenThuongHieu : String", "- quocGia : String", "- website : String"],
                    ["+ THUONG_HIEU()", "+ THUONG_HIEU(maTH, tenTH)"])

    # 2. Row 2: SAN_PHAM & CHI_TIET_GIAY
    b_sp = draw_box(0.8, 11.2, 4.6, 0.45, 1.95, 0.85, "SAN_PHAM",
                    ["- maSanPham : String", "- tenSanPham : String", "- xuatXu : String", "- chatLieu : String", "- giaNhap : double", "- giaBan : double", "- hinhAnh : String", "- trangThai : boolean"],
                    ["+ SAN_PHAM()", "+ SAN_PHAM(maSP, tenSP, giaBan...)", "+ setGiaBan(giaBan : double) : void"])

    b_ctg = draw_box(6.8, 11.2, 4.4, 0.45, 1.5, 0.85, "CHI_TIET_GIAY",
                     ["- maChiTietGiay : String", "- kichThuoc : int", "- mauSac : String", "- soLuongTon : int", "- hinhAnhBienThe : String", "- trangThai : boolean"],
                     ["+ CHI_TIET_GIAY()", "+ giamTonKho(soLuong : int) : boolean", "+ tangTonKho(soLuong : int) : void"])

    # 3. Row 3: HOA_DON & CHI_TIET_HOA_DON
    b_hd = draw_box(0.8, 7.0, 4.6, 0.45, 1.95, 0.85, "HOA_DON",
                    ["- maHoaDon : String", "- ngayLap : LocalDateTime", "- tongTien : double", "- phuongThucThanhToan : String", "- tienKhachDua : double", "- tienThua : double", "- ghiChu : String", "- trangThai : String"],
                    ["+ HOA_DON()", "+ HOA_DON(maHD, ngayLap, tongTien...)", "+ tinhTongTien() : double"])

    b_cthd = draw_box(6.8, 7.0, 4.4, 0.45, 1.05, 0.65, "CHI_TIET_HOA_DON",
                      ["- soLuong : int", "- donGia : double", "- giamGia : double", "- thanhTien : double"],
                      ["+ CHI_TIET_HOA_DON()", "+ tinhThanhTien() : double"])

    # 4. Row 4: NHAN_VIEN & KHACH_HANG
    b_nv = draw_box(0.8, 3.0, 4.6, 0.45, 1.95, 0.65, "NHAN_VIEN",
                    ["- maNhanVien : String", "- hoTen : String", "- ngaySinh : LocalDate", "- gioiTinh : boolean", "- soDienThoai : String", "- chucVu : String", "- luongCoBan : double", "- trangThai : boolean"],
                    ["+ NHAN_VIEN()", "+ isQuanLy() : boolean"])

    b_kh = draw_box(6.8, 3.0, 4.4, 0.45, 1.45, 0.65, "KHACH_HANG",
                    ["- maKhachHang : String", "- hoTen : String", "- soDienThoai : String", "- email : String", "- diaChi : String", "- diemTichLuy : int"],
                    ["+ KHACH_HANG()", "+ congDiem(diem : int) : void"])

    # 5. Row 5: TAI_KHOAN & ROLE
    b_tk = draw_box(0.8, -0.6, 4.6, 0.45, 1.25, 0.65, "TAI_KHOAN",
                    ["- tenDangNhap : String", "- matKhau : String", "- quyenHan : Role", "- ngayTao : LocalDate", "- trangThai : boolean"],
                    ["+ TAI_KHOAN()", "+ xacThuc(matKhau : String) : boolean"])

    b_role = draw_box(6.8, -0.6, 2.8, 0.55, 0.65, 0.05, "ROLE",
                      ["<<Constant>> - ADMIN", "<<Constant>> - STAFF"], [], is_enum=True)

    # -------------------------------------------------------------
    # DRAW CONNECTOR LINES (ORTHOGONAL, CLEAN, ZERO TEXT CLASH)
    # -------------------------------------------------------------
    # Helper for lines
    def draw_line(points, mult_start="", mult_end="", role=""):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.plot(xs, ys, color='#000000', lw=1.1, zorder=3)
        if mult_start:
            ax.text(xs[0] + 0.08, ys[0] + 0.08, mult_start, fontsize=8, family='sans-serif', zorder=5)
        if mult_end:
            ax.text(xs[-1] + 0.08, ys[-1] + 0.08, mult_end, fontsize=8, family='sans-serif', zorder=5)
        if role:
            # Place role label near middle segment
            mid_i = len(points) // 2
            mx = (points[mid_i-1][0] + points[mid_i][0]) / 2
            my = (points[mid_i-1][1] + points[mid_i][1]) / 2
            ax.text(mx + 0.08, my + 0.08, role, fontsize=8, family='sans-serif', zorder=5)

    def draw_composition_h(x1, y1, x2, y2, mult_start="", mult_end="", role=""):
        # Diamond at (x1, y1)
        d = 0.14
        pts = [[x1, y1], [x1 + d, y1 + d/1.5], [x1 + 2*d, y1], [x1 + d, y1 - d/1.5]]
        poly = patches.Polygon(pts, closed=True, facecolor='#000000', edgecolor='#000000', zorder=6)
        ax.add_patch(poly)
        ax.plot([x1 + 2*d, x2], [y1, y2], color='#000000', lw=1.1, zorder=3)
        if mult_start:
            ax.text(x1 + 2*d + 0.08, y1 + 0.1, mult_start, fontsize=8, family='sans-serif', zorder=5)
        if mult_end:
            ax.text(x2 - 0.28, y2 + 0.1, mult_end, fontsize=8, family='sans-serif', zorder=5)
        if role:
            ax.text((x1 + x2)/2, y1 - 0.18, role, fontsize=8, family='sans-serif', ha='center', zorder=5)

    # 1. LOAI_GIAY (bottom: 2.7, 12.05) -> SAN_PHAM (top: 2.7, 11.2)
    draw_line([[2.7, 12.05], [2.7, 11.2]], mult_start="1", mult_end="*", role="-loaiGiay")

    # 2. THUONG_HIEU (bottom: 8.0, 11.85) -> SAN_PHAM (top: 4.2, 11.2)
    draw_line([[8.0, 11.85], [8.0, 11.55], [4.2, 11.55], [4.2, 11.2]], mult_start="1", mult_end="*", role="-thuongHieu")

    # 3. SAN_PHAM (right: 5.4, 9.6) --◆ CHI_TIET_GIAY (left: 6.8, 9.6)
    draw_composition_h(5.4, 9.6, 6.8, 9.6, mult_start="1", mult_end="1..*", role="-chiTietGiay")

    # 4. HOA_DON (right: 5.4, 5.4) --◆ CHI_TIET_HOA_DON (left: 6.8, 5.4)
    draw_composition_h(5.4, 5.4, 6.8, 5.4, mult_start="1", mult_end="1..*", role="-danhSachChiTiet")

    # 5. CHI_TIET_HOA_DON (top: 9.0, 7.0) -> CHI_TIET_GIAY (bottom: 9.0, 8.4)
    draw_line([[9.0, 7.0], [9.0, 8.4]], mult_start="*", mult_end="1", role="-chiTietGiay")

    # 6. NHAN_VIEN (top: 3.1, 3.0) -> HOA_DON (bottom: 3.1, 3.75)
    draw_line([[3.1, 3.0], [3.1, 3.75]], mult_start="1", mult_end="*", role="-nhanVien")

    # 7. KHACH_HANG (top: 7.8, 3.0) -> HOA_DON (bottom: 4.5, 3.75)
    draw_line([[7.8, 3.0], [7.8, 3.4], [4.5, 3.4], [4.5, 3.75]], mult_start="0..1", mult_end="*", role="-khachHang")

    # 8. NHAN_VIEN (bottom: 3.1, 0.2) -> TAI_KHOAN (top: 3.1, -0.6)
    draw_line([[3.1, 0.2], [3.1, -0.6]], mult_start="1", mult_end="1", role="-nhanVien")

    # 9. TAI_KHOAN (right: 5.4, -1.8) -> ROLE (left: 6.8, -1.8) [Dashed use]
    ax.annotate('', xy=(6.8, -1.8), xytext=(5.4, -1.8),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.1, linestyle='dashed'))
    ax.text(6.1, -1.65, "<<use>>", ha='center', fontsize=8, family='sans-serif')

    ax.set_xlim(0, 12.0)
    ax.set_ylim(-3.5, 14.5)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig("SoDoLop_QuanLyBanGiay.png", dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"Clean monochrome Draw.io diagram rendered to: {output_path}")

if __name__ == '__main__':
    create_drawio_file("SoDoLop_QuanLyBanGiay.drawio")
    render_clean_drawio_diagram("diagram_class_shoe.png")
    print("All tasks finished!")

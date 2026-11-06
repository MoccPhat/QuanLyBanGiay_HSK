import xml.etree.ElementTree as ET

def build_perfect_drawio():
    mxfile = ET.Element("mxfile", attrib={
        "host": "app.diagrams.net",
        "agent": "Mozilla/5.0",
        "version": "21.6.8",
        "type": "device"
    })
    
    diagram = ET.SubElement(mxfile, "diagram", attrib={
        "id": "ClassDiagram_ShoePOS",
        "name": "SoDoLop_QuanLyBanGiay"
    })
    
    model = ET.SubElement(diagram, "mxGraphModel", attrib={
        "dx": "1422",
        "dy": "850",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "1654",
        "pageHeight": "1169",
        "math": "0",
        "shadow": "0"
    })
    
    root = ET.SubElement(model, "root")
    
    # Layer 0 & 1
    ET.SubElement(root, "mxCell", attrib={"id": "0"})
    ET.SubElement(root, "mxCell", attrib={"id": "1", "parent": "0"})
    
    id_counter = 10
    
    # Helper to add standard Draw.io UML Class (Composite Swimlane)
    def add_class(x, y, w, name, attrs, methods):
        nonlocal id_counter
        cid = str(id_counter)
        id_counter += 1
        
        attr_h = max(26, len(attrs) * 18 + 8)
        meth_h = max(26, len(methods) * 18 + 8)
        total_h = 26 + attr_h + 8 + meth_h
        
        # Parent swimlane
        c_style = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;rounded=0;"
        cell = ET.SubElement(root, "mxCell", attrib={
            "id": cid,
            "value": name,
            "style": c_style,
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", attrib={
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(total_h),
            "as": "geometry"
        })
        
        # Child 1: Attributes
        attr_id = str(id_counter)
        id_counter += 1
        attr_val = "\n".join([f"- {a}" for a in attrs])
        attr_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
        c_attr = ET.SubElement(root, "mxCell", attrib={
            "id": attr_id,
            "value": attr_val,
            "style": attr_style,
            "vertex": "1",
            "parent": cid
        })
        ET.SubElement(c_attr, "mxGeometry", attrib={
            "y": "26",
            "width": str(w),
            "height": str(attr_h),
            "as": "geometry"
        })
        
        # Child 2: Divider Line
        div_id = str(id_counter)
        id_counter += 1
        div_style = "line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#000000;"
        c_div = ET.SubElement(root, "mxCell", attrib={
            "id": div_id,
            "value": "",
            "style": div_style,
            "vertex": "1",
            "parent": cid
        })
        ET.SubElement(c_div, "mxGeometry", attrib={
            "y": str(26 + attr_h),
            "width": str(w),
            "height": "8",
            "as": "geometry"
        })
        
        # Child 3: Methods
        meth_id = str(id_counter)
        id_counter += 1
        meth_val = "\n".join([f"+ {m}" for m in methods])
        meth_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
        c_meth = ET.SubElement(root, "mxCell", attrib={
            "id": meth_id,
            "value": meth_val,
            "style": meth_style,
            "vertex": "1",
            "parent": cid
        })
        ET.SubElement(c_meth, "mxGeometry", attrib={
            "y": str(26 + attr_h + 8),
            "width": str(w),
            "height": str(meth_h),
            "as": "geometry"
        })
        
        return cid

    # Helper for Enum
    def add_enum(x, y, w, name, values):
        nonlocal id_counter
        cid = str(id_counter)
        id_counter += 1
        
        val_h = len(values) * 18 + 8
        total_h = 36 + val_h
        
        c_style = "swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=36;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;rounded=0;"
        val_title = f"&lt;&lt;enumeration&gt;&gt;\n<b>{name}</b>"
        cell = ET.SubElement(root, "mxCell", attrib={
            "id": cid,
            "value": val_title,
            "style": c_style,
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", attrib={
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(total_h),
            "as": "geometry"
        })
        
        val_id = str(id_counter)
        id_counter += 1
        val_str = "\n".join([f"&lt;&lt;Constant&gt;&gt; - {v}" for v in values])
        v_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
        c_val = ET.SubElement(root, "mxCell", attrib={
            "id": val_id,
            "value": val_str,
            "style": v_style,
            "vertex": "1",
            "parent": cid
        })
        ET.SubElement(c_val, "mxGeometry", attrib={
            "y": "36",
            "width": str(w),
            "height": str(val_h),
            "as": "geometry"
        })
        return cid

    # Helper for Edges
    def add_edge(source_id, target_id, label="", start_arrow="none", end_arrow="none", start_fill="0", dashed="0", exit_x="0.5", exit_y="1", entry_x="0.5", entry_y="0"):
        nonlocal id_counter
        eid = str(id_counter)
        id_counter += 1
        
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.2;startArrow={start_arrow};endArrow={end_arrow};startFill={start_fill};exitX={exit_x};exitY={exit_y};entryX={entry_x};entryY={entry_y};"
        if dashed == "1":
            style += "dashed=1;"
            
        edge = ET.SubElement(root, "mxCell", attrib={
            "id": eid,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source_id,
            "target": target_id
        })
        ET.SubElement(edge, "mxGeometry", attrib={
            "relative": "1",
            "as": "geometry"
        })
        return eid

    # =========================================================================
    # POSITIONS (Well spaced, 0 overlaps, 100% clean academic Draw.io canvas)
    # =========================================================================
    # Row 1 (y=40): LOAI_GIAY (x=80), THUONG_HIEU (x=420)
    c_lg = add_class(80, 40, 260, "LOAI_GIAY",
                     ["maLoai : String", "tenLoai : String", "moTa : String"],
                     ["LOAI_GIAY()", "getMaLoai() : String", "setTenLoai(ten : String)"])

    c_th = add_class(420, 40, 280, "THUONG_HIEU",
                     ["maThuongHieu : String", "tenThuongHieu : String", "quocGia : String", "website : String"],
                     ["THUONG_HIEU()", "getMaThuongHieu() : String"])

    # Row 2 (y=260): SAN_PHAM (x=80), CHI_TIET_GIAY (x=480)
    c_sp = add_class(80, 260, 320, "SAN_PHAM",
                     ["maSanPham : String", "tenSanPham : String", "xuatXu : String", "chatLieu : String", "giaNhap : double", "giaBan : double", "hinhAnh : String", "trangThai : boolean"],
                     ["SAN_PHAM()", "getMaSanPham() : String", "setGiaBan(giaBan : double)"])

    c_ctg = add_class(480, 260, 300, "CHI_TIET_GIAY",
                      ["maChiTietGiay : String", "kichThuoc : int", "mauSac : String", "soLuongTon : int", "hinhAnhBienThe : String", "trangThai : boolean"],
                      ["CHI_TIET_GIAY()", "giamTonKho(qty : int) : boolean", "tangTonKho(qty : int) : void"])

    # Row 3 (y=560): HOA_DON (x=80), CHI_TIET_HOA_DON (x=480)
    c_hd = add_class(80, 560, 320, "HOA_DON",
                     ["maHoaDon : String", "ngayLap : LocalDateTime", "tongTien : double", "phuongThucThanhToan : String", "tienKhachDua : double", "tienThua : double", "ghiChu : String", "trangThai : String"],
                     ["HOA_DON()", "tinhTongTien() : double", "tinhTienThua() : double"])

    c_cthd = add_class(480, 560, 300, "CHI_TIET_HOA_DON",
                       ["soLuong : int", "donGia : double", "giamGia : double", "thanhTien : double"],
                       ["CHI_TIET_HOA_DON()", "tinhThanhTien() : double"])

    # Row 4 (y=840): NHAN_VIEN (x=80), KHACH_HANG (x=480)
    c_nv = add_class(80, 840, 320, "NHAN_VIEN",
                     ["maNhanVien : String", "hoTen : String", "ngaySinh : LocalDate", "gioiTinh : boolean", "soDienThoai : String", "chucVu : String", "luongCoBan : double", "trangThai : boolean"],
                     ["NHAN_VIEN()", "isQuanLy() : boolean"])

    c_kh = add_class(480, 840, 300, "KHACH_HANG",
                     ["maKhachHang : String", "hoTen : String", "soDienThoai : String", "email : String", "diaChi : String", "diemTichLuy : int"],
                     ["KHACH_HANG()", "congDiem(diem : int) : void", "truDiem(diem : int) : boolean"])

    # Row 5 (y=1120): TAI_KHOAN (x=80), ROLE (x=480)
    c_tk = add_class(80, 1120, 320, "TAI_KHOAN",
                     ["tenDangNhap : String", "matKhau : String", "quyenHan : Role", "ngayTao : LocalDate", "trangThai : boolean"],
                     ["TAI_KHOAN()", "xacThuc(matKhau : String) : boolean"])

    c_role = add_enum(480, 1120, 200, "ROLE", ["ADMIN", "STAFF"])

    # =========================================================================
    # EDGES WITH CLEAR LABELS (NO CROSSINGS)
    # =========================================================================
    # 1. LOAI_GIAY (bottom) -> SAN_PHAM (top)
    add_edge(c_lg, c_sp, label="-loaiGiay [*]", exit_x="0.5", exit_y="1", entry_x="0.3", entry_y="0")

    # 2. THUONG_HIEU (bottom) -> SAN_PHAM (top)
    add_edge(c_th, c_sp, label="-thuongHieu [*]", exit_x="0.3", exit_y="1", entry_x="0.7", entry_y="0")

    # 3. SAN_PHAM (right) --◆ CHI_TIET_GIAY (left) [Composition]
    add_edge(c_sp, c_ctg, label="-chiTietGiay [1..*]", start_arrow="diamond", start_fill="1", exit_x="1", exit_y="0.5", entry_x="0", entry_y="0.5")

    # 4. HOA_DON (right) --◆ CHI_TIET_HOA_DON (left) [Composition]
    add_edge(c_hd, c_cthd, label="-danhSachChiTiet [1..*]", start_arrow="diamond", start_fill="1", exit_x="1", exit_y="0.5", entry_x="0", entry_y="0.5")

    # 5. CHI_TIET_HOA_DON (top) -> CHI_TIET_GIAY (bottom)
    add_edge(c_cthd, c_ctg, label="-chiTietGiay [1]", exit_x="0.5", exit_y="0", entry_x="0.5", entry_y="1")

    # 6. NHAN_VIEN (top) -> HOA_DON (bottom)
    add_edge(c_nv, c_hd, label="-nhanVien [1]", exit_x="0.5", exit_y="0", entry_x="0.5", entry_y="1")

    # 7. KHACH_HANG (top) -> HOA_DON (bottom right)
    add_edge(c_kh, c_hd, label="-khachHang [0..1]", exit_x="0.2", exit_y="0", entry_x="0.8", entry_y="1")

    # 8. NHAN_VIEN (bottom) -> TAI_KHOAN (top)
    add_edge(c_nv, c_tk, label="-nhanVien [1]", exit_x="0.5", exit_y="1", entry_x="0.5", entry_y="0")

    # 9. TAI_KHOAN (right) ..> ROLE (left) [<<use>>]
    add_edge(c_tk, c_role, label="&lt;&lt;use&gt;&gt;", end_arrow="open", dashed="1", exit_x="1", exit_y="0.5", entry_x="0", entry_y="0.5")

    tree = ET.ElementTree(mxfile)
    tree.write("SoDoLop_QuanLyBanGiay.drawio", encoding="utf-8", xml_declaration=True)
    print("Generated perfect SoDoLop_QuanLyBanGiay.drawio!")

if __name__ == '__main__':
    build_perfect_drawio()

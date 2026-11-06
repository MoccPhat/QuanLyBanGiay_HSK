import xml.etree.ElementTree as ET
import sys
import os

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Root elements
mxfile = ET.Element('mxfile', {
    'host': 'app.diagrams.net',
    'agent': 'Mozilla/5.0',
    'version': '21.6.8',
    'type': 'device'
})
diagram = ET.SubElement(mxfile, 'diagram', {
    'id': 'ClassDiagram_ShoePOS_OOP',
    'name': 'SoDoLop_OOP_QuanLyBanGiay'
})
graph_model = ET.SubElement(diagram, 'mxGraphModel', {
    'dx': '1422',
    'dy': '850',
    'grid': '1',
    'gridSize': '10',
    'guides': '1',
    'tooltips': '1',
    'connect': '1',
    'arrows': '1',
    'fold': '1',
    'page': '1',
    'pageScale': '1',
    'pageWidth': '1500',
    'pageHeight': '1050',
    'math': '0',
    'shadow': '0'
})

root = ET.SubElement(graph_model, 'root')
ET.SubElement(root, 'mxCell', {'id': '0'})
ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

# Helper to add UML class
def add_uml_class(cell_id, title, attrs, methods, x, y, w, h, is_abstract=False):
    style_title = f"&lt;&lt;abstract&gt;&gt;&#10;&lt;b&gt;{title}&lt;/b&gt;" if is_abstract else f"&lt;b&gt;{title}&lt;/b&gt;"
    start_size = '36' if is_abstract else '28'
    swimlane_style = (
        f"swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;"
        f"horizontal=1;startSize={start_size};horizontalStack=0;resizeParent=1;resizeParentMax=0;"
        f"resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;"
        f"fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;rounded=0;"
    )
    
    # Swimlane
    c_swimlane = ET.SubElement(root, 'mxCell', {
        'id': str(cell_id),
        'value': style_title,
        'style': swimlane_style,
        'vertex': '1',
        'parent': '1'
    })
    geom = ET.SubElement(c_swimlane, 'mxGeometry', {
        'x': str(x),
        'y': str(y),
        'width': str(w),
        'height': str(h)
    })
    geom.set('as', 'geometry')
    
    # Attributes
    attr_lines = attrs.strip().split('\n')
    attr_h = len(attr_lines) * 18 + 12
    c_attr = ET.SubElement(root, 'mxCell', {
        'id': f"{cell_id}_attr",
        'value': attrs,
        'style': (
            "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;"
            "spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;"
            "points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
            "fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
        ),
        'vertex': '1',
        'parent': str(cell_id)
    })
    g_attr = ET.SubElement(c_attr, 'mxGeometry', {
        'y': str(start_size),
        'width': str(w),
        'height': str(attr_h)
    })
    g_attr.set('as', 'geometry')
    
    # Divider line
    div_y = int(start_size) + attr_h
    c_line = ET.SubElement(root, 'mxCell', {
        'id': f"{cell_id}_line",
        'value': '',
        'style': (
            "line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;"
            "spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;"
            "points=[];portConstraint=eastwest;strokeColor=#000000;"
        ),
        'vertex': '1',
        'parent': str(cell_id)
    })
    g_line = ET.SubElement(c_line, 'mxGeometry', {
        'y': str(div_y),
        'width': str(w),
        'height': '8'
    })
    g_line.set('as', 'geometry')
    
    # Methods
    meth_lines = methods.strip().split('\n')
    meth_h = len(meth_lines) * 18 + 12
    meth_y = div_y + 8
    c_meth = ET.SubElement(root, 'mxCell', {
        'id': f"{cell_id}_meth",
        'value': methods,
        'style': (
            "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;"
            "spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;"
            "points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
            "fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
        ),
        'vertex': '1',
        'parent': str(cell_id)
    })
    g_meth = ET.SubElement(c_meth, 'mxGeometry', {
        'y': str(meth_y),
        'width': str(w),
        'height': str(meth_h)
    })
    g_meth.set('as', 'geometry')

# Helper to add Edge
def add_edge(edge_id, source, target, label, arrow_type, exit_xy=None, entry_xy=None):
    if arrow_type == 'generalization':
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#000000;strokeWidth=1.2;startArrow=none;endArrow=block;endFill=0;"
        )
    elif arrow_type == 'composition':
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#000000;strokeWidth=1.2;startArrow=diamond;startFill=1;endArrow=none;"
        )
    else:  # association
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#000000;strokeWidth=1.2;startArrow=none;endArrow=none;"
        )
        
    props = {
        'id': str(edge_id),
        'value': label,
        'style': style,
        'edge': '1',
        'parent': '1',
        'source': str(source),
        'target': str(target)
    }
    if exit_xy:
        props['style'] += f"exitX={exit_xy[0]};exitY={exit_xy[1]};"
    if entry_xy:
        props['style'] += f"entryX={entry_xy[0]};entryY={entry_xy[1]};"
        
    c_edge = ET.SubElement(root, 'mxCell', props)
    g_edge = ET.SubElement(c_edge, 'mxGeometry', {'relative': '1'})
    g_edge.set('as', 'geometry')

# --- ĐỊNH NGHĨA 7 CLASS VỚI BỐ CỤC CỰC KỲ RỘNG RÃI & KHÔNG CẮT NHAU ---
# CỘT 1 (TRÁI): NGUOI (TRÊN) -> NHANVIEN & KHACHHANG (GIỮA) -> HOADON (DƯỚI)
# 1. NGUOI (Abstract)
add_uml_class(
    cell_id=10,
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
    x=210, y=50, w=330, h=250,
    is_abstract=True
)

# 2. NHAN_VIEN
add_uml_class(
    cell_id=20,
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
    ),
    x=50, y=360, w=290, h=220
)

# 3. KHACH_HANG
add_uml_class(
    cell_id=30,
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
    ),
    x=410, y=360, w=290, h=200
)

# 4. HOA_DON
add_uml_class(
    cell_id=40,
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
    ),
    x=190, y=660, w=330, h=250
)

# CỘT 2 (GIỮA DƯỚI): CHI TIẾT HÓA ĐƠN
# 5. CHI_TIET_HOA_DON
add_uml_class(
    cell_id=50,
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
    ),
    x=640, y=700, w=270, h=165
)

# CỘT 3 (PHẢI): CHI TIẾT GIÀY (DƯỚI) VÀ SẢN PHẨM (TRÊN)
# 6. CHI_TIET_GIAY (SKU)
add_uml_class(
    cell_id=60,
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
    ),
    x=1050, y=680, w=320, h=220
)

# 7. SAN_PHAM
add_uml_class(
    cell_id=70,
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
    ),
    x=1050, y=340, w=320, h=250
)

# --- CÁC ĐƯỜNG NỐI CHUẨN UML ĐẸP MẮT ---
# 1. Kế thừa: NhanVien extends Nguoi
add_edge(80, 20, 10, 'extends', 'generalization', exit_xy=(0.5, 0), entry_xy=(0.25, 1))

# 2. Kế thừa: KhachHang extends Nguoi
add_edge(81, 30, 10, 'extends', 'generalization', exit_xy=(0.5, 0), entry_xy=(0.75, 1))

# 3. Liên kết: NhanVien lập HoaDon (1 -- 0..*)
add_edge(82, 20, 40, '1          lập           0..*', 'association', exit_xy=(0.5, 1), entry_xy=(0.25, 0))

# 4. Liên kết: KhachHang mua HoaDon (0..1 -- 0..*)
add_edge(83, 30, 40, '0..1       mua           0..*', 'association', exit_xy=(0.5, 1), entry_xy=(0.75, 0))

# 5. Tổng thành: HoaDon ◆-- ChiTietHoaDon (1 -- 1..*)
add_edge(84, 40, 50, '1          chứa          1..*', 'composition', exit_xy=(1, 0.4), entry_xy=(0, 0.4))

# 6. Liên kết: ChiTietHoaDon bán ChiTietGiay (0..* -- 1)
add_edge(85, 50, 60, '0..*       bán           1', 'association', exit_xy=(1, 0.4), entry_xy=(0, 0.4))

# 7. Tổng thành: SanPham ◆-- ChiTietGiay (1 -- 1..*)
add_edge(86, 70, 60, '1          gồm           1..*', 'composition', exit_xy=(0.5, 1), entry_xy=(0.5, 0))

# Xuất file XML
tree = ET.ElementTree(mxfile)
target_path = r'e:\Project_HSK\SoDoLop_QuanLyBanGiay.drawio'
tree.write(target_path, encoding='utf-8', xml_declaration=True)
print(f"Successfully generated clean Draw.io diagram at: {target_path}")

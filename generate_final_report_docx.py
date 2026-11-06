import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def create_document():
    doc = docx.Document()
    
    # 1. Page Setup: Standard Academic A4 Margins (Left 3cm, Right 2cm, Top 2cm, Bottom 2cm)
    section = doc.sections[0]
    section.page_width = Inches(8.27)  # A4
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.79)   # 2 cm
    section.bottom_margin = Inches(0.79)# 2 cm
    section.left_margin = Inches(1.18)  # 3 cm
    section.right_margin = Inches(0.79) # 2 cm
    
    # Header & Footer setup
    header = section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_head = p_head.add_run("Báo cáo môn học: Lập trình hướng sự kiện với Java - Đề tài: Quản lý bán giày thời trang")
    r_head.font.name = "Times New Roman"
    r_head.font.size = Pt(8.5)
    r_head.font.italic = True
    r_head.font.color.rgb = RGBColor(100, 116, 139)
    
    footer = section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("Trường Đại học Công nghiệp TP.HCM (IUH) - Khoa Công nghệ Thông tin")
    r_foot.font.name = "Times New Roman"
    r_foot.font.size = Pt(8.5)
    r_foot.font.italic = True
    r_foot.font.color.rgb = RGBColor(100, 116, 139)

    # Styles helper
    def set_font(run, name="Times New Roman", size=13, bold=False, italic=False, color_rgb=(0, 0, 0)):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def add_p(text, bold_prefix="", italic_prefix="", space_before=2, space_after=4, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            set_font(r_b, bold=True)
        if italic_prefix:
            r_i = p.add_run(italic_prefix)
            set_font(r_i, italic=True)
        if text:
            r_t = p.add_run(text)
            set_font(r_t)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=14, bold=True, color_rgb=(30, 58, 138)) # Navy
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13, bold=True, color_rgb=(37, 99, 235)) # Blue
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13, bold=True, italic=True, color_rgb=(15, 23, 42))
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            set_font(r_b, bold=True)
        r_t = p.add_run(text)
        set_font(r_t)
        return p

    def add_callout(text, title="LƯU Ý NGHIỆP VỤ:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.3)
        
        # Light blue background
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(f"💡 {title} ")
        set_font(r1, bold=True, color_rgb=(37, 99, 235))
        r2 = p.add_run(text)
        set_font(r2, italic=True, color_rgb=(51, 65, 85))
        
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(4)

    def style_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'
        
        # Header Row
        hdr_row = table.rows[0]
        for idx, title in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.text = title
            cell.width = Inches(col_widths[idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="DBEAFE"/>')) # Light blue
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                set_font(r, size=11, bold=True, color_rgb=(30, 58, 138))
                
        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                cell.width = Inches(col_widths[c_idx])
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tcPr = cell._tc.get_or_add_tcPr()
                if bg_color != "FFFFFF":
                    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>'))
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or len(str(val)) < 12 else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    set_font(r, size=10.5, color_rgb=(30, 41, 59))

    # ==========================================
    # TRANG BÌA (COVER PAGE)
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("BỘ CÔNG THƯƠNG\nTRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP. HỒ CHÍ MINH\nKHOA CÔNG NGHỆ THÔNG TIN")
    set_font(r, size=13, bold=True, color_rgb=(15, 23, 42))
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub = p_sub.add_run("------------------***------------------")
    set_font(r_sub, size=11, color_rgb=(100, 116, 139))
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(8)
    r_t1 = p_title.add_run("BÁO CÁO MÔN HỌC\n")
    set_font(r_t1, size=16, bold=True, color_rgb=(30, 58, 138))
    r_t2 = p_title.add_run("LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA\n\n")
    set_font(r_t2, size=15, bold=True, color_rgb=(37, 99, 235))
    r_t3 = p_title.add_run("ĐỀ TÀI SỐ 3:\nHỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG\n(STEPUP FOOTWEAR POS SYSTEM)")
    set_font(r_t3, size=18, bold=True, color_rgb=(185, 28, 28)) # Dark Red
    
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.space_before = Pt(80)
    p_info.paragraph_format.space_after = Pt(4)
    p_info.paragraph_format.left_indent = Inches(1.5)
    
    r_info = p_info.add_run(
        "Giảng viên hướng dẫn:    ThS. Trần Thị Anh Thi\n"
        "Nhóm sinh viên thực hiện: Nguyễn Trọng Vinh      - 24704381 (Nhóm trưởng)\n"
        "                          Nhiêu Minh Kỳ          - 24718221\n"
        "                          Trần Tấn Kiệt          - 24695041\n"
        "                          Trần Mộc Tấn Phát      - 24638311\n"
        "Lớp học phần:             DHKTPM18A\n"
        "Khóa học:                 2022 - 2026\n"
        "Chuyên ngành:             Kỹ thuật Phần mềm"
    )
    set_font(r_info, size=12, bold=False, color_rgb=(30, 41, 59))
    
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(70)
    p_date.paragraph_format.space_after = Pt(0)
    r_date = p_date.add_run("Thành phố Hồ Chí Minh, Năm 2026")
    set_font(r_date, size=12, italic=True, color_rgb=(71, 85, 105))
    
    doc.add_page_break()

    # ==========================================
    # DANH SÁCH THÀNH VIÊN & NHẬN XÉT GIẢNG VIÊN
    # ==========================================
    add_h1("DANH SÁCH THÀNH VIÊN TRONG NHÓM THỰC HIỆN")
    t_members = doc.add_table(rows=5, cols=5)
    members_data = [
        ["1", "24704381", "Nguyễn Trọng Vinh", "Nhóm trưởng, Thiết kế CSDL & Tầng DAO", "100%"],
        ["2", "24718221", "Nhiêu Minh Kỳ", "Xây dựng Báo cáo Thống kê & Soạn thảo tài liệu", "100%"],
        ["3", "24695041", "Trần Tấn Kiệt", "Phân tích nghiệp vụ, Tầng BUS & Bắt lỗi Regex", "100%"],
        ["4", "24638311", "Trần Mộc Tấn Phát", "Thiết kế Giao diện POS & Xử lý sự kiện Swing", "100%"]
    ]
    style_table(t_members, [0.5, 1.2, 1.8, 2.2, 0.6], ["STT", "MSSV", "Họ và tên", "Nhiệm vụ phân công", "Đánh giá"], members_data)

    add_h1("LỜI CẢM ƠN")
    add_p("Trong suốt quá trình học tập và hoàn thành đồ án môn học Lập trình hướng sự kiện đối với công nghệ Java, nhóm chúng em đã nhận được sự quan tâm, giảng dạy tận tình và định hướng quý báu từ quý Thầy Cô trong Khoa Công nghệ Thông tin - Trường Đại học Công nghiệp TP.HCM (IUH).")
    add_p("Đặc biệt, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc nhất tới cô Trần Thị Anh Thi – Giảng viên trực tiếp giảng dạy và hướng dẫn học phần. Nhờ những bài giảng sinh động, tâm huyết cùng những chỉ dẫn chuyên môn thực tế của cô về lập trình hướng sự kiện, mô hình kiến trúc 3 lớp, kết nối cơ sở dữ liệu JDBC và thiết kế giao diện đồ họa người dùng, nhóm em đã có đủ kiến thức và tự tin để hoàn thành trọn vẹn đề tài 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang'.")
    add_p("Mặc dù nhóm đã nỗ lực hết mình với tinh thần học hỏi cao nhất, song do kiến thức và kinh nghiệm thực tiễn của sinh viên năm 3 còn có những giới hạn, đồ án chắc chắn khó tránh khỏi những thiếu sót nhất định. Nhóm chúng em rất mong nhận được những ý kiến đóng góp quý báu từ cô để đề tài được hoàn thiện tốt hơn nữa trong tương lai.")
    add_p("Kính chúc cô luôn dồi dào sức khỏe, hạnh phúc và gặt hái thêm nhiều thành công trên con đường nghiên cứu và giảng dạy!", italic_prefix="")

    add_h1("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN")
    t_eval = doc.add_table(rows=6, cols=3)
    eval_data = [
        ["1", "Tài liệu báo cáo (Rõ ràng, đầy đủ phân tích, sơ đồ lớp, CSDL, giao diện)", "........ / 2.0"],
        ["2", "Thiết kế Sơ đồ lớp (Class) và CSDL SQL Server (Đầy đủ ràng buộc)", "........ / 2.5"],
        ["3", "Hiện thực chức năng Bán hàng (POS) & Xử lý nghiệp vụ Size/Màu/Tồn kho", "........ / 3.0"],
        ["4", "Giao diện thân thiện, sử dụng phím tắt, Coding Convention Java", "........ / 1.5"],
        ["5", "Báo cáo thống kê doanh thu và trả lời phản biện", "........ / 1.0"]
    ]
    style_table(t_eval, [0.6, 4.5, 1.2], ["STT", "Tiêu chí đánh giá", "Điểm số"], eval_data)
    
    add_p("\nNhận xét chung của Giảng viên:\n.......................................................................................................................................................................................\n.......................................................................................................................................................................................\n.......................................................................................................................................................................................", space_before=4)
    p_sign = add_p("Thành phố Hồ Chí Minh, ngày ...... tháng ...... năm 2026\nChữ ký của Giảng viên hướng dẫn\n\n\n\nThS. Trần Thị Anh Thi", align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # ==========================================
    # MỤC LỤC & LỜI MỞ ĐẦU
    # ==========================================
    add_h1("MỤC LỤC BÁO CÁO")
    toc_items = [
        ("LỜI CẢM ƠN", "2"),
        ("DANH SÁCH THÀNH VIÊN VÀ NHẬN XÉT GIẢNG VIÊN", "2"),
        ("LỜI MỞ ĐẦU", "4"),
        ("DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU", "5"),
        ("PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU", "6"),
        ("    I. Lý do chọn đề tài", "6"),
        ("    II. Thu thập yêu cầu nghiệp vụ thực tế", "7"),
        ("    III. Tác nhân chính trong hệ thống", "8"),
        ("    IV. Phân tích yêu cầu chức năng và phi chức năng", "9"),
        ("PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP (CLASS DIAGRAM)", "11"),
        ("    I. Sơ đồ Class tổng thể hệ thống", "11"),
        ("    II. Mô tả các ràng buộc thuộc tính của các lớp đối tượng", "12"),
        ("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)", "17"),
        ("    I. Sơ đồ thực thể liên kết trên HQTCSDL SQL Server", "17"),
        ("    II. Mô tả chi tiết cấu trúc các bảng dữ liệu", "18"),
        ("    III. Cơ chế xử lý toàn vẹn dữ liệu nâng cao (Trigger & Transaction)", "22"),
        ("PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH", "24"),
        ("    I. Chức năng Đăng nhập & Phân quyền", "24"),
        ("    II. Chức năng Bán hàng tại quầy (POS - Nghiệp vụ trọng tâm)", "25"),
        ("    III. Chức năng Quản lý sản phẩm giày dép & Biến thể", "28"),
        ("    IV. Chức năng Quản lý khách hàng & Tích điểm", "30"),
        ("    V. Chức năng Thống kê doanh thu & Top sản phẩm bán chạy", "31"),
        ("    VI. Bảng hệ thống phím tắt & Điều hướng bán hàng", "33"),
        ("PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN", "34"),
        ("    I. Đánh giá kết quả đạt được và những hạn chế", "34"),
        ("    II. Hướng phát triển trong tương lai", "35"),
        ("    III. Lời kết", "36")
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        r1 = p_t.add_run(item)
        set_font(r1, size=11.5, bold=item.strip().startswith("PHẦN") or item.strip().startswith("LỜI"))
        # Add tab and page
        r_dots = p_t.add_run(" " + "." * (85 - len(item) * 2) + " ")
        set_font(r_dots, size=9, color_rgb=(148, 163, 184))
        r2 = p_t.add_run(page)
        set_font(r2, size=11, bold=True)

    add_h1("LỜI MỞ ĐẦU")
    add_p("Trong kỷ nguyên chuyển đổi số và thương mại hiện đại, việc ứng dụng công nghệ thông tin vào quản lý bán lẻ không còn là một lựa chọn xa xỉ mà đã trở thành điều kiện sống còn của các doanh nghiệp. Đối với ngành hàng thời trang, đặc biệt là kinh doanh giày dép, bài toán quản lý luôn chứa đựng những nét đặc thù phức tạp vượt trội so với các mô hình bán lẻ hàng hóa thông thường khác.")
    add_p("Nếu như một lon nước ngọt hay một cuốn sách chỉ có một mã vạch định danh duy nhất thì một đôi giày thời trang lại gắn liền với một ma trận biến thể: cùng một kiểu dáng nhưng có từ 8 đến 10 kích cỡ khác nhau (Size EU từ 35 đến 44) và nhiều phiên bản màu sắc (Trắng, Đen, Phối màu...). Nhân viên bán hàng tại quầy thu ngân không thể chỉ trả lời khách hàng rằng 'cửa hàng còn mẫu này', mà bắt buộc phải nắm rõ: 'Mẫu này ở Size 41 màu Trắng hiện tại trong kho còn chính xác bao nhiêu đôi?'.")
    add_p("Nhằm giải quyết triệt để bài toán hóc búa này, đề tài 'Hệ thống quản lý bán hàng tại cửa hàng giày dép thời trang (StepUp Footwear)' được nhóm chúng em xây dựng với định hướng chuyên sâu phục vụ nghiệp vụ tại quầy của nhân viên thu ngân và người quản lý cửa hàng (Desktop POS Application). Bằng việc mô hình hóa chuẩn xác cấu trúc sản phẩm 2 tầng (Mẫu giày cha -> Biến thể SKU con), kết hợp kiến trúc 3 lớp (3-Tier Architecture) trên nền tảng Java Swing và hệ quản trị cơ sở dữ liệu Microsoft SQL Server, hệ thống cam kết mang đến trải nghiệm thanh toán tốc độ cao, loại bỏ hoàn toàn hiện tượng bán âm kho và sai lệch số liệu doanh thu.")
    add_p("Báo cáo này được biên soạn với mục tiêu diễn giải toàn diện, rõ ràng từng khâu từ khảo sát yêu cầu, thiết kế kiến trúc đối tượng, sơ đồ cơ sở dữ liệu đến các bước thao tác trên màn hình thực tế, giúp quý Thầy Cô cùng các bạn sinh viên dễ dàng nắm bắt được cơ chế vận hành của hệ thống.")

    add_h1("DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU")
    figures = [
        ("Hình 1. Sơ đồ lớp hướng đối tượng (UML Class Diagram) hệ thống quản lý bán giày", "11"),
        ("Hình 2. Sơ đồ cơ sở dữ liệu quan hệ trên Microsoft SQL Server (Database ERD)", "17"),
        ("Hình 3. Minh họa thống kê doanh thu và phân tích top sản phẩm bán chạy", "32"),
        ("Hình 4. Giao diện Đăng nhập hệ thống và phân quyền vai trò (Login & RBAC)", "24"),
        ("Hình 5. Giao diện Bán hàng tại quầy POS (Tra cứu biến thể Size và Màu sắc)", "26"),
        ("Hình 6. Hóa đơn thanh toán bán lẻ nhiệt khổ K80 in trực tiếp từ hệ thống", "27"),
        ("Hình 7. Giao diện Quản lý danh mục sản phẩm và biến thể kích cỡ", "29"),
        ("Hình 8. Giao diện Quản lý khách hàng thân thiết và tích lũy điểm thưởng", "30")
    ]
    for fig_title, p_num in figures:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_before = Pt(1)
        p_f.paragraph_format.space_after = Pt(2)
        r1 = p_f.add_run(fig_title)
        set_font(r1, size=11, italic=True)
        r_dots = p_f.add_run(" " + "." * (85 - len(fig_title)) + " ")
        set_font(r_dots, size=9, color_rgb=(148, 163, 184))
        r2 = p_f.add_run(p_num)
        set_font(r2, size=11, bold=True)

    doc.add_page_break()

    # ==========================================
    # PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU
    # ==========================================
    add_h1("PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU")
    
    add_h2("I. Lý do chọn đề tài")
    add_p("Trong đời sống giới trẻ và xã hội hiện đại, giày dép thời trang không còn dừng lại ở vai trò là vật dụng che chở bàn chân mà đã vươn lên trở thành tuyên ngôn về gu thẩm mỹ và phong cách sống cá nhân. Nhu cầu mua sắm các dòng Sneaker năng động, giày thể thao chạy bộ, giày da công sở lịch lãm hay sandal trẻ trung không ngừng tăng trưởng mạnh mẽ, kéo theo sự bùng nổ của các cửa hàng bán lẻ thời trang giày dép.")
    add_p("Tuy nhiên, việc vận hành một cửa hàng giày dép lại tiềm ẩn nhiều khó khăn hơn các ngành hàng đóng gói sẵn:")
    add_bullet("Đặc thù biến thể SKU phức tạp: Mỗi mẫu giày sở hữu nhiều size (35 đến 44) và màu sắc khác nhau. Tồn kho của từng size là hoàn toàn riêng biệt. Khách hàng thử giày thường hỏi liên tục: 'Mẫu này có size 40 màu đen không em?'.", "1. ")
    add_bullet("Quản lý thủ công kém hiệu quả: Đa số cửa hàng quy mô vừa và nhỏ vẫn ghi chép sổ tay hoặc dùng Excel rời rạc. Nhân viên không biết size nào còn hay hết, phải chạy vào kho lục tìm mất 5-10 phút khiến khách hàng nản lòng bỏ đi.", "2. ")
    add_bullet("Ùn tắc thanh toán giờ cao điểm: Việc cộng tiền thủ công dễ sai lệch giá, nhầm chương trình khuyến mãi và làm khách hàng phải chờ đợi lâu tại quầy thu ngân.", "3. ")
    add_bullet("Thất thoát hàng hóa và thiếu dữ liệu khách hàng: Không kiểm soát được tình trạng nhân viên tự ý giảm giá, không có hệ thống tích điểm để giữ chân khách quen và người quản lý khó thống kê được đâu là mẫu giày 'hot' để nhập thêm hàng.", "4. ")
    add_p("Xuất phát từ thực tiễn trên, nhóm sinh viên chúng em đã chọn đề tài 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang' nhằm ứng dụng kiến thức chuyên môn của môn Lập trình hướng sự kiện Java để giải quyết triệt để các bất cập trong khâu bán hàng tại quầy.")

    add_h2("II. Thu thập yêu cầu nghiệp vụ thực tế")
    add_h3("1. Nghiệp vụ của nhân viên quầy thu ngân (POS)")
    add_bullet("Cần một màn hình POS trực quan, tốc độ xử lý tức thì, hỗ trợ tối đa việc dùng phím tắt (F10 thanh toán, F2 tìm kiếm, F3 nhập SĐT khách hàng) để thu ngân không cần rời tay khỏi bàn phím.", "Tốc độ và công thái học: ")
    add_bullet("Gõ tên hoặc quét mã là hệ thống hiển thị ngay danh sách các size (36-44) kèm màu sắc và số lượng tồn thực tế trong kho.", "Tra cứu biến thể theo size: ")
    add_bullet("Nhập số điện thoại là hệ thống tự hiển thị tên khách, hạng thẻ thành viên và số điểm tích lũy. Cho phép dùng điểm để trừ tiền trực tiếp trên đơn hàng hiện tại.", "Tích điểm và chăm sóc khách hàng: ")
    add_bullet("Tự động tính tổng tiền hàng, tiền khách đưa, tiền thừa phải thối lại; tự động trừ tồn kho theo đúng size/màu và in hóa đơn bán lẻ rõ ràng.", "Thanh toán và in hóa đơn: ")
    add_bullet("Hỗ trợ tra cứu lại hóa đơn cũ khi khách hàng mang giày đến đổi size trong thời hạn quy định (chính sách đổi hàng trong 7 ngày).", "Nghiệp vụ đổi trả hàng: ")

    add_h3("2. Nghiệp vụ của người quản lý cửa hàng (Store Manager)")
    add_bullet("Thêm mẫu giày mới, bổ sung các biến thể kích cỡ và màu sắc tương ứng, cập nhật giá nhập và giá bán niêm yết.", "Quản lý danh mục & biến thể: ")
    add_bullet("Cấp phát tài khoản đăng nhập cho nhân viên, phân quyền truy cập nghiêm ngặt (Thu ngân chỉ được bán hàng, không được xem báo cáo tài chính hay sửa giá sản phẩm).", "Quản lý nhân viên & Phân quyền: ")
    add_bullet("Theo dõi doanh thu theo ngày, theo tháng hoặc theo khoảng thời gian tùy chọn; xem biểu đồ trực quan về Top 5 mẫu giày bán chạy nhất và tỷ lệ tiêu thụ theo từng kích cỡ.", "Báo cáo thống kê kinh doanh: ")

    add_h3("3. Yêu cầu vận hành kinh doanh của cửa hàng")
    add_bullet("Ngăn chặn tuyệt đối tình trạng bán âm tồn kho (không cho phép bán số lượng vượt quá tồn kho thực tế của size đó).", "Kiểm soát kho hàng: ")
    add_bullet("Bảo toàn 100% dữ liệu lịch sử hóa đơn trong quá khứ. Khi ngừng kinh doanh một mẫu giày, hệ thống áp dụng kỹ thuật Xóa mềm (Soft-Delete) chứ không xóa cứng khỏi cơ sở dữ liệu.", "Toàn vẹn số liệu tài chính: ")

    add_h2("III. Tác nhân chính trong hệ thống (Actors)")
    add_p("Hệ thống xác định rõ 3 tác nhân tham gia tương tác:")
    add_bullet("Người trực tiếp sử dụng máy POS tại quầy để tra cứu tồn kho giày, lập hóa đơn, nhận tiền từ khách và in hóa đơn bán lẻ.", "1. Nhân viên thu ngân (Staff / Cashier): ")
    add_bullet("Người nắm toàn quyền điều hành hệ thống: quản lý danh mục sản phẩm, biến thể kho hàng, hồ sơ nhân sự, tài khoản và theo dõi các báo cáo doanh thu tổng hợp.", "2. Người quản lý (Admin / Store Manager): ")
    add_bullet("Tác nhân ngoài thụ hưởng dịch vụ mua sắm tại cửa hàng, được cấp mã thành viên theo số điện thoại để tích lũy điểm thưởng và hưởng các chính sách ưu đãi.", "3. Khách hàng (Customer): ")

    add_h2("IV. Phân tích yêu cầu hệ thống")
    add_h3("1. Yêu cầu chức năng")
    add_p("Hệ thống phân rã thành các phân hệ chức năng rõ ràng:")
    add_bullet("Xác thực thông tin tài khoản và điều hướng giao diện phù hợp với vai trò (Admin hoặc Staff).", "Phân hệ Đăng nhập: ")
    add_bullet("Tìm kiếm sản phẩm theo tên hoặc quét mã, chọn biến thể size/màu, hiển thị tồn kho, thêm vào giỏ, áp dụng tích điểm thành viên, tính tiền thừa, thanh toán và in hóa đơn K80.", "Phân hệ Bán hàng (POS): ")
    add_bullet("Thêm, sửa, tìm kiếm nâng cao, lọc theo loại/hãng/size, cập nhật số lượng tồn kho theo biến thể, ngừng kinh doanh sản phẩm.", "Phân hệ Quản lý sản phẩm: ")
    add_bullet("Quản lý danh sách thành viên, cập nhật thông tin cá nhân, tra cứu lịch sử mua hàng và quản lý điểm thưởng tích lũy.", "Phân hệ Quản lý khách hàng: ")
    add_bullet("Quản lý danh sách nhân viên, thông tin lương cơ bản, cấp phát và khóa tài khoản đăng nhập.", "Phân hệ Quản lý nhân viên: ")
    add_bullet("Báo cáo doanh thu theo mốc thời gian, thống kê số lượng giày đã bán ra, vẽ biểu đồ Top sản phẩm và xuất file Excel.", "Phân hệ Thống kê: ")

    add_h3("2. Yêu cầu phi chức năng")
    add_bullet("Thời gian phản hồi tìm kiếm tức thì dưới 0.5 giây; thời gian thực thi giao dịch thanh toán và in hóa đơn dưới 1 giây.", "Hiệu năng xử lý: ")
    add_bullet("Áp dụng JDBC Transaction để đảm bảo tính toàn vẹn (ACID): thêm hóa đơn, thêm chi tiết và trừ tồn kho phải thành công đồng thời, nếu một bước lỗi thì rollback toàn bộ.", "An toàn dữ liệu & Concurrency: ")
    add_bullet("Giao diện đồ họa Swing FlatLaf hiện đại, trực quan, hỗ trợ 100% thao tác bàn phím thông qua các phím tắt chuyên dụng.", "Tính dễ dùng & Công thái học: ")

    add_callout("Quy trình bán hàng chuẩn 6 bước: [1] Tiếp nhận mẫu giày -> [2] Tra cứu tồn kho theo size/màu -> [3] Thêm vào giỏ hàng -> [4] Nhập SĐT tích điểm -> [5] Nhập tiền khách đưa & kiểm tra tiền thừa -> [6] Nhấn F10 thanh toán, trừ kho và in hóa đơn K80.", "CHUỖI HÀNH ĐỘNG CỐT LÕI TẠI QUẦY:")

    doc.add_page_break()

    # ==========================================
    # PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)
    # ==========================================
    add_h1("PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)")
    add_h2("I. Kiến trúc Sơ đồ lớp tổng thể theo chuẩn OOP")
    add_p("Khác với cách tiếp cận ánh xạ phẳng từ các bảng cơ sở dữ liệu vật lý, sơ đồ lớp của hệ thống được nhóm chúng em thiết kế chuẩn mực theo đúng 4 trụ cột của Lập trình hướng đối tượng (OOP: Kế thừa, Đóng gói, Trừu tượng và Đa hình). Đồng thời, sơ đồ tập trung vào 7 lớp đối tượng quan trọng nhất, gắn liền trực tiếp với bản sắc của bài toán Quản lý bán hàng giày dép thời trang, lược bỏ bớt các lớp cấu hình phụ trợ để bức tranh nghiệp vụ trở nên mạch lạc, rõ ràng và dễ bảo vệ trước Hội đồng chấm thi.")
    
    if os.path.exists("SoDoLop_QuanLyBanGiay.png"):
        doc.add_picture("SoDoLop_QuanLyBanGiay.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 1. Sơ đồ lớp thực thể hướng đối tượng (OOP Entity Class Diagram) chuẩn UML")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))
    elif os.path.exists("diagram_class_shoe.png"):
        doc.add_picture("diagram_class_shoe.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 1. Sơ đồ lớp thực thể hướng đối tượng (OOP Entity Class Diagram) chuẩn UML")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("II. Phân tích 4 đặc trưng Hướng đối tượng (OOP) áp dụng trong hệ thống")
    add_bullet("Hệ thống xây dựng lớp cơ sở trừu tượng Nguoi (Person) gom chung các thuộc tính nhân thân (hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email). Cả NhanVien và KhachHang đều kế thừa từ Nguoi thông qua mối quan hệ Tổng quát hóa (Generalization ──▷). Điều này giúp tái sử dụng mã nguồn tối đa và phản ánh đúng bản chất thế giới thực.", "1. Tính Kế thừa (Inheritance): ")
    add_bullet("Toàn bộ thuộc tính trong các lớp đều được đặt ở mức truy cập Private (-). Việc đọc và ghi dữ liệu ra bên ngoài bắt buộc phải thông qua các phương thức Getter/Setter công khai (+), kèm theo các logic kiểm tra tính hợp lệ (Validation) như kiểm tra số điện thoại đúng đầu số mạng Việt Nam, kiểm tra tuổi lao động >= 18, kiểm tra tồn kho không âm.", "2. Tính Đóng gói (Encapsulation): ")
    add_bullet("Lớp Nguoi là lớp trừu tượng (abstract class) khai báo phương thức trừu tượng getThongTin(). Cả hai lớp con NhanVien và KhachHang bắt buộc phải Override (ghi đè) phương thức này để xuất ra thông tin tóm tắt tương ứng với vai trò của mình. Ngoài ra, các hàm toString(), equals(), hashCode() cũng được cài đặt đa hình.", "3. Tính Trừu tượng & Đa hình (Abstraction & Polymorphism): ")
    add_bullet("Hệ thống thể hiện rõ sự khác biệt giữa hai cấp độ sở hữu: Quan hệ Tổng thành chặt chẽ (Composition ◆──) được áp dụng giữa SanPham ◆── ChiTietGiay (Một mẫu giày sở hữu các biến thể size/màu) và HoaDon ◆── ChiTietHoaDon (Hóa đơn sở hữu các dòng hàng). Khi đối tượng cha bị hủy thì các đối tượng con thành phần không tồn tại độc lập. Trong khi đó, quan hệ giữa NhanVien, KhachHang và HoaDon là quan hệ Liên kết (Association ──).", "4. Quan hệ Tổng thành (Composition) & Liên kết (Association): ")

    add_callout("Chiến lược ánh xạ giữa OOP và CSDL SQL Server: Ở tầng ứng dụng Java, NhanVien và KhachHang kế thừa lớp Nguoi. Khi lưu xuống CSDL quan hệ, nhóm áp dụng chiến lược 'Table per Concrete Class' (tạo 2 bảng vật lý độc lập là NhanVien và KhachHang) để tối ưu hóa tốc độ truy vấn SELECT/JOIN khi bán hàng tại quầy POS mà không cần JOIN qua bảng trung gian.", "LƯU Ý VỀ ÁNH XẠ KIẾN TRÚC:");

    add_h2("III. Mô tả chi tiết 7 Lớp đối tượng quan trọng cốt lõi")
    
    # Table 1: Nguoi (Abstract)
    add_h3("1. Lớp trừu tượng Nguoi (Lớp cơ sở nhân thân)")
    add_p("Lớp cha đại diện cho con người tham gia vào hoạt động của cửa hàng, định nghĩa cấu trúc dữ liệu và hành vi dùng chung.")
    t_ng = doc.add_table(rows=7, cols=5)
    ng_data = [
        ["1", "hoTen", "String", "Không rỗng, Độ dài từ 3 - 50 ký tự", "Họ và tên đầy đủ theo tiếng Việt"],
        ["2", "soDienThoai", "String", "Không rỗng, Chuẩn 10 số (03/05/07/08/09)", "Số điện thoại liên lạc chính"],
        ["3", "ngaySinh", "LocalDate", "Không rỗng, Phải trước ngày hiện tại", "Ngày tháng năm sinh"],
        ["4", "gioiTinh", "boolean", "Không rỗng, True: Nam, False: Nữ", "Giới tính sinh học"],
        ["5", "diaChi", "String", "Có thể rỗng, Tối đa 200 ký tự", "Địa chỉ cư trú hoặc thường trú"],
        ["6", "email", "String", "Có thể rỗng, Đúng chuẩn RFC định dạng email", "Địa chỉ thư điện tử liên hệ"]
    ]
    style_table(t_ng, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ng_data)

    # Table 2: NhanVien (extends Nguoi)
    add_h3("2. Lớp NhanVien (Nhân sự - Kế thừa từ Nguoi)")
    add_p("Lớp kế thừa lớp Nguoi, bổ sung các thuộc tính và hành vi nghiệp vụ dành riêng cho nhân viên thu ngân và quản lý cửa hàng.")
    t_nv = doc.add_table(rows=6, cols=5)
    nv_data = [
        ["1", "maNhanVien", "String", "PK, Không rỗng, Regex: ^NV[0-9]{4}$", "Mã định danh nhân viên (NV0001, NV0002...)"],
        ["2", "chucVu", "String", "Không rỗng, {'Quản lý', 'Nhân viên bán hàng'}", "Vị trí công tác tại cửa hàng"],
        ["3", "luongCoBan", "double", "Không rỗng, Giá trị >= 3.000.000 VNĐ", "Mức lương cơ bản thỏa thuận"],
        ["4", "caLamViec", "String", "Không rỗng, {'Ca sáng', 'Ca chiều', 'Ca tối'}", "Ca trực bán hàng trong ngày"],
        ["5", "trangThai", "boolean", "Không rỗng, True: Đang làm, False: Đã nghỉ", "Trạng thái lao động tại shop"]
    ]
    style_table(t_nv, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], nv_data)

    # Table 3: KhachHang (extends Nguoi)
    add_h3("3. Lớp KhachHang (Khách hàng thân thiết - Kế thừa từ Nguoi)")
    add_p("Lớp kế thừa lớp Nguoi, quản lý thông tin tích điểm, xếp hạng thành viên và tính toán mức chiết khấu ưu đãi.")
    t_kh = doc.add_table(rows=5, cols=5)
    kh_data = [
        ["1", "maKhachHang", "String", "PK, Không rỗng, Regex: ^KH[0-9]{4}$", "Mã khách hàng thành viên (KH0001...)"],
        ["2", "diemTichLuy", "int", "Không rỗng, Giá trị >= 0, Mặc định 0", "Điểm thưởng (1 điểm quy đổi = 1.000 VNĐ)"],
        ["3", "hangThanhVien", "String", "Không rỗng, {'Đồng', 'Bạc', 'Vàng', 'Kim Cương'}", "Hạng thẻ tính theo tổng tiền mua sắm"],
        ["4", "ngayDangKy", "LocalDate", "Không rỗng, Mặc định ngày hiện tại", "Ngày đăng ký làm thẻ thành viên"]
    ]
    style_table(t_kh, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], kh_data)

    # Table 4: SanPham
    add_h3("4. Lớp SanPham (Thông tin mẫu giày thời trang)")
    add_p("Lớp cha tổng quát đại diện cho một model/mẫu giày thời trang trước khi phân tách kích cỡ.")
    t_sp = doc.add_table(rows=9, cols=5)
    sp_data = [
        ["1", "maSanPham", "String", "PK, Không rỗng, Regex: ^SP[0-9]{4}$", "Mã định danh mẫu giày (SP0001...)"],
        ["2", "tenSanPham", "String", "Không rỗng, Độ dài từ 5 - 150 ký tự", "Tên thương mại của đôi giày"],
        ["3", "loaiGiay", "String", "Không rỗng, {'Sneaker', 'Sandal', 'Giày Da'}", "Phân loại phong cách giày"],
        ["4", "thuongHieu", "String", "Không rỗng, Tối đa 50 ký tự", "Nhãn hàng sản xuất (Nike, Adidas, Biti's...)"],
        ["5", "giaNhap", "double", "Không rỗng, Giá trị > 0", "Giá nhập sỉ từ nhà sản xuất"],
        ["6", "giaBan", "double", "Không rỗng, giaBan >= giaNhap * 1.1", "Giá bán lẻ niêm yết tại quầy"],
        ["7", "chatLieu", "String", "Có thể rỗng, Tối đa 100 ký tự", "Chất liệu (Da thật, Vải lưới Canvas, Cao su)"],
        ["8", "trangThai", "boolean", "Không rỗng, Mặc định true", "True: Đang bán, False: Ngừng kinh doanh"]
    ]
    style_table(t_sp, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], sp_data)

    # Table 5: ChiTietGiay (Biến thể SKU Size/Màu)
    add_h3("5. Lớp ChiTietGiay (Biến thể SKU: Kích cỡ & Màu sắc)")
    add_p("Lớp cốt lõi giải quyết bài toán nghiệp vụ giày dép: mỗi mẫu giày có nhiều size và màu sắc với số lượng tồn kho riêng biệt.")
    t_ctg = doc.add_table(rows=7, cols=5)
    ctg_data = [
        ["1", "maChiTietGiay", "String", "PK, Không rỗng, Regex: ^CTG[0-9]{5}$", "Mã SKU chi tiết (CTG00001...)"],
        ["2", "sanPham", "SanPham", "FK, Không rỗng, Quan hệ Composition", "Mẫu giày cha sở hữu biến thể này"],
        ["3", "kichThuoc", "int", "Không rỗng, Thuộc đoạn [35, 45]", "Kích cỡ giày chuẩn EU"],
        ["4", "mauSac", "String", "Không rỗng, Độ dài 2 - 30 ký tự", "Màu sắc (Trắng, Đen, Xám, Đỏ, Phối màu)"],
        ["5", "soLuongTon", "int", "Không rỗng, Giá trị >= 0, Mặc định 0", "Số lượng đôi giày còn lại trong kho"],
        ["6", "hinhAnh", "String", "Có thể rỗng, Đường dẫn ảnh hợp lệ", "Ảnh chụp thực tế góc cạnh đôi giày"]
    ]
    style_table(t_ctg, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ctg_data)
    add_callout("Ràng buộc duy nhất (Unique Constraint): Cặp thuộc tính (sanPham, kichThuoc, mauSac) là duy nhất nhằm bảo đảm không bao giờ xảy ra tình trạng tạo trùng 2 biến thể cùng size và màu cho một mẫu giày.", "RÀNG BUỘC BIẾN THỂ:");

    # Table 6: HoaDon
    add_h3("6. Lớp HoaDon (Phiếu bán hàng POS)")
    add_p("Lớp quản lý giao dịch thanh toán mua bán giày tại quầy thu ngân.")
    t_hd = doc.add_table(rows=10, cols=5)
    hd_data = [
        ["1", "maHoaDon", "String", "PK, Không rỗng, Regex: ^HD[0-9]{6}$", "Mã hóa đơn duy nhất (HD000001...)"],
        ["2", "ngayLap", "LocalDateTime", "Không rỗng, <= Thời điểm hiện tại", "Thời gian chính xác xuất đơn hàng"],
        ["3", "nhanVien", "NhanVien", "FK, Không rỗng, Nhân viên lập phiếu", "Thu ngân phụ trách ca bán"],
        ["4", "khachHang", "KhachHang", "FK, Có thể rỗng (Khách vãng lai)", "Khách hàng mua (để tích điểm)"],
        ["5", "tongTien", "double", "Không rỗng, Giá trị >= 0", "Tổng số tiền thực khách cần thanh toán"],
        ["6", "phuongThucTT", "String", "Không rỗng, {'Tiền mặt', 'Chuyển khoản'}", "Hình thức giao dịch"],
        ["7", "tienKhachDua", "double", "Không rỗng, tienKhachDua >= tongTien", "Số tiền mặt khách đưa tại quầy"],
        ["8", "tienThua", "double", "Không rỗng, tienThua = tienKhachDua - tongTien", "Tiền thừa thối lại cho khách"],
        ["9", "danhSachChiTiet", "List<ChiTietHoaDon>", "Không rỗng khi hoàn tất thanh toán", "Danh sách các đôi giày đã bán (Composition)"]
    ]
    style_table(t_hd, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], hd_data)

    # Table 7: ChiTietHoaDon
    add_h3("7. Lớp ChiTietHoaDon (Dòng sản phẩm đã bán)")
    add_p("Lớp trung gian thể hiện từng biến thể đôi giày (kèm size/màu cụ thể) được bán ra trong hóa đơn.")
    t_cthd = doc.add_table(rows=7, cols=5)
    cthd_data = [
        ["1", "hoaDon", "HoaDon", "PK, FK, Không rỗng", "Hóa đơn chứa dòng hàng này"],
        ["2", "chiTietGiay", "ChiTietGiay", "PK, FK, Không rỗng", "Đúng biến thể size/màu giày đã xuất kho"],
        ["3", "soLuong", "int", "Không rỗng, 0 < soLuong <= soLuongTon", "Số lượng bán (kiểm tra tồn kho trước khi lưu)"],
        ["4", "donGia", "double", "Không rỗng, Giá trị > 0", "Đơn giá niêm yết tại thời điểm bán"],
        ["5", "giamGia", "double", "Không rỗng, Giá trị >= 0", "Tiền giảm trừ trực tiếp hoặc chiết khấu thẻ"],
        ["6", "thanhTien", "double", "thanhTien = (soLuong * donGia) - giamGia", "Thành tiền thực tế của dòng hàng"]
    ]
    style_table(t_cthd, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], cthd_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU
    # ==========================================
    add_h1("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)")
    add_h2("I. Sơ đồ thực thể liên kết trên HQTCSDL Microsoft SQL Server")
    add_p("Cơ sở dữ liệu được thiết kế đạt chuẩn chuẩn hóa 3NF (Third Normal Form), đảm bảo không dư thừa dữ liệu, duy trì tính toàn vẹn tham chiếu thông qua các ràng buộc Khóa chính (Primary Key), Khóa ngoại (Foreign Key) và các ràng buộc toàn vẹn CHECK.")
    
    if os.path.exists("diagram_erd_shoe.png"):
        doc.add_picture("diagram_erd_shoe.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 2. Sơ đồ cơ sở dữ liệu quan hệ trên Microsoft SQL Server (Database ERD)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("II. Mô tả chi tiết cấu trúc các bảng dữ liệu (Data Dictionary)")
    add_p("Chi tiết 9 bảng vật lý được cài đặt trên hệ quản trị Microsoft SQL Server:")

    # Tables in DB
    tables_db = [
        ("Bảng LoaiGiay", [
            ["MaLoai", "VARCHAR(10)", "PK", "No", "Mã phân loại giày (LG001...)"],
            ["TenLoai", "NVARCHAR(50)", "None", "No", "Tên loại giày (UNIQUE)"],
            ["MoTa", "NVARCHAR(255)", "None", "Yes", "Ghi chú đặc điểm loại giày"]
        ]),
        ("Bảng ThuongHieu", [
            ["MaThuongHieu", "VARCHAR(10)", "PK", "No", "Mã thương hiệu (TH001...)"],
            ["TenThuongHieu", "NVARCHAR(50)", "None", "No", "Tên thương hiệu (UNIQUE)"],
            ["QuocGia", "NVARCHAR(50)", "None", "Yes", "Quốc gia xuất xứ nhãn hàng"],
            ["Website", "VARCHAR(100)", "None", "Yes", "Website chính hãng"]
        ]),
        ("Bảng SanPham", [
            ["MaSanPham", "VARCHAR(10)", "PK", "No", "Mã mẫu giày cha (SP0001...)"],
            ["TenSanPham", "NVARCHAR(100)", "None", "No", "Tên mẫu giày thời trang"],
            ["MaLoai", "VARCHAR(10)", "FK", "No", "Tham chiếu LoaiGiay(MaLoai)"],
            ["MaThuongHieu", "VARCHAR(10)", "FK", "No", "Tham chiếu ThuongHieu(MaThuongHieu)"],
            ["XuatXu", "NVARCHAR(50)", "None", "Yes", "Nước sản xuất"],
            ["ChatLieu", "NVARCHAR(100)", "None", "Yes", "Chất liệu (Da, Canvas, Mesh...)"],
            ["GiaNhap", "DECIMAL(18,2)", "None", "No", "CHECK (GiaNhap > 0)"],
            ["GiaBan", "DECIMAL(18,2)", "None", "No", "CHECK (GiaBan >= GiaNhap)"],
            ["HinhAnh", "VARCHAR(255)", "None", "Yes", "Đường dẫn ảnh đại diện"],
            ["TrangThai", "BIT", "None", "No", "DEFAULT 1 (1: Kinh doanh, 0: Ngừng)"]
        ]),
        ("Bảng ChiTietGiay (Biến thể SKU)", [
            ["MaChiTietGiay", "VARCHAR(10)", "PK", "No", "Mã biến thể SKU (CTG00001...)"],
            ["MaSanPham", "VARCHAR(10)", "FK", "No", "Tham chiếu SanPham(MaSanPham)"],
            ["KichThuoc", "INT", "None", "No", "CHECK (KichThuoc BETWEEN 35 AND 45)"],
            ["MauSac", "NVARCHAR(30)", "None", "No", "Màu sắc (Trắng, Đen, Xám...)"],
            ["SoLuongTon", "INT", "None", "No", "CHECK (SoLuongTon >= 0), DEFAULT 0"],
            ["HinhAnhBienThe", "VARCHAR(255)", "None", "Yes", "Đường dẫn ảnh biến thể màu"],
            ["TrangThai", "BIT", "None", "No", "DEFAULT 1 (1: Khả dụng)"]
        ]),
        ("Bảng KhachHang", [
            ["MaKhachHang", "VARCHAR(10)", "PK", "No", "Mã khách hàng (KH0001...)"],
            ["HoTen", "NVARCHAR(50)", "None", "No", "Họ và tên khách hàng"],
            ["SoDienThoai", "VARCHAR(10)", "None", "No", "UNIQUE, CHECK (LEN=10)"],
            ["Email", "VARCHAR(50)", "None", "Yes", "Hòm thư điện tử"],
            ["DiaChi", "NVARCHAR(200)", "None", "Yes", "Địa chỉ liên lạc"],
            ["DiemTichLuy", "INT", "None", "No", "CHECK (DiemTichLuy >= 0), DEFAULT 0"],
            ["NgayDangKy", "DATE", "None", "No", "DEFAULT GETDATE()"]
        ]),
        ("Bảng NhanVien", [
            ["MaNhanVien", "VARCHAR(10)", "PK", "No", "Mã nhân viên (NV0001...)"],
            ["HoTen", "NVARCHAR(50)", "None", "No", "Họ tên đầy đủ"],
            ["NgaySinh", "DATE", "None", "No", "CHECK (DATEDIFF(YEAR, NgaySinh, GETDATE()) >= 18)"],
            ["GioiTinh", "BIT", "None", "No", "1: Nam, 0: Nữ"],
            ["SoDienThoai", "VARCHAR(10)", "None", "No", "UNIQUE, CHECK (LEN=10)"],
            ["DiaChi", "NVARCHAR(200)", "None", "No", "Nơi thường trú"],
            ["ChucVu", "NVARCHAR(30)", "None", "No", "CHECK ('Quản lý', 'Nhân viên bán hàng')"],
            ["LuongCoBan", "DECIMAL(18,2)", "None", "No", "CHECK (LuongCoBan >= 3000000)"],
            ["TrangThai", "BIT", "None", "No", "DEFAULT 1 (1: Đang làm, 0: Đã nghỉ)"]
        ]),
        ("Bảng TaiKhoan", [
            ["TenDangNhap", "VARCHAR(10)", "PK, FK", "No", "Tham chiếu NhanVien(MaNhanVien)"],
            ["MatKhau", "VARCHAR(100)", "None", "No", "Mật khẩu đã mã hóa"],
            ["QuyenHan", "VARCHAR(20)", "None", "No", "CHECK ('ADMIN', 'STAFF')"],
            ["NgayTao", "DATE", "None", "No", "DEFAULT GETDATE()"],
            ["TrangThai", "BIT", "None", "No", "DEFAULT 1 (1: Mở khóa, 0: Khóa)"]
        ]),
        ("Bảng HoaDon", [
            ["MaHoaDon", "VARCHAR(10)", "PK", "No", "Mã hóa đơn (HD000001...)"],
            ["NgayLap", "DATETIME", "None", "No", "DEFAULT GETDATE()"],
            ["MaNhanVien", "VARCHAR(10)", "FK", "No", "Tham chiếu NhanVien(MaNhanVien)"],
            ["MaKhachHang", "VARCHAR(10)", "FK", "Yes", "Tham chiếu KhachHang(MaKhachHang)"],
            ["TongTien", "DECIMAL(18,2)", "None", "No", "CHECK (TongTien >= 0)"],
            ["PhuongThuc", "NVARCHAR(30)", "None", "No", "CHECK ('Tiền mặt', 'Chuyển khoản')"],
            ["TienKhachDua", "DECIMAL(18,2)", "None", "No", "Số tiền khách đưa"],
            ["TienThua", "DECIMAL(18,2)", "None", "No", "Tiền thối lại cho khách"],
            ["GhiChu", "NVARCHAR(255)", "None", "Yes", "Ghi chú đơn hàng"],
            ["TrangThai", "NVARCHAR(30)", "None", "No", "DEFAULT N'Đã thanh toán'"]
        ]),
        ("Bảng ChiTietHoaDon", [
            ["MaHoaDon", "VARCHAR(10)", "PK, FK", "No", "Tham chiếu HoaDon(MaHoaDon)"],
            ["MaChiTietGiay", "VARCHAR(10)", "PK, FK", "No", "Tham chiếu ChiTietGiay(MaChiTietGiay)"],
            ["SoLuong", "INT", "None", "No", "CHECK (SoLuong > 0)"],
            ["DonGia", "DECIMAL(18,2)", "None", "No", "CHECK (DonGia > 0)"],
            ["GiamGia", "DECIMAL(18,2)", "None", "No", "CHECK (GiamGia >= 0), DEFAULT 0"],
            ["ThanhTien", "DECIMAL(18,2)", "None", "No", "CHECK (ThanhTien >= 0)"]
        ])
    ]

    for t_name, rows_info in tables_db:
        add_h3(t_name)
        t_elem = doc.add_table(rows=len(rows_info) + 1, cols=5)
        style_table(t_elem, [1.5, 1.2, 0.7, 0.7, 2.2], ["Tên cột", "Kiểu dữ liệu", "Khóa", "Null", "Ràng buộc & Mô tả"], rows_info)

    add_h2("III. Cơ chế xử lý toàn vẹn dữ liệu nâng cao trên SQL Server")
    add_h3("1. Database Triggers tự động cập nhật tồn kho")
    add_p("Hệ thống cài đặt Trigger trực tiếp trong SQL Server để đảm bảo tính nhất quán tuyệt đối giữa Hóa đơn và Kho hàng:")
    add_bullet("Trigger TRG_ChiTietHoaDon_Insert: Tự động kiểm tra tồn kho trước khi ghi nhận dòng hàng. Nếu số lượng mua vượt quá số lượng tồn hiện có, Trigger sẽ phát lệnh RAISERROR và ROLLBACK TRANSACTION để hủy giao dịch. Nếu hợp lệ, tự động thực thi UPDATE ChiTietGiay SET SoLuongTon = SoLuongTon - i.SoLuong.", "Trừ kho tự động: ")
    add_bullet("Trigger TRG_ChiTietHoaDon_Delete: Khi có yêu cầu hủy hóa đơn hoặc đổi trả hàng, Trigger sẽ tự động cộng hoàn trả số lượng giày vào kho: UPDATE ChiTietGiay SET SoLuongTon = SoLuongTon + d.SoLuong.", "Hoàn kho khi hủy đơn: ")

    add_h3("2. Quản lý JDBC Transaction & Chống bán âm kho (Concurrency)")
    add_p("Trong giờ cao điểm, tình huống có thể xảy ra: Một đôi giày size 40 chỉ còn đúng 1 đôi duy nhất trong kho, nhưng cả 2 quầy thu ngân cùng thêm vào giỏ và nhấn thanh toán đồng thời. Nếu không kiểm soát, hệ thống sẽ trừ 2 lần dẫn đến tồn kho bị âm (-1).")
    add_p("Nhóm chúng em xử lý bằng JDBC Transaction nguyên tử tại tầng DAO:")
    add_bullet("Thiết lập conn.setAutoCommit(false) trước khi thực hiện chuỗi thao tác lưu hóa đơn.", "Tắt Auto-Commit: ")
    add_bullet("Dùng câu lệnh UPDATE có điều kiện kiểm tra tồn: UPDATE ChiTietGiay SET SoLuongTon = SoLuongTon - ? WHERE MaChiTietGiay = ? AND SoLuongTon >= ?. Nếu rowsAffected == 0, lập tức conn.rollback() và ném thông báo: 'Đôi giày size này vừa được quầy khác thanh toán, kho đã hết hàng!'.", "Khóa nguyên tử: ")
    add_bullet("Khi toàn bộ hóa đơn và các dòng chi tiết được ghi thành công, mới gọi conn.commit().", "Commit đồng bộ: ")

    add_h3("3. Chiến lược Xóa mềm (Soft-Delete Pattern)")
    add_p("Nếu người quản lý xóa một mẫu giày bằng lệnh DELETE vật lý, SQL Server sẽ báo lỗi khóa ngoại FK Constraint Error 547 vì sản phẩm đó đã từng xuất hiện trong các hóa đơn bán hàng cũ. Nếu dùng CASCADE DELETE, hệ thống sẽ xóa sạch các hóa đơn cũ, làm sai lệch toàn bộ báo cáo doanh thu tài chính.")
    add_p("Giải pháp của nhóm: Toàn bộ bảng SanPham và ChiTietGiay đều có cột TrangThai (BIT). Khi người quản lý chọn xóa, hệ thống chỉ cập nhật TrangThai = 0. Màn hình bán hàng chỉ truy vấn WHERE TrangThai = 1, đôi giày sẽ không còn xuất hiện tại quầy thu ngân nhưng toàn bộ hóa đơn và doanh thu trong quá khứ vẫn được bảo toàn nguyên vẹn 100%.")

    doc.add_page_break()

    # ==========================================
    # PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN
    # ==========================================
    add_h1("PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH")
    
    add_h2("I. Chức năng Đăng nhập & Phân quyền truy cập (Login & RBAC)")
    add_p("Giao diện Đăng nhập là cửa ngõ bảo vệ của hệ thống, thiết kế theo chuẩn FlatLaf hiện đại với khung hình chữ nhật nổi bật giữa màn hình.")
    add_bullet("Nhân viên khởi chạy ứng dụng. Con trỏ chuột tự động focus sẵn vào ô 'Tên đăng nhập' (Mã nhân viên, vd: NV0001 hoặc QL0001).", "Bước 1 - Mở ứng dụng: ")
    add_bullet("Nhân viên nhập mã tài khoản và nhấn Tab để chuyển xuống ô 'Mật khẩu'. Trường mật khẩu sử dụng JPasswordField với icon con mắt cho phép ẩn/hiện mật khẩu.", "Bước 2 - Nhập tài khoản: ")
    add_bullet("Nhấn Enter hoặc click nút 'Đăng nhập'. Hệ thống gọi TaiKhoanDAO đối chiếu mật khẩu đã mã hóa.", "Bước 3 - Xác thực: ")
    add_bullet("Nếu là Quản lý (ADMIN): Mở toàn bộ các menu chức năng: Bán hàng, Quản lý sản phẩm, Quản lý nhân viên, Báo cáo doanh thu. Nếu là Thu ngân (STAFF): Hệ thống tự động ẩn hoặc vô hiệu hóa các menu quản trị nhân sự và báo cáo tài chính để bảo mật số liệu.", "Bước 4 - Phân quyền giao diện: ")
    add_callout("Thông báo lỗi thân thiện: Nếu người dùng nhập sai mật khẩu quá 5 lần, tài khoản sẽ tạm thời bị khóa trong 15 phút để phòng chống tấn công dò mật khẩu (Brute-force).", "BẢO MẬT ĐĂNG NHẬP:");

    add_h2("II. Chức năng Bán hàng tại quầy (POS - Nghiệp vụ trọng tâm)")
    add_p("Màn hình Bán hàng (POS) là phân hệ cốt lõi được nhóm đầu tư thiết kế tỉ mỉ nhất, chia thành 3 khu vực trực quan giúp thu ngân chốt đơn trong vòng chưa đầy 30 giây:")
    add_bullet("Bao gồm thanh tìm kiếm Live Search (gõ tên hoặc quét mã Barcode), bộ lọc nhanh theo Danh mục (Sneaker, Chạy bộ), Hãng (Nike, Adidas) và Kích cỡ (36 -> 44).", "Khu vực 1 (Bên trái): Danh mục & Tra cứu biến thể: ")
    add_bullet("Hiển thị danh sách các đôi giày đã chọn với đầy đủ cột: STT, Mã SKU, Tên giày, Size, Màu sắc, Đơn giá, Số lượng, Thành tiền và nút Xóa.", "Khu vực 2 (Ở giữa): Chi tiết Giỏ hàng hiện tại: ")
    add_bullet("Khối Khách hàng (nhập SĐT, hiển thị điểm tích lũy, checkbox dùng điểm) và Khối Thanh toán (Tổng tiền hàng, Giảm giá, Tiền cần trả, Tiền khách đưa, Tiền thừa thối lại) cùng nút bấm to nổi bật 'F10 - Thanh toán & In hóa đơn'.", "Khu vực 3 (Bên phải): Bảng điều khiển Thanh toán: ")

    add_p("Kịch bản 5 bước thao tác bán hàng siêu tốc:")
    add_bullet("Thu ngân nhấn F2, con trỏ nhảy ngay vào ô tìm kiếm. Thu ngân gõ 'Air Force' hoặc quét mã súng Barcode. Bảng tự động lọc dòng sản phẩm trong vòng 0.2 giây.", "Bước 1 - Tra cứu giày nhanh: ")
    add_bullet("Thu ngân nhấn Enter, một Popup nhỏ xuất hiện cho phép chọn Size (38, 39, 40, 41, 42) và Màu sắc (Trắng, Đen). Nhãn tồn kho hiển thị tức thì: 'Size 41 - Màu Trắng: Còn 8 đôi'. Nhập số lượng mua (mặc định là 1) và nhấn Enter để đưa vào giỏ hàng.", "Bước 2 - Chọn biến thể Size & Màu: ")
    add_bullet("Thu ngân nhấn F3 nhảy sang ô SĐT khách hàng, nhập '0912345678'. Nếu là khách quen, hệ thống hiện: 'Nguyễn Văn A - Thành viên Bạc - Điểm: 150 điểm'. Nếu khách đồng ý dùng 50 điểm để giảm 50.000 VNĐ, thu ngân nhấn phím Space để tích chọn.", "Bước 3 - Nhập thông tin thành viên: ")
    add_bullet("Nhấn Tab sang ô 'Tiền khách đưa', nhập 1.500.000 VNĐ (cho hóa đơn 1.250.000 VNĐ). Nhãn tiền thừa tự động nhảy số màu xanh lá to rõ: '250.000 VNĐ'.", "Bước 4 - Tính tiền thừa: ")
    add_bullet("Thu ngân nhấn phím tắt F10. Hộp thoại xác nhận xuất hiện, nhấn Enter để chốt đơn. Hệ thống tự động lưu Transaction CSDL, trừ tồn kho theo đúng Size/Màu, cộng điểm thưởng cho khách và xuất hóa đơn nhiệt K80 ra máy in.", "Bước 5 - Thanh toán F10 & In vé: ")

    add_callout("Định dạng hóa đơn K80 chuyên nghiệp: Hóa đơn in ra có đầy đủ Logo cửa hàng, Tên shop, Địa chỉ, Mã hóa đơn HD000123, Tên nhân viên thu ngân, Chi tiết từng đôi giày kèm Size và Màu sắc rõ ràng, Tổng tiền, Điểm tích lũy mới và Lời cảm ơn quý khách.", "HÓA ĐƠN BÁN LẺ IN TẠI QUẦY:");

    add_h2("III. Chức năng Quản lý sản phẩm giày dép & Biến thể SKU")
    add_p("Phân hệ dành riêng cho Quản lý cửa hàng để theo dõi và điều chỉnh danh mục sản phẩm:")
    add_bullet("Áp dụng mô hình Master - Detail: Nửa trên là Form nhập thông tin mẫu giày chung (Tên giày, Thương hiệu, Phân loại, Chất liệu, Giá nhập, Giá bán, Nút chọn ảnh từ máy tính). Nửa dưới là Tab chi tiết các biến thể kích cỡ và màu sắc tương ứng.", "Bố cục Master - Detail: ")
    add_bullet("Khi thêm một mẫu giày mới, quản lý click 'Thêm biến thể', tích chọn các size kinh doanh (ví dụ: size 40, 41, 42) và nhập màu sắc. Hệ thống tự động sinh các mã SKU biến thể con và gán số lượng nhập ban đầu cho từng size.", "Tạo ma trận biến thể tự động: ")
    add_bullet("Hệ thống kiểm tra tính hợp lệ bằng Regex: Tên sản phẩm từ 5-150 ký tự; Giá bán bắt buộc phải lớn hơn Giá nhập tối thiểu 10% để đảm bảo cửa hàng không bị lỗ.", "Kiểm tra dữ liệu nhập liệu: ")
    add_bullet("Khi một mẫu giày ngừng sản xuất, quản lý chuyển trạng thái sang 'Ngừng kinh doanh'. Hệ thống thực hiện Soft-Delete, bảo toàn toàn bộ dữ liệu lịch sử bán hàng.", "Ngừng kinh doanh an toàn: ")

    add_h2("IV. Chức năng Quản lý khách hàng & Tích điểm thành viên")
    add_p("Phân hệ hỗ trợ xây dựng mối quan hệ thân thiết với khách hàng quen thuộc:")
    add_bullet("Quản lý danh sách thành viên với bảng dữ liệu hiển thị Mã KH, Họ tên, SĐT, Điểm tích lũy và Hạng thẻ (Đồng, Bạc, Vàng, Kim Cương).", "Danh sách & Tra cứu: ")
    add_bullet("Hỗ trợ tạo nhanh thẻ thành viên mới ngay tại quầy thu ngân chỉ trong 5 giây bằng cách nhập SĐT và Họ tên.", "Đăng ký thành viên siêu tốc: ")
    add_bullet("Cho phép xem lại toàn bộ các hóa đơn trong quá khứ mà khách hàng đã mua, hỗ trợ đắc lực khi khách mang giày đến yêu cầu đổi size trong vòng 7 ngày.", "Xem lịch sử mua hàng: ")

    add_h2("V. Chức năng Thống kê doanh thu & Biểu đồ phân tích kinh doanh")
    add_p("Phân hệ hỗ trợ người quản lý nắm bắt toàn diện sức khỏe tài chính của cửa hàng:")
    add_bullet("Cung cấp 4 thẻ chỉ số tổng quan (KPI Cards): Tổng doanh thu (VNĐ), Tổng số đôi giày đã bán ra, Tổng số hóa đơn và Số lượng khách hàng mới.", "Chỉ số tổng hợp (KPI Cards): ")
    add_bullet("Hỗ trợ lọc linh hoạt theo Ngày hôm nay, theo Tháng/Năm hoặc chọn Khoảng thời gian từ ngày A đến ngày B bằng JDateChooser.", "Bộ lọc thời gian đa dạng: ")
    add_bullet("Tích hợp thư viện đồ họa JFreeChart để trực quan hóa: Biểu đồ cột biểu diễn doanh thu qua các mốc thời gian và Biểu đồ tròn thể hiện Top 5 mẫu giày bán chạy nhất.", "Trực quan hóa biểu đồ: ")
    add_bullet("Tích hợp thư viện Apache POI xuất toàn bộ báo cáo doanh thu ra file Excel chuẩn (.xlsx) có công thức tính tổng và định dạng tiền tệ chuyên nghiệp.", "Xuất báo cáo Excel: ")

    if os.path.exists("diagram_chart_shoe.png"):
        doc.add_picture("diagram_chart_shoe.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 3. Minh họa thống kê doanh thu và phân tích top sản phẩm bán chạy")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("VI. Bảng hệ thống phím tắt & Điều hướng bán hàng (Hotkeys)")
    add_p("Nhằm giải phóng nhân viên thu ngân khỏi việc phải liên tục dùng chuột, hệ thống trang bị bộ phím tắt công thái học:")
    t_hotkeys = doc.add_table(rows=11, cols=3)
    hotkey_data = [
        ["F2", "Màn hình Bán hàng (POS)", "Focus con trỏ ngay vào ô Tìm kiếm sản phẩm / Quét mã vạch"],
        ["F3", "Màn hình Bán hàng (POS)", "Chuyển con trỏ sang ô Nhập Số điện thoại Khách hàng"],
        ["F4", "Màn hình Bán hàng (POS)", "Làm mới đơn hàng / Tạo hóa đơn mới"],
        ["F8", "Màn hình Bán hàng (POS)", "Tạm lưu đơn hàng hiện tại (khi khách đang chọn thêm giày)"],
        ["F10", "Màn hình Bán hàng (POS)", "Xác nhận thanh toán và in hóa đơn K80 (Nghiệp vụ quan trọng nhất)"],
        ["Ctrl + N", "Quản lý SP / Khách hàng", "Thêm mới một bản ghi (Tạo mẫu giày mới / Thêm khách hàng)"],
        ["Ctrl + S", "Quản lý SP / Khách hàng", "Lưu dữ liệu vừa nhập vào cơ sở dữ liệu"],
        ["Ctrl + E", "Thống kê / Báo cáo", "Xuất dữ liệu báo cáo ra file Excel (.xlsx)"],
        ["Delete", "Giỏ hàng / Danh sách", "Xóa sản phẩm khỏi giỏ hàng / Ngừng kinh doanh mẫu giày"],
        ["Esc", "Toàn bộ Dialog / Popup", "Đóng cửa sổ hiện tại, hủy bỏ thao tác"]
    ]
    style_table(t_hotkeys, [1.0, 2.0, 3.3], ["Phím tắt", "Phạm vi áp dụng", "Hành động thực thi"], hotkey_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN
    # ==========================================
    add_h1("PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN")
    
    add_h2("I. Đánh giá kết quả đạt được và những hạn chế")
    add_h3("1. Những ưu điểm nổi bật của hệ thống")
    add_bullet("Hệ thống giải quyết trọn vẹn bài toán khó nhất của cửa hàng giày dép là quản lý ma trận biến thể kích cỡ (size 35-44) và màu sắc, giúp nhân viên tra cứu tồn kho từng size trong 0.2 giây.", "Xử lý biến thể chuyên sâu: ")
    add_bullet("Phân tách ranh giới mạch lạc giữa GUI (Swing FlatLaf), BUS (Validation & Logic) và DAO (JDBC Prepared Statements), tuân thủ 100% chuẩn mực đào tạo của Khoa CNTT - IUH.", "Kiến trúc 3 lớp chuẩn mực: ")
    add_bullet("Nhờ hệ thống phím tắt (F2, F3, F10) và cơ chế Live Search, thời gian thao tác thanh toán cho một lượt khách được rút ngắn xuống chỉ còn 20 - 30 giây.", "Trải nghiệm người dùng vượt trội: ")
    add_bullet("Cơ chế JDBC Transaction và kỹ thuật Xóa mềm (Soft-Delete) đảm bảo tuyệt đối không bao giờ xảy ra tình trạng bán âm kho và bảo toàn trọn vẹn lịch sử hóa đơn kế toán cũ.", "Toàn vẹn dữ liệu an toàn cao: ")
    add_bullet("Cung cấp báo cáo trực quan, biểu đồ trực tiếp hỗ trợ đắc lực cho người quản lý đưa ra quyết định kinh doanh.", "Hỗ trợ quản trị kinh doanh: ")

    add_h3("2. Những điểm còn hạn chế")
    add_bullet("Hiện tại ứng dụng mới vận hành trên môi trường Desktop nội bộ (mạng LAN cửa hàng), chưa hỗ trợ người quản lý theo dõi doanh thu từ xa qua điện thoại di động.", "Chưa có phiên bản Mobile/Web: ")
    add_bullet("Chức năng thanh toán chuyển khoản hiện vẫn yêu cầu thu ngân mở ứng dụng ngân hàng trên điện thoại để kiểm tra tiền về thủ công trước khi bấm xác nhận.", "Thanh toán chuyển khoản bán tự động: ")
    add_bullet("Chưa tích hợp đồng bộ đa kênh (Omnichannel) với các sàn thương mại điện tử (Shopee, TikTok Shop, Lazada).", "Chưa liên kết sàn TMĐT: ")

    add_h2("II. Hướng phát triển trong tương lai")
    add_p("Để hệ thống ngày càng hoàn thiện và đáp ứng tốt hơn nhu cầu mở rộng quy mô chuỗi cửa hàng, nhóm định hướng các giai đoạn nâng cấp tiếp theo:")
    add_bullet("Tích hợp cổng thanh toán VietQR động: Khi bấm thanh toán, màn hình hiển thị mã QR có sẵn số tiền và mã hóa đơn. Khi khách quét mã chuyển tiền thành công, hệ thống tự động nhận Webhook và in hóa đơn tức thì mà thu ngân không cần kiểm tra điện thoại.", "1. Tích hợp thanh toán QR Code tự động: ")
    add_bullet("Xây dựng hệ thống Backend RESTful API bằng Spring Boot và phát triển ứng dụng di động (Flutter / React Native) cho phép nhân viên dùng camera điện thoại quét mã vạch kiểm kê kho và quản lý theo dõi doanh thu thời gian thực ở bất kỳ đâu.", "2. Mở rộng kiến trúc Web & Mobile: ")
    add_bullet("Ứng dụng học máy (Machine Learning) để phân tích xu hướng tiêu thụ giày theo mùa, dự báo cỡ giày nào sắp hết hàng để gợi ý người quản lý lên đơn nhập hàng sớm.", "3. Trí tuệ nhân tạo dự báo nhập hàng: ")

    add_h2("III. Lời kết")
    add_p("Đồ án 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang (StepUp Footwear)' đã hoàn thành xuất sắc các mục tiêu nghiên cứu và thực nghiệm đề ra trong đề cương học phần Lập trình hướng sự kiện đối với công nghệ Java. Thông qua đồ án, nhóm sinh viên năm 3 chúng em không chỉ củng cố vững chắc nền tảng kiến thức về lập trình hướng đối tượng, xử lý sự kiện trong Java Swing, kỹ thuật tương tác cơ sở dữ liệu qua JDBC Transaction và thiết kế chuẩn hóa SQL Server, mà quan trọng hơn cả là đã rèn luyện được tư duy phân tích bài toán thực tế của doanh nghiệp bán lẻ.")
    add_p("Nhóm chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới cô Trần Thị Anh Thi cùng toàn thể quý Thầy Cô trong Khoa Công nghệ Thông tin đã tận tình chỉ bảo, giúp đỡ chúng em trong suốt quá trình thực hiện đề tài này!")

    # Save document
    output_filename = "BaoCao_QuanLyBanGiay_HSK.docx"
    doc.save(output_filename)
    print(f"Document saved successfully as: {output_filename}")
    
    # Also save a copy as QuanLyBanGiay_HSK.docx
    doc.save("QuanLyBanGiay_HSK.docx")
    print("Also saved copy as: QuanLyBanGiay_HSK.docx")

if __name__ == '__main__':
    create_document()

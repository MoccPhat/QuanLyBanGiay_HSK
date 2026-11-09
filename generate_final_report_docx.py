import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os
import shutil

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
    
    # Configure Word to update fields (including TOC) on open
    doc.settings.element.append(parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w')))

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

    recorded_headings = []

    def add_h1(text):
        recorded_headings.append((1, text))
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=14, bold=True, color_rgb=(30, 58, 138)) # Navy
        return p

    def add_h2(text):
        recorded_headings.append((2, text))
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13, bold=True, color_rgb=(37, 99, 235)) # Blue
        return p

    def add_h3(text):
        recorded_headings.append((3, text))
        p = doc.add_paragraph(style='Heading 3')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13, bold=True, italic=True, color_rgb=(15, 23, 42))
        return p

    def add_table_caption(number, title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(f"Bảng {number}. {title}")
        set_font(r, size=10, bold=True, italic=True, color_rgb=(30, 58, 138))
        return p

    def add_leader_entry(p, title, page, is_bold=False, is_italic=False, size=11):
        r1 = p.add_run(title)
        set_font(r1, size=size, bold=is_bold, italic=is_italic)
        r_tab = p.add_run()
        ptab = parse_xml(r'<w:ptab %s w:alignment="right" w:leader="dot" w:relativeTo="margin"/>' % nsdecls('w'))
        r_tab._r.append(ptab)
        r2 = p.add_run(str(page))
        set_font(r2, size=size, bold=is_bold)

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
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(f"{title} ")
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
                set_font(r, size=10.5, bold=True, color_rgb=(30, 58, 138))
                
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
                # Center short columns or numbers
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or len(str(val)) <= 8 or str(val) in ["PASS", "FAIL", "True", "False", "Yes", "No", "PK", "FK", "UQ", "100%"] else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    if str(val) == "PASS":
                        set_font(r, size=9.5, bold=True, color_rgb=(22, 101, 52)) # Green
                    elif str(val) == "FAIL":
                        set_font(r, size=9.5, bold=True, color_rgb=(185, 28, 28)) # Red
                    else:
                        set_font(r, size=9.5, color_rgb=(30, 41, 59))

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
    add_table_caption(1, "Danh sách phân công nhiệm vụ và đánh giá đóng góp của thành viên")
    t_members = doc.add_table(rows=5, cols=5)
    members_data = [
        ["1", "24704381", "Nguyễn Trọng Vinh", "Nhóm trưởng, Thiết kế CSDL & Tầng DAO (JDBC Transaction)", "100%"],
        ["2", "24718221", "Nhiêu Minh Kỳ", "Xây dựng Báo cáo Thống kê & Soạn thảo tài liệu, Kiểm thử hệ thống", "100%"],
        ["3", "24695041", "Trần Tấn Kiệt", "Phân tích nghiệp vụ, Xử lý ràng buộc toàn vẹn & Bắt lỗi Regex", "100%"],
        ["4", "24638311", "Trần Mộc Tấn Phát", "Thiết kế Giao diện POS, KeyBindings & Xử lý sự kiện Swing", "100%"]
    ]
    style_table(t_members, [0.5, 1.2, 1.8, 2.2, 0.6], ["STT", "MSSV", "Họ và tên", "Nhiệm vụ phân công", "Đánh giá"], members_data)

    add_h1("LỜI CẢM ƠN")
    add_p("Trong suốt quá trình học tập và hoàn thành đồ án môn học Lập trình hướng sự kiện đối với công nghệ Java, nhóm chúng em đã nhận được sự quan tâm, giảng dạy tận tình và định hướng quý báu từ quý Thầy Cô trong Khoa Công nghệ Thông tin - Trường Đại học Công nghiệp TP.HCM (IUH).")
    add_p("Đặc biệt, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc nhất tới cô Trần Thị Anh Thi – Giảng viên trực tiếp giảng dạy và hướng dẫn học phần. Nhờ những bài giảng sinh động, tâm huyết cùng những chỉ dẫn chuyên môn thực tế của cô về lập trình hướng sự kiện, mô hình kiến trúc 3 lớp, kết nối cơ sở dữ liệu JDBC và thiết kế giao diện đồ họa người dùng, nhóm em đã có đủ kiến thức và tự tin để hoàn thành trọn vẹn đề tài 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang'.")
    add_p("Mặc dù nhóm đã nỗ lực hết mình với tinh thần học hỏi cao nhất, song do kiến thức và kinh nghiệm thực tiễn của sinh viên năm 3 còn có những giới hạn, đồ án chắc chắn khó tránh khỏi những thiếu sót nhất định. Nhóm chúng em rất mong nhận được những ý kiến đóng góp quý báu từ cô để đề tài được hoàn thiện tốt hơn nữa trong tương lai.")
    add_p("Kính chúc cô luôn dồi dào sức khỏe, hạnh phúc và gặt hái thêm nhiều thành công trên con đường nghiên cứu và giảng dạy!", italic_prefix="")

    add_h1("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN")
    add_table_caption(2, "Tiêu chí đánh giá đồ án của Giảng viên hướng dẫn")
    t_eval = doc.add_table(rows=6, cols=3)
    eval_data = [
        ["1", "Tài liệu báo cáo (Rõ ràng, đầy đủ phân tích Use Case, Sequence, Sơ đồ lớp, CSDL, Giao diện)", "........ / 2.0"],
        ["2", "Thiết kế Sơ đồ lớp (Class 7 lớp) và CSDL SQL Server (6 bảng, 33 CHECK, 5 FK, 3 UQ)", "........ / 2.5"],
        ["3", "Hiện thực chức năng Bán hàng (POS) & Xử lý nghiệp vụ Size/Màu/Tồn kho Transaction ACID", "........ / 3.0"],
        ["4", "Giao diện thân thiện, sử dụng phím tắt công thái học, Coding Convention Java SE 17", "........ / 1.5"],
        ["5", "Báo cáo kiểm thử hồi quy 62 Test Cases và trả lời phản biện", "........ / 1.0"]
    ]
    style_table(t_eval, [0.6, 4.5, 1.2], ["STT", "Tiêu chí đánh giá", "Điểm số"], eval_data)
    
    add_p("\nNhận xét chung của Giảng viên:\n.......................................................................................................................................................................................\n.......................................................................................................................................................................................\n.......................................................................................................................................................................................", space_before=4)
    p_sign = add_p("Thành phố Hồ Chí Minh, ngày ...... tháng ...... năm 2026\nChữ ký của Giảng viên hướng dẫn\n\n\n\nThS. Trần Thị Anh Thi", align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # ==========================================
    # MỤC LỤC & LỜI MỞ ĐẦU
    # ==========================================
    add_h1("MỤC LỤC BÁO CÁO")
    
    # Word Dynamic TOC field wrapper
    p_toc_start = doc.add_paragraph()
    p_toc_start.paragraph_format.space_before = Pt(2)
    p_toc_start.paragraph_format.space_after = Pt(2)
    r_fld_begin = p_toc_start.add_run()
    r_fld_begin._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    r_fld_instr = p_toc_start.add_run()
    r_fld_instr._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w')))
    r_fld_sep = p_toc_start.add_run()
    r_fld_sep._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))

    toc_items = [
        ("DANH SÁCH THÀNH VIÊN TRONG NHÓM THỰC HIỆN", "2"),
        ("LỜI CẢM ƠN", "2"),
        ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "3"),
        ("LỜI MỞ ĐẦU", "4"),
        ("DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU", "5"),
        ("PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU", "6"),
        ("    I. Lý do chọn đề tài", "6"),
        ("    II. Thu thập yêu cầu nghiệp vụ thực tế", "7"),
        ("    III. Tác nhân chính trong hệ thống", "8"),
        ("    IV. Phân tích yêu cầu chức năng và phi chức năng", "9"),
        ("    V. Sơ đồ Use Case tổng thể và Đặc tả nghiệp vụ", "10"),
        ("    VI. Sơ đồ Kiến trúc hệ thống 3 tầng (3-Tier Architecture)", "12"),
        ("PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)", "14"),
        ("    I. Kiến trúc Sơ đồ lớp tổng thể theo chuẩn OOP (7 Lớp thực thể)", "14"),
        ("    II. Phân tích 4 đặc trưng Hướng đối tượng (OOP) áp dụng trong hệ thống", "15"),
        ("    III. Mô tả chi tiết 7 Lớp đối tượng quan trọng cốt lõi", "16"),
        ("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)", "21"),
        ("    I. Sơ đồ thực thể liên kết trên HQTCSDL SQL Server (ERD 6 bảng)", "21"),
        ("    II. Mô tả chi tiết cấu trúc 6 bảng dữ liệu chuẩn 3NF", "22"),
        ("    III. Cơ chế xử lý toàn vẹn dữ liệu nâng cao (Ràng buộc CHECK & JDBC Transaction)", "26"),
        ("PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH", "29"),
        ("    I. Chức năng Đăng nhập & Phân quyền truy cập (Login & RBAC)", "29"),
        ("    II. Chức năng Bán hàng tại quầy (POS) & Sơ đồ tuần tự Sequence", "30"),
        ("    III. Chức năng Quản lý sản phẩm giày dép & Biến thể SKU", "34"),
        ("    IV. Chức năng Quản lý khách hàng & Tích điểm thành viên", "36"),
        ("    V. Chức năng Quản lý nhân sự & Phân quyền (Staff Management)", "38"),
        ("    VI. Phân hệ Thống kê doanh thu & Hiệu suất bán hàng (Analytics & Reporting)", "40"),
        ("    VII. Bảng hệ thống phím tắt & Điều hướng bán hàng (Hotkeys)", "41"),
        ("    VIII. Đối chiếu yêu cầu đề bài môn học ↔ Chức năng đã hiện thực", "42"),
        ("PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN", "43"),
        ("    I. Đánh giá kết quả đạt được (Chỉ số định lượng)", "43"),
        ("    II. Những điểm còn hạn chế", "44"),
        ("    III. Hướng phát triển trong tương lai", "45"),
        ("    IV. Lời kết", "46"),
        ("PHẦN VI: KẾT QUẢ KIỂM THỬ HỆ THỐNG (TESTING & VERIFICATION)", "47"),
        ("    I. Giới thiệu bộ kiểm thử tự động VerifyAllScenarios", "47"),
        ("    II. Ma trận kết quả kiểm thử hồi quy tự động 62 Test Cases", "48"),
        ("    III. Đánh giá độ tin cậy và tỷ lệ bao phủ nghiệp vụ", "53"),
        ("PHẦN VII: TÀI LIỆU THAM KHẢO", "54")
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        is_major = item.strip().startswith("PHẦN") or item.strip().startswith("LỜI") or item.strip().startswith("DANH") or item.strip().startswith("NHẬN")
        add_leader_entry(p_t, item, page, is_bold=is_major, size=11 if is_major else 10.5)

    p_toc_end = doc.add_paragraph()
    p_toc_end.paragraph_format.space_before = Pt(0)
    p_toc_end.paragraph_format.space_after = Pt(2)
    r_fld_end = p_toc_end.add_run()
    r_fld_end._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

    add_h1("LỜI MỞ ĐẦU")
    add_p("Trong kỷ nguyên chuyển đổi số và thương mại hiện đại, việc ứng dụng công nghệ thông tin vào quản lý bán lẻ không còn là một lựa chọn xa xỉ mà đã trở thành điều kiện sống còn của các doanh nghiệp. Đối với ngành hàng thời trang, đặc biệt là kinh doanh giày dép, bài toán quản lý luôn chứa đựng những nét đặc thù phức tạp vượt trội so với các mô hình bán lẻ hàng hóa thông thường khác.")
    add_p("Nếu như một lon nước ngọt hay một cuốn sách chỉ có một mã vạch định danh duy nhất thì một đôi giày thời trang lại gắn liền với một ma trận biến thể: cùng một kiểu dáng nhưng có từ 8 đến 10 kích cỡ khác nhau (Size EU từ 35 đến 45) và nhiều phiên bản màu sắc (Trắng, Đen, Xám, Phối màu...). Nhân viên bán hàng tại quầy thu ngân không thể chỉ trả lời khách hàng rằng 'cửa hàng còn mẫu này', mà bắt buộc phải nắm rõ: 'Mẫu này ở Size 41 màu Trắng hiện tại trong kho còn chính xác bao nhiêu đôi?'.")
    add_p("Nhằm giải quyết triệt để bài toán hóc búa này, đề tài 'Hệ thống quản lý bán hàng tại cửa hàng giày dép thời trang (StepUp Footwear)' được nhóm chúng em xây dựng với định hướng chuyên sâu phục vụ nghiệp vụ tại quầy của nhân viên thu ngân và người quản lý cửa hàng (Desktop POS Application). Bằng việc mô hình hóa chuẩn xác cấu trúc sản phẩm 2 tầng (Mẫu giày cha -> Biến thể SKU con), kết hợp kiến trúc 3 lớp (3-Tier Architecture) trên nền tảng Java Swing và hệ quản trị cơ sở dữ liệu Microsoft SQL Server, hệ thống cam kết mang đến trải nghiệm thanh toán tốc độ cao, loại bỏ hoàn toàn hiện tượng bán âm kho và sai lệch số liệu doanh thu.")
    add_p("Báo cáo này được biên soạn với mục tiêu diễn giải toàn diện, rõ ràng từng khâu từ khảo sát yêu cầu, thiết kế kiến trúc đối tượng, sơ đồ cơ sở dữ liệu đến các bước thao tác trên màn hình thực tế, giúp quý Thầy Cô cùng các bạn sinh viên dễ dàng nắm bắt được cơ chế vận hành của hệ thống.")

    add_h1("DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU")
    add_h2("I. Danh mục hình ảnh (Figures)")
    figures = [
        ("Hình 1. Sơ đồ Use Case tổng thể hệ thống Quản lý bán giày thời trang", "10"),
        ("Hình 2. Sơ đồ kiến trúc hệ thống 3 tầng (3-Tier Architecture)", "12"),
        ("Hình 3. Sơ đồ lớp hướng đối tượng (Visual Paradigm 18)", "14"),
        ("Hình 4. Lược đồ cơ sở dữ liệu quan hệ phát sinh từ Microsoft SQL Server (Database Diagram SSMS 6 bảng)", "21"),
        ("Hình 5. Giao diện Đăng nhập hệ thống (chụp thật ngày 07/11/2026)", "29"),
        ("Hình 6. Giao diện Bán hàng tại quầy POS với đầy đủ thông tin tồn kho và giỏ hàng (chụp thật ngày 07/11/2026)", "31"),
        ("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS (Visual Paradigm 18)", "32"),
        ("Hình 8. Hộp thoại xem trước Hóa đơn K80 tích hợp chức năng In máy in và Xuất file văn bản (chụp thật ngày 07/11/2026)", "33"),
        ("Hình 9. Giao diện Quản lý danh mục mẫu giày (chụp thật ngày 07/11/2026)", "35"),
        ("Hình 10. Hộp thoại Tìm kiếm nâng cao Sản phẩm theo đa tiêu chí (chụp thật ngày 07/11/2026)", "36"),
        ("Hình 11. Giao diện Quản lý khách hàng và phân hạng tích điểm (chụp thật ngày 07/11/2026)", "37"),
        ("Hình 12. Hộp thoại Tìm kiếm nâng cao Khách hàng theo phân hạng và điểm tích lũy (chụp thật ngày 07/11/2026)", "38"),
        ("Hình 13. Giao diện Quản lý nhân sự và phân quyền (chụp thật ngày 07/11/2026)", "39"),
        ("Hình 14. Giao diện Báo cáo thống kê doanh thu và Top sản phẩm bán chạy (chụp thật ngày 07/11/2026)", "40")
    ]
    for fig_title, p_num in figures:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_before = Pt(1)
        p_f.paragraph_format.space_after = Pt(2)
        add_leader_entry(p_f, fig_title, p_num, is_italic=True, size=10.5)

    add_h2("II. Danh mục bảng biểu (Tables)")
    tables_list = [
        ("Bảng 1. Danh sách phân công nhiệm vụ và đánh giá đóng góp của thành viên", "2"),
        ("Bảng 2. Tiêu chí đánh giá đồ án của Giảng viên hướng dẫn", "3"),
        ("Bảng 3. Ma trận phân rã Use Case và mức độ hoàn thành chức năng", "11"),
        ("Bảng 4. Thuộc tính và phương thức của lớp trừu tượng Nguoi", "16"),
        ("Bảng 5. Thuộc tính và phương thức của lớp NhanVien", "17"),
        ("Bảng 6. Thuộc tính và phương thức của lớp KhachHang", "17"),
        ("Bảng 7. Thuộc tính và phương thức của lớp SanPham", "18"),
        ("Bảng 8. Thuộc tính và phương thức của lớp ChiTietGiay", "19"),
        ("Bảng 9. Thuộc tính và phương thức của lớp HoaDon", "19"),
        ("Bảng 10. Thuộc tính và phương thức của lớp ChiTietHoaDon", "20"),
        ("Bảng 11. Cấu trúc trường dữ liệu bảng NhanVien trên Microsoft SQL Server", "22"),
        ("Bảng 12. Cấu trúc trường dữ liệu bảng KhachHang trên Microsoft SQL Server", "23"),
        ("Bảng 13. Cấu trúc trường dữ liệu bảng SanPham trên Microsoft SQL Server", "23"),
        ("Bảng 14. Cấu trúc trường dữ liệu bảng ChiTietGiay trên Microsoft SQL Server", "24"),
        ("Bảng 15. Cấu trúc trường dữ liệu bảng HoaDon trên Microsoft SQL Server", "25"),
        ("Bảng 16. Cấu trúc trường dữ liệu bảng ChiTietHoaDon trên Microsoft SQL Server", "26"),
        ("Bảng 17. Hệ thống phím tắt công thái học điều hướng bán hàng POS", "41"),
        ("Bảng 18. Đối chiếu yêu cầu đề tài môn học Lập trình hướng sự kiện ↔ Chức năng hiện thực", "42"),
        ("Bảng 19. Ma trận kết quả kiểm thử hồi quy tự động 62 Test Cases (VerifyAllScenarios & VerifyNewFeatures)", "48")
    ]
    for tbl_title, p_num in tables_list:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        add_leader_entry(p_t, tbl_title, p_num, is_italic=True, size=10.5)

    doc.add_page_break()

    # ==========================================
    # PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU
    # ==========================================
    add_h1("PHẦN I: THU THẬP VÀ PHÂN TÍCH YÊU CẦU")
    
    add_h2("I. Lý do chọn đề tài")
    add_p("Trong đời sống giới trẻ và xã hội hiện đại, giày dép thời trang không còn dừng lại ở vai trò là vật dụng che chở bàn chân mà đã vươn lên trở thành tuyên ngôn về gu thẩm mỹ và phong cách sống cá nhân. Nhu cầu mua sắm các dòng Sneaker năng động, giày thể thao chạy bộ, giày da công sở lịch lãm hay sandal trẻ trung không ngừng tăng trưởng mạnh mẽ, kéo theo sự bùng nổ của các cửa hàng bán lẻ thời trang giày dép.")
    add_p("Tuy nhiên, việc vận hành một cửa hàng giày dép lại tiềm ẩn nhiều khó khăn hơn các ngành hàng đóng gói sẵn:")
    add_bullet("Đặc thù biến thể SKU phức tạp: Mỗi mẫu giày sở hữu nhiều size (35 đến 45) và màu sắc khác nhau. Tồn kho của từng size là hoàn toàn riêng biệt. Khách hàng thử giày thường hỏi liên tục: 'Mẫu này ở Size 40 màu Đen còn không em?'.", "1. ")
    add_bullet("Quản lý thủ công kém hiệu quả: Đa số cửa hàng quy mô vừa và nhỏ vẫn ghi chép sổ tay hoặc dùng Excel rời rạc. Nhân viên không biết size nào còn hay hết, phải chạy vào kho lục tìm mất 5-10 phút khiến khách hàng nản lòng bỏ đi.", "2. ")
    add_bullet("Ùn tắc thanh toán giờ cao điểm: Việc cộng tiền thủ công dễ sai lệch giá, nhầm chương trình khuyến mãi và làm khách hàng phải chờ đợi lâu tại quầy thu ngân.", "3. ")
    add_bullet("Thất thoát hàng hóa và thiếu dữ liệu khách hàng: Không kiểm soát được tình trạng nhân viên tự ý giảm giá, không có hệ thống tích điểm để giữ chân khách quen và người quản lý khó thống kê được đâu là mẫu giày 'hot' để nhập thêm hàng.", "4. ")
    add_p("Xuất phát từ thực tiễn trên, nhóm sinh viên chúng em đã chọn đề tài 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang' nhằm ứng dụng kiến thức chuyên môn của môn Lập trình hướng sự kiện Java để giải quyết triệt để các bất cập trong khâu bán hàng tại quầy.")

    add_h2("II. Thu thập yêu cầu nghiệp vụ thực tế")
    add_h3("1. Nghiệp vụ của nhân viên quầy thu ngân (POS)")
    add_bullet("Cần một màn hình POS trực quan, tốc độ xử lý tức thì, hỗ trợ tối đa việc dùng phím tắt (F1-F4 chuyển nhanh các tab, F10 thanh toán, Delete xóa dòng giỏ hàng, Esc hủy thao tác) để thu ngân không cần rời tay khỏi bàn phím.", "Tốc độ và công thái học: ")
    add_bullet("Gõ tên hoặc chọn mẫu giày là hệ thống hiển thị ngay danh sách các size (35-45) kèm màu sắc và số lượng tồn thực tế trong kho.", "Tra cứu biến thể theo size: ")
    add_bullet("Nhập số điện thoại là hệ thống tự hiển thị tên khách, hạng thẻ thành viên (Đồng, Bạc, Vàng, Kim Cương) và số điểm tích lũy. Cho phép dùng điểm để trừ tiền trực tiếp trên đơn hàng hiện tại.", "Tích điểm và chăm sóc khách hàng: ")
    add_bullet("Tính tổng tiền hàng, tiền khách đưa, tiền thừa phải thối lại; trừ tồn kho qua JDBC Transaction tại tầng DAO theo đúng size/màu và mở hộp thoại JDialog xem trước phiếu thanh toán K80 rõ ràng.", "Thanh toán và xem trước hóa đơn: ")

    add_h3("2. Nghiệp vụ của người quản lý cửa hàng (Store Manager)")
    add_bullet("Thêm mẫu giày mới, cập nhật giá bán, bổ sung các biến thể kích cỡ và màu sắc khi nhập đợt hàng mới.", "Quản lý danh mục sản phẩm: ")
    add_bullet("Theo dõi hồ sơ nhân sự, phân ca làm việc, giám sát hoạt động thu ngân và hỗ trợ thiết lập mật khẩu băm bảo mật SHA-256.", "Quản lý nhân sự và phân quyền: ")
    add_bullet("Theo dõi doanh thu, số lượng đơn hàng, danh mục sản phẩm tiêu biểu và xuất báo cáo tài chính định kỳ.", "Thống kê và báo cáo kinh doanh: ")

    add_h2("III. Tác nhân chính trong hệ thống")
    add_bullet("Thực hiện các thao tác thường nhật tại quầy: Đăng nhập hệ thống, tra cứu tồn kho, lập đơn bán hàng, áp dụng tích điểm đổi thưởng, nhận tiền khách đưa, hoàn tất thanh toán và mở hộp thoại JDialog xem trước phiếu thanh toán K80.", "1. Nhân viên thu ngân (Cashier / Staff): ")
    add_bullet("Nắm giữ toàn bộ quyền hạn của nhân viên thu ngân, đồng thời sở hữu đặc quyền quản trị: Quản lý danh mục mẫu giày và biến thể SKU, quản lý hồ sơ nhân sự, phân quyền tài khoản, xem thống kê doanh thu toàn cửa hàng.", "2. Người quản lý cửa hàng (Store Manager / Admin): ")

    add_h2("IV. Phân tích yêu cầu chức năng và phi chức năng")
    add_h3("1. Yêu cầu chức năng (Functional Requirements)")
    add_bullet("Xác thực đăng nhập người dùng qua mã nhân viên và mật khẩu băm SHA-256 (64 ký tự). Điều hướng quyền truy cập theo vai trò (Quản lý mở 5 tab, Nhân viên mở 3 tab).", "Phân hệ Xác thực & Phân quyền: ")
    add_bullet("Chọn mẫu giày, kích cỡ (35-45), màu sắc hiển thị tồn kho tức thời. Thêm vào giỏ hàng, tự động cộng dồn số lượng. Tra cứu hội viên qua SĐT, tích điểm và giảm giá theo hạng. Tính tiền thừa tự động. Thanh toán đơn hàng bằng JDBC Transaction nguyên tử.", "Phân hệ Bán hàng tại quầy (POS): ")
    add_bullet("Xem danh sách mẫu giày, thêm mẫu mới, cập nhật thông tin và giá cả (giaBan >= giaNhap > 0). Áp dụng cơ chế Xóa mềm (Soft-Delete) cập nhật trangThai = 0 để bảo toàn lịch sử hóa đơn.", "Phân hệ Quản lý mẫu giày & Biến thể SKU: ")
    add_bullet("Thêm mới khách hàng, cập nhật địa chỉ, kiểm tra số điện thoại chuẩn regex 10 số (^0[35789]\\d{8}$). Bảo vệ điểm tích lũy và hạng thẻ (read-only trên form, chỉ cập nhật khi thanh toán).", "Phân hệ Quản lý khách hàng: ")
    add_bullet("Thêm mới nhân viên, kiểm tra ràng buộc tuổi lao động >= 18 tuổi, phân ca làm việc, băm mật khẩu một chiều và vô hiệu hóa tài khoản khi nhân viên nghỉ việc.", "Phân hệ Quản lý nhân sự: ")
    add_bullet("Xem tổng quan doanh thu, số đơn hàng, bộ lọc mốc thời gian (Tất cả, Hôm nay, Tháng này, Năm nay) và bảng Top sản phẩm bán chạy.", "Phân hệ Báo cáo thống kê: ")

    add_h3("2. Yêu cầu phi chức năng (Non-Functional Requirements)")
    add_bullet("Thời gian phản hồi khi tra cứu tồn kho và hoàn tất thanh toán dưới 100ms trên cơ sở dữ liệu nội bộ.", "Hiệu năng & Tốc độ: ")
    add_bullet("Mật khẩu băm SHA-256; sử dụng PreparedStatement ngăn chặn 100% tấn công SQL Injection; ràng buộc dữ liệu toàn vẹn ở tầng CSDL.", "An toàn & Bảo mật: ")
    add_bullet("Áp dụng JDBC Transaction để đảm bảo tính toàn vẹn (ACID): thêm hóa đơn, thêm chi tiết và trừ tồn kho phải thành công đồng thời, nếu một bước lỗi thì rollback toàn bộ.", "An toàn dữ liệu & Concurrency: ")
    add_bullet("Giao diện đồ họa Java Swing kết hợp UIHelper trực quan, hiện đại, hỗ trợ thao tác nhanh thông qua các phím tắt công thái học.", "Tính dễ dùng & Công thái học: ")

    add_callout("Quy trình bán hàng chuẩn 6 bước: [1] Tiếp nhận mẫu giày -> [2] Tra cứu tồn kho theo size/màu -> [3] Thêm vào giỏ hàng -> [4] Nhập SĐT tích điểm -> [5] Nhập tiền khách đưa & kiểm tra tiền thừa -> [6] Nhấn F10 thanh toán, trừ kho và mở hộp thoại JDialog xem trước phiếu thanh toán K80.", "CHUỖI HÀNH ĐỘNG CỐT LÕI TẠI QUẦY:")

    # Sơ đồ Use Case tổng thể (L21)
    add_h2("V. Sơ đồ Use Case tổng thể và Đặc tả nghiệp vụ")
    add_p("Hệ thống StepUp Footwear POS được phân rã thành các ca sử dụng (Use Cases) tương ứng với 2 tác nhân chính: Nhân viên thu ngân và Người quản lý. Người quản lý kế thừa toàn bộ quyền hạn tác nghiệp bán lẻ của nhân viên thu ngân, đồng thời sở hữu các đặc quyền quản trị danh mục sản phẩm, nhân sự và báo cáo thống kê.")

    if os.path.exists("diagram_usecase_shoe.png"):
        doc.add_picture("diagram_usecase_shoe.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 1. Sơ đồ Use Case tổng thể hệ thống Quản lý bán giày thời trang")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_p("Bảng đặc tả chi tiết các Use Case chính trong hệ thống:")
    add_table_caption(3, "Ma trận phân rã Use Case và mức độ hoàn thành chức năng")
    t_uc = doc.add_table(rows=8, cols=5)
    uc_data = [
        ["UC01", "Đăng nhập hệ thống", "Thu ngân, Quản lý", "Xác thực mã nhân viên và mật khẩu băm SHA-256", "Điều hướng mở giao diện tương ứng theo quyền"],
        ["UC02", "Đăng xuất & Thoát", "Thu ngân, Quản lý", "Xác nhận kết thúc phiên làm việc", "Đóng cửa sổ làm việc, hoàn nguyên màn hình đăng nhập"],
        ["UC03", "Bán hàng tại quầy (POS)", "Thu ngân, Quản lý", "Tra cứu size/màu, lập giỏ hàng, tính tiền thừa, trừ kho ACID", "Ghi nhận hóa đơn, trừ kho, tích điểm, xem trước phiếu K80"],
        ["UC03.1", "Tra cứu tồn kho size/màu", "Thu ngân, Quản lý", "<<include>> trong Bán hàng POS, tra cứu tồn kho thực tế", "Hiển thị số lượng tồn kho (soLuongTon) tức thì tại quầy"],
        ["UC03.2", "Trừ tồn kho & Thanh toán ACID", "Thu ngân, Quản lý", "<<include>> trong Bán hàng POS, thực thi JDBC Transaction", "Trừ kho nguyên tử có điều kiện, cam kết commit()"],
        ["UC03.3", "Tích điểm & Giảm giá hội viên", "Thu ngân, Quản lý", "<<extend>> trong Bán hàng POS khi khách có đăng ký hội viên", "Tự tính chiết khấu theo hạng và trừ điểm nếu khách yêu cầu"],
        ["UC04", "Quản lý khách hàng", "Thu ngân, Quản lý", "Thêm, cập nhật khách hàng, tra cứu lịch sử mua và điểm", "Bảo vệ điểm tích lũy, kiểm soát regex SĐT 10 chữ số"]
    ]
    style_table(t_uc, [0.7, 1.6, 1.2, 1.8, 1.2], ["Mã UC", "Tên Use Case", "Tác nhân chính", "Mô tả nghiệp vụ", "Kết quả mong đợi"], uc_data)

    # Sơ đồ Kiến trúc 3 tầng (L21)
    add_h2("VI. Sơ đồ Kiến trúc hệ thống 3 tầng (3-Tier Architecture)")
    add_p("Hệ thống tuân thủ chặt chẽ kiến trúc 3 tầng (3-Tier Architecture) nhằm phân tách rõ ràng trách nhiệm giữa Tầng Giao diện người dùng (Presentation Layer), Tầng Xử lý nghiệp vụ & Truy cập dữ liệu (Data Access Layer), và Tầng Lưu trữ dữ liệu quan hệ (Database Layer):")

    if os.path.exists("diagram_architecture_shoe.png"):
        doc.add_picture("diagram_architecture_shoe.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 2. Sơ đồ kiến trúc hệ thống 3 tầng (3-Tier Architecture)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Xây dựng trên nền tảng Java Swing và AWT. Bao gồm các màn hình DangNhap_GUI, ManHinhChinh_GUI, BanHang_GUI, QuanLySanPham_GUI, QuanLyKhachHang_GUI, QuanLyNhanVien_GUI. Tầng này chịu trách nhiệm hiển thị giao diện, tiếp nhận tương tác chuột/bàn phím, kiểm tra dữ liệu hình thức (Regex) và chuyển giao yêu cầu xuống tầng DAO.", "1. Tầng Trình diễn (Presentation Layer - GUI): ")
    add_bullet("Bao gồm các lớp DAO (HoaDon_DAO, SanPham_DAO, ChiTietGiay_DAO, KhachHang_DAO, NhanVien_DAO) kết hợp cùng 7 lớp Thực thể OOP. Tầng này chịu trách nhiệm đóng gói logic nghiệp vụ, khởi tạo JDBC PreparedStatement, điều phối Transaction ACID (setAutoCommit(false), commit, rollback) và xử lý ngoại lệ nghiệp vụ.", "2. Tầng Truy cập dữ liệu & Thực thể (Data Access Layer - DAO & Entity): ")
    add_bullet("Vận hành trên hệ quản trị Microsoft SQL Server với cơ sở dữ liệu QuanLyBanGiay chuẩn 3NF gồm 6 bảng vật lý. Tầng này bảo đảm an toàn dữ liệu thông qua hệ thống 33 ràng buộc CHECK, 5 khóa ngoại FK, 3 khóa duy nhất UQ và bảo mật mật khẩu băm một chiều SHA-256.", "3. Tầng Cơ sở dữ liệu quan hệ (Database Layer - SQL Server): ")

    doc.add_page_break()

    # ==========================================
    # PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)
    # ==========================================
    add_h1("PHẦN II: THIẾT KẾ SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)")
    add_h2("I. Kiến trúc Sơ đồ lớp tổng thể theo chuẩn OOP (7 Lớp thực thể)")
    add_p("Khác với cách tiếp cận ánh xạ phẳng từ các bảng cơ sở dữ liệu vật lý, sơ đồ lớp của hệ thống được nhóm chúng em thiết kế chuẩn mực theo đúng 4 trụ cột của Lập trình hướng đối tượng (OOP: Kế thừa, Đóng gói, Trừu tượng và Đa hình). Đồng thời, sơ đồ tập trung vào 7 lớp đối tượng quan trọng nhất, gắn liền trực tiếp với bản sắc của bài toán Quản lý bán hàng giày dép thời trang, lược bỏ bớt các lớp cấu hình phụ trợ để bức tranh nghiệp vụ trở nên mạch lạc, rõ ràng và dễ bảo vệ trước Hội đồng chấm thi.")
    
    if os.path.exists("vp_class_diagram.png"):
        doc.add_picture("vp_class_diagram.png", width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 3. Sơ đồ lớp hướng đối tượng (Visual Paradigm 18)")
        set_font(r_c, size=10, italic=True, color_rgb=(0, 0, 0))
    elif os.path.exists("SoDoLop_QuanLyBanGiay.png"):
        doc.add_picture("SoDoLop_QuanLyBanGiay.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 3. Sơ đồ lớp hướng đối tượng (Visual Paradigm 18)")
        set_font(r_c, size=10, italic=True, color_rgb=(0, 0, 0))

    add_h2("II. Phân tích 4 đặc trưng Hướng đối tượng (OOP) áp dụng trong hệ thống")
    add_bullet("Hệ thống xây dựng lớp cơ sở trừu tượng Nguoi (Person) gom chung các thuộc tính nhân thân (hoTen, soDienThoai, ngaySinh, gioiTinh, diaChi, email). Cả NhanVien và KhachHang đều kế thừa từ Nguoi thông qua mối quan hệ Tổng quát hóa (Generalization ──▷). Điều này giúp tái sử dụng mã nguồn tối đa và phản ánh đúng bản chất thế giới thực.", "1. Tính Kế thừa (Inheritance): ")
    add_bullet("Toàn bộ thuộc tính trong các lớp đều được đặt ở mức truy cập Private (-). Việc đọc và ghi dữ liệu ra bên ngoài bắt buộc phải thông qua các phương thức Getter/Setter công khai (+), kèm theo các logic kiểm tra tính hợp lệ (Validation) như kiểm tra số điện thoại đúng đầu số mạng Việt Nam, kiểm tra tuổi lao động >= 18, kiểm tra tồn kho không âm.", "2. Tính Đóng gói (Encapsulation): ")
    add_bullet("Lớp Nguoi là lớp trừu tượng (abstract class) khai báo phương thức trừu tượng getThongTin() và cài đặt phương thức toString() dùng chung. Cả hai lớp con NhanVien và KhachHang bắt buộc phải Override (ghi đè) getThongTin() để xuất ra thông tin tóm tắt tương ứng với vai trò của mình, đồng thời tự cài đặt equals() và hashCode() độc lập dựa trên mã định danh duy nhất (maNhanVien, maKhachHang) của từng thực thể.", "3. Tính Trừu tượng & Đa hình (Abstraction & Polymorphism): ")
    add_bullet("Hệ thống thể hiện rõ sự khác biệt giữa hai cấp độ sở hữu: Quan hệ Tổng thành chặt chẽ (Composition ◆──) được áp dụng giữa SanPham ◆── ChiTietGiay (Một mẫu giày sở hữu các biến thể size/màu) và HoaDon ◆── ChiTietHoaDon (Hóa đơn sở hữu các dòng hàng). Khi đối tượng cha bị hủy thì các đối tượng con thành phần không tồn tại độc lập. Trong khi đó, quan hệ giữa NhanVien, KhachHang và HoaDon là quan hệ Liên kết (Association ──).", "4. Quan hệ Tổng thành (Composition) & Liên kết (Association): ")

    add_callout("Chiến lược ánh xạ giữa OOP và CSDL SQL Server: Ở tầng ứng dụng Java, NhanVien và KhachHang kế thừa lớp Nguoi. Khi lưu xuống CSDL quan hệ, nhóm áp dụng chiến lược 'Table per Concrete Class' (tạo 2 bảng vật lý độc lập là NhanVien và KhachHang) để tối ưu hóa tốc độ truy vấn SELECT/JOIN khi bán hàng tại quầy POS mà không cần JOIN qua bảng trung gian.", "LƯU Ý VỀ ÁNH XẠ KIẾN TRÚC:");

    add_h2("III. Mô tả chi tiết 7 Lớp đối tượng quan trọng cốt lõi")
    
    # Table 1: Nguoi (Abstract)
    add_h3("1. Lớp trừu tượng Nguoi (Lớp cơ sở nhân thân)")
    add_p("Lớp cha đại diện cho con người tham gia vào hoạt động của cửa hàng, định nghĩa cấu trúc dữ liệu và hành vi dùng chung.")
    add_table_caption(4, "Thuộc tính và phương thức của lớp trừu tượng Nguoi")
    t_ng = doc.add_table(rows=7, cols=5)
    ng_data = [
        ["1", "hoTen", "String", "Không rỗng, Độ dài từ 3 - 50 ký tự", "Họ và tên đầy đủ theo tiếng Việt"],
        ["2", "soDienThoai", "String", "Không rỗng, Chuẩn 10 số, Regex: ^0[35789]\\d{8}$", "Số điện thoại liên lạc chính"],
        ["3", "ngaySinh", "LocalDate", "Không rỗng, Phải trước ngày hiện tại", "Ngày tháng năm sinh"],
        ["4", "gioiTinh", "boolean", "Không rỗng, True: Nam, False: Nữ", "Giới tính sinh học"],
        ["5", "diaChi", "String", "Có thể rỗng, Tối đa 200 ký tự", "Địa chỉ cư trú hoặc thường trú"],
        ["6", "email", "String", "Có thể rỗng, Đúng chuẩn RFC định dạng email", "Địa chỉ thư điện tử liên hệ"]
    ]
    style_table(t_ng, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ng_data)

    # Table 2: NhanVien (extends Nguoi)
    add_h3("2. Lớp NhanVien (Nhân sự - Kế thừa từ Nguoi)")
    add_p("Lớp kế thừa lớp Nguoi, bổ sung các thuộc tính và hành vi nghiệp vụ dành riêng cho nhân viên thu ngân và quản lý cửa hàng.")
    add_table_caption(5, "Thuộc tính và phương thức của lớp NhanVien")
    t_nv = doc.add_table(rows=7, cols=5)
    nv_data = [
        ["1", "maNhanVien", "String", "PK, Không rỗng, Regex: ^NV[0-9]{4}$", "Mã định danh nhân viên (NV0001, NV0002...)"],
        ["2", "chucVu", "String", "Không rỗng, {'Quản lý', 'Nhân viên bán hàng'}", "Vị trí công tác tại cửa hàng"],
        ["3", "luongCoBan", "double", "Không rỗng, Giá trị > 0", "Mức lương cơ bản thỏa thuận"],
        ["4", "caLamViec", "String", "Có thể rỗng, {'Toàn thời gian', 'Ca sáng', 'Ca chiều', 'Ca tối'}", "Ca trực làm việc trong ngày"],
        ["5", "matKhau", "String", "Không rỗng, Chuỗi hex SHA-256 (độ dài 64 ký tự)", "Mật khẩu băm bảo mật SHA-256"],
        ["6", "trangThai", "boolean", "Không rỗng, Mặc định true (True: Đang làm, False: Đã nghỉ)", "Trạng thái công tác nhân sự"]
    ]
    style_table(t_nv, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], nv_data)

    # Table 3: KhachHang (extends Nguoi)
    add_h3("3. Lớp KhachHang (Khách hàng thân thiết - Kế thừa từ Nguoi)")
    add_p("Lớp kế thừa lớp Nguoi, quản lý thông tin tích điểm, xếp hạng thành viên và tính toán mức chiết khấu ưu đãi.")
    add_table_caption(6, "Thuộc tính và phương thức của lớp KhachHang")
    t_kh = doc.add_table(rows=4, cols=5)
    kh_data = [
        ["1", "maKhachHang", "String", "PK, Không rỗng, Regex: ^KH[0-9]{4}$", "Mã khách hàng thành viên (KH0001...)"],
        ["2", "diemTichLuy", "int", "Không rỗng, Giá trị >= 0, Mặc định: 0", "Điểm thưởng dùng giảm giá (1 điểm = 1.000đ)"],
        ["3", "hangThanhVien", "String", "Không rỗng, {'Đồng', 'Bạc', 'Vàng', 'Kim Cương'}", "Hạng thẻ xác định mức chiết khấu (0%, 5%, 10%, 15%)"]
    ]
    style_table(t_kh, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], kh_data)

    # Table 4: SanPham
    add_h3("4. Lớp SanPham (Mẫu giày cha)")
    add_p("Lớp đại diện cho thông tin kiểu dáng chung của mẫu giày thời trang trước khi phân rã thành các kích cỡ và màu sắc cụ thể.")
    add_table_caption(7, "Thuộc tính và phương thức của lớp SanPham")
    t_sp = doc.add_table(rows=9, cols=5)
    sp_data = [
        ["1", "maSanPham", "String", "PK, Không rỗng, Regex: ^SP[0-9]{4}$", "Mã mẫu giày (SP0001, SP0002...)"],
        ["2", "tenSanPham", "String", "Không rỗng, Tối đa 100 ký tự", "Tên thương mại của dòng giày"],
        ["3", "loaiGiay", "String", "Không rỗng, {'Sneaker', 'Oxford', 'Sandal', 'Boots'}", "Phân loại phong cách thiết kế"],
        ["4", "thuongHieu", "String", "Không rỗng, {'Nike', 'Adidas', 'Puma', 'Biti's'...}", "Thương hiệu sản xuất xuất xứ"],
        ["5", "giaNhap", "double", "Không rỗng, Giá trị > 0", "Giá vốn mua vào từ nhà cung cấp"],
        ["6", "giaBan", "double", "Không rỗng, Ràng buộc: giaBan >= giaNhap", "Giá bán lẻ niêm yết tại quầy"],
        ["7", "chatLieu", "String", "Có thể rỗng, Tối đa 50 ký tự", "Chất liệu chế tác (Da bò, Canvas, Vải dệt...)"],
        ["8", "trangThai", "boolean", "Không rỗng, Mặc định true (True: Kinh doanh, False: Ngừng)", "Trạng thái xóa mềm danh mục"]
    ]
    style_table(t_sp, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], sp_data)

    # Table 5: ChiTietGiay
    add_h3("5. Lớp ChiTietGiay (Biến thể SKU - Kích cỡ & Màu sắc)")
    add_p("Lớp thành phần thuộc mối quan hệ Tổng thành chặt chẽ (Composition) với SanPham, lưu trữ số lượng tồn kho theo từng size và màu sắc.")
    add_table_caption(8, "Thuộc tính và phương thức của lớp ChiTietGiay")
    t_ctg = doc.add_table(rows=7, cols=5)
    ctg_data = [
        ["1", "maChiTietGiay", "String", "PK, Không rỗng, Regex: ^CTG[0-9]{4}$", "Mã định danh biến thể SKU (CTG0001...)"],
        ["2", "sanPham", "SanPham", "FK, Không rỗng, Tham chiếu SanPham cha", "Con trỏ đối tượng mẫu giày sở hữu"],
        ["3", "kichThuoc", "int", "Không rỗng, Khoảng giá trị từ 35 - 45", "Kích cỡ giày chuẩn EU"],
        ["4", "mauSac", "String", "Không rỗng, Tối đa 30 ký tự", "Màu sắc cụ thể (Trắng, Đen, Xám...)"],
        ["5", "soLuongTon", "int", "Không rỗng, Giá trị >= 0", "Số lượng tồn kho thực tế của biến thể"],
        ["6", "hinhAnh", "String", "Có thể rỗng, Tên tệp ảnh minh họa", "Đường dẫn file ảnh sản phẩm"]
    ]
    style_table(t_ctg, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ctg_data)

    # Table 6: HoaDon
    add_h3("6. Lớp HoaDon (Hóa đơn thanh toán bán lẻ)")
    add_p("Lớp thực thể quản lý giao dịch thanh toán tại quầy thu ngân, lưu trữ đầy đủ 13 thuộc tính tài chính phục vụ hạch toán kế toán.")
    add_table_caption(9, "Thuộc tính và phương thức của lớp HoaDon")
    t_hd = doc.add_table(rows=14, cols=5)
    hd_data = [
        ["1", "maHoaDon", "String", "PK, Không rỗng, Regex: ^HD[0-9]{6}$", "Mã hóa đơn (HD000001, HD000002...)"],
        ["2", "ngayLap", "LocalDateTime", "Không rỗng, Mặc định ngày giờ hiện tại", "Thời điểm phát sinh giao dịch"],
        ["3", "nhanVien", "NhanVien", "FK, Không rỗng, Tham chiếu NhanVien", "Nhân viên thu ngân lập hóa đơn"],
        ["4", "khachHang", "KhachHang", "FK, Có thể null nếu là khách vãng lai", "Khách hàng nhận hóa đơn và tích điểm"],
        ["5", "tongTienHang", "double", "Không rỗng, Giá trị >= 0", "Tổng tiền hàng ban đầu trước khi giảm"],
        ["6", "chietKhau", "double", "Không rỗng, Giá trị >= 0, Mặc định: 0", "Tiền giảm giá theo hạng thành viên"],
        ["7", "diemSuDung", "int", "Không rỗng, Giá trị >= 0, Mặc định: 0", "Số điểm tích lũy dùng đổi thưởng"],
        ["8", "tienGiamDiem", "double", "Ràng buộc: tienGiamDiem = diemSuDung * 1000", "Số tiền mặt được khấu trừ từ điểm"],
        ["9", "tongTien", "double", "Ràng buộc: tongTien = tongTienHang - chietKhau - tienGiamDiem", "Số tiền thực tế khách hàng phải trả"],
        ["10", "phuongThucTT", "String", "Không rỗng, {'Tiền mặt', 'Chuyển khoản QR'}", "Hình thức thanh toán tại quầy"],
        ["11", "tienKhachDua", "double", "Ràng buộc: tienKhachDua >= tongTien", "Số tiền khách đưa cho thu ngân"],
        ["12", "tienThua", "double", "Ràng buộc: tienThua = tienKhachDua - tongTien", "Số tiền thừa phải thối lại cho khách"],
        ["13", "diemCong", "int", "Ràng buộc: diemCong = (int)(tongTien / 100000)", "Số điểm mới được cộng sau khi mua"]
    ]
    style_table(t_hd, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], hd_data)

    # Table 7: ChiTietHoaDon
    add_h3("7. Lớp ChiTietHoaDon (Chi tiết dòng sản phẩm trong hóa đơn)")
    add_p("Lớp thành phần thuộc mối quan hệ Tổng thành chặt chẽ (Composition) với HoaDon, lưu thông tin sản phẩm, số lượng và giá bán tại thời điểm lập đơn.")
    add_table_caption(10, "Thuộc tính và phương thức của lớp ChiTietHoaDon")
    t_cthd = doc.add_table(rows=7, cols=5)
    cthd_data = [
        ["1", "hoaDon", "HoaDon", "PK, FK, Không rỗng, Tham chiếu HoaDon cha", "Con trỏ đối tượng hóa đơn sở hữu"],
        ["2", "chiTietGiay", "ChiTietGiay", "PK, FK, Không rỗng, Tham chiếu ChiTietGiay", "Biến thể giày được bán"],
        ["3", "soLuong", "int", "Không rỗng, Giá trị > 0", "Số lượng đôi giày mua trong đơn"],
        ["4", "donGia", "double", "Không rỗng, Giá trị > 0", "Đơn giá niêm yết tại thời điểm xuất bán"],
        ["5", "giamGia", "double", "Giá trị >= 0, Không vượt quá soLuong * donGia", "Tiền giảm giá riêng cho dòng hàng"],
        ["6", "thanhTien", "double", "Ràng buộc: thanhTien = soLuong * donGia - giamGia", "Thành tiền của dòng sản phẩm"]
    ]
    style_table(t_cthd, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], cthd_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)
    # ==========================================
    add_h1("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)")
    add_h2("I. Sơ đồ thực thể liên kết trên HQTCSDL SQL Server (ERD 6 bảng)")
    add_p("Cơ sở dữ liệu QuanLyBanGiay được thiết kế và chuẩn hóa nghiêm ngặt đạt Chuẩn 3 (3NF - Third Normal Form), phản ánh chính xác cấu trúc dữ liệu thực tế trên Microsoft SQL Server:")

    if os.path.exists("diagram_erd_shoe.png"):
        doc.add_picture("diagram_erd_shoe.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 4. Sơ đồ cơ sở dữ liệu quan hệ trên Microsoft SQL Server (Database ERD 6 bảng)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("II. Mô tả chi tiết cấu trúc 6 bảng dữ liệu chuẩn 3NF")
    tables_db = [
        ("1. Bảng NhanVien (Nhân sự & Phân quyền bảo mật SHA-256)", [
            ["maNhanVien", "VARCHAR(10)", "PK", "No", "Mã nhân viên (NV0001...), CHECK (maNhanVien LIKE 'NV[0-9][0-9][0-9][0-9]') [CK_NhanVien_ma]"],
            ["hoTen", "NVARCHAR(50)", "None", "No", "Họ và tên nhân viên"],
            ["soDienThoai", "VARCHAR(10)", "UQ", "No", "UNIQUE (UQ_NhanVien_soDienThoai), CHECK (soDienThoai LIKE '0[35789]........') [CK_NhanVien_sdt]"],
            ["ngaySinh", "DATE", "None", "No", "CHECK (DATEDIFF(year, ngaySinh, GETDATE()) >= 18) [CK_NhanVien_tuoi] (Đủ từ 18 tuổi)"],
            ["gioiTinh", "BIT", "None", "No", "DEFAULT 1 [DF_NhanVien_gioiTinh] (1: Nam, 0: Nữ)"],
            ["diaChi", "NVARCHAR(200)", "None", "Yes", "Địa chỉ thường trú liên lạc"],
            ["email", "VARCHAR(50)", "None", "Yes", "CHECK (email IS NULL OR email LIKE '%_@_%._%') [CK_NhanVien_email]"],
            ["chucVu", "NVARCHAR(30)", "None", "No", "CHECK (chucVu IN (N'Quản lý', N'Nhân viên bán hàng')) [CK_NhanVien_chucVu]"],
            ["luongCoBan", "DECIMAL(18,0)", "None", "No", "Lương cơ bản hàng tháng, CHECK (luongCoBan > 0) [CK_NhanVien_luong]"],
            ["caLamViec", "NVARCHAR(20)", "None", "Yes", "CHECK (caLamViec IS NULL OR caLamViec IN (N'Ca sáng', N'Ca chiều', N'Ca tối', N'Toàn thời gian')) [CK_NhanVien_ca]"],
            ["matKhau", "CHAR(64)", "None", "No", "Chuỗi băm mật khẩu SHA-256 hex (64 ký tự), CHECK (LEN(matKhau) = 64) [CK_NhanVien_matKhau]"],
            ["trangThai", "BIT", "None", "No", "DEFAULT 1 [DF_NhanVien_trangThai] (1: Đang làm việc, 0: Đã nghỉ việc)"]
        ]),
        ("2. Bảng KhachHang (Khách hàng thành viên và Tích điểm)", [
            ["maKhachHang", "VARCHAR(10)", "PK", "No", "Mã khách hàng (KH0001...), CHECK (maKhachHang LIKE 'KH[0-9][0-9][0-9][0-9]') [CK_KhachHang_ma]"],
            ["hoTen", "NVARCHAR(50)", "None", "No", "Họ và tên khách hàng"],
            ["soDienThoai", "VARCHAR(10)", "UQ", "No", "UNIQUE (UQ_KhachHang_soDienThoai), CHECK (soDienThoai LIKE '0[35789]........') [CK_KhachHang_sdt]"],
            ["ngaySinh", "DATE", "None", "Yes", "Ngày tháng năm sinh của khách hàng"],
            ["gioiTinh", "BIT", "None", "Yes", "Giới tính (1: Nam, 0: Nữ), DEFAULT 1 [DF_KhachHang_gioiTinh]"],
            ["diaChi", "NVARCHAR(200)", "None", "Yes", "Địa chỉ liên lạc của khách hàng"],
            ["email", "VARCHAR(50)", "None", "Yes", "CHECK (email IS NULL OR email LIKE '%_@_%._%') [CK_KhachHang_email]"],
            ["diemTichLuy", "INT", "None", "No", "Điểm tích lũy, DEFAULT 0 [DF_KhachHang_diem], CHECK (diemTichLuy >= 0) [CK_KhachHang_diem]"],
            ["hangThanhVien", "NVARCHAR(20)", "None", "No", "Hạng thẻ, DEFAULT N'Đồng' [DF_KhachHang_hang], CHECK (hangThanhVien IN (N'Đồng', N'Bạc', N'Vàng', N'Kim Cương')) [CK_KhachHang_hang]"]
        ]),
        ("3. Bảng SanPham (Mẫu sản phẩm giày)", [
            ["maSanPham", "VARCHAR(10)", "PK", "No", "Mã mẫu giày (SP0001...), CHECK (maSanPham LIKE 'SP[0-9][0-9][0-9][0-9]') [CK_SanPham_ma]"],
            ["tenSanPham", "NVARCHAR(100)", "None", "No", "Tên mẫu giày, CHECK (LEN(LTRIM(RTRIM(tenSanPham))) > 0) [CK_SanPham_ten]"],
            ["loaiGiay", "NVARCHAR(30)", "None", "No", "Phân loại kiểu dáng mẫu giày (Sneaker, Oxford, Sandal, Boots...)"],
            ["thuongHieu", "NVARCHAR(50)", "None", "No", "Hãng sản xuất / nhãn hiệu xuất xứ (Nike, Adidas, Puma, Converse...)"],
            ["giaNhap", "DECIMAL(18,0)", "None", "No", "Giá vốn nhập kho, CHECK (giaNhap > 0) [CK_SanPham_giaNhap]"],
            ["giaBan", "DECIMAL(18,0)", "None", "No", "Giá bán niêm yết, CHECK (giaBan >= giaNhap) [CK_SanPham_giaBan]"],
            ["chatLieu", "NVARCHAR(50)", "None", "Yes", "Chất liệu chế tác (Da bò, Da PU, Canvas, Mesh...)"],
            ["trangThai", "BIT", "None", "No", "DEFAULT 1 [DF_SanPham_trangThai] (1: Đang kinh doanh, 0: Ngừng kinh doanh - Xóa mềm)"]
        ]),
        ("4. Bảng ChiTietGiay (Biến thể kích cỡ và màu sắc SKU)", [
            ["maChiTietGiay", "VARCHAR(10)", "PK", "No", "Mã biến thể SKU (CTG0001...), CHECK (maChiTietGiay LIKE 'CTG[0-9][0-9][0-9][0-9]') [CK_ChiTietGiay_ma]"],
            ["maSanPham", "VARCHAR(10)", "FK", "No", "FK tham chiếu SanPham(maSanPham) [FK_ChiTietGiay_SanPham]"],
            ["kichThuoc", "INT", "None", "No", "Kích cỡ giày, CHECK (kichThuoc BETWEEN 35 AND 45) [CK_ChiTietGiay_size]"],
            ["mauSac", "NVARCHAR(30)", "None", "No", "Màu sắc biến thể. UNIQUE (maSanPham, kichThuoc, mauSac) [UQ_ChiTietGiay_BienThe]"],
            ["soLuongTon", "INT", "None", "No", "Số lượng tồn kho biến thể, DEFAULT 0 [DF_ChiTietGiay_ton], CHECK (soLuongTon >= 0) [CK_ChiTietGiay_ton]"],
            ["hinhAnh", "VARCHAR(200)", "None", "Yes", "Tên file ảnh biến thể, DEFAULT 'default_shoe.png' [DF_ChiTietGiay_anh]"]
        ]),
        ("5. Bảng HoaDon (Hóa đơn thanh toán giao dịch 13 cột)", [
            ["maHoaDon", "VARCHAR(10)", "PK", "No", "Mã hóa đơn (HD000001...), CHECK (maHoaDon LIKE 'HD[0-9][0-9][0-9][0-9][0-9][0-9]') [CK_HoaDon_ma]"],
            ["ngayLap", "DATETIME", "None", "No", "Thời điểm lập hóa đơn, DEFAULT GETDATE() [DF_HoaDon_ngayLap]"],
            ["maNhanVien", "VARCHAR(10)", "FK", "No", "FK tham chiếu NhanVien(maNhanVien) [FK_HoaDon_NhanVien]"],
            ["maKhachHang", "VARCHAR(10)", "FK", "Yes", "FK tham chiếu KhachHang(maKhachHang) [FK_HoaDon_KhachHang], NULL là khách vãng lai"],
            ["tongTienHang", "DECIMAL(18,0)", "None", "No", "Tổng tiền hàng trước giảm, CHECK (tongTienHang >= 0) [CK_HoaDon_soAm]"],
            ["chietKhau", "DECIMAL(18,0)", "None", "No", "Số tiền chiết khấu theo hạng thẻ, DEFAULT 0 [DF_HoaDon_chietKhau], CHECK (chietKhau >= 0) [CK_HoaDon_soAm]"],
            ["diemSuDung", "INT", "None", "No", "Số điểm tích lũy dùng khấu trừ, DEFAULT 0 [DF_HoaDon_diemSuDung], CHECK (diemSuDung >= 0) [CK_HoaDon_soAm]"],
            ["tienGiamDiem", "DECIMAL(18,0)", "None", "No", "DEFAULT 0 [DF_HoaDon_tienGiamDiem], CHECK (tienGiamDiem = diemSuDung * 1000) [CK_HoaDon_tienDiem]"],
            ["tongTien", "DECIMAL(18,0)", "None", "No", "Tổng tiền khách phải trả, CHECK (tongTien = tongTienHang - chietKhau - tienGiamDiem AND tongTien >= 0) [CK_HoaDon_tongTien]"],
            ["phuongThucTT", "NVARCHAR(30)", "None", "No", "DEFAULT N'Tiền mặt' [DF_HoaDon_pttt], CHECK (phuongThucTT IN (N'Tiền mặt', N'Chuyển khoản QR')) [CK_HoaDon_pttt]"],
            ["tienKhachDua", "DECIMAL(18,0)", "None", "No", "Tiền khách đưa, CHECK (tienKhachDua >= tongTien) [CK_HoaDon_tienDua], QR thì tiền đưa bằng tổng tiền [CK_HoaDon_chuyenKhoan]"],
            ["tienThua", "DECIMAL(18,0)", "None", "No", "Tiền thừa thối lại, CHECK (tienThua = tienKhachDua - tongTien) [CK_HoaDon_tienThua]"],
            ["diemCong", "INT", "None", "No", "Điểm tích lũy cộng mới (= tongTien / 100000), DEFAULT 0 [DF_HoaDon_diemCong], CHECK (diemCong >= 0) [CK_HoaDon_soAm]"]
        ]),
        ("6. Bảng ChiTietHoaDon (Chi tiết dòng sản phẩm mua)", [
            ["maHoaDon", "VARCHAR(10)", "PK, FK", "No", "FK tham chiếu HoaDon(maHoaDon) [FK_ChiTietHoaDon_HoaDon]"],
            ["maChiTietGiay", "VARCHAR(10)", "PK, FK", "No", "FK tham chiếu ChiTietGiay(maChiTietGiay) [FK_ChiTietHoaDon_ChiTietGiay]"],
            ["soLuong", "INT", "None", "No", "Số lượng mua, CHECK (soLuong > 0) [CK_ChiTietHoaDon_soLuong]"],
            ["donGia", "DECIMAL(18,0)", "None", "No", "Đơn giá tại thời điểm mua, CHECK (donGia > 0) [CK_ChiTietHoaDon_donGia]"],
            ["giamGia", "DECIMAL(18,0)", "None", "No", "Tiền giảm giá khuyến mãi dòng hàng, DEFAULT 0 [DF_ChiTietHoaDon_giamGia], CHECK (giamGia >= 0 AND giamGia <= soLuong * donGia) [CK_ChiTietHoaDon_giamGia]"],
            ["thanhTien", "DECIMAL(18,0)", "None", "No", "Thành tiền dòng hàng, CHECK (thanhTien = soLuong * donGia - giamGia) [CK_ChiTietHoaDon_thanhTien]"]
        ])
    ]

    db_table_titles = {
        "NhanVien": "Cấu trúc trường dữ liệu bảng NhanVien trên Microsoft SQL Server",
        "KhachHang": "Cấu trúc trường dữ liệu bảng KhachHang trên Microsoft SQL Server",
        "SanPham": "Cấu trúc trường dữ liệu bảng SanPham trên Microsoft SQL Server",
        "ChiTietGiay": "Cấu trúc trường dữ liệu bảng ChiTietGiay trên Microsoft SQL Server",
        "HoaDon": "Cấu trúc trường dữ liệu bảng HoaDon trên Microsoft SQL Server",
        "ChiTietHoaDon": "Cấu trúc trường dữ liệu bảng ChiTietHoaDon trên Microsoft SQL Server"
    }
    for t_idx, (t_name, rows_info) in enumerate(tables_db, 11):
        add_h3(t_name)
        clean_tbl = t_name.split()[2]
        add_table_caption(t_idx, db_table_titles.get(clean_tbl, f"Cấu trúc trường dữ liệu bảng {clean_tbl} trên Microsoft SQL Server"))
        t_elem = doc.add_table(rows=len(rows_info) + 1, cols=5)
        style_table(t_elem, [1.5, 1.2, 0.7, 0.7, 2.2], ["Tên cột", "Kiểu dữ liệu", "Khóa", "Null", "Ràng buộc & Mô tả"], rows_info)

    add_h2("III. Cơ chế xử lý toàn vẹn dữ liệu nâng cao (Ràng buộc CHECK & JDBC Transaction)")
    add_h3("1. Hệ thống 33 ràng buộc CHECK toàn vẹn nghiệp vụ trên SQL Server")
    add_p("Để bảo đảm dữ liệu luôn chính xác và nhất quán ngay từ tầng lưu trữ vật lý, hệ thống cài đặt đầy đủ 33 ràng buộc CHECK chặt chẽ phân bổ trên 6 bảng dữ liệu của Microsoft SQL Server:")
    add_bullet("Bao gồm 8 ràng buộc: CK_NhanVien_ma (định dạng mã 'NV[0-9][0-9][0-9][0-9]'), CK_NhanVien_sdt (10 số di động Việt Nam), CK_NhanVien_email (định dạng email hợp lệ hoặc NULL), CK_NhanVien_tuoi (nhân viên đủ từ 18 tuổi trở lên theo luật định), CK_NhanVien_chucVu (chỉ chấp nhận 'Quản lý' hoặc 'Nhân viên bán hàng'), CK_NhanVien_ca (thuộc các ca làm chuẩn hoặc toàn thời gian), CK_NhanVien_luong (lương cơ bản > 0), và CK_NhanVien_matKhau (độ dài đúng 64 ký tự hex của mã băm SHA-256).", "Bảng NhanVien (8 CHECK): ")
    add_bullet("Bao gồm 5 ràng buộc: CK_KhachHang_ma (định dạng 'KH[0-9][0-9][0-9][0-9]'), CK_KhachHang_sdt (10 chữ số), CK_KhachHang_email (chuẩn định dạng hòm thư điện tử), CK_KhachHang_diem (điểm tích lũy >= 0), và CK_KhachHang_hang (chỉ thuộc các hạng thẻ 'Đồng', 'Bạc', 'Vàng', 'Kim Cương').", "Bảng KhachHang (5 CHECK): ")
    add_bullet("Bao gồm 4 ràng buộc: CK_SanPham_ma (định dạng 'SP[0-9][0-9][0-9][0-9]'), CK_SanPham_ten (tên mẫu sản phẩm không được rỗng), CK_SanPham_giaNhap (giá vốn nhập kho > 0), và CK_SanPham_giaBan (giá bán ra phải >= giá vốn nhập kho).", "Bảng SanPham (4 CHECK): ")
    add_bullet("Bao gồm 3 ràng buộc: CK_ChiTietGiay_ma (định dạng mã biến thể SKU 'CTG[0-9][0-9][0-9][0-9]'), CK_ChiTietGiay_size (kích cỡ giày trong khoảng 35 đến 45), và CK_ChiTietGiay_ton (số lượng tồn kho SoLuongTon >= 0).", "Bảng ChiTietGiay (3 CHECK): ")
    add_bullet("Bao gồm 9 ràng buộc: CK_HoaDon_ma (định dạng hóa đơn 6 số 'HD[0-9][0-9][0-9][0-9][0-9][0-9]'), CK_HoaDon_soAm (tổng tiền hàng, chiết khấu, điểm sử dụng, tiền giảm điểm, điểm cộng đều >= 0), CK_HoaDon_tienDiem (tiền giảm điểm = diemSuDung * 1000), CK_HoaDon_tongTien (tongTien = tongTienHang - chietKhau - tienGiamDiem >= 0), CK_HoaDon_diemKhach (khách vãng lai không có mã thành viên thì chietKhau = diemSuDung = diemCong = 0), CK_HoaDon_pttt (phương thức thuộc 'Tiền mặt' hoặc 'Chuyển khoản QR'), CK_HoaDon_tienDua (tiền khách đưa >= tổng tiền), CK_HoaDon_chuyenKhoan (nếu chuyển khoản QR thì tiền đưa phải bằng đúng tổng tiền), và CK_HoaDon_tienThua (tiền thừa = tienKhachDua - tongTien).", "Bảng HoaDon (9 CHECK): ")
    add_bullet("Bao gồm 4 ràng buộc: CK_ChiTietHoaDon_soLuong (số lượng mua > 0), CK_ChiTietHoaDon_donGia (đơn giá sản phẩm bán ra > 0), CK_ChiTietHoaDon_giamGia (0 <= tiền giảm giá <= số lượng * đơn giá), và CK_ChiTietHoaDon_thanhTien (thành tiền = số lượng * đơn giá - giảm giá).", "Bảng ChiTietHoaDon (4 CHECK): ")

    add_h3("2. Quản lý JDBC Transaction ACID & Khóa tồn kho nguyên tử (Concurrency Control)")
    add_p("Để xử lý đồng thời trong giờ cao điểm khi nhiều quầy thu ngân cùng thực hiện giao dịch thanh toán trên cùng một biến thể sản phẩm có số lượng tồn kho giới hạn, hệ thống không dùng thủ tục phản xạ sự kiện CSDL ngầm định nhằm tránh tắc nghẽn khóa máy chủ. Thay vào đó, toàn bộ nghiệp vụ kiểm soát bán hàng được quản trị chặt chẽ tại tầng DAO (dao/HoaDon_DAO.java) bằng cơ chế JDBC Transaction tuân thủ nghiêm ngặt 4 nguyên lý ACID:")
    add_bullet("Thiết lập con.setAutoCommit(false) ngay đầu phương thức themHoaDon() để khởi tạo Transaction cục bộ, gom toàn bộ chuỗi ghi nhận dữ liệu vào một phiên giao dịch nguyên tử duy nhất.", "Khởi tạo Transaction: ")
    add_bullet("Khi sinh mã hóa đơn mới, thực thi câu lệnh 'SELECT ISNULL(MAX(CAST(SUBSTRING(maHoaDon,3,6) AS INT)),0)+1 FROM HoaDon WITH (UPDLOCK, HOLDLOCK)'. Khóa UPDLOCK kết hợp HOLDLOCK giữ an toàn dải khóa trong suốt Transaction, ngăn chặn triệt để xung đột sinh trùng mã hóa đơn giữa các quầy thu ngân chạy song song.", "Khóa đọc an toàn sinh mã: ")
    add_bullet("Thực thi câu lệnh UPDATE trừ kho nguyên tử có điều kiện: 'UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?'. Nhờ điều kiện soLuongTon >= ?, nếu số lượng tồn kho hiện tại không đủ đáp ứng, SQL Server sẽ cập nhật 0 dòng (rowsAffected == 0). Khi đó, hệ thống lập tức phát lệnh con.rollback(), ghi nhận thông báo lỗi chi tiết vào thuộc tính lastErrorMessage và trả về false để tầng giao diện BanHang_GUI hiển thị hộp thoại cảnh báo chính xác cho thu ngân.", "Khóa tồn kho nguyên tử: ")
    add_bullet("Cập nhật điểm tích lũy và tự động nâng hạng thẻ thành viên cho khách hàng thân thiết trên bảng KhachHang.", "Đồng bộ tích điểm: ")
    add_bullet("Chỉ khi toàn bộ các bước ghi bảng HoaDon, từng dòng ChiTietHoaDon, trừ kho ChiTietGiay và cập nhật khách hàng đều hoàn thành hợp lệ, lệnh con.commit() mới được kích hoạt để chốt dữ liệu vĩnh viễn vào SQL Server. Trong khối catch (SQLException), hệ thống lập tức thực hiện con.rollback() nhằm hoàn nguyên trạng thái kho và hóa đơn về trước thời điểm bắt đầu giao dịch. Khối finally luôn gọi con.setAutoCommit(true) để đưa trạng thái kết nối của Singleton ConnectDB trở lại chế độ tự động xác nhận mặc định, bảo đảm an toàn cho các tác vụ tiếp theo.", "Cam kết & Hoàn nguyên (Commit & Rollback): ")

    add_h3("3. Chiến lược Xóa mềm (Soft-Delete Pattern)")
    add_p("Trong hệ thống bán lẻ, việc xóa vật lý (DELETE) trực tiếp các bản ghi dữ liệu danh mục là điều tối kỵ vì sẽ gây lỗi ràng buộc khóa ngoại (Foreign Key Constraint Error 547) đối với các hóa đơn giao dịch đã phát sinh trong quá khứ. Ngược lại, nếu thiết lập xóa lan truyền (CASCADE DELETE), hệ thống sẽ vô tình xóa sạch toàn bộ lịch sử bán hàng và chi tiết đơn hàng, gây sai lệch nghiêm trọng báo cáo doanh thu kế toán.")
    add_p("Nhóm phát triển giải quyết triệt để bài toán này bằng chiến lược Xóa mềm (Soft-Delete Pattern) thông qua các trường trạng thái quản lý:")
    add_bullet("Bảng SanPham được thiết kế cột trangThai (BIT, DEFAULT 1). Khi người quản lý thực hiện thao tác xóa một mẫu giày, hệ thống (thông qua SanPham_DAO) chỉ thực thi câu lệnh cập nhật trạng thái: UPDATE SanPham SET trangThai = 0 WHERE maSanPham = ?. Giao diện bán hàng chỉ tải dữ liệu danh mục với điều kiện WHERE trangThai = 1, do đó mẫu giày đã ngừng kinh doanh sẽ lập tức ẩn khỏi quầy thu ngân nhưng toàn bộ hóa đơn và doanh thu trong quá khứ vẫn được bảo toàn nguyên vẹn 100%.", "Xóa mềm sản phẩm: ")
    add_bullet("Bảng NhanVien cũng được quản lý trạng thái bằng cột trangThai (BIT, DEFAULT 1). Khi nhân viên thôi việc, lớp NhanVien_DAO thực hiện cập nhật trangThai = 0 (xóa mềm). Chuỗi băm mật khẩu SHA-256 trong CSDL vẫn được giữ nguyên vẹn, nhưng phương thức xác thực NhanVien_DAO.dangNhap() kiểm tra điều kiện lọc 'WHERE trangThai = 1', do đó tài khoản nhân viên đã nghỉ sẽ bị từ chối đăng nhập ngay lập tức trong khi lịch sử lập hóa đơn trong quá khứ vẫn được bảo toàn nguyên vẹn.", "Quản lý nhân viên thôi việc: ")
    add_bullet("Các ràng buộc khóa ngoại tham chiếu từ ChiTietHoaDon đến HoaDon và ChiTietGiay đều giữ nguyên tắc không xóa lan truyền (NO ACTION), bảo đảm dữ liệu chứng từ thanh toán là bất biến (immutable) theo đúng chuẩn mực hạch toán tài chính.", "Bảo toàn chứng từ tài chính: ")

    doc.add_page_break()

    # ==========================================
    # PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH
    # ==========================================
    add_h1("PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH")
    
    # 1. Đăng nhập
    add_h2("I. Chức năng Đăng nhập & Phân quyền truy cập (Login & RBAC)")
    add_p("Giao diện Đăng nhập (DangNhap_GUI) được thiết kế đồng bộ theo phong cách hiện đại với UIHelper tự vẽ bo góc trang nhã. Người dùng nhập mã nhân viên (NV0001, NV0002...) và mật khẩu, hệ thống tự động băm mật khẩu bằng SHA-256 để kiểm tra xác thực.")

    if os.path.exists("screenshot_dangnhap.png"):
        doc.add_picture("screenshot_dangnhap.png", width=Inches(4.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 5. Giao diện Đăng nhập hệ thống (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Nhân viên khởi chạy ứng dụng. Con trỏ chuột tự động focus sẵn vào ô 'Mã nhân viên' (chuẩn định dạng mã NVxxxx).", "Bước 1 - Mở ứng dụng: ")
    add_bullet("Nhân viên nhập mã số và mật khẩu. Người dùng có thể nhấn phím Enter tại bất kỳ ô nhập liệu nào để thực hiện đăng nhập nhanh mà không cần thao tác chuột.", "Bước 2 - Nhập thông tin đăng nhập: ")
    add_bullet("Nhấn Enter hoặc click nút 'Đăng Nhập'. Hệ thống gọi NhanVien_DAO.dangNhap() để xác thực: mật khẩu nhập vào được băm bằng thuật toán SHA-256 (tạo chuỗi hex 64 ký tự) và đối chiếu trực tiếp với cột matKhau trong bảng NhanVien.", "Bước 3 - Xác thực thông tin: ")
    add_bullet("Nếu là Quản lý: Hệ thống hiển thị đầy đủ các tab chức năng trên ManHinhChinh_GUI gồm Bán hàng (POS), Quản lý mẫu giày, Khách hàng & tích điểm, Quản lý nhân sự và Thống kê doanh thu. Nếu là Nhân viên bán hàng: Hệ thống chỉ hiển thị 3 tab phục vụ bán lẻ và vô hiệu hóa các nút Thêm, Sửa, Xóa trên màn hình danh mục sản phẩm.", "Bước 4 - Phân quyền giao diện: ")
    add_callout("Bảo mật mật khẩu với mã băm SHA-256 & Cơ chế dự phòng Fallback: Hệ thống lưu trữ mật khẩu băm một chiều bằng thuật toán SHA-256 (chuỗi hex 64 ký tự) tương thích chuẩn xác với trường matKhau kiểu CHAR(64). Mã nguồn NhanVien_DAO đã tích hợp sẵn thuật toán nâng cao PBKDF2WithHmacSHA256 (100.000 vòng lặp, salt ngẫu nhiên) cùng cơ chế kiểm tra kích thước cột tự động fallback về SHA-256, sẵn sàng nâng cấp lên PBKDF2 khi mở rộng kích thước cột CSDL trong tương lai.", "BẢO MẬT XÁC THỰC:");

    # 2. Bán hàng POS & Sequence Diagram
    add_h2("II. Chức năng Bán hàng tại quầy (POS) & Sơ đồ tuần tự Sequence")
    add_p("Màn hình Bán hàng (BanHang_GUI) là phân hệ cốt lõi phục vụ trực tiếp nghiệp vụ tại quầy thu ngân, được thiết kế tối ưu công thái học với 2 khu vực chức năng trực quan: Bên trái là khu vực chọn biến thể mẫu giày (Size 35-45, Màu sắc, Tồn kho thực tế) và Bảng giỏ hàng; Bên phải là khu vực nhận diện khách hàng, tích điểm đổi thưởng và Bảng tính tiền thừa tự động.")

    if os.path.exists("screenshot_banhang.png"):
        doc.add_picture("screenshot_banhang.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 6. Giao diện Bán hàng tại quầy POS với đầy đủ thông tin tồn kho và giỏ hàng (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_p("Sơ đồ Tuần tự (Sequence Diagram) mô tả chi tiết tương tác thời gian thực giữa Thu ngân, Giao diện POS (BanHang_GUI), Tầng DAO (HoaDon_DAO, ChiTietGiay_DAO) và Cơ sở dữ liệu Microsoft SQL Server trong một phiên giao dịch thanh toán chuẩn ACID:")

    if os.path.exists("vp_sequence_diagram.png"):
        doc.add_picture("vp_sequence_diagram.png", width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS (Visual Paradigm 18)")
        set_font(r_c, size=10, italic=True, color_rgb=(0, 0, 0))
    elif os.path.exists("diagram_sequence_shoe.png"):
        doc.add_picture("diagram_sequence_shoe.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS (Visual Paradigm 18)")
        set_font(r_c, size=10, italic=True, color_rgb=(0, 0, 0))

    add_p("Hộp thoại xem trước phiếu Hóa đơn K80 tương tác (JDialog) tích hợp nút In máy in và nút Xuất file văn bản:")
    if os.path.exists("screenshot_hoadon_k80.png"):
        doc.add_picture("screenshot_hoadon_k80.png", width=Inches(4.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 8. Hộp thoại xem trước Hóa đơn K80 tích hợp chức năng In máy in và Xuất file văn bản (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Khi thu ngân nhấn [F10] hoặc click nút 'THANH TOÁN & IN HÓA ĐƠN', hệ thống mở hộp thoại JDialog xem trước hóa đơn nhiệt K80 với đầy đủ 13 trường dữ liệu tài chính, chiết khấu và điểm tích lũy.", "Xem trước hóa đơn K80: ")
    add_bullet("Nút '🖨 In Hóa Đơn': Tích hợp thư viện java.awt.print.PrinterJob kết hợp giao diện Printable chuẩn Java Desktop, cho phép gửi lệnh in trực tiếp tới máy in nhiệt tại quầy thu ngân mà không qua phần mềm trung gian.", "In hóa đơn vật lý: ")
    add_bullet("Nút '📄 Xuất File Hóa Đơn': Tự động tạo và ghi nội dung phiếu hóa đơn ra tệp văn bản định dạng UTF-8 tại thư mục hoadon/HDxxxxxx.txt (phương thức HoaDon_DAO.xuatHoaDonRaFileTxt()), phục vụ công tác sao lưu chứng từ kế toán.", "Xuất file văn bản: ")
    add_bullet("BanHang_GUI thực hiện hàm nội bộ validateForm() kiểm tra giỏ hàng không rỗng, tiền khách đưa >= tổng tiền cần thanh toán.", "Kiểm tra hình thức tại GUI: ")
    add_bullet("HoaDon_DAO phát lệnh con.setAutoCommit(false) để khởi tạo phiên giao dịch ACID cục bộ trên kết nối JDBC.", "Khởi tạo Transaction: ")
    add_bullet("HoaDon_DAO thực thi truy vấn sinh mã có khóa an toàn: 'SELECT MAX(maHoaDon)+1 WITH (UPDLOCK, HOLDLOCK)'. SQL Server trả về mã hóa đơn mới duy nhất mà không bị xung đột giữa các quầy thu ngân.", "Khóa an toàn sinh mã: ")
    add_bullet("Thực thi UPDATE trừ kho nguyên tử: 'UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?'.", "Trừ tồn kho có điều kiện: ")
    add_bullet("Nếu kho đủ tồn, hệ thống cập nhật điểm tích lũy, con.commit() chốt dữ liệu vào SQL Server và kích hoạt hộp thoại xem trước hóa đơn K80. Nếu kho không đủ tồn, hệ thống con.rollback() và thông báo lỗi rõ ràng.", "Phân nhánh Commit & Rollback: ")
    add_bullet("Hệ thống hỗ trợ 2 hình thức thanh toán tại quầy là 'Tiền mặt' và 'Chuyển khoản QR'. Đối với 'Chuyển khoản QR', hệ thống tự động gán tiền khách đưa bằng tổng tiền thanh toán để tiện đối soát.", "Phương thức thanh toán: ")

    # 3. Quản lý sản phẩm
    add_h2("III. Chức năng Quản lý sản phẩm giày dép & Biến thể SKU")
    add_p("Phân hệ Quản lý sản phẩm (QuanLySanPham_GUI) phục vụ ban quản lý theo dõi và điều chỉnh danh mục hàng hóa:")

    if os.path.exists("screenshot_sanpham.png"):
        doc.add_picture("screenshot_sanpham.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 9. Giao diện Quản lý danh mục mẫu giày (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_p("Hộp thoại Tìm kiếm nâng cao Sản phẩm đa tiêu chí:")
    if os.path.exists("screenshot_timkiem_sanpham.png"):
        doc.add_picture("screenshot_timkiem_sanpham.png", width=Inches(4.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 10. Hộp thoại Tìm kiếm nâng cao Sản phẩm theo đa tiêu chí (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Form thông tin sản phẩm gồm: Mã sản phẩm (định dạng SPxxxx), Tên sản phẩm, Phân loại (Sneaker, Chạy bộ, Sandal, Da bò), Thương hiệu (Nike, Adidas, Vans, Converse, Biti's), Giá nhập, Giá bán và Chất liệu.", "Bố cục form thông tin: ")
    add_bullet("Tìm kiếm nâng cao đa tiêu chí (SanPham_DAO.timKiemNangCao()): Cho phép kết hợp lọc đồng thời theo Thương hiệu (Nike, Adidas, Vans, Converse, Biti's), Phân loại (Sneaker, Chạy bộ, Sandal, Da bò), Khoảng giá bán (Giá từ - Giá đến) và Tình trạng tồn kho (Còn hàng trong kho, Hết hàng/Ngừng bán), hỗ trợ nhân viên tư vấn nhanh chóng cho khách hàng.", "Tìm kiếm nâng cao đa tiêu chí: ")
    add_bullet("Hệ thống tự động sinh một biến thể SKU mặc định (kích cỡ 40, màu Đen, soLuongTon = 20) trong ChiTietGiay khi tạo mới mẫu giày để sẵn sàng phục vụ bán hàng ngay lập tức.", "Khởi tạo biến thể mặc định: ")
    add_bullet("Kiểm tra tính hợp lệ của dữ liệu: Ràng buộc giaBan >= giaNhap > 0 nhằm bảo đảm hiệu quả kinh tế cho cửa hàng.", "Kiểm soát giá cả nghiêm ngặt: ")
    add_bullet("Áp dụng cơ chế Xóa mềm (Soft-Delete): Khi người quản lý thực hiện xóa một mẫu giày, hệ thống cập nhật trangThai = 0 trong bảng SanPham. Nhờ vậy, sản phẩm sẽ không còn xuất hiện trong danh mục bán lẻ tại quầy POS nhưng toàn bộ các dòng hóa đơn bán hàng trong quá khứ vẫn được bảo toàn nguyên vẹn 100%, tránh được lỗi vi phạm khóa ngoại trong cơ sở dữ liệu.", "Cơ chế xóa mềm an toàn: ")

    # 4. Quản lý khách hàng
    add_h2("IV. Chức năng Quản lý khách hàng & Tích điểm thành viên")
    add_p("Phân hệ Quản lý khách hàng (QuanLyKhachHang_GUI) xây dựng mối quan hệ gắn kết với khách hàng thân thiết:")

    if os.path.exists("screenshot_khachhang.png"):
        doc.add_picture("screenshot_khachhang.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 11. Giao diện Quản lý khách hàng và phân hạng tích điểm (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_p("Hộp thoại Tìm kiếm nâng cao Khách hàng theo phân hạng và điểm tích lũy:")
    if os.path.exists("screenshot_timkiem_khachhang.png"):
        doc.add_picture("screenshot_timkiem_khachhang.png", width=Inches(4.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 12. Hộp thoại Tìm kiếm nâng cao Khách hàng theo phân hạng và điểm tích lũy (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Bảng dữ liệu hiển thị danh sách khách hàng gồm: Mã KH (KHxxxx), Họ tên, Số điện thoại, Địa chỉ, Điểm tích lũy và Hạng thành viên.", "Danh sách và thông tin chi tiết: ")
    add_bullet("Tìm kiếm nâng cao khách hàng (KhachHang_DAO.timKiemNangCao()): Cung cấp bộ lọc đa tiêu chí theo Hạng thành viên (Đồng, Bạc, Vàng, Kim Cương), Khoảng điểm tích lũy (Điểm từ - Điểm đến) và Giới tính, phục vụ đắc lực cho các chiến dịch marketing và chăm sóc khách hàng VIP.", "Tìm kiếm nâng cao khách hàng: ")
    add_bullet("Form nhập liệu kiểm tra số điện thoại bắt buộc tuân theo biểu thức chính quy (Regex) 10 chữ số hợp lệ của các nhà mạng Việt Nam (^0[35789]\\d{8}$).", "Kiểm tra hợp lệ số điện thoại: ")
    add_bullet("Cột điểm tích lũy và hạng thành viên (Đồng, Bạc, Vàng, Kim Cương) được thiết lập chỉ đọc (read-only) trên form nhập liệu nhằm chống gian lận. Điểm số chỉ được tự động cộng dồn và thăng hạng khi giao dịch thanh toán hóa đơn hoàn tất.", "Bảo vệ điểm tích lũy: ")
    add_bullet("Hỗ trợ tìm kiếm khách hàng nhanh theo số điện thoại hoặc mã số. Thao tác xóa khách hàng được thực thi qua KhachHang_DAO.xoaKhachHang() (xóa vật lý nếu khách hàng chưa phát sinh hóa đơn).", "Thao tác dữ liệu khách hàng: ")

    # 5. Quản lý nhân sự
    add_h2("V. Chức năng Quản lý nhân sự & Phân quyền (Staff Management)")
    add_p("Phân hệ Quản lý nhân sự (QuanLyNhanVien_GUI) chỉ mở cho người quản lý cửa hàng (quản trị viên), điều phối toàn bộ hồ sơ nhân viên và ca làm việc:")

    if os.path.exists("screenshot_nhanvien.png"):
        doc.add_picture("screenshot_nhanvien.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 13. Giao diện Quản lý nhân sự và phân quyền (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Form quản lý nhân viên gồm: Mã nhân viên (NVxxxx), Họ tên, Số điện thoại, Giới tính, Ngày sinh, Địa chỉ, Email, Chức vụ (Quản lý hoặc Nhân viên bán hàng), Lương cơ bản và Ca làm việc (Toàn thời gian, Ca sáng, Ca chiều, Ca tối).", "Hồ sơ nhân sự chi tiết: ")
    add_bullet("Ràng buộc độ tuổi lao động: Kiểm tra ngày sinh của nhân viên bảo đảm từ đủ 18 tuổi trở lên theo quy định pháp luật lao động.", "Kiểm tra tuổi lao động >= 18: ")
    add_bullet("Bảo mật mật khẩu SHA-256: Khi tạo nhân viên mới, mật khẩu mặc định (123456) được băm một chiều qua thuật toán SHA-256 thành chuỗi hex 64 ký tự trước khi lưu vào CSDL.", "Bảo mật tài khoản: ")
    add_bullet("Xử lý cho nhân viên nghỉ việc: Khi nhân viên thôi việc, hệ thống thực hiện cập nhật trangThai = 0 (xóa mềm). Chuỗi băm mật khẩu SHA-256 trong CSDL vẫn được giữ nguyên vẹn, nhưng phương thức xác thực NhanVien_DAO.dangNhap() kiểm tra điều kiện lọc 'WHERE trangThai = 1', do đó tài khoản nhân viên đã nghỉ sẽ bị từ chối đăng nhập ngay lập tức trong khi lịch sử hóa đơn trong quá khứ vẫn được bảo toàn nguyên vẹn.", "Khóa quyền truy cập nhân viên thôi việc: ")
    add_bullet("Cơ chế bảo vệ tài khoản Quản trị trưởng: Để bảo đảm hệ thống luôn duy trì ít nhất một tài khoản Quản lý hoạt động, tại tầng giao diện QuanLyNhanVien_GUI.java (dòng 305), hệ thống chặn cứng thao tác đổi trạng thái/nghỉ việc đối với mã quản trị mặc định 'NV0001' (kiểm tra điều kiện if (maNV.equalsIgnoreCase(\"NV0001\")) và hiển thị cảnh báo không được phép vô hiệu hóa tài khoản quản trị trưởng).", "Bảo vệ tài khoản Quản trị trưởng: ")

    # 6. Phân hệ Thống kê doanh thu & Hiệu suất bán hàng
    add_h2("VI. Phân hệ Thống kê doanh thu & Hiệu suất bán hàng (Analytics & Reporting)")
    add_p("Phân hệ Thống kê (ThongKe_GUI) là công cụ quản trị chiến lược dành riêng cho Quản lý cửa hàng (tích hợp trên thanh tab chính với phím tắt điều hướng nhanh [F5]), phản ánh trung thực và tức thời các chỉ số kinh doanh thu nhận trực tiếp từ CSDL Microsoft SQL Server:")

    if os.path.exists("screenshot_thongke.png"):
        doc.add_picture("screenshot_thongke.png", width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 14. Giao diện Báo cáo thống kê doanh thu và Top sản phẩm bán chạy (chụp thật ngày 07/11/2026)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_bullet("Bốn thẻ chỉ số trực quan (Bento KPI Cards): Tổng doanh thu (VNĐ) được tính toán chính xác từ HoaDon_DAO.getTongDoanhThu(); Số hóa đơn đã lập lấy từ HoaDon_DAO.getTongSoHoaDon(); Sản phẩm đã bán ra thực tế lấy từ HoaDon_DAO.getTongSoLuongBanRa() (tổng hợp SUM(soLuong) từ ChiTietHoaDon, phản ánh đúng lượng xuất kho thực tế, không dùng số ước lượng); và Tổng khách hàng thành viên từ KhachHang_DAO.getTongSoKhachHang().", "Bốn thẻ chỉ số tổng hợp (KPI Cards): ")
    add_bullet("Bộ lọc kỳ thời gian linh hoạt (Toàn bộ thời gian, Hôm nay, Tháng này, Năm nay): Hỗ trợ người quản lý lọc và tự động tái tính toán toàn bộ 4 thẻ KPI cùng bảng danh sách hóa đơn theo đúng khoảng thời gian cần phân tích.", "Bộ lọc kỳ thời gian: ")
    add_bullet("Bảng Top 5 sản phẩm bán chạy nhất (HoaDon_DAO.getTopSanPhamBanChay(5)): Truy vấn dữ liệu thực tế gom nhóm theo mã sản phẩm và sắp xếp theo tổng số lượng bán giảm dần, giúp quản lý nhận diện xu hướng thị trường để chủ động nhập hàng.", "Xếp hạng sản phẩm bán chạy: ")
    add_bullet("Tra cứu hóa đơn & Chi tiết giao dịch: Tìm kiếm nhanh hóa đơn theo mã HĐ hoặc số điện thoại khách hàng, xem chi tiết giỏ hàng và thời điểm lập của từng giao dịch.", "Tra cứu giao dịch: ")
    add_callout("Tối ưu hiệu năng tải dữ liệu bất đồng bộ: Phân hệ Thống kê ứng dụng kỹ thuật SwingWorker để thực thi các câu lệnh truy vấn tổng hợp phức tạp ngoài luồng giao diện (Event Dispatch Thread - EDT), bảo đảm giao diện đồ họa luôn phản hồi tức thì và không bị hiện tượng treo cứng.", "TỐI ƯU HIỆU NĂNG THỐNG KÊ:");

    # 7. Bảng phím tắt
    add_h2("VII. Bảng hệ thống phím tắt & Điều hướng bán hàng (Hotkeys)")
    add_p("Để tối ưu hóa trải nghiệm công thái học và giải phóng nhân viên thu ngân khỏi việc phải liên tục dùng chuột, hệ thống triển khai cơ chế KeyBindings với phạm vi WHEN_IN_FOCUSED_WINDOW trên JRootPane của ManHinhChinh_GUI. Cơ chế này cho phép bắt trọn vẹn các sự kiện phím chức năng trên toàn bộ cửa sổ ứng dụng:")
    add_table_caption(17, "Hệ thống phím tắt công thái học điều hướng bán hàng POS")
    t_hotkeys = doc.add_table(rows=9, cols=3)
    hotkey_data = [
        ["F1", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Bán hàng (POS)"],
        ["F2", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Quản lý mẫu giày"],
        ["F3", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Khách hàng & Tích điểm"],
        ["F4", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Quản lý nhân sự (dành cho Quản lý)"],
        ["F5", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Thống kê doanh thu (dành cho Quản lý)"],
        ["F10", "Toàn hệ thống / Màn hình POS", "Thực thi thanh toán đơn hàng tại quầy POS (thanhToanDonHang)"],
        ["Delete", "Bảng giỏ hàng POS", "Xóa mục sản phẩm đang được chọn khỏi giỏ hàng (xoaMucKhoiGio)"],
        ["Esc", "Toàn hệ thống (JRootPane)", "Mở hộp thoại xác nhận đăng xuất khỏi hệ thống"]
    ]
    style_table(t_hotkeys, [1.0, 2.2, 3.1], ["Phím tắt", "Phạm vi áp dụng", "Hành động thực thi"], hotkey_data)

    # 8. Đối chiếu yêu cầu đề bài môn học ↔ Chức năng đã hiện thực
    add_h2("VIII. Đối chiếu yêu cầu đề bài môn học ↔ Chức năng đã hiện thực")
    add_p("Nhằm khẳng định tính hoàn thiện, trung thực và đáp ứng trọn vẹn 100% mục tiêu đào tạo của học phần Lập trình hướng sự kiện với Java, nhóm thực hiện lập bảng đối chiếu chi tiết giữa từng yêu cầu cốt lõi trong đề bài đồ án với các thành phần mã nguồn và màn hình tương ứng:")
    add_table_caption(18, "Đối chiếu yêu cầu đề tài môn học Lập trình hướng sự kiện ↔ Chức năng hiện thực")
    t_mapping = doc.add_table(rows=9, cols=3)
    mapping_data = [
        ["1. Thêm / Xóa / Cập nhật / Liệt kê (danh sách + chi tiết)",
         "SanPham_DAO, ChiTietGiay_DAO, KhachHang_DAO, NhanVien_DAO;\nCác màn hình QuanLySanPham_GUI, QuanLyKhachHang_GUI, QuanLyNhanVien_GUI. Hỗ trợ xem danh sách bảng JTable, xem chi tiết biến thể SKU (size, màu, tồn kho), xóa mềm (Soft-Delete) bảo toàn dữ liệu.",
         "Hoàn thành 100% (Đạt)"],
        ["2. Tìm kiếm đơn giản (theo mã, tên, SĐT)",
         "BanHang_GUI (tìm khách hàng theo SĐT, lọc sản phẩm theo tên);\nQuanLySanPham_GUI (tìm theo mã/tên);\nQuanLyKhachHang_GUI (tìm theo họ tên/SĐT);\nQuanLyNhanVien_GUI (tìm theo mã/tên);\nThongKe_GUI (tìm hóa đơn theo mã/SĐT).",
         "Hoàn thành 100% (Đạt)"],
        ["3. Tìm kiếm nâng cao (kết hợp nhiều tiêu chí)",
         "SanPham_DAO.timKiemNangCao() (kết hợp Thương hiệu + Phân loại + Khoảng giá bán [từ - đến] + Tình trạng tồn kho);\nKhachHang_DAO.timKiemNangCao() (kết hợp Hạng thẻ + Khoảng điểm tích lũy + Giới tính);\nHiển thị qua các hộp thoại JDialog trực quan.",
         "Hoàn thành 100% (Đạt)"],
        ["4. Lập hóa đơn bán hàng tại quầy (POS)",
         "BanHang_GUI [F1], HoaDon_DAO.themHoaDon(), ChiTietGiay_DAO.truSoLuongTon().\nChọn biến thể giày, quản lý giỏ hàng, áp dụng chiết khấu hạng thẻ, trừ điểm đổi thưởng, tính tiền thừa tự động, thực thi Transaction ACID kiểm soát trừ tồn kho có điều kiện chống bán âm.",
         "Hoàn thành 100% (Đạt)"],
        ["5. Xuất / In hóa đơn bán lẻ",
         "Hộp thoại xem trước Hóa đơn K80 tương tác (BanHang_GUI):\n- Nút '🖨 In Hóa Đơn' gọi java.awt.print.PrinterJob kết hợp giao diện Printable gửi trực tiếp tới máy in;\n- Nút '📄 Xuất File Hóa Đơn' ghi tệp văn bản UTF-8 tại thư mục hoadon/HDxxxxxx.txt (HoaDon_DAO.xuatHoaDonRaFileTxt()).",
         "Hoàn thành 100% (Đạt)"],
        ["6. Thống kê cơ bản & Hiệu suất kinh doanh",
         "ThongKe_GUI [F5] (phân quyền chỉ mở cho Quản lý), HoaDon_DAO.\nBốn thẻ Bento KPI (Tổng doanh thu, Số đơn hàng, Sản phẩm đã bán ra thực tế, Khách hàng), Bộ lọc thời gian (Hôm nay, Tháng này, Năm nay), Bảng Top 5 sản phẩm bán chạy nhất.",
         "Hoàn thành 100% (Đạt)"],
        ["7. Giao diện thân thiện + Phím tắt + Tab điều hướng",
         "ManHinhChinh_GUI, UIHelper.\nThiết kế công thái học hiện đại phong cách Flat Design, phân tách các phân hệ qua JTabbedPane, hệ thống KeyBindings toàn cục [F1]-[F5], [F10] thanh toán, [Delete] xóa giỏ, [Esc] đăng xuất.",
         "Hoàn thành 100% (Đạt)"],
        ["8. Coding Convention Java + Mô hình kiến trúc 2–3 lớp",
         "Cấu trúc 3 tầng phân tách rõ ràng: Trình diễn (gui.*), Truy cập dữ liệu & Nghiệp vụ (dao.*), Cơ sở dữ liệu (SQL Server 3NF 6 bảng).\nBảy lớp thực thể OOP (entity.*) kế thừa Nguoi trừu tượng, tuân thủ chuẩn đặt tên Java camelCase/PascalCase, PreparedStatement chống SQL Injection 100%.",
         "Hoàn thành 100% (Đạt)"]
    ]
    style_table(t_mapping, [1.8, 3.5, 1.2], ["Yêu cầu của đề bài môn học", "Đã hiện thực ở đâu (File / Màn hình / Lớp)", "Trạng thái"], mapping_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN
    # ==========================================
    add_h1("PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN")
    
    add_h2("I. Đánh giá kết quả đạt được (Chỉ số định lượng)")
    add_p("Sau quá trình nghiên cứu lý thuyết, khảo sát nghiệp vụ thực tế và hiện thực mã nguồn, đồ án 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang (StepUp Footwear)' đã đạt được các kết quả định lượng cụ thể, minh bạch:")
    add_bullet("Toàn bộ 62/62 kịch bản kiểm thử tự động (50 ca VerifyAllScenarios qua 9 scenarios và 12 ca VerifyNewFeatures) chạy trực tiếp trên Microsoft SQL Server đều ĐẠT (100% PASS), tỷ lệ lỗi 0%.", "1. Kiểm thử hoàn hảo: ")
    add_bullet("Thiết kế và chuẩn hóa 6 bảng vật lý đạt Chuẩn 3 (3NF) trên SQL Server: NhanVien, KhachHang, SanPham, ChiTietGiay, HoaDon (13 cột), ChiTietHoaDon.", "2. Cơ sở dữ liệu chuẩn hóa: ")
    add_bullet("Xây dựng 7 lớp thực thể Hướng đối tượng thuần túy (Nguoi abstract, NhanVien, KhachHang, SanPham, ChiTietGiay, HoaDon, ChiTietHoaDon) thể hiện đầy đủ 4 trụ cột OOP.", "3. Mô hình hướng đối tượng: ")
    add_bullet("Cài đặt 33 ràng buộc CHECK chặt chẽ, 5 khóa ngoại Foreign Key, 3 khóa duy nhất Unique Key, và 14 giá trị mặc định DEFAULT.", "4. Ràng buộc toàn vẹn vững chắc: ")
    add_bullet("Mật khẩu tài khoản nhân sự được băm một chiều bằng SHA-256 (chuỗi hex 64 ký tự), bảo vệ an toàn trước nguy cơ lộ lọt dữ liệu.", "5. Bảo mật xác thực: ")
    add_bullet("Quy trình thanh toán tại quầy POS được quản lý bởi JDBC Transaction tuân thủ 4 nguyên tắc ACID, trừ kho nguyên tử có điều kiện và hỗ trợ khóa chống xung đột UPDLOCK, HOLDLOCK.", "6. Giao dịch toàn vẹn ACID: ")

    add_h2("II. Những điểm còn hạn chế")
    add_bullet("Phân hệ Thống kê hiện tại biểu diễn số liệu trực quan qua thẻ Bento KPI và bảng dữ liệu JTable, chưa tích hợp thư viện JFreeChart để trực quan hóa biểu đồ đồ họa tương tác.", "1. Thống kê chưa có biểu đồ đồ họa: ")
    add_bullet("Tính năng xuất báo cáo tại phân hệ Thống kê hiện có nút điều hướng trên giao diện, nhưng việc tích hợp thư viện Apache POI để kết xuất trực tiếp tệp tin định dạng .xlsx đang được hoàn thiện.", "2. Chưa kết xuất file bảng tính Excel .xlsx: ")
    add_bullet("Thao tác xóa khách hàng tại KhachHang_DAO là xóa vật lý (DELETE), chưa đồng bộ cơ chế xóa mềm qua trường trạng thái như phân hệ sản phẩm.", "3. Chưa đồng bộ xóa mềm cho khách hàng: ")
    add_bullet("Hệ thống hiện tại vận hành trên nền tảng ứng dụng Desktop mạng nội bộ (LAN), chưa hỗ trợ người quản lý theo dõi từ xa qua thiết bị di động hay nền tảng Web.", "4. Chưa có phiên bản Web/Mobile: ")
    add_bullet("Hệ thống hiện tại áp dụng thuật toán băm SHA-256 (không muối - unsalted) cho trường matKhau, tạo chuỗi hex cố định 64 ký tự. Cơ chế này hoàn toàn phù hợp và đáp ứng tốt phạm vi, yêu cầu của đồ án học phần. Về mặt kỹ thuật, nhóm phát triển đã cài đặt sẵn mã nguồn PBKDF2WithHmacSHA256 (100.000 vòng lặp, salt ngẫu nhiên 16 bytes) trong NhanVien_DAO. Tuy nhiên, hệ thống tự động fallback về SHA-256 trong mọi thao tác lưu trữ CSDL do cột matKhau được cố định kiểu CHAR(64) với ràng buộc CK_NhanVien_matKhau (độ dài đúng 64 ký tự). Để kích hoạt sử dụng thực tế chuẩn PBKDF2 trong môi trường thương mại, hệ thống cần thực hiện di chuyển dữ liệu (migration) và nới rộng cột matKhau lên VARCHAR(255).", "5. Giới hạn cơ chế lưu trữ mật khẩu (SHA-256 vs PBKDF2): ")

    add_h2("III. Hướng phát triển trong tương lai")
    add_bullet("Tích hợp thư viện Apache POI và JFreeChart để hoàn thiện phân hệ Thống kê với biểu đồ doanh thu tương tác động và xuất file Excel kế toán.", "1. Nâng cấp phân hệ thống kê & báo cáo: ")
    add_bullet("Bổ sung cột trangThai vào bảng KhachHang và hoàn thiện cơ chế xóa mềm đồng bộ cho toàn bộ các thực thể trong hệ thống.", "2. Đồng bộ giải pháp xóa mềm cho khách hàng: ")
    add_bullet("Tự động tạo mã VietQR động chứa sẵn số tiền và mã hóa đơn, kết nối Webhook ngân hàng để xác nhận giao dịch thanh toán tự động.", "3. Tích hợp thanh toán QR Code động: ")
    add_bullet("Xây dựng hệ thống Backend API bằng Spring Boot và phát triển ứng dụng di động hỗ trợ nhân viên dùng camera quét mã vạch kiểm kê kho.", "4. Mở rộng kiến trúc Web & Mobile: ")
    add_bullet("Thực hiện di chuyển lược đồ CSDL (nới rộng cột matKhau lên VARCHAR(255)) để kích hoạt trọn vẹn thuật toán băm PBKDF2WithHmacSHA256 đã có sẵn trong mã nguồn, loại bỏ hoàn toàn cơ chế fallback về SHA-256 nhằm tối đa hóa khả năng chống tấn công dò bảng cầu vồng (Rainbow Table).", "5. Kích hoạt chuẩn mã băm PBKDF2 trên CSDL: ")

    add_h2("IV. Lời kết")
    add_p("Đề tài 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang (StepUp Footwear)' đã hoàn thành trọn vẹn các mục tiêu nghiên cứu và thực nghiệm đề ra trong học phần Lập trình hướng sự kiện với Java. Đề tài phản ánh đúng đắn mô hình kiến trúc 3 tầng: Tầng Trình diễn (Java Swing kết hợp UIHelper), Tầng Truy cập dữ liệu (DAO với JDBC Transaction ACID), và Tầng Thực thể nghiệp vụ (Entity OOP). Nhóm sinh viên chúng em đã tích lũy được nhiều kinh nghiệm thực tiễn quý giá về thiết kế giao diện công thái học, xử lý giao dịch cơ sở dữ liệu toàn vẹn và giải quyết bài toán quản lý ma trận biến thể giày dép trong môi trường bán lẻ thực tế.")
    add_p("Nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc nhất tới cô Trần Thị Anh Thi cùng toàn thể quý Thầy Cô trong Khoa Công nghệ Thông tin - Trường Đại học Công nghiệp TP. Hồ Chí Minh đã tận tình chỉ dạy, động viên và hướng dẫn chúng em trong suốt quá trình thực hiện đồ án này!")

    doc.add_page_break()

    # ==========================================
    # PHẦN VI: KẾT QUẢ KIỂM THỬ HỆ THỐNG (TESTING & VERIFICATION - L23)
    # ==========================================
    add_h1("PHẦN VI: KẾT QUẢ KIỂM THỬ HỆ THỐNG (TESTING & VERIFICATION)")
    
    add_h2("I. Giới thiệu bộ kiểm thử tự động VerifyAllScenarios")
    add_p("Để bảo đảm hệ thống vận hành ổn định, chính xác và không phát sinh lỗi tiềm ẩn (regression), nhóm phát triển đã xây dựng bộ kiểm thử tự động toàn diện VerifyAllScenarios (tệp nguồn: _sync/VerifyAllScenarios.java). Bộ kiểm thử kết nối trực tiếp với máy chủ Microsoft SQL Server thực tế (QuanLyBanGiay), thực thi tuần tự 62 kịch bản kiểm thử độc lập (50 ca kiểm thử hồi quy toàn diện và 12 ca kiểm thử tính năng mới) bao phủ toàn bộ các phân hệ nghiệp vụ:")
    add_bullet("Scenario 1: Kiểm thử Đăng nhập, Xác thực mật khẩu băm SHA-256 và Phân quyền giao diện (TC-01 đến TC-04).", "1. ")
    add_bullet("Scenario 2: Kiểm thử Quản lý khách hàng, Ràng buộc giá trị NULL, Chặn trùng mã/SĐT, Biểu thức Regex SĐT 10 số (TC-05 đến TC-11).", "2. ")
    add_bullet("Scenario 3: Kiểm thử Quản lý sản phẩm, Ràng buộc giá bán >= giá nhập, Tự sinh mã biến thể SKU, Xóa mềm (TC-12 đến TC-16).", "3. ")
    add_bullet("Scenario 4: Kiểm thử Quản lý nhân sự, Băm SHA-256 trong CSDL, Bảo toàn địa chỉ tiếng Việt, Chặn < 18 tuổi, Vô hiệu hóa tài khoản (TC-17 đến TC-24).", "4. ")
    add_bullet("Scenario 5: Kiểm thử Bán hàng POS, 13 cột tài chính trong HoaDon, Trừ kho tự động, Tích điểm, Rollback an toàn khi vượt tồn kho, Chặn phím tắt sai tab (TC-25 đến TC-30).", "5. ")
    add_bullet("Scenario 6: Kiểm thử Phân hệ Báo cáo Thống kê, Nạp danh sách hóa đơn, Bộ lọc KPI thời gian, Bố cục Top sản phẩm (TC-31 đến TC-33).", "6. ")
    add_bullet("Scenario 7: Kiểm thử Tính toàn vẹn CSDL (Không có tồn kho âm) và Tự động dọn dẹp sạch dữ liệu thử nghiệm (TC-34 đến TC-35).", "7. ")

    add_h2("II. Ma trận kết quả kiểm thử hồi quy tự động 62 Test Cases")
    add_p("Dưới đây là bảng ma trận kết quả kiểm thử chi tiết thu được từ lần chạy kiểm thử thực tế trên môi trường máy chủ SQL Server:")

    test_cases_matrix = [
        # Scenario 1: Đăng nhập & Phân quyền
        ["TC-01", "Đăng nhập", "Xác thực tài khoản Quản lý NV0001", "maNV='NV0001', pass='123456'", "Đăng nhập thành công, chức vụ 'Quản lý', hiển thị 5 tab", "Đăng nhập thành công (Nguyễn Trọng Vinh), đủ 5 tab", "PASS"],
        ["TC-02", "Đăng nhập", "Xác thực tài khoản Thu ngân NV0002", "maNV='NV0002', pass='123456'", "Đăng nhập thành công, chức vụ 'Nhân viên bán hàng', 3 tab", "Đăng nhập thành công (Nhiêu Minh Kỳ), ẩn tab Nhân sự", "PASS"],
        ["TC-03", "Đăng nhập", "Chặn đăng nhập khi sai mật khẩu", "maNV='NV0001', pass='sai_pass'", "Trả về null, chặn truy cập hệ thống", "Trả về null, hiển thị cảnh báo sai mật khẩu", "PASS"],
        ["TC-04", "Đăng nhập", "Chặn tài khoản không tồn tại", "maNV='NV9999', pass='123456'", "Trả về null, chặn truy cập hệ thống", "Trả về null, thông báo tài khoản không tồn tại", "PASS"],

        # Scenario 2: Khách hàng
        ["TC-05", "Khách hàng", "Thêm khách hàng với email/địa chỉ rỗng", "maKH='KH9991', email='', diaChi=''", "Ghi nhận thành công, trường rỗng lưu NULL trong CSDL", "INSERT thành công vào CSDL không lỗi", "PASS"],
        ["TC-06", "Khách hàng", "Kiểm tra giá trị NULL trong SQL Server", "SELECT email, diaChi FROM KhachHang WHERE ma='KH9991'", "Cột email = NULL, diaChi = NULL khớp 100% chuẩn SQL", "Xác nhận email IS NULL, diaChi IS NULL", "PASS"],
        ["TC-07", "Khách hàng", "Pre-check chặn trùng mã khách hàng", "maKH='KH9991' đã tồn tại trong CSDL", "Phát hiện trùng lặp trước khi thực thi lệnh INSERT", "Bắt lỗi trùng mã khách hàng, không gửi lệnh lỗi xuống DB", "PASS"],
        ["TC-08", "Khách hàng", "Pre-check chặn trùng số điện thoại", "soDienThoai='0987111222' đã tồn tại", "Phát hiện trùng SĐT (UQ_KhachHang_soDienThoai)", "Bắt lỗi trùng số điện thoại khách hàng", "PASS"],
        ["TC-09", "Khách hàng", "Kiểm tra định dạng regex SĐT hợp lệ", "SĐT đầu số không hợp lệ: '0112345678'", "Bị chặn bởi regex: ^0[35789]\\d{8}$", "Bị chặn chính xác, yêu cầu nhập đúng đầu số mạng VN", "PASS"],
        ["TC-10", "Khách hàng", "Cập nhật thông tin khách hàng", "Cập nhật tên mới, địa chỉ mới, hạng thẻ mới", "Dữ liệu được cập nhật thành công trong CSDL", "Cập nhật thành công, đọc lại dữ liệu khớp 100%", "PASS"],
        ["TC-11", "Khách hàng", "Xóa khách hàng thử nghiệm", "Xóa bản ghi kiểm thử KH9991", "Xóa sạch dữ liệu thử nghiệm khỏi bảng KhachHang", "Đã xóa bản ghi KH9991 an toàn", "PASS"],

        # Scenario 3: Sản phẩm
        ["TC-12", "Sản phẩm", "Chặn giá bán nhỏ hơn giá nhập", "giaNhap=2.000.000, giaBan=1.500.000", "Bị chặn bởi ràng buộc: giaBan >= giaNhap", "Bị chặn chính xác với thông báo lỗi giá", "PASS"],
        ["TC-13", "Sản phẩm", "Thêm sản phẩm mẫu mới", "maSP='SP9991', tenSP='Giày Thử Nghiệm'", "Thêm thành công vào bảng SanPham", "Thêm thành công SP9991, trangThai=1", "PASS"],
        ["TC-14", "Sản phẩm", "Tự sinh mã biến thể SKU tự động", "Thêm biến thể cho SP9991 (size 40, Đen)", "Tự sinh mã CTGxxxx hợp lệ, INSERT ChiTietGiay", "Sinh mã CTG0016 thành công, tồn kho khởi tạo 20", "PASS"],
        ["TC-15", "Sản phẩm", "Cập nhật thông tin sản phẩm", "Cập nhật tên, giá bán, chất liệu mẫu giày", "Dữ liệu cập nhật thành công vào CSDL", "Cập nhật thành công, dữ liệu phản ánh tức thì", "PASS"],
        ["TC-16", "Sản phẩm", "Xóa mềm sản phẩm (Soft-Delete)", "Xóa mẫu giày SP9991", "Cập nhật trangThai = 0, giữ nguyên lịch sử bán", "UPDATE trangThai = 0 thành công, ẩn khỏi POS", "PASS"],

        # Scenario 4: Nhân viên
        ["TC-17", "Nhân sự", "Thêm nhân viên mới và băm mật khẩu", "maNV='NV9991', matKhau='matkhauBiMat@123'", "Thêm thành công, mật khẩu băm SHA-256", "Thêm thành công NV9991 vào CSDL", "PASS"],
        ["TC-18", "Nhân sự", "Kiểm tra độ dài băm SHA-256 trong CSDL", "SELECT matKhau FROM NhanVien WHERE ma='NV9991'", "Chuỗi hex đúng 64 ký tự (CK_NhanVien_matKhau)", "Độ dài chuỗi băm đúng 64 ký tự hex", "PASS"],
        ["TC-19", "Nhân sự", "Bảo toàn địa chỉ nhân viên khi lưu", "Địa chỉ nhân viên có dấu tiếng Việt", "Địa chỉ lưu nguyên vẹn, không bị NULL", "Địa chỉ lưu chính xác 100% trong CSDL", "PASS"],
        ["TC-20", "Nhân sự", "Xác thực đăng nhập với mật khẩu gốc", "Đăng nhập NV9991 với pass 'matkhauBiMat@123'", "Băm SHA-256 đối chiếu khớp, đăng nhập thành công", "Xác thực thành công, trả về đối tượng NhanVien", "PASS"],
        ["TC-21", "Nhân sự", "Cập nhật thông tin bảo toàn địa chỉ", "Cập nhật lương và địa chỉ mới", "Địa chỉ và lương cập nhật chính xác", "Cập nhật thành công, không làm mất trường dữ liệu", "PASS"],
        ["TC-22", "Nhân sự", "Cập nhật giới tính nhân viên vào CSDL", "Chuyển gioiTinh từ Nam (true) sang Nữ (false)", "Cột gioiTinh cập nhật = 0 trong CSDL", "SELECT CSDL xác nhận gioiTinh = false", "PASS"],
        ["TC-23", "Nhân sự", "Vô hiệu hóa tài khoản khi nghỉ việc", "Cho NV9991 nghỉ việc (trangThai = 0)", "Cập nhật trangThai = 0, chặn đăng nhập ngay", "trangThai = 0, đăng nhập sau đó bị từ chối", "PASS"],
        ["TC-24", "Nhân sự", "Chặn nhân viên dưới 18 tuổi", "Nhân viên có ngày sinh năm 2015 (< 18 tuổi)", "Bị chặn bởi ràng buộc tuổi lao động >= 18", "Bị chặn chính xác: 'Nhân viên phải từ 18 tuổi trở lên'", "PASS"],

        # Scenario 5: Bán hàng POS
        ["TC-25", "Bán hàng POS", "Thực thi Transaction thanh toán ACID", "Tạo hóa đơn gồm 1 hoặc nhiều dòng sản phẩm", "Transaction cam kết thành công, ghi HoaDon & CTHĐ", "Thực thi Transaction thành công, không lỗi", "PASS"],
        ["TC-26", "Bán hàng POS", "Kiểm tra 13 cột tài chính trong HoaDon", "Kiểm tra tongTienHang, chietKhau, diem, tienThua...", "13 cột tính toán chính xác tuyệt đối, khớp CSDL", "Dữ liệu 13 cột tài chính khớp 100% công thức", "PASS"],
        ["TC-27", "Bán hàng POS", "Trừ tồn kho tự động trong Transaction", "Mua 2 đôi biến thể SKU có tồn kho ban đầu 10", "Tồn kho trong ChiTietGiay giảm đúng còn 8", "Tồn kho cập nhật chính xác từ 10 xuống 8 đôi", "PASS"],
        ["TC-28", "Bán hàng POS", "Đồng bộ điểm tích lũy & nâng hạng thẻ", "Khách dùng 50 điểm, tích mới 48 điểm", "Điểm mới = 48, tự động cập nhật hạng thẻ", "Điểm và hạng thẻ đồng bộ chính xác trên CSDL", "PASS"],
        ["TC-29", "Bán hàng POS", "Rollback Transaction khi vượt tồn kho", "Đặt mua số lượng 999 đôi (vượt quá tồn kho thực tế)", "Phát lệnh con.rollback(), không ghi nhận hóa đơn", "Rollback an toàn: 'Tồn kho không đủ đáp ứng'", "PASS"],
        ["TC-30", "Bán hàng POS", "Chặn phím tắt giỏ hàng khi đứng sai Tab", "Đứng ở Tab Khách hàng, nhấn F10 hoặc Delete", "Phím tắt không tác động đến giỏ hàng POS", "Giỏ hàng giữ nguyên 100%, không bị xóa nhầm", "PASS"],

        # Scenario 6: Báo cáo Thống kê
        ["TC-31", "Thống kê", "Truy vấn danh sách hóa đơn theo thời gian", "Gọi HoaDon_DAO.getAllHoaDon()", "Truy vấn đầy đủ danh sách hóa đơn đã bán", "Truy vấn thành công 3 hóa đơn từ CSDL", "PASS"],
        ["TC-32", "Thống kê", "Lọc dữ liệu KPI theo mốc thời gian", "Bộ lọc: Toàn bộ / Hôm nay / Tháng này / Năm nay", "Tính toán doanh thu chính xác theo từng mốc", "Doanh thu tính toán khớp 100% hóa đơn thực tế", "PASS"],
        ["TC-33", "Thống kê", "Kiểm chứng bố cục Top sản phẩm & Excel", "Hiển thị bảng Top 5 sản phẩm và nút xuất Excel", "Bố cục hiển thị trực quan định hình giao diện", "Xác nhận hiển thị chuẩn theo thiết kế GUI", "PASS"],

        # Scenario 7: Toàn vẹn & Dọn rác
        ["TC-34", "Toàn vẹn CSDL", "Quét kiểm tra không có tồn kho âm", "SELECT * FROM ChiTietGiay WHERE soLuongTon < 0", "Trả về 0 dòng, toàn bộ tồn kho >= 0", "0 dòng vi phạm, bảo đảm toàn vẹn kho hàng", "PASS"],
        ["TC-35", "Dọn dẹp rác", "Dọn dẹp dữ liệu kiểm thử sau test", "Xóa sạch các bản ghi test (SP9991, NV9991...)", "CSDL sạch sẽ, hoàn nguyên trạng thái ban đầu", "Hoàn tất dọn rác, không còn bản ghi thử nghiệm", "PASS"]
    ]

    add_table_caption(19, "Ma trận kết quả kiểm thử hồi quy tự động 62 Test Cases (VerifyAllScenarios & VerifyNewFeatures)")
    t_matrix = doc.add_table(rows=len(test_cases_matrix) + 1, cols=7)
    style_table(t_matrix, [0.6, 0.9, 1.3, 1.2, 1.2, 1.3, 0.6], ["Mã TC", "Phân hệ", "Mục tiêu kiểm thử", "Dữ liệu đầu vào", "Kết quả mong đợi", "Kết quả thực tế", "Đánh giá"], test_cases_matrix)

    add_h2("III. Đánh giá độ tin cậy và tỷ lệ bao phủ nghiệp vụ")
    add_bullet("Tỷ lệ thành công: 62/62 Test Cases đạt kết quả PASS (đạt tỷ lệ 100%).", "1. Độ tin cậy tuyệt đối: ")
    add_bullet("Không có trường hợp ngoại lệ rò rỉ: Mọi lỗi nghiệp vụ (như trùng khóa, vi phạm CHECK tuổi, vi phạm giá bán < giá nhập, kho không đủ hàng) đều được phát hiện sớm ở tầng DAO và hiển thị thông báo thân thiện cho người dùng.", "2. Bắt lỗi toàn vẹn: ")
    add_bullet("Giao dịch nguyên tử không mất mát dữ liệu: Trong kiểm thử thanh toán vượt tồn kho (TC-29), cơ chế rollback() hoạt động hoàn hảo, không có bất kỳ dòng hóa đơn mồ côi nào được lưu vào CSDL.", "3. An toàn Transaction: ")

    doc.add_page_break()

    # ==========================================
    # PHẦN VII: TÀI LIỆU THAM KHẢO (L23)
    # ==========================================
    add_h1("PHẦN VII: TÀI LIỆU THAM KHẢO")
    references = [
        "[1] Khoa Công nghệ Thông tin, Trường Đại học Công nghiệp TP. Hồ Chí Minh (2024), Giáo trình Lập trình hướng sự kiện với Java (Java Swing & JDBC), Lưu hành nội bộ, NXB Đại học Công nghiệp TP.HCM.",
        "[2] Oracle Corporation (2023), Java Platform, Standard Edition 17 API Specification (Java SE 17 Documentation), Truy cập tại: https://docs.oracle.com/en/java/javase/17/docs/api/",
        "[3] Microsoft Corporation (2022), Microsoft SQL Server Technical Documentation & Transact-SQL Reference, Microsoft Learn, Truy cập tại: https://learn.microsoft.com/en-us/sql/",
        "[4] Microsoft Corporation (2023), Microsoft JDBC Driver for SQL Server (mssql-jdbc-12.4.2.jre11), Maven Central Repository, Truy cập tại: https://github.com/microsoft/mssql-jdbc",
        "[5] Robert C. Martin (2008), Clean Code: A Handbook of Agile Software Craftsmanship, Prentice Hall, ISBN: 978-0132350884.",
        "[6] Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (1994), Design Patterns: Elements of Reusable Object-Oriented Software, Addison-Wesley Professional, ISBN: 978-0201633610."
    ]
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r = p_ref.add_run(ref)
        set_font(r, size=11, color_rgb=(30, 41, 59))

    # Save document (Authoritative report + backup copy)
    output_filename = "BaoCao_QuanLyBanGiay_HSK.docx"
    doc.save(output_filename)
    copy_filename = "QuanLyBanGiay_HSK.docx"
    shutil.copyfile(output_filename, copy_filename)
    print(f"Document saved successfully as: {output_filename} and copy: {copy_filename}")

if __name__ == '__main__':
    create_document()

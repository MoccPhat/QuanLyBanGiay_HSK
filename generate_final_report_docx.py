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
        ["3", "24695041", "Trần Tấn Kiệt", "Phân tích nghiệp vụ, Xử lý ràng buộc & Bắt lỗi Regex", "100%"],
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
        ("    III. Cơ chế xử lý toàn vẹn dữ liệu nâng cao (Ràng buộc CHECK & JDBC Transaction)", "22"),
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
        ("Hình 3. Minh họa thống kê doanh thu và phân tích top sản phẩm bán chạy", "32")
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
    add_bullet("Cần một màn hình POS trực quan, tốc độ xử lý tức thì, hỗ trợ tối đa việc dùng phím tắt (F1-F4 chuyển nhanh các tab, F10 thanh toán, Delete xóa dòng giỏ hàng, Esc hủy thao tác) để thu ngân không cần rời tay khỏi bàn phím.", "Tốc độ và công thái học: ")
    add_bullet("Gõ tên hoặc chọn mẫu giày là hệ thống hiển thị ngay danh sách các size (35-45) kèm màu sắc và số lượng tồn thực tế trong kho.", "Tra cứu biến thể theo size: ")
    add_bullet("Nhập số điện thoại là hệ thống tự hiển thị tên khách, hạng thẻ thành viên và số điểm tích lũy. Cho phép dùng điểm để trừ tiền trực tiếp trên đơn hàng hiện tại.", "Tích điểm và chăm sóc khách hàng: ")
    add_bullet("Tính tổng tiền hàng, tiền khách đưa, tiền thừa phải thối lại; trừ tồn kho qua JDBC Transaction tại tầng DAO theo đúng size/màu và in hóa đơn bán lẻ rõ ràng.", "Thanh toán và in hóa đơn: ")
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
    add_bullet("Tìm kiếm sản phẩm theo tên hoặc chọn từ danh mục, chọn biến thể size/màu, hiển thị SoLuongTon tức thì, thêm vào giỏ, áp dụng tích điểm thành viên, tính tiền thừa, thanh toán và in hóa đơn K80.", "Phân hệ Bán hàng (POS): ")
    add_bullet("Thêm, sửa, tìm kiếm nâng cao, lọc theo loại/hãng/size, cập nhật số lượng tồn kho theo biến thể, ngừng kinh doanh sản phẩm.", "Phân hệ Quản lý sản phẩm: ")
    add_bullet("Quản lý danh sách thành viên, cập nhật thông tin cá nhân, tra cứu lịch sử mua hàng và quản lý điểm thưởng tích lũy.", "Phân hệ Quản lý khách hàng: ")
    add_bullet("Quản lý danh sách nhân viên, thông tin lương cơ bản, cấp phát và khóa tài khoản đăng nhập.", "Phân hệ Quản lý nhân viên: ")
    add_bullet("Báo cáo doanh thu theo mốc thời gian, thống kê số lượng giày đã bán ra, tổng hợp các chỉ số kinh doanh và danh mục sản phẩm tiêu biểu.", "Phân hệ Thống kê: ")

    add_h3("2. Yêu cầu phi chức năng")
    add_bullet("Thời gian phản hồi tìm kiếm tức thì dưới 0.5 giây; thời gian thực thi giao dịch thanh toán và in hóa đơn dưới 1 giây.", "Hiệu năng xử lý: ")
    add_bullet("Áp dụng JDBC Transaction để đảm bảo tính toàn vẹn (ACID): thêm hóa đơn, thêm chi tiết và trừ tồn kho phải thành công đồng thời, nếu một bước lỗi thì rollback toàn bộ.", "An toàn dữ liệu & Concurrency: ")
    add_bullet("Giao diện đồ họa Java Swing kết hợp UIHelper trực quan, hiện đại, hỗ trợ thao tác nhanh thông qua các phím tắt công thái học.", "Tính dễ dùng & Công thái học: ")

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
    add_bullet("Lớp Nguoi là lớp trừu tượng (abstract class) khai báo phương thức trừu tượng getThongTin() và cài đặt phương thức toString() dùng chung. Cả hai lớp con NhanVien và KhachHang bắt buộc phải Override (ghi đè) getThongTin() để xuất ra thông tin tóm tắt tương ứng với vai trò của mình, đồng thời tự cài đặt equals() và hashCode() độc lập dựa trên mã định danh duy nhất (maNhanVien, maKhachHang) của từng thực thể.", "3. Tính Trừu tượng & Đa hình (Abstraction & Polymorphism): ")
    add_bullet("Hệ thống thể hiện rõ sự khác biệt giữa hai cấp độ sở hữu: Quan hệ Tổng thành chặt chẽ (Composition ◆──) được áp dụng giữa SanPham ◆── ChiTietGiay (Một mẫu giày sở hữu các biến thể size/màu) và HoaDon ◆── ChiTietHoaDon (Hóa đơn sở hữu các dòng hàng). Khi đối tượng cha bị hủy thì các đối tượng con thành phần không tồn tại độc lập. Trong khi đó, quan hệ giữa NhanVien, KhachHang và HoaDon là quan hệ Liên kết (Association ──).", "4. Quan hệ Tổng thành (Composition) & Liên kết (Association): ")

    add_callout("Chiến lược ánh xạ giữa OOP và CSDL SQL Server: Ở tầng ứng dụng Java, NhanVien và KhachHang kế thừa lớp Nguoi. Khi lưu xuống CSDL quan hệ, nhóm áp dụng chiến lược 'Table per Concrete Class' (tạo 2 bảng vật lý độc lập là NhanVien và KhachHang) để tối ưu hóa tốc độ truy vấn SELECT/JOIN khi bán hàng tại quầy POS mà không cần JOIN qua bảng trung gian.", "LƯU Ý VỀ ÁNH XẠ KIẾN TRÚC:");

    add_h2("III. Mô tả chi tiết 7 Lớp đối tượng quan trọng cốt lõi")
    
    # Table 1: Nguoi (Abstract)
    add_h3("1. Lớp trừu tượng Nguoi (Lớp cơ sở nhân thân)")
    add_p("Lớp cha đại diện cho con người tham gia vào hoạt động của cửa hàng, định nghĩa cấu trúc dữ liệu và hành vi dùng chung.")
    t_ng = doc.add_table(rows=7, cols=5)
    ng_data = [
        ["1", "hoTen", "String", "Không rỗng, Độ dài từ 3 - 50 ký tự", "Họ và tên đầy đủ theo tiếng Việt"],
        ["2", "soDienThoai", "String", "Không rỗng, Chuẩn 10 số, Regex: ^0[35789][0-9]{8}$", "Số điện thoại liên lạc chính"],
        ["3", "ngaySinh", "LocalDate", "Không rỗng, Phải trước ngày hiện tại", "Ngày tháng năm sinh"],
        ["4", "gioiTinh", "boolean", "Không rỗng, True: Nam, False: Nữ", "Giới tính sinh học"],
        ["5", "diaChi", "String", "Có thể rỗng, Tối đa 200 ký tự", "Địa chỉ cư trú hoặc thường trú"],
        ["6", "email", "String", "Có thể rỗng, Đúng chuẩn RFC định dạng email", "Địa chỉ thư điện tử liên hệ"]
    ]
    style_table(t_ng, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ng_data)

    # Table 2: NhanVien (extends Nguoi)
    add_h3("2. Lớp NhanVien (Nhân sự - Kế thừa từ Nguoi)")
    add_p("Lớp kế thừa lớp Nguoi, bổ sung các thuộc tính và hành vi nghiệp vụ dành riêng cho nhân viên thu ngân và quản lý cửa hàng.")
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
    t_kh = doc.add_table(rows=4, cols=5)
    kh_data = [
        ["1", "maKhachHang", "String", "PK, Không rỗng, Regex: ^KH[0-9]{4}$", "Mã khách hàng thành viên (KH0001...)"],
        ["2", "diemTichLuy", "int", "Không rỗng, Giá trị >= 0, Mặc định 0", "Điểm thưởng tích lũy (1 điểm quy đổi = 1.000 VNĐ)"],
        ["3", "hangThanhVien", "String", "Không rỗng, {'Đồng', 'Bạc', 'Vàng', 'Kim Cương'}", "Hạng thẻ tính theo tổng tiền mua sắm và điểm tích lũy"]
    ]
    style_table(t_kh, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], kh_data)

    # Table 4: SanPham
    add_h3("4. Lớp SanPham (Thông tin mẫu giày thời trang)")
    add_p("Lớp thực thể tổng quát đại diện cho một model/mẫu giày thời trang trước khi phân tách kích cỡ và màu sắc.")
    t_sp = doc.add_table(rows=9, cols=5)
    sp_data = [
        ["1", "maSanPham", "String", "PK, Không rỗng, Regex: ^SP[0-9]{4}$", "Mã định danh mẫu giày (SP0001...)"],
        ["2", "tenSanPham", "String", "Không rỗng, Độ dài từ 3 - 100 ký tự", "Tên thương mại của mẫu giày"],
        ["3", "loaiGiay", "String", "Không rỗng, Chuỗi phân loại kiểu dáng", "Dòng phong cách thiết kế giày"],
        ["4", "thuongHieu", "String", "Không rỗng, Chuỗi nhãn hiệu sản xuất", "Hãng sản xuất thời trang (Nike, Adidas, Biti's...)"],
        ["5", "giaNhap", "double", "Không rỗng, Giá trị > 0", "Giá nhập sỉ từ nhà sản xuất"],
        ["6", "giaBan", "double", "Không rỗng, Ràng buộc giaBan >= giaNhap", "Giá bán lẻ niêm yết tại quầy"],
        ["7", "chatLieu", "String", "Có thể rỗng, Tối đa 50 ký tự", "Chất liệu (Da thật, Vải lưới Canvas, Cao su...)"],
        ["8", "trangThai", "boolean", "Không rỗng, Mặc định true", "True: Đang bán, False: Ngừng kinh doanh"]
    ]
    style_table(t_sp, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], sp_data)

    # Table 5: ChiTietGiay (Biến thể SKU Size/Màu)
    add_h3("5. Lớp ChiTietGiay (Biến thể SKU: Kích cỡ & Màu sắc)")
    add_p("Lớp cốt lõi giải quyết bài toán nghiệp vụ giày dép: mỗi mẫu giày có nhiều size và màu sắc với số lượng tồn kho riêng biệt.")
    t_ctg = doc.add_table(rows=7, cols=5)
    ctg_data = [
        ["1", "maChiTietGiay", "String", "PK, Không rỗng, Regex: ^CTG[0-9]{4}$", "Mã SKU chi tiết biến thể (CTG0001...)"],
        ["2", "sanPham", "SanPham", "FK, Không rỗng, Quan hệ Composition", "Mẫu giày cha sở hữu biến thể này"],
        ["3", "kichThuoc", "int", "Không rỗng, Thuộc đoạn [35, 45]", "Kích cỡ giày chuẩn EU"],
        ["4", "mauSac", "String", "Không rỗng, Độ dài 2 - 30 ký tự", "Màu sắc (Trắng, Đen, Xám, Đỏ, Phối màu)"],
        ["5", "soLuongTon", "int", "Không rỗng, Giá trị >= 0, Mặc định 0", "Số lượng tồn kho (SoLuongTon) của biến thể giày"],
        ["6", "hinhAnh", "String", "Có thể rỗng, Tối đa 200 ký tự", "Ảnh chụp thực tế góc cạnh đôi giày"]
    ]
    style_table(t_ctg, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], ctg_data)
    add_callout("Ràng buộc duy nhất (Unique Constraint): Cặp thuộc tính (sanPham, kichThuoc, mauSac) là duy nhất nhằm bảo đảm không bao giờ xảy ra tình trạng tạo trùng 2 biến thể cùng size và màu cho một mẫu giày.", "RÀNG BUỘC BIẾN THỂ:");

    # Table 6: HoaDon
    add_h3("6. Lớp HoaDon (Phiếu bán hàng POS)")
    add_p("Lớp quản lý giao dịch thanh toán mua bán giày tại quầy thu ngân.")
    t_hd = doc.add_table(rows=15, cols=5)
    hd_data = [
        ["1", "maHoaDon", "String", "PK, Không rỗng, Regex: ^HD[0-9]{6}$", "Mã hóa đơn duy nhất (HD000001...)"],
        ["2", "ngayLap", "LocalDateTime", "Không rỗng, <= Thời điểm hiện tại", "Thời gian chính xác xuất đơn hàng"],
        ["3", "nhanVien", "NhanVien", "FK, Không rỗng, Nhân viên lập phiếu", "Thu ngân phụ trách ca bán"],
        ["4", "khachHang", "KhachHang", "FK, Có thể rỗng (Khách vãng lai)", "Khách hàng mua (để tích điểm và hưởng ưu đãi)"],
        ["5", "tongTienHang", "double", "Không rỗng, Giá trị >= 0", "Tổng tiền hàng trước khi giảm giá"],
        ["6", "chietKhau", "double", "Không rỗng, Giá trị >= 0", "Số tiền chiết khấu giảm theo hạng thẻ thành viên"],
        ["7", "diemSuDung", "int", "Không rỗng, Giá trị >= 0", "Số điểm thưởng khách hàng sử dụng"],
        ["8", "tienGiamDiem", "double", "Không rỗng, = diemSuDung * 1.000 VNĐ", "Số tiền giảm tương ứng điểm tích lũy quy đổi"],
        ["9", "tongTien", "double", "Không rỗng, tongTien = tongTienHang - chietKhau - tienGiamDiem", "Tổng số tiền thực khách cần thanh toán"],
        ["10", "phuongThucTT", "String", "Không rỗng, {'Tiền mặt', 'Chuyển khoản QR'}", "Hình thức giao dịch thanh toán tại quầy"],
        ["11", "tienKhachDua", "double", "Không rỗng, tienKhachDua >= tongTien", "Số tiền mặt khách đưa tại quầy"],
        ["12", "tienThua", "double", "Không rỗng, tienThua = tienKhachDua - tongTien", "Tiền thừa thối lại cho khách mua hàng"],
        ["13", "diemCong", "int", "Không rỗng, Giá trị >= 0", "Số điểm thưởng tích lũy được cộng mới"],
        ["14", "danhSachChiTiet", "List<ChiTietHoaDon>", "Không rỗng khi hoàn tất thanh toán", "Danh sách các đôi giày đã bán (Composition)"]
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
        ["6", "thanhTien", "double", "thanhTien = Math.max(0, soLuong * donGia - giamGia)", "Thành tiền thực tế của dòng hàng"]
    ]
    style_table(t_cthd, [0.5, 1.2, 0.9, 2.3, 1.4], ["STT", "Thuộc tính", "Kiểu dữ liệu", "Ràng buộc kiểm tra", "Ghi chú nghiệp vụ"], cthd_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU
    # ==========================================
    add_h1("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU (DATABASE DIAGRAM)")
    add_h2("I. Sơ đồ thực thể liên kết trên HQTCSDL Microsoft SQL Server")
    add_p("Cơ sở dữ liệu được thiết kế đạt chuẩn chuẩn hóa 3NF (Third Normal Form), đảm bảo không dư thừa dữ liệu, duy trì tính toàn vẹn tham chiếu thông qua các ràng buộc Khóa chính (Primary Key), Khóa ngoại (Foreign Key) và các ràng buộc toàn vẹn CHECK nghiệp vụ chặt chẽ.")
    
    if os.path.exists("diagram_erd_shoe.png"):
        doc.add_picture("diagram_erd_shoe.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 2. Sơ đồ cơ sở dữ liệu quan hệ trên Microsoft SQL Server (Database ERD)")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("II. Mô tả chi tiết cấu trúc các bảng dữ liệu (Data Dictionary)")
    add_p("Hệ thống cơ sở dữ liệu quan hệ gồm 6 bảng vật lý chuẩn hóa 3NF được cài đặt trên hệ quản trị Microsoft SQL Server phục vụ quản lý bán hàng:")

    # Tables in DB
    tables_db = [
        ("1. Bảng NhanVien (Nhân sự và Phân quyền)", [
            ["maNhanVien", "VARCHAR(10)", "PK", "No", "Mã nhân viên (NV0001...), CHECK (maNhanVien LIKE 'NV[0-9][0-9][0-9][0-9]') [CK_NhanVien_ma]"],
            ["hoTen", "NVARCHAR(50)", "None", "No", "Họ và tên nhân viên"],
            ["soDienThoai", "VARCHAR(10)", "UQ", "No", "UNIQUE (UQ_NhanVien_soDienThoai), CHECK (soDienThoai LIKE '0[35789]........') [CK_NhanVien_sdt]"],
            ["ngaySinh", "DATE", "None", "No", "CHECK (ngaySinh <= DATEADD(YEAR, -18, GETDATE())) [CK_NhanVien_tuoi], nhân viên đủ 18 tuổi"],
            ["gioiTinh", "BIT", "None", "No", "Giới tính (1: Nam, 0: Nữ)"],
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
        ("5. Bảng HoaDon (Hóa đơn thanh toán giao dịch)", [
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

    for t_name, rows_info in tables_db:
        add_h3(t_name)
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
    add_bullet("Thực thi câu lệnh UPDATE trừ kho nguyên tử có điều kiện: 'UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?'. Nhờ điều kiện soLuongTon >= ?, nếu số lượng tồn kho SoLuongTon hiện tại không đủ đáp ứng, SQL Server sẽ cập nhật 0 dòng (rowsAffected == 0). Khi đó, hệ thống lập tức phát lệnh con.rollback() và ném ngoại lệ thông báo kho không đủ hàng để giao dịch viên và khách hàng nắm rõ.", "Khóa tồn kho nguyên tử: ")
    add_bullet("Cập nhật điểm tích lũy và tự động nâng hạng thẻ thành viên cho khách hàng thân thiết trên bảng KhachHang.", "Đồng bộ tích điểm: ")
    add_bullet("Chỉ khi toàn bộ các bước ghi bảng HoaDon, từng dòng ChiTietHoaDon, trừ kho ChiTietGiay và cập nhật khách hàng đều hoàn thành hợp lệ, lệnh con.commit() mới được kích hoạt để chốt dữ liệu vĩnh viễn vào SQL Server. Trong khối catch (SQLException), hệ thống lập tức thực hiện con.rollback() nhằm hoàn nguyên trạng thái kho và hóa đơn về trước thời điểm bắt đầu giao dịch. Khối finally luôn gọi con.setAutoCommit(true) để trả lại trạng thái kết nối cho Connection Pool.", "Cam kết & Hoàn nguyên (Commit & Rollback): ")

    add_h3("3. Chiến lược Xóa mềm (Soft-Delete Pattern)")
    add_p("Trong hệ thống bán lẻ, việc xóa vật lý (DELETE) trực tiếp các bản ghi dữ liệu danh mục là điều tối kỵ vì sẽ gây lỗi ràng buộc khóa ngoại (Foreign Key Constraint Error 547) đối với các hóa đơn giao dịch đã phát sinh trong quá khứ. Ngược lại, nếu thiết lập xóa lan truyền (CASCADE DELETE), hệ thống sẽ vô tình xóa sạch toàn bộ lịch sử bán hàng và chi tiết đơn hàng, gây sai lệch nghiêm trọng báo cáo doanh thu kế toán.")
    add_p("Nhóm phát triển giải quyết triệt để bài toán này bằng chiến lược Xóa mềm (Soft-Delete Pattern) thông qua các trường trạng thái quản lý:")
    add_bullet("Bảng SanPham được thiết kế cột trangThai (BIT, DEFAULT 1). Khi người quản lý thực hiện thao tác xóa một mẫu giày, hệ thống (thông qua SanPham_DAO) chỉ thực thi câu lệnh cập nhật trạng thái: UPDATE SanPham SET trangThai = 0 WHERE maSanPham = ?. Giao diện bán hàng chỉ tải dữ liệu danh mục với điều kiện WHERE trangThai = 1, do đó mẫu giày đã ngừng kinh doanh sẽ lập tức ẩn khỏi quầy thu ngân nhưng toàn bộ hóa đơn và doanh thu trong quá khứ vẫn được bảo toàn nguyên vẹn 100%.", "Xóa mềm sản phẩm: ")
    add_bullet("Bảng NhanVien cũng được quản lý trạng thái bằng cột trangThai (BIT, DEFAULT 1). Khi nhân viên nghỉ việc, lớp NhanVien_DAO thực hiện cập nhật trangThai = 0. Hệ thống sẽ chặn nhân viên này đăng nhập bằng mật khẩu SHA-256 đã vô hiệu hóa, nhưng toàn bộ mã nhân viên phụ trách trên các chứng từ hóa đơn cũ vẫn được lưu giữ phục vụ tra cứu kiểm toán.", "Quản lý nhân viên nghỉ việc: ")
    add_bullet("Các ràng buộc khóa ngoại tham chiếu từ ChiTietHoaDon đến HoaDon và ChiTietGiay đều giữ nguyên tắc không xóa lan truyền (NO ACTION), bảo đảm dữ liệu chứng từ thanh toán là bất biến (immutable) theo đúng chuẩn mực hạch toán tài chính.", "Bảo toàn chứng từ tài chính: ")

    doc.add_page_break()

    # ==========================================
    # PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH
    # ==========================================
    add_h1("PHẦN IV: HIỆN THỰC VÀ MÔ TẢ GIAO DIỆN CHƯƠNG TRÌNH")
    
    add_h2("I. Chức năng Đăng nhập & Phân quyền truy cập (Login & RBAC)")
    add_p("Giao diện Đăng nhập (DangNhap_GUI) được thiết kế đồng bộ theo giao diện hệ thống của Windows thông qua UIManager.getSystemLookAndFeelClassName(), kết hợp cùng lớp tiện ích UIHelper tự vẽ các nút bấm bo góc và màu sắc nhận diện trang nhã.")
    add_bullet("Nhân viên khởi chạy ứng dụng. Con trỏ chuột tự động focus sẵn vào ô 'Mã nhân viên' (hỗ trợ định dạng mã chuẩn NV0001 theo đúng quy chuẩn CSDL).", "Bước 1 - Mở ứng dụng: ")
    add_bullet("Nhân viên nhập mã số và mật khẩu vào trường JPasswordField. Người dùng có thể nhấn phím Enter tại bất kỳ ô nhập liệu nào để thực hiện đăng nhập nhanh mà không cần thao tác chuột.", "Bước 2 - Nhập thông tin đăng nhập: ")
    add_bullet("Nhấn Enter hoặc click nút 'Đăng Nhập'. Hệ thống gọi NhanVien_DAO.dangNhap() để xác thực: mật khẩu nhập vào được băm bằng thuật toán SHA-256 (tạo chuỗi hex 64 ký tự) và đối chiếu trực tiếp với cột matKhau trong bảng NhanVien.", "Bước 3 - Xác thực thông tin: ")
    add_bullet("Nếu là Quản lý: Hệ thống hiển thị đầy đủ 4 tab chức năng trên giao diện chính ManHinhChinh_GUI gồm Bán hàng (POS), Quản lý mẫu giày, Khách hàng & tích điểm và Quản lý nhân sự. Nếu là Nhân viên bán hàng: Hệ thống chỉ hiển thị 3 tab phục vụ bán lẻ và vô hiệu hóa các nút Thêm, Sửa, Xóa trên màn hình danh mục sản phẩm.", "Bước 4 - Phân quyền giao diện: ")
    add_callout("Bảo mật mật khẩu với mã băm SHA-256: Hệ thống không lưu trữ mật khẩu ở dạng văn bản rõ mà mã hóa một chiều qua thuật toán SHA-256 thành chuỗi cố định 64 ký tự hex. Quá trình kiểm tra quyền hạn được xử lý tập trung trong NhanVien_DAO, bảo đảm an toàn dữ liệu và tối ưu tốc độ xử lý.", "BẢO MẬT XÁC THỰC:");

    add_h2("II. Chức năng Bán hàng tại quầy (POS - Nghiệp vụ trọng tâm)")
    add_p("Màn hình Bán hàng (BanHang_GUI) là phân hệ cốt lõi phục vụ trực tiếp nghiệp vụ tại quầy thu ngân, được thiết kế tối ưu công thái học với 2 khu vực chức năng trực quan:")
    add_bullet("Khối Chọn sản phẩm: Cho phép thu ngân lựa chọn mẫu giày từ danh sách (cboSanPham), chọn kích cỡ (cboSize) và màu sắc (cboMauSac). Khi lựa chọn một biến thể cụ thể, nhãn hiển thị số lượng tồn kho SoLuongTon tức thì (vd: 'Còn: 15 đôi') cùng đơn giá niêm yết. Thu ngân nhập số lượng mua và click 'Thêm vào giỏ'. Phía dưới là Bảng giỏ hàng hiển thị danh sách các đôi giày đã chọn với đầy đủ cột: STT, Mã chi tiết, Tên sản phẩm, Size, Màu sắc, Số lượng, Đơn giá, Giảm giá, Thành tiền và hỗ trợ nút 'Xóa mục' (hoặc nhấn phím Delete).", "Khu vực 1 (Bên trái): Chọn biến thể & Giỏ hàng: ")
    add_bullet("Khối Khách hàng: Nhập số điện thoại khách hàng vào ô txtSDTKhach và nhấn 'Tìm' để tra cứu nhanh qua KhachHang_DAO. Nếu là khách quen, hệ thống hiển thị tên khách, hạng thành viên (Đồng, Bạc, Vàng, Kim Cương) và số điểm tích lũy hiện có. Checkbox 'Dùng điểm' cho phép quy đổi 1 điểm = 1.000 VNĐ để trừ tiền trực tiếp vào đơn hàng. Khối Thanh toán: Hiển thị Tổng tiền hàng, Chiết khấu hạng thẻ, Tiền giảm điểm, Tổng tiền cần thanh toán. Thu ngân chọn phương thức (Tiền mặt hoặc Chuyển khoản QR), nhập tiền khách đưa và hệ thống tự động tính tiền thừa realtime có cơ chế kiểm soát ngoại lệ NumberFormatException.", "Khu vực 2 (Bên phải): Thông tin khách hàng & Bảng thanh toán: ")

    add_p("Kịch bản 5 bước thao tác thanh toán chuẩn hóa:")
    add_bullet("Thu ngân chọn mẫu giày từ combobox, lựa chọn kích cỡ và màu sắc tương ứng. Hệ thống truy xuất dữ liệu hiển thị SoLuongTon thực tế trong kho và đơn giá bán.", "Bước 1 - Chọn biến thể mẫu giày: ")
    add_bullet("Nhập số lượng cần mua vào spinner và click nút 'Thêm vào giỏ' (hoặc nhấn Enter). Sản phẩm được đưa vào bảng giỏ hàng, tự động cộng dồn số lượng nếu trùng biến thể SKU.", "Bước 2 - Đưa vào giỏ hàng: ")
    add_bullet("Thu ngân nhập số điện thoại khách hàng, click 'Tìm'. Nếu khách yêu cầu sử dụng điểm tích lũy để giảm giá, thu ngân tích chọn checkbox 'Dùng điểm' (1 điểm tương đương 1.000 VNĐ tiền mặt).", "Bước 3 - Nhận diện khách hàng & Tích điểm: ")
    add_bullet("Nhập số tiền khách đưa vào ô nhập liệu. Hệ thống tự động tính toán số tiền thừa cần thối lại theo thời gian thực và hiển thị bằng chữ số to rõ.", "Bước 4 - Tính tiền thừa: ")
    add_bullet("Thu ngân nhấn phím tắt F10 (hoặc click nút 'Thanh toán (F10)'). Hệ thống gọi phương thức thanhToanDonHang() kích hoạt giao dịch CSDL với Transaction toàn vẹn, cập nhật trừ kho SoLuongTon nguyên tử và hiển thị hộp thoại hóa đơn nhiệt K80 (JDialog) xác nhận thanh toán.", "Bước 5 - Thanh toán F10 & Hóa đơn K80: ")

    add_callout("Giao dịch toàn vẹn với JDBC Transaction: Quy trình thanh toán được thực thi thông qua Transaction trong HoaDon_DAO. Hệ thống đặt con.setAutoCommit(false), sinh mã hóa đơn có khóa bảo vệ, thêm dữ liệu hóa đơn, duyệt trừ kho từng đôi giày theo câu lệnh có điều kiện (WHERE soLuongTon >= ?) và tích điểm khách hàng. Nếu có bất kỳ lỗi nào xảy ra hoặc kho hàng không đủ số lượng, hệ thống gọi rollback() ngay lập tức để bảo đảm dữ liệu tuyệt đối nhất quán.", "TOÀN VẸN GIAO DỊCH:");

    add_h2("III. Chức năng Quản lý sản phẩm giày dép & Biến thể SKU")
    add_p("Phân hệ Quản lý sản phẩm (QuanLySanPham_GUI) phục vụ ban quản lý theo dõi và điều chỉnh danh mục hàng hóa:")
    add_bullet("Form thông tin sản phẩm gồm: Mã sản phẩm (định dạng SP[0-9]{4}), Tên sản phẩm, Loại giày (danh sách lựa chọn như Sneaker, Thể Thao, Giày Da, Sandal), Thương hiệu (lựa chọn nhãn hàng như Nike, Adidas, Puma, Biti's, Vans), Giá nhập, Giá bán và Chất liệu.", "Bố cục form thông tin: ")
    add_bullet("Hệ thống tự động sinh một biến thể SKU mặc định (kích cỡ 40, màu Đen, SoLuongTon = 20) trong ChiTietGiay khi tạo mới mẫu giày để sẵn sàng phục vụ bán hàng ngay lập tức.", "Khởi tạo biến thể mặc định: ")
    add_bullet("Kiểm tra tính hợp lệ của dữ liệu nhập liệu: Giá nhập phải lớn hơn 0, Giá bán phải lớn hơn hoặc bằng Giá nhập nhằm bảo đảm hiệu quả kinh tế cho cửa hàng.", "Kiểm soát giá cả nghiêm ngặt: ")
    add_bullet("Áp dụng cơ chế Xóa mềm (Soft-Delete): Khi người quản lý thực hiện xóa một mẫu giày, hệ thống cập nhật trangThai = 0 trong bảng SanPham. Nhờ vậy, sản phẩm sẽ không còn xuất hiện trong danh mục bán lẻ tại quầy POS nhưng toàn bộ các dòng hóa đơn bán hàng trong quá khứ vẫn được bảo toàn nguyên vẹn 100%, tránh được lỗi vi phạm khóa ngoại trong cơ sở dữ liệu.", "Cơ chế xóa mềm an toàn: ")

    add_h2("IV. Chức năng Quản lý khách hàng & Tích điểm thành viên")
    add_p("Phân hệ Quản lý khách hàng (QuanLyKhachHang_GUI) xây dựng mối quan hệ gắn kết với khách hàng thân thiết:")
    add_bullet("Bảng dữ liệu hiển thị danh sách khách hàng gồm: Mã khách hàng (KH[0-9]{4}), Họ tên, Số điện thoại, Giới tính, Ngày sinh, Địa chỉ, Email, Điểm tích lũy và Hạng thành viên.", "Danh sách và thông tin chi tiết: ")
    add_bullet("Form nhập liệu kiểm tra số điện thoại bắt buộc tuân theo biểu thức chính quy (Regex) 10 chữ số hợp lệ của các nhà mạng Việt Nam (^0[35789]\\d{8}$).", "Kiểm tra hợp lệ số điện thoại: ")
    add_bullet("Cột điểm tích lũy và hạng thành viên (Đồng, Bạc, Vàng, Kim Cương) được thiết lập chỉ đọc (read-only) trên form nhập liệu nhằm chống gian lận. Điểm số chỉ được tự động cộng dồn và thăng hạng khi giao dịch thanh toán hóa đơn hoàn tất.", "Bảo vệ điểm tích lũy: ")
    add_bullet("Hỗ trợ tìm kiếm khách hàng nhanh theo số điện thoại hoặc mã số. Thao tác xóa khách hàng được thực thi qua KhachHang_DAO.xoaKhachHang() (xóa vật lý nếu khách hàng chưa phát sinh hóa đơn).", "Thao tác dữ liệu khách hàng: ")

    add_h2("V. Chức năng Thống kê doanh thu & Hiệu suất bán hàng")
    add_p("Phân hệ Thống kê (ThongKe_GUI) hỗ trợ người quản lý theo dõi tổng quan tình hình kinh doanh của cửa hàng:")
    add_bullet("Hệ thống bố trí 4 thẻ chỉ số tổng quan (KPI Cards) được tính toán trực tiếp từ danh sách hóa đơn lấy từ HoaDon_DAO.getAllHoaDon(): Tổng doanh thu (VNĐ), Tổng số đơn hàng, Số lượng giày bán ra (ước lượng trên giao diện bằng công thức: số đơn hàng nhân 2 để định hình quy mô) và Tổng số khách hàng.", "Thẻ chỉ số tổng hợp (KPI Cards): ")
    add_bullet("Combobox thời gian (cboThoiGian) cung cấp các tùy chọn xem mốc thời gian báo cáo như 'Tất cả', 'Hôm nay', 'Tháng này', 'Năm nay', đi kèm nút 'Lọc dữ liệu' và 'Làm mới' cập nhật bảng hóa đơn.", "Bộ lọc mốc thời gian: ")
    add_bullet("Bảng danh mục Top 5 sản phẩm bán chạy hiển thị danh sách các mẫu giày tiêu biểu của cửa hàng (hiện tại hiển thị danh sách mẫu 5 dòng cố định trên giao diện GUI nhằm định hình trực quan bố cục).", "Bảng top sản phẩm tiêu biểu: ")
    add_bullet("Nút 'Xuất Báo Cáo [Excel]' trên giao diện khi người dùng nhấn sẽ kích hoạt hộp thoại JOptionPane thông báo trạng thái xuất báo cáo tới đường dẫn lưu trữ, đóng vai trò định hướng mở rộng tính năng trong giai đoạn tiếp theo.", "Nút xuất báo cáo doanh thu: ")

    if os.path.exists("diagram_chart_shoe.png"):
        doc.add_picture("diagram_chart_shoe.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Hình 3. Minh họa thống kê doanh thu và phân tích top sản phẩm bán chạy")
        set_font(r_c, size=10, italic=True, color_rgb=(71, 85, 105))

    add_h2("VI. Bảng hệ thống phím tắt & Điều hướng bán hàng (Hotkeys)")
    add_p("Để tối ưu hóa trải nghiệm công thái học và giải phóng nhân viên thu ngân khỏi việc phải liên tục dùng chuột, hệ thống triển khai cơ chế KeyBindings với phạm vi WHEN_IN_FOCUSED_WINDOW trên JRootPane của ManHinhChinh_GUI. Cơ chế này cho phép bắt trọn vẹn các sự kiện phím chức năng trên toàn bộ cửa sổ ứng dụng bất kể thành phần giao diện nào đang nhận tiêu điểm:")
    t_hotkeys = doc.add_table(rows=8, cols=3)
    hotkey_data = [
        ["F1", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Bán hàng (POS)"],
        ["F2", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Quản lý mẫu giày"],
        ["F3", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Khách hàng & Tích điểm"],
        ["F4", "Toàn hệ thống (JRootPane)", "Chuyển nhanh đến Tab Quản lý nhân sự (dành cho Quản lý)"],
        ["F10", "Toàn hệ thống / Màn hình POS", "Thực thi thanh toán đơn hàng tại quầy POS (thanhToanDonHang)"],
        ["Delete", "Bảng giỏ hàng POS", "Xóa mục sản phẩm đang được chọn khỏi giỏ hàng (xoaMucKhoiGio)"],
        ["Esc", "Toàn hệ thống (JRootPane)", "Mở hộp thoại xác nhận đăng xuất khỏi hệ thống"]
    ]
    style_table(t_hotkeys, [1.0, 2.2, 3.1], ["Phím tắt", "Phạm vi áp dụng", "Hành động thực thi"], hotkey_data)

    doc.add_page_break()

    # ==========================================
    # PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN
    # ==========================================
    add_h1("PHẦN V: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN")
    
    add_h2("I. Đánh giá kết quả đạt được và những hạn chế")
    add_h3("1. Những ưu điểm nổi bật của hệ thống")
    add_bullet("Phân tách ranh giới rõ ràng theo kiến trúc 3 tầng chuẩn mực: Tầng Trình diễn (GUI Java Swing với UIHelper tự vẽ giao diện), Tầng Truy cập dữ liệu (DAO với JDBC PreparedStatement và Transaction kiểm soát an toàn), và Tầng Thực thể (Entity hướng đối tượng thuần túy).", "Kiến trúc 3 tầng chuẩn mực: ")
    add_bullet("Giải quyết triệt để bài toán biến thể giày dép qua liên kết giữa SanPham và ChiTietGiay, quản lý chi tiết kích cỡ và màu sắc, hiển thị SoLuongTon chính xác tại quầy.", "Quản lý biến thể chuyên sâu: ")
    add_bullet("Cơ chế JDBC Transaction với khóa nguyên tử và lệnh gọi rollback() khi có lỗi trong HoaDon_DAO, kết hợp kỹ thuật Xóa mềm cập nhật cột trangThai trong SanPham_DAO giúp bảo vệ toàn vẹn dữ liệu, loại bỏ hiện tượng bán âm kho và giữ nguyên lịch sử kế toán.", "An toàn dữ liệu tuyệt đối: ")
    add_bullet("Hệ thống phím tắt toàn cục đăng ký qua WHEN_IN_FOCUSED_WINDOW (F1-F4, F10, Delete, Esc) cùng giao diện tính tiền thừa realtime giúp thu ngân thao tác nhanh chóng, rút ngắn thời gian phục vụ tại quầy.", "Công thái học và tốc độ: ")
    add_bullet("Giao diện đồ họa trang nhã, phân chia rõ ràng các phân hệ bán hàng, sản phẩm, khách hàng thân thiết, quản trị nhân sự và thống kê tổng quan.", "Giao diện thân thiện và dễ dùng: ")

    add_h3("2. Những điểm còn hạn chế")
    add_bullet("Thống kê số lượng đôi giày bán ra tại thẻ KPI hiện là con số ước lượng (tính bằng công thức số đơn hàng nhân 2), chưa thực hiện câu lệnh truy vấn tổng hợp số lượng thực tế từ bảng ChiTietHoaDon.", "Ước lượng số lượng bán ra: ")
    add_bullet("Bảng Top 5 sản phẩm bán chạy đang hiển thị danh sách cố định trên giao diện GUI nhằm định hình bố cục, chưa liên kết truy vấn gom nhóm theo doanh số bán hàng thực tế từ cơ sở dữ liệu.", "Top sản phẩm hiển thị cố định: ")
    add_bullet("Nút 'Xuất Báo Cáo [Excel]' trên giao diện mới chỉ dừng lại ở việc hiển thị hộp thoại thông báo định hướng tính năng, chưa tích hợp thư viện tạo file bảng tính thực tế.", "Chưa xuất file bảng tính thực tế: ")
    add_bullet("Phân hệ Thống kê chưa có biểu đồ tương tác động mà hiện đang sử dụng hình ảnh minh họa phân tích kinh doanh để định hình giao diện báo cáo.", "Chưa có biểu đồ tương tác: ")
    add_bullet("Thao tác xóa khách hàng tại KhachHang_DAO là thao tác xóa cứng (DELETE vật lý trong CSDL), chưa đồng bộ cơ chế xóa mềm qua trạng thái như phân hệ sản phẩm.", "Xóa khách hàng là xóa cứng: ")
    add_bullet("Hệ thống hiện tại vận hành trên nền tảng ứng dụng Desktop nội bộ (mạng LAN cửa hàng), chưa hỗ trợ người quản lý theo dõi tình hình bán hàng từ xa qua thiết bị di động hay website.", "Chưa có phiên bản Web/Mobile: ")

    add_h2("II. Hướng phát triển trong tương lai")
    add_p("Nhằm hoàn thiện hệ thống và đáp ứng nhu cầu mở rộng quy mô kinh doanh bán lẻ giày dép, nhóm đề xuất các định hướng nâng cấp tiếp theo:")
    add_bullet("Xây dựng các câu lệnh truy vấn chi tiết từ bảng ChiTietHoaDon để tính toán chính xác tuyệt đối số lượng giày đã bán và xếp hạng Top sản phẩm bán chạy tự động; tích hợp thư viện xuất dữ liệu ra file bảng tính phục vụ công tác kế toán định kỳ.", "1. Hoàn thiện phân hệ thống kê & báo cáo: ")
    add_bullet("Bổ sung cột trangThai vào bảng KhachHang và hoàn thiện cơ chế xóa mềm đồng bộ cho toàn bộ các thực thể trong hệ thống.", "2. Đồng bộ giải pháp xóa mềm cho khách hàng: ")
    add_bullet("Tự động tạo mã QR thanh toán chứa sẵn số tiền và mã hóa đơn, kết nối Webhook ngân hàng để xác nhận giao dịch tự động mà thu ngân không cần kiểm tra điện thoại.", "3. Tích hợp thanh toán QR Code động: ")
    add_bullet("Xây dựng hệ thống Backend API bằng Spring Boot và phát triển ứng dụng di động hỗ trợ nhân viên dùng camera quét kiểm kê kho và quản lý theo dõi doanh thu thời gian thực từ xa.", "4. Mở rộng kiến trúc Web & Mobile: ")
    add_bullet("Phân tích dữ liệu mua hàng và xu hướng tiêu dùng theo mùa, đưa ra dự báo sớm về các kích cỡ sắp hết hàng để hỗ trợ lập kế hoạch nhập hàng kịp thời.", "5. Ứng dụng trí tuệ nhân tạo dự báo tồn kho: ")

    add_h2("III. Lời kết")
    add_p("Đồ án 'Hệ thống Quản lý Bán hàng tại Cửa hàng Giày dép Thời trang (StepUp Footwear)' đã hoàn thành các mục tiêu nghiên cứu và thực nghiệm đề ra trong học phần Lập trình hướng sự kiện trên nền tảng Java. Đề tài phản ánh đúng đắn mô hình kiến trúc 3 tầng: Tầng Trình diễn (GUI Swing kết hợp UIHelper), Tầng Truy cập dữ liệu (DAO với JDBC Transaction), và Tầng Thực thể nghiệp vụ (Entity). Nhóm sinh viên chúng em đã tích lũy được nhiều kinh nghiệm thực tiễn quý giá về thiết kế giao diện công thái học, xử lý giao dịch cơ sở dữ liệu toàn vẹn và giải quyết bài toán quản lý ma trận biến thể giày dép trong môi trường bán lẻ.")
    add_p("Nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc nhất tới cô Trần Thị Anh Thi cùng toàn thể quý Thầy Cô trong Khoa Công nghệ Thông tin - Trường Đại học Công nghiệp TP. Hồ Chí Minh đã tận tình chỉ dạy, động viên và hướng dẫn chúng em trong suốt quá trình thực hiện đồ án này!")

    # Save document
    output_filename = "BaoCao_QuanLyBanGiay_HSK.docx"
    doc.save(output_filename)
    print(f"Document saved successfully as: {output_filename}")
    
    # Also save a copy as QuanLyBanGiay_HSK.docx
    doc.save("QuanLyBanGiay_HSK.docx")
    print("Also saved copy as: QuanLyBanGiay_HSK.docx")

if __name__ == '__main__':
    create_document()

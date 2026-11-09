#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Áp dụng thiết kế lại trang bìa chính thức vào:
- E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx
- E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx

Các tiêu chuẩn kỹ thuật:
1. Thứ tự: Tên trường/khoa -> Gạch phân cách -> Logo IUH (4cm) -> Tên báo cáo -> Đề tài -> Bảng thông tin -> Năm
2. Bảng không viền 3 cột: 5.3cm, 7.4cm, 2.8cm (tổng 15.5cm)
3. Không rớt dòng trên nhãn và trên tên nhóm trưởng
4. Cột MSSV thẳng hàng tuyệt đối bên phải
5. Giữ nguyên 100% nội dung từ trang 2 trở đi, tổng số trang 45/45
6. Độ sạch định dạng: 0 shading, 0 highlight, màu mặc định 000000, font Times New Roman
"""

import os
import sys
import shutil
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

PROJ_DOCX = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
DELIV_DOCX = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
LOGO_PATH = r"E:\Eclipse Java\project\logo_iuh_new.png"
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
PREVIEW_PNG = r"E:\Eclipse Java\project\_sync\cover_preview.png"

def apply_redesign(docx_file):
    print(f"=== Đang thiết kế lại trang bìa cho: {docx_file} ===")
    doc = docx.Document(docx_file)

    # 1. Bật different_first_page_header_footer để trang bìa không có running header
    sec = doc.sections[0]
    sec.different_first_page_header_footer = True
    for p in sec.first_page_header.paragraphs:
        p.text = ""

    # 2. Xác định vị trí ngắt trang đầu tiên (kết thúc trang bìa cũ)
    break_p_idx = -1
    for i, p in enumerate(doc.paragraphs[:15]):
        if len(p._p.xpath('.//w:br[@w:type="page"]')) > 0:
            break_p_idx = i
            break

    print(f"Trang bìa cũ kết thúc tại Paragraph P{break_p_idx}")
    assert break_p_idx != -1, "Không tìm thấy dấu ngắt trang đầu tiên!"

    # Xóa toàn bộ paragraph của trang bìa cũ
    for i in range(break_p_idx - 1, -1, -1):
        p = doc.paragraphs[i]
        p._p.getparent().remove(p._p)

    # Đoạn break_p lúc này trở thành paragraph đầu tiên của document
    p_anchor = doc.paragraphs[0]

    # [1] Tên cơ quan & trường (cùng cỡ chữ 13pt bold)
    p_univ = p_anchor.insert_paragraph_before()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_before = Pt(0)
    p_univ.paragraph_format.space_after = Pt(2)
    p_univ.paragraph_format.line_spacing = 1.15
    r = p_univ.add_run("BỘ CÔNG THƯƠNG\nTRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP. HỒ CHÍ MINH\nKHOA CÔNG NGHỆ THÔNG TIN")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Gạch phân cách
    p_div = p_anchor.insert_paragraph_before()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(2)
    p_div.paragraph_format.space_after = Pt(12)
    r_div = p_div.add_run("------------------***------------------")
    r_div.font.name = "Times New Roman"
    r_div.font.size = Pt(10)
    r_div.font.bold = True
    r_div.font.color.rgb = RGBColor(0, 0, 0)

    # [2] Logo IUH (căn giữa, rộng 4cm = 1.5748 in)
    p_logo = p_anchor.insert_paragraph_before()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(4)
    p_logo.paragraph_format.space_after = Pt(14)
    r_logo = p_logo.add_run()
    r_logo.add_picture(LOGO_PATH, width=Inches(4.0 / 2.54))

    # [3] Báo cáo môn học
    p_report = p_anchor.insert_paragraph_before()
    p_report.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_report.paragraph_format.space_before = Pt(4)
    p_report.paragraph_format.space_after = Pt(2)
    p_report.paragraph_format.line_spacing = 1.15
    r_rep = p_report.add_run("BÁO CÁO MÔN HỌC")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(14)
    r_rep.font.bold = True
    r_rep.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = p_anchor.insert_paragraph_before()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(15)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0, 0, 0)

    # [4] Đề tài số 3:
    p_de_tai = p_anchor.insert_paragraph_before()
    p_de_tai.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_de_tai.paragraph_format.space_before = Pt(2)
    p_de_tai.paragraph_format.space_after = Pt(4)
    r_dt = p_de_tai.add_run("ĐỀ TÀI SỐ 3:")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(13)
    r_dt.font.bold = True
    r_dt.font.color.rgb = RGBColor(0, 0, 0)

    p_title = p_anchor.insert_paragraph_before()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.2
    r_tit = p_title.add_run("HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG\nGIÀY DÉP THỜI TRANG")
    r_tit.font.name = "Times New Roman"
    r_tit.font.size = Pt(17)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(0, 0, 0)

    p_eng = p_anchor.insert_paragraph_before()
    p_eng.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eng.paragraph_format.space_before = Pt(2)
    p_eng.paragraph_format.space_after = Pt(18)
    r_eng = p_eng.add_run("(STEPUP FOOTWEAR POS SYSTEM)")
    r_eng.font.name = "Times New Roman"
    r_eng.font.size = Pt(13)
    r_eng.font.bold = True
    r_eng.font.color.rgb = RGBColor(0, 0, 0)

    # [5] Khối thông tin: Bảng không viền 3 cột
    # Cột 1: 5.3 cm = 3005 dxa
    # Cột 2: 7.4 cm = 4195 dxa
    # Cột 3: 2.8 cm = 1587 dxa
    # Tổng: 15.5 cm = 8787 dxa
    col_dxa = [3005, 4195, 1587]
    total_dxa = sum(col_dxa)

    p_tbl_anchor = p_anchor.insert_paragraph_before()

    table = doc.add_table(rows=8, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # 5.1 Thiết lập tblPr (tblW dxa & tblBorders none)
    tblPr = table._tbl.tblPr
    for w in tblPr.xpath('w:tblW'):
        tblPr.remove(w)
    tblPr.insert(0, parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>'))

    tblBorders = tblPr.xpath('w:tblBorders')
    for b in tblBorders:
        tblPr.remove(b)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'</w:tblBorders>'
    ))

    # 5.2 Xóa mọi tblGrid cũ do python-docx tạo và thay bằng tblGrid duy nhất
    for g in table._tbl.xpath('w:tblGrid'):
        table._tbl.remove(g)

    tblGrid = parse_xml(
        f'<w:tblGrid {nsdecls("w")}>\n'
        f'  <w:gridCol w:w="{col_dxa[0]}"/>\n'
        f'  <w:gridCol w:w="{col_dxa[1]}"/>\n'
        f'  <w:gridCol w:w="{col_dxa[2]}"/>\n'
        f'</w:tblGrid>'
    )
    table._tbl.insert(table._tbl.index(tblPr) + 1, tblGrid)

    table_data = [
        ("Giảng viên hướng dẫn:", "ThS. Trần Thị Anh Thi", ""),
        ("Nhóm sinh viên thực hiện:", "Nguyễn Trọng Vinh (Nhóm trưởng)", "24704381"),
        ("", "Nhiêu Minh Kỳ", "24718221"),
        ("", "Trần Tấn Kiệt", "24695041"),
        ("", "Trần Mộc Tấn Phát", "24638311"),
        ("Lớp học phần:", "DHKTPM18A", ""),
        ("Khóa học:", "2022 – 2026", ""),
        ("Chuyên ngành:", "Kỹ thuật Phần mềm", "")
    ]

    for row_idx, (c0_text, c1_text, c2_text) in enumerate(table_data):
        row = table.rows[row_idx]
        for col_idx, text in enumerate([c0_text, c1_text, c2_text]):
            cell = row.cells[col_idx]
            
            tcPr = cell._tc.get_or_add_tcPr()
            for w in tcPr.xpath('w:tcW'):
                tcPr.remove(w)
            tcPr.insert(0, parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_dxa[col_idx]}" w:type="dxa"/>'))
            
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>\n'
                f'  <w:top w:w="30" w:type="dxa"/>\n'
                f'  <w:bottom w:w="30" w:type="dxa"/>\n'
                f'  <w:left w:w="20" w:type="dxa"/>\n'
                f'  <w:right w:w="20" w:type="dxa"/>\n'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif col_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            if text:
                r = p.add_run(text)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11.5)
                r.font.color.rgb = RGBColor(0, 0, 0)
                r.font.bold = (col_idx == 0)

    p_tbl_anchor._p.addprevious(table._tbl)
    p_tbl_anchor._p.getparent().remove(p_tbl_anchor._p)

    # [6] Cuối trang: Thành phố Hồ Chí Minh, Năm 2026 (cân đối 80pt space_before)
    p_city = p_anchor.insert_paragraph_before()
    p_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_city.paragraph_format.space_before = Pt(80)
    p_city.paragraph_format.space_after = Pt(0)
    r_city = p_city.add_run("Thành phố Hồ Chí Minh, Năm 2026")
    r_city.font.name = "Times New Roman"
    r_city.font.size = Pt(12)
    r_city.font.italic = True
    r_city.font.color.rgb = RGBColor(0, 0, 0)

    # Lưu lại file
    doc.save(docx_file)
    print(f"[OK] Đã lưu thành công: {docx_file}")

def verify_and_render():
    print("\n=== Đang convert sang PDF và kiểm tra 5 tiêu chí checklist ===")
    outdir = r"E:\Eclipse Java\project\_sync"
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", "--outdir", outdir, PROJ_DOCX]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    assert res.returncode == 0, f"Convert thất bại: {res.stderr}"

    pdf_file = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"
    doc_pdf = pymupdf.open(pdf_file)
    total_pages = len(doc_pdf)
    print(f"Tổng số trang: {total_pages} / 45")
    assert total_pages == 45, f"Tổng số trang bị lệch: {total_pages} (kỳ vọng 45)"

    # Render ảnh preview
    page0 = doc_pdf[0]
    pix = page0.get_pixmap(dpi=150)
    pix.save(PREVIEW_PNG)
    print(f"[OK] Đã lưu cover_preview.png: {pix.width}x{pix.height}")

    words = page0.get_text("words")

    # 1. Thứ tự dọc
    school_words = [w for w in words if "CÔNG" in w[4] or "NGHIỆP" in w[4]]
    report_words = [w for w in words if "BÁO" in w[4] or "CÁO" in w[4]]
    topic_words = [w for w in words if "STEPUP" in w[4]]
    table_words = [w for w in words if "Giảng" in w[4] or "Nhóm" in w[4]]
    city_words = [w for w in words if "2026" in w[4] and w[1] > 550]

    y_school = school_words[0][1]
    y_report = report_words[0][1]
    y_topic = topic_words[0][1]
    y_table = table_words[0][1]
    y_city = city_words[0][1]

    print(f"Thứ tự dọc: School={y_school:.1f} < Report={y_report:.1f} < Topic={y_topic:.1f} < Table={y_table:.1f} < City={y_city:.1f}")
    assert y_school < y_report < y_topic < y_table < y_city, "Thứ tự không đúng!"

    # 2. 'Nguyễn Trọng Vinh (Nhóm trưởng)' trọn vẹn 1 dòng
    vinh_words = [w for w in words if w[4] in ["Nguyễn", "Trọng", "Vinh", "(Nhóm", "trưởng)"]]
    y_vinh = set([round(w[1], 1) for w in vinh_words])
    print(f"Tọa độ y nhóm trưởng: {y_vinh}")
    assert len(y_vinh) == 1, f"Tên nhóm trưởng bị rớt dòng: {y_vinh}"

    # 3. MSSV thẳng hàng
    mssv_list = ["24704381", "24718221", "24695041", "24638311"]
    mssv_words = [w for w in words if w[4] in mssv_list]
    x1_coords = set([round(w[2], 1) for w in mssv_words])
    print(f"Tọa độ x1 cột MSSV: {x1_coords}")
    assert len(x1_coords) == 1, f"Cột MSSV không thẳng hàng: {x1_coords}"

    # 4. Nhãn cột 1 không bị gãy
    col0_labels = ["Giảng viên hướng dẫn:", "Nhóm sinh viên thực hiện:", "Lớp học phần:", "Khóa học:", "Chuyên ngành:"]
    t0 = page0.get_text("text")
    for lbl in col0_labels:
        assert lbl in t0, f"Nhãn bị gãy: {lbl}"

    # 5. Kiểm tra trang 2
    t1 = doc_pdf[1].get_text("text")
    assert "DANH SÁCH THÀNH VIÊN TRONG NHÓM THỰC HIỆN" in t1, "Nội dung trang 2 không khớp!"

    print("\n>>> TẤT CẢ 5 TIÊU CHÍ CHECKLIST ĐỀU ĐẠT 100% <<<")

if __name__ == "__main__":
    # Áp dụng cho file chính
    apply_redesign(PROJ_DOCX)
    
    # Kiểm tra và render
    verify_and_render()
    
    # Đồng bộ sang Deliverable
    shutil.copy2(PROJ_DOCX, DELIV_DOCX)
    print(f"[OK] Đã đồng bộ sang Deliverable: {DELIV_DOCX}")

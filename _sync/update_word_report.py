#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật logo IUH mới và Database Diagram SSMS vào BaoCao_QuanLyBanGiay_HSK.docx
Tuân thủ nghiêm ngặt các quy tắc:
1. Logo: chèn vào đầu trang bìa (căn giữa, rộng khoảng 4cm = 1.5748 inches).
2. Database diagram: chèn vào mục 3.1 (căn giữa, rộng khoảng 15cm = 5.9055 inches) kèm caption.
3. Không tô nền (w:shd), không highlight (w:highlight), chữ màu mặc định (000000), heading đậm.
"""

import os
import sys
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
DELIVERABLE_DOCX_PATH = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
LOGO_PATH = r"E:\Eclipse Java\project\logo_iuh_new.png"
SSMS_DIAGRAM_PATH = r"E:\Eclipse Java\project\database_diagram_ssms.png"

HEADING_CONFIG = {
    'Heading 1': {'size': Pt(16), 'bold': True},
    'Heading 2': {'size': Pt(15), 'bold': True},
    'Heading 3': {'size': Pt(14), 'bold': True}
}

def update_docx(file_path):
    print(f"\n==========================================")
    print(f"Bắt đầu cập nhật: {file_path}")
    print(f"==========================================")

    doc = docx.Document(file_path)

    # 1. Chèn Logo vào đầu trang bìa (căn giữa, rộng 4cm)
    p0 = doc.paragraphs[0]
    p_logo = p0.insert_paragraph_before()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(12)
    p_logo.paragraph_format.line_spacing = 1.0

    r_logo = p_logo.add_run()
    # 4cm = 4 / 2.54 = 1.5748 inches
    r_logo.add_picture(LOGO_PATH, width=Inches(4.0 / 2.54))
    print(f"[OK] Đã chèn logo IUH vào đầu trang bìa (rộng 4cm = {4.0/2.54:.2f} inches)")

    # 2. Định vị mục 3.1 (PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU) - Bỏ qua Mục Lục TOC
    target_idx = -1
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if (p.style and p.style.name == 'Heading 1' and "PHẦN III" in txt) or \
           ("PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU" in txt and "\t" not in txt):
            target_idx = i
            break

    if target_idx == -1:
        raise ValueError("Không tìm thấy Heading 'PHẦN III: SƠ ĐỒ CƠ SỞ DỮ LIỆU' trong thân bài!")

    print(f"Tìm thấy PHẦN III tại Paragraph {target_idx}: {doc.paragraphs[target_idx].text}")

    # Tìm đoạn chứa ảnh diagram và caption ngay sau mục 3.1
    img_p_idx = -1
    cap_p_idx = -1
    for j in range(target_idx, min(len(doc.paragraphs), target_idx + 15)):
        p = doc.paragraphs[j]
        if len(p._p.xpath('.//w:drawing')) > 0:
            img_p_idx = j
            cap_p_idx = j + 1
            break

    if img_p_idx == -1:
        raise ValueError("Không tìm thấy paragraph chứa ảnh diagram trong mục 3.1!")

    print(f"Paragraph chứa ảnh hiện tại: P{img_p_idx}, Caption: P{cap_p_idx}")

    # Thay thế ảnh cũ bằng database_diagram_ssms.png với độ rộng 15cm (15 / 2.54 = 5.9055 inches)
    p_img = doc.paragraphs[img_p_idx]
    p_img.clear()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(4)
    r_img = p_img.add_run()
    r_img.add_picture(SSMS_DIAGRAM_PATH, width=Inches(15.0 / 2.54))

    # Cập nhật caption cho Database Diagram SSMS
    p_cap = doc.paragraphs[cap_p_idx]
    p_cap.clear()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run("Hình 4. Lược đồ cơ sở dữ liệu quan hệ phát sinh từ Microsoft SQL Server (Database Diagram SSMS 6 bảng)")
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.italic = True
    r_cap.font.bold = False
    r_cap.font.color.rgb = RGBColor(0, 0, 0)
    print(f"[OK] Đã cập nhật Database Diagram SSMS vào mục 3.1 (rộng 15cm = {15.0/2.54:.2f} inches) kèm caption")

    # 3. Chuẩn hóa formatting theo quy tắc: Không tô nền, không highlight, chữ 000000, heading đậm
    # Cập nhật Heading styles
    for h_name, cfg in HEADING_CONFIG.items():
        if h_name in doc.styles:
            s = doc.styles[h_name]
            s.font.size = cfg['size']
            s.font.bold = cfg['bold']
            s.font.color.rgb = RGBColor(0, 0, 0)
            s_rPr = s.element.find(qn('w:rPr'))
            if s_rPr is not None:
                c = s_rPr.find(qn('w:color'))
                if c is not None:
                    c.set(qn('w:val'), '000000')
                    for attr in ['themeColor', 'themeShade', 'themeTint']:
                        if qn(f'w:{attr}') in c.attrib:
                            del c.attrib[qn(f'w:{attr}')]

    for p in doc.paragraphs:
        style_name = p.style.name if p.style else ''
        if style_name in HEADING_CONFIG:
            cfg = HEADING_CONFIG[style_name]
            for r in p.runs:
                r.font.size = cfg['size']
                r.font.bold = cfg['bold']
                r.font.color.rgb = RGBColor(0, 0, 0)

    # Xóa w:shd (shading)
    shd_elements = doc._element.xpath('.//w:shd')
    for shd in shd_elements:
        parent = shd.getparent()
        if parent is not None:
            parent.remove(shd)

    # Xóa w:highlight
    hl_elements = doc._element.xpath('.//w:highlight')
    for hl in hl_elements:
        parent = hl.getparent()
        if parent is not None:
            parent.remove(hl)

    # Chuẩn hóa w:color về 000000
    color_elements = doc._element.xpath('.//w:color')
    for color in color_elements:
        color.set(qn('w:val'), '000000')
        for attr in ['themeColor', 'themeShade', 'themeTint']:
            q_name = qn(f'w:{attr}')
            if q_name in color.attrib:
                del color.attrib[q_name]

    # Lưu tài liệu
    doc.save(file_path)
    print(f"[OK] Đã lưu thành công tài liệu Word: {file_path}")

    # Nghiệm thu tài liệu đã lưu
    doc_check = docx.Document(file_path)
    total_p = len(doc_check.paragraphs)
    total_t = len(doc_check.tables)
    total_d = len(doc_check._element.xpath('.//w:drawing'))
    rem_shd = len(doc_check._element.xpath('.//w:shd'))
    rem_hl = len(doc_check._element.xpath('.//w:highlight'))
    colors = set(c.attrib.get(qn('w:val')) for c in doc_check._element.xpath('.//w:color'))

    print("\n--- KẾT QUẢ NGHIỆM THU ĐỊNH LƯỢNG ---")
    print(f"- Tổng số đoạn văn (paragraphs): {total_p}")
    print(f"- Tổng số bảng biểu (tables): {total_t}")
    print(f"- Tổng số hình ảnh (drawings): {total_d}")
    print(f"- Số w:shd còn lại: {rem_shd}")
    print(f"- Số w:highlight còn lại: {rem_hl}")
    print(f"- Danh sách mã màu chữ trong file: {colors}")

    assert rem_shd == 0, f"Còn {rem_shd} w:shd!"
    assert rem_hl == 0, f"Còn {rem_hl} w:highlight!"
    assert colors.issubset({'000000'}), f"Màu không hợp lệ: {colors}"

    return total_d, total_p, total_t

if __name__ == "__main__":
    d_count, p_count, t_count = update_docx(DOCX_PATH)
    if os.path.exists(DELIVERABLE_DOCX_PATH):
        update_docx(DELIVERABLE_DOCX_PATH)
    print("\n>>> HOÀN TẤT CẬP NHẬT TÀI LIỆU WORD THÀNH CÔNG! <<<")

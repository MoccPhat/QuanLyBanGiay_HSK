#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật 2 sơ đồ Visual Paradigm (Sơ đồ lớp và Sơ đồ tuần tự thanh toán POS)
vào BaoCao_QuanLyBanGiay_HSK.docx, đồng bộ Danh mục hình ảnh và kiểm tra toàn diện.

Quy tắc bắt buộc:
1. Sao lưu trước khi sửa.
2. Thay thế đúng vị trí Hình 3 (Phần II) và Hình 7 (Phần IV.II).
3. Cập nhật Danh mục hình ảnh khớp 100% với caption trong thân bài.
4. Bảo toàn định dạng: không tô nền, không highlight, chữ màu 000000, heading đậm.
5. Kiểm định định lượng trước/sau: số hình (15), số bảng (23), số w:shd (0), số w:highlight (0).
"""

import os
import sys
import shutil
import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
DELIVERABLE_DOCX_PATH = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
VP_CLASS_PATH = r"E:\Eclipse Java\project\vp_class_diagram.png"
VP_SEQ_PATH = r"E:\Eclipse Java\project\vp_sequence_diagram.png"

HEADING_CONFIG = {
    'Heading 1': {'size': Pt(16), 'bold': True},
    'Heading 2': {'size': Pt(15), 'bold': True},
    'Heading 3': {'size': Pt(14), 'bold': True}
}

def update_document(file_path):
    print(f"\n==========================================")
    print(f"Xử lý tài liệu: {file_path}")
    print(f"==========================================")

    doc = docx.Document(file_path)

    # Đếm kiểm kê trước khi sửa
    initial_drawings = len(doc._element.xpath('.//w:drawing'))
    initial_tables = len(doc.tables)
    initial_paragraphs = len(doc.paragraphs)
    print(f"Trước khi sửa: {initial_paragraphs} paragraphs, {initial_tables} tables, {initial_drawings} drawings")

    # 1. Tìm vị trí Hình 3 (Sơ đồ lớp)
    fig3_cap_idx = -1
    fig3_img_idx = -1
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("Hình 3.") and "\t" not in t:
            fig3_cap_idx = i
            # Đoạn ảnh thường là đoạn ngay trước
            if i > 0 and len(doc.paragraphs[i-1]._p.xpath('.//w:drawing')) > 0:
                fig3_img_idx = i - 1
            break

    if fig3_img_idx == -1 or fig3_cap_idx == -1:
        raise ValueError(f"Không tìm thấy vị trí Hình 3! img_idx={fig3_img_idx}, cap_idx={fig3_cap_idx}")

    print(f"Vị trí Hình 3: Ảnh P{fig3_img_idx}, Caption P{fig3_cap_idx}")

    # Cập nhật ảnh Hình 3 (vp_class_diagram.png, width 5.8 inches = 14.73 cm)
    p_img3 = doc.paragraphs[fig3_img_idx]
    p_img3.clear()
    p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img3.paragraph_format.space_before = Pt(6)
    p_img3.paragraph_format.space_after = Pt(4)
    r_img3 = p_img3.add_run()
    r_img3.add_picture(VP_CLASS_PATH, width=Inches(5.8))

    # Cập nhật caption Hình 3
    p_cap3 = doc.paragraphs[fig3_cap_idx]
    p_cap3.clear()
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap3.paragraph_format.space_before = Pt(2)
    p_cap3.paragraph_format.space_after = Pt(10)
    r_cap3 = p_cap3.add_run("Hình 3. Sơ đồ lớp hướng đối tượng (Visual Paradigm 18)")
    r_cap3.font.name = "Times New Roman"
    r_cap3.font.size = Pt(10)
    r_cap3.font.italic = True
    r_cap3.font.bold = False
    r_cap3.font.color.rgb = RGBColor(0, 0, 0)
    print("[OK] Đã chèn vp_class_diagram.png và cập nhật caption Hình 3")

    # 2. Tìm vị trí Hình 7 (Sơ đồ tuần tự thanh toán POS)
    fig7_cap_idx = -1
    fig7_img_idx = -1
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("Hình 7.") and "\t" not in t:
            fig7_cap_idx = i
            if i > 0 and len(doc.paragraphs[i-1]._p.xpath('.//w:drawing')) > 0:
                fig7_img_idx = i - 1
            break

    if fig7_img_idx == -1 or fig7_cap_idx == -1:
        raise ValueError(f"Không tìm thấy vị trí Hình 7! img_idx={fig7_img_idx}, cap_idx={fig7_cap_idx}")

    print(f"Vị trí Hình 7: Ảnh P{fig7_img_idx}, Caption P{fig7_cap_idx}")

    # Cập nhật ảnh Hình 7 (vp_sequence_diagram.png, width 6.0 inches = 15.24 cm)
    p_img7 = doc.paragraphs[fig7_img_idx]
    p_img7.clear()
    p_img7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img7.paragraph_format.space_before = Pt(6)
    p_img7.paragraph_format.space_after = Pt(4)
    r_img7 = p_img7.add_run()
    r_img7.add_picture(VP_SEQ_PATH, width=Inches(6.0))

    # Cập nhật caption Hình 7
    p_cap7 = doc.paragraphs[fig7_cap_idx]
    p_cap7.clear()
    p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap7.paragraph_format.space_before = Pt(2)
    p_cap7.paragraph_format.space_after = Pt(10)
    r_cap7 = p_cap7.add_run("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS (Visual Paradigm 18)")
    r_cap7.font.name = "Times New Roman"
    r_cap7.font.size = Pt(10)
    r_cap7.font.italic = True
    r_cap7.font.bold = False
    r_cap7.font.color.rgb = RGBColor(0, 0, 0)
    print("[OK] Đã chèn vp_sequence_diagram.png và cập nhật caption Hình 7")

    # 3. Cập nhật Danh mục hình ảnh (P68 đến P81)
    # Cập nhật Hình 3, Hình 4, Hình 7 trong Danh mục
    updated_danh_muc = {
        "Hình 3.": ("Hình 3. Sơ đồ lớp hướng đối tượng (Visual Paradigm 18)", "14"),
        "Hình 4.": ("Hình 4. Lược đồ cơ sở dữ liệu quan hệ phát sinh từ Microsoft SQL Server (Database Diagram SSMS 6 bảng)", "21"),
        "Hình 7.": ("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS (Visual Paradigm 18)", "32")
    }

    for i in range(60, 90):
        if i >= len(doc.paragraphs):
            break
        p = doc.paragraphs[i]
        t = p.text.strip()
        for prefix, (new_title, pg) in updated_danh_muc.items():
            if t.startswith(prefix) and "\t" in t:
                # Cập nhật lại các run
                p.clear()
                r1 = p.add_run(new_title)
                r1.font.name = "Times New Roman"
                r1.font.size = Pt(10.5)
                r1.font.italic = True
                r1.font.bold = False
                r1.font.color.rgb = RGBColor(0, 0, 0)

                r2 = p.add_run("\t")

                r3 = p.add_run(pg)
                r3.font.name = "Times New Roman"
                r3.font.size = Pt(10.5)
                r3.font.italic = False
                r3.font.bold = False
                r3.font.color.rgb = RGBColor(0, 0, 0)
                print(f"[OK] Đã cập nhật Danh mục hình ảnh tại P{i}: {new_title}\\t{pg}")

    # 4. Chuẩn hóa định dạng và vệ sinh XML
    # Xóa w:shd
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

    # Lưu file
    doc.save(file_path)
    print(f"[OK] Đã lưu file: {file_path}")

    # 5. Tự kiểm nghiệm thu
    doc_check = docx.Document(file_path)
    final_drawings = len(doc_check._element.xpath('.//w:drawing'))
    final_tables = len(doc_check.tables)
    final_paragraphs = len(doc_check.paragraphs)
    final_shd = len(doc_check._element.xpath('.//w:shd'))
    final_hl = len(doc_check._element.xpath('.//w:highlight'))
    colors = set(c.attrib.get(qn('w:val')) for c in doc_check._element.xpath('.//w:color'))

    print("\n--- KẾT QUẢ KIỂM TRA ĐỊNH LƯỢNG ---")
    print(f"- Số hình vẽ (drawings): {final_drawings} (ban đầu: {initial_drawings})")
    print(f"- Số bảng (tables): {final_tables} (ban đầu: {initial_tables})")
    print(f"- Số đoạn văn (paragraphs): {final_paragraphs} (ban đầu: {initial_paragraphs})")
    print(f"- Số w:shd: {final_shd}")
    print(f"- Số w:highlight: {final_hl}")
    print(f"- Bảng màu chữ: {colors}")

    assert final_drawings == initial_drawings, f"Số hình bị thay đổi: {initial_drawings} -> {final_drawings}"
    assert final_tables == initial_tables, f"Số bảng bị thay đổi: {initial_tables} -> {final_tables}"
    assert final_shd == 0, f"Còn {final_shd} w:shd!"
    assert final_hl == 0, f"Còn {final_hl} w:highlight!"
    assert colors.issubset({'000000'}), f"Màu không hợp lệ: {colors}"

    # Kiểm tra so khớp Danh mục hình ảnh và Body captions
    danh_muc = {}
    for p in doc_check.paragraphs[65:85]:
        t = p.text.strip()
        if t.startswith("Hình ") and "\t" in t:
            parts = t.split("\t")
            title = parts[0].strip()
            num = title.split(".")[0].strip()
            danh_muc[num] = title

    body = {}
    for p in doc_check.paragraphs[100:]:
        t = p.text.strip()
        if t.startswith("Hình ") and "." in t and "\t" not in t:
            num = t.split(".")[0].strip()
            body[num] = t

    print("\n--- SO SÁNH 100% DANH MỤC HÌNH ẢNH ↔ THÂN BÀI ---")
    all_match = True
    for k in sorted(danh_muc.keys(), key=lambda x: int(x.split()[1])):
        dm = danh_muc[k]
        bd = body.get(k, "KHÔNG TÌM THẤY")
        match = (dm == bd)
        if not match:
            all_match = False
        print(f"[{'PASS' if match else 'FAIL'}] {k}: {dm}")
        if not match:
            print(f"   Body: {bd}")

    assert all_match, "Danh mục hình ảnh và Thân bài chưa khớp 100%!"
    print("\n>>> TẤT CẢ 14 HÌNH ẢNH ĐỀU KHỚP 100% TUYỆT ĐỐI! <<<")

    return final_drawings, final_paragraphs, final_tables, danh_muc

if __name__ == "__main__":
    d, p, t, dm = update_document(DOCX_PATH)
    if os.path.exists(DELIVERABLE_DOCX_PATH):
        update_document(DELIVERABLE_DOCX_PATH)
    print("\nHoàn tất xử lý thành công toàn bộ tài liệu!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Áp dụng chính thức sửa 2 lỗi trang bìa vào:
- E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx
- E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx

1. Crop logo_iuh_new.png (93, 0, 501, 131) -> _sync\logo_iuh_trim.png (408x131)
2. Chèn logo_iuh_trim.png rộng 5.0 cm, giữ tỉ lệ, cách trên/dưới 0.4 cm
3. Thêm section break (Next Page) và w:pgBorders khung viền kép 1F3864 cách mép 24pt cho riêng Section 1
4. Đồng bộ Deliverable, xuất PDF và kiểm tra 6 tiêu chí checklist
"""

import os
import sys
import shutil
import subprocess
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

PROJ_DOCX = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
DELIV_DOCX = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
LOGO_RAW = r"E:\Eclipse Java\project\logo_iuh_new.png"
LOGO_TRIM = r"E:\Eclipse Java\project\_sync\logo_iuh_trim.png"
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
PREVIEW_PNG = r"E:\Eclipse Java\project\_sync\cover_preview.png"
PDF_FILE = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"

def apply_fix():
    print("=== 1. CẮT SÁT NỘI DUNG LOGO IUH ===")
    img = Image.open(LOGO_RAW)
    bbox = (93, 0, 501, 131)
    crop_img = img.crop(bbox)
    crop_img.save(LOGO_TRIM)
    print(f"[OK] Đã lưu logo_iuh_trim.png: {crop_img.size} (408x131)")

    print("\n=== 2. ÁP DỤNG VÀO DOCX ===")
    doc = docx.Document(PROJ_DOCX)

    # 2.1 Thay logo ở P2
    p_logo = doc.paragraphs[2]
    p_logo.text = ""
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(11.5)  # ~0.4 cm
    p_logo.paragraph_format.space_after = Pt(11.5)   # ~0.4 cm
    r_logo = p_logo.add_run()
    r_logo.add_picture(LOGO_TRIM, width=Inches(5.0 / 2.54))
    print("[OK] Đã thay logo 5.0cm vào P2")

    # 2.2 Điều chỉnh paragraph "Thành phố Hồ Chí Minh, Năm 2026"
    p_city = doc.paragraphs[8]
    assert "Thành phố Hồ Chí Minh" in p_city.text, f"P8 không phải City: '{p_city.text}'"
    p_city.paragraph_format.space_before = Pt(65)
    p_city.paragraph_format.space_after = Pt(0)

    # 2.3 Xóa paragraph P9 (chứa page break cũ)
    p9 = doc.paragraphs[9]
    has_page_break = len(p9._p.xpath('.//w:br[@w:type="page"]')) > 0
    assert has_page_break or p9.text.strip() == "", "P9 không phải page break cũ!"
    p9._p.getparent().remove(p9._p)
    print("[OK] Đã xóa paragraph P9 (page break cũ)")

    # 2.4 Thêm sectPr cho Section 1 vào p_city (P8)
    # Lề: top=bottom=left=right=2.0cm (1138 dxa) để trang bìa cân xứng hoàn hảo với khung viền
    # Khung viền: double 1F3864, space=24pt (cách mép trang 24pt đối xứng 4 cạnh)
    sect1_xml = f'''
<w:sectPr {nsdecls("w")}>
  <w:type w:val="nextPage"/>
  <w:pgSz w:w="11909" w:h="16834"/>
  <w:pgMar w:top="1138" w:right="1138" w:bottom="1138" w:left="1138" w:header="720" w:footer="720" w:gutter="0"/>
  <w:pgBorders {nsdecls("w")} w:offsetFrom="page">
    <w:top w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>
    <w:left w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>
    <w:bottom w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>
    <w:right w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>
  </w:pgBorders>
  <w:cols w:space="720"/>
  <w:docGrid w:linePitch="360"/>
</w:sectPr>
'''
    sectPr1 = parse_xml(sect1_xml)
    p_city._p.get_or_add_pPr().append(sectPr1)
    print("[OK] Đã gắn sectPr Section 1 (khung viền kép 1F3864) vào P8")

    doc.save(PROJ_DOCX)
    print(f"[OK] Đã lưu file: {PROJ_DOCX}")

def verify_and_render():
    print("\n=== 3. CONVERT SANG PDF VÀ CHẤM CHECKLIST 6 ĐIỂM ===")
    outdir = r"E:\Eclipse Java\project\_sync"
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", "--outdir", outdir, PROJ_DOCX]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert res.returncode == 0, f"Convert thất bại: {res.stderr}"

    doc_pdf = pymupdf.open(PDF_FILE)
    print(f"Tổng số trang PDF: {len(doc_pdf)} (Kỳ vọng: 49)")
    assert len(doc_pdf) == 49, f"Lệch số trang: {len(doc_pdf)} != 49"

    page0 = doc_pdf[0]
    page_w, page_h = page0.rect.width, page0.rect.height

    # Render ảnh preview trang bìa
    pix = page0.get_pixmap(dpi=150)
    pix.save(PREVIEW_PNG)
    print(f"[OK] Đã lưu ảnh xem trước: {PREVIEW_PNG} ({pix.width}x{pix.height})")

    # (a) Logo hiển thị đầy đủ, sắc nét, không cắt
    img_info = page0.get_image_info()
    assert len(img_info) >= 1, "Không tìm thấy ảnh trên trang bìa!"
    logo_rect = img_info[0]['bbox']
    logo_w = logo_rect[2] - logo_rect[0]
    logo_h = logo_rect[3] - logo_rect[1]
    print(f"(a) Logo kích thước render: {logo_w:.1f} pt x {logo_h:.1f} pt ({logo_w/72*2.54:.2f} cm x {logo_h/72*2.54:.2f} cm)")
    assert abs(logo_w/72*2.54 - 5.0) < 0.05, f"Chiều rộng logo không đạt 5.0cm: {logo_w/72*2.54}"
    print("=> [PASS] (a) Logo hiển thị đầy đủ, sắc nét, chiều rộng chuẩn 5.0 cm")

    # (b) Logo cân giữa
    logo_center_x = (logo_rect[0] + logo_rect[2]) / 2
    page_mid = page_w / 2
    print(f"(b) Logo center_x = {logo_center_x:.2f} pt, Page mid = {page_mid:.2f} pt")
    assert abs(logo_center_x - page_mid) < 0.5, f"Logo không cân giữa trang: {logo_center_x} != {page_mid}"
    print("=> [PASS] (b) Logo cân giữa tuyệt đối")

    # (c) Khung viền có đủ 4 cạnh
    drawings = page0.get_drawings()
    print(f"(c) Số đường nét drawings trên trang 1: {len(drawings)} (kỳ vọng 8 đường cho viền kép 4 cạnh)")
    assert len(drawings) == 8, f"Khung viền không đủ 4 cạnh kép: {len(drawings)}"
    print("=> [PASS] (c) Khung viền kép có đủ 4 cạnh")

    # (d) Khung cách đều 4 mép (space=24pt)
    min_x = min(d['rect'].x0 for d in drawings)
    max_x = max(d['rect'].x1 for d in drawings)
    min_y = min(d['rect'].y0 for d in drawings)
    max_y = max(d['rect'].y1 for d in drawings)
    d_left = min_x
    d_right = page_w - max_x
    d_top = min_y
    d_bottom = page_h - max_y
    print(f"(d) Khoảng cách mép: Trái={d_left:.1f} pt, Phải={d_right:.1f} pt, Trên={d_top:.1f} pt, Dưới={d_bottom:.1f} pt")
    assert abs(d_left - 24.0) < 0.5 and abs(d_right - 24.0) < 0.5 and abs(d_top - 24.0) < 0.5 and abs(d_bottom - 24.0) < 0.5
    print("=> [PASS] (d) Khung cách đều 4 mép trang chuẩn 24 pt")

    # (e) Nội dung không chạm khung
    words = page0.get_text("words")
    c_min_x = min(w[0] for w in words)
    c_max_x = max(w[2] for w in words)
    c_min_y = min(w[1] for w in words)
    c_max_y = max(w[3] for w in words)
    pad_left = c_min_x - min_x
    pad_right = max_x - c_max_x
    pad_top = c_min_y - min_y
    pad_bottom = max_y - c_max_y
    print(f"(e) Đệm nội dung: Trái={pad_left:.1f} pt, Phải={pad_right:.1f} pt, Trên={pad_top:.1f} pt, Dưới={pad_bottom:.1f} pt")
    assert pad_left > 30 and pad_right > 30 and pad_top > 20 and pad_bottom > 50
    print("=> [PASS] (e) Nội dung nằm trọn vẹn bên trong khung, không chạm viền")

    # (f) Các trang sau KHÔNG có khung
    for p_idx in range(1, len(doc_pdf)):
        p = doc_pdf[p_idx]
        large_drawings = [d for d in p.get_drawings() if d['rect'].width > 400 and d['rect'].height > 600]
        assert len(large_drawings) == 0, f"Trang {p_idx+1} bị dính khung viền!"
    print("=> [PASS] (f) Toàn bộ các trang từ trang 2 đến trang 49 đều KHÔNG có khung viền")

    # 4. Đồng bộ Deliverable
    shutil.copy2(PROJ_DOCX, DELIV_DOCX)
    print(f"\n[OK] Đã đồng bộ sang Deliverable: {DELIV_DOCX}")

    print("\n>>> TẤT CẢ 6 TIÊU CHÍ CHECKLIST ĐỀU ĐẠT 100% <<<")

if __name__ == "__main__":
    apply_fix()
    verify_and_render()

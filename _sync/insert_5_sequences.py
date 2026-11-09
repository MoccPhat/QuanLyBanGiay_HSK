#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chèn 5 sơ đồ tuần tự mới vào Phần IV của BaoCao_QuanLyBanGiay_HSK.docx:
1. vp_seq_dangnhap.png -> IV.I Chức năng Đăng nhập (Hình 15)
2. vp_seq_sanpham.png  -> IV.III Quản lý sản phẩm (Hình 16)
3. vp_seq_khachhang.png -> IV.IV Quản lý khách hàng (Hình 17)
4. vp_seq_nhanvien.png -> IV.V Quản lý nhân sự (Hình 18)
5. vp_seq_thongke.png  -> IV.VI Thống kê doanh thu (Hình 19)

Yêu cầu kỹ thuật:
- Chiều rộng ảnh: 15.5 cm (vừa vặn lề 16cm, căn giữa)
- Caption: Hình N. Sơ đồ tuần tự nghiệp vụ <tên chức năng> (Visual Paradigm 18)
- Cập nhật Danh mục hình ảnh: thêm 5 dòng mới đúng số và tên, giữ thứ tự
- Cập nhật số lượng hình: 19 hình ảnh nghiệp vụ + 1 logo IUH = 20 drawings OpenXML
- Tự động lấy số trang thật từ PDF render
"""

import os
import sys
import shutil
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

DOCX_FILE = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
DELIV_FILE = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

IMAGES = [
    {
        "id": "dangnhap",
        "path": r"E:\Eclipse Java\project\_sync\vp_seq_dangnhap.png",
        "caption": "Hình 15. Sơ đồ tuần tự nghiệp vụ Đăng nhập (Visual Paradigm 18)",
        "anchor_text": "Bước 4 - Phân quyền giao diện:",
        "section": "IV.I"
    },
    {
        "id": "sanpham",
        "path": r"E:\Eclipse Java\project\_sync\vp_seq_sanpham.png",
        "caption": "Hình 16. Sơ đồ tuần tự nghiệp vụ Quản lý sản phẩm (Visual Paradigm 18)",
        "anchor_text": "Cơ chế xóa mềm an toàn:",
        "section": "IV.III"
    },
    {
        "id": "khachhang",
        "path": r"E:\Eclipse Java\project\_sync\vp_seq_khachhang.png",
        "caption": "Hình 17. Sơ đồ tuần tự nghiệp vụ Quản lý khách hàng (Visual Paradigm 18)",
        "anchor_text": "Thao tác dữ liệu khách hàng:",
        "section": "IV.IV"
    },
    {
        "id": "nhanvien",
        "path": r"E:\Eclipse Java\project\_sync\vp_seq_nhanvien.png",
        "caption": "Hình 18. Sơ đồ tuần tự nghiệp vụ Quản lý nhân sự (Visual Paradigm 18)",
        "anchor_text": "Bảo vệ tài khoản Quản trị trưởng:",
        "section": "IV.V"
    },
    {
        "id": "thongke",
        "path": r"E:\Eclipse Java\project\_sync\vp_seq_thongke.png",
        "caption": "Hình 19. Sơ đồ tuần tự nghiệp vụ Thống kê doanh thu (Visual Paradigm 18)",
        "anchor_text": "Tra cứu giao dịch:",
        "section": "IV.VI"
    }
]

def insert_diagrams():
    doc = docx.Document(DOCX_FILE)
    print("--- 1. Kiểm tra số lượng drawings ban đầu ---")
    d_before = len(doc._body._element.xpath('.//w:drawing'))
    print(f"Số lượng drawings trước khi chèn: {d_before} (kỳ vọng 15)")

    # 1. Chèn từng hình vào sau đoạn mô tả luồng
    # Chúng ta duyệt từ dưới lên (ngược chiều) để không làm lệch index của các đoạn phía trước
    # Hoặc tìm theo anchor_text
    for item in reversed(IMAGES):
        anchor_p_idx = -1
        for idx, p in enumerate(doc.paragraphs):
            if item["anchor_text"] in p.text:
                anchor_p_idx = idx
                break
        
        assert anchor_p_idx != -1, f"Không tìm thấy đoạn neo cho {item['id']}: '{item['anchor_text']}'"
        print(f"Đoạn neo cho {item['id']} nằm tại P{anchor_p_idx}: {doc.paragraphs[anchor_p_idx].text[:60]}")

        # Chèn trước paragraph tiếp theo (anchor_p_idx + 1)
        next_p = doc.paragraphs[anchor_p_idx + 1]

        # 1. Paragraph chứa hình ảnh
        p_img = next_p.insert_paragraph_before()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r_img = p_img.add_run()
        r_img.add_picture(item["path"], width=Inches(15.5 / 2.54))

        # 2. Paragraph chứa caption
        p_cap = next_p.insert_paragraph_before()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run(item["caption"])
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.font.bold = False
        r_cap.font.color.rgb = RGBColor(0, 0, 0)
        print(f"-> Đã chèn {item['caption']}")

    # 2. Cập nhật Danh mục hình ảnh ở đầu báo cáo
    # Tìm đoạn Hình 14 và ghi chú kỹ thuật
    h14_idx = -1
    tech_note_idx = -1
    for idx, p in enumerate(doc.paragraphs[:130]):
        if p.text.strip().startswith("Hình 14.") and "\t" in p.text:
            h14_idx = idx
        if "Ghi chú kỹ thuật:" in p.text and "phần tử hình ảnh" in p.text:
            tech_note_idx = idx

    print(f"Hình 14 trong danh mục tại P{h14_idx}, Ghi chú kỹ thuật tại P{tech_note_idx}")
    assert h14_idx != -1 and tech_note_idx != -1, "Không tìm thấy danh mục hình ảnh!"

    # Thêm 5 dòng mới ngay trước tech_note
    tech_p = doc.paragraphs[tech_note_idx]
    for item in IMAGES:
        p_list = tech_p.insert_paragraph_before()
        p_list.paragraph_format.space_before = Pt(1)
        p_list.paragraph_format.space_after = Pt(2)
        p_list.paragraph_format.line_spacing = 1.15
        
        # Thêm text với tab phân cách và số trang tạm thời (sẽ cập nhật sau khi convert PDF)
        r_txt = p_list.add_run(f"{item['caption']}\t00")
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10.5)
        r_txt.font.italic = True
        r_txt.font.color.rgb = RGBColor(0, 0, 0)

    # Cập nhật ghi chú kỹ thuật
    tech_p.text = "*(Ghi chú kỹ thuật: Danh mục bao gồm 19 hình ảnh nghiệp vụ đánh số từ Hình 1 đến Hình 19 và 01 Logo IUH tại trang bìa, tổng cộng 20 phần tử hình ảnh OpenXML).*"
    for r in tech_p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.italic = True
        r.font.color.rgb = RGBColor(0, 0, 0)

    # Lưu lại
    doc.save(DOCX_FILE)
    print(f"[OK] Đã lưu file sau khi chèn 5 hình: {DOCX_FILE}")

    d_after = len(doc._body._element.xpath('.//w:drawing'))
    print(f"Số lượng drawings sau khi chèn: {d_after} (kỳ vọng 20)")
    assert d_after == 20, f"Số drawing không đúng: {d_after} != 20"

def update_page_numbers_from_pdf():
    print("\n--- 2. Convert sang PDF để trích xuất số trang thực tế ---")
    outdir = r"E:\Eclipse Java\project\_sync"
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", "--outdir", outdir, DOCX_FILE]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert res.returncode == 0, f"Convert thất bại: {res.stderr}"

    pdf_file = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"
    doc_pdf = pymupdf.open(pdf_file)
    print(f"Tổng số trang PDF: {len(doc_pdf)}")

    # Trích xuất số trang của tất cả 19 hình
    figure_pages = {}
    for num in range(1, 20):
        prefix = f"Hình {num}."
        found_page = None
        for page_idx, page in enumerate(doc_pdf):
            # Bỏ qua các trang đầu chứa mục lục và danh mục (trang 1 đến 8)
            if page_idx < 8:
                continue
            text = page.get_text("text")
            if prefix in text:
                found_page = page_idx + 1  # 1-based page number
                break
        figure_pages[num] = found_page
        print(f"Hình {num}: trang {found_page}")

    # Cập nhật số trang vào lại docx
    doc = docx.Document(DOCX_FILE)
    for p in doc.paragraphs[:135]:
        text = p.text.strip()
        if text.startswith("Hình ") and "\t" in text:
            parts = text.split("\t")
            cap_part = parts[0].strip()
            # Lấy số hình
            num_str = cap_part.split(".")[0].replace("Hình", "").strip()
            if num_str.isdigit():
                num = int(num_str)
                real_page = figure_pages.get(num, parts[1].strip())
                new_text = f"{cap_part}\t{real_page}"
                p.text = new_text
                # Format lại run
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(0, 0, 0)

    doc.save(DOCX_FILE)
    print(f"[OK] Đã cập nhật số trang chuẩn vào danh mục hình trong docx")

    # Convert lại PDF lần cuối để chốt
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    print("[OK] Đã convert lại PDF chuẩn hóa")

    # Render 3 ảnh preview cho các trang có hình mới
    # Hình 15 (Đăng nhập), Hình 16 (Sản phẩm), Hình 19 (Thống kê)
    doc_pdf_final = pymupdf.open(pdf_file)
    p_dangnhap = figure_pages[15] - 1
    p_sanpham = figure_pages[16] - 1
    p_thongke = figure_pages[19] - 1

    preview_pages = [
        ("preview_seq_dangnhap.png", p_dangnhap, "IV.I Đăng nhập (Hình 15)"),
        ("preview_seq_sanpham.png", p_sanpham, "IV.III Sản phẩm (Hình 16)"),
        ("preview_seq_thongke.png", p_thongke, "IV.VI Thống kê (Hình 19)")
    ]

    for fname, p_num, label in preview_pages:
        pix = doc_pdf_final[p_num].get_pixmap(dpi=150)
        out_p = os.path.join(outdir, fname)
        pix.save(out_p)
        print(f"[OK] Đã lưu preview {label} -> {out_p} ({pix.width}x{pix.height})")

    # Đồng bộ sang Deliverable
    shutil.copy2(DOCX_FILE, DELIV_FILE)
    print(f"[OK] Đã đồng bộ sang Deliverable: {DELIV_FILE}")

if __name__ == "__main__":
    insert_diagrams()
    update_page_numbers_from_pdf()

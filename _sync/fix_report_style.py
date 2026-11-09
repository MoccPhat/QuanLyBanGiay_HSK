"""
Script chuẩn hóa định dạng báo cáo Word BaoCao_QuanLyBanGiay_HSK.docx
Thực hiện các yêu cầu V3:
1. Đưa toàn bộ chữ về màu đen mặc định (w:val="000000" và loại bỏ themeColor/themeShade/themeTint).
2. Bỏ toàn bộ tô nền (w:shd) và highlight (w:highlight) trong mọi paragraph, run, table cell.
3. Heading 1, 2, 3: in đậm (w:b) và tăng cỡ chữ thêm 1-2pt (Heading 1: 16pt, Heading 2: 15pt, Heading 3: 14pt).
4. Giữ nguyên 100% nội dung chữ, cấu trúc đoạn văn, bảng biểu, ảnh.
"""

import os
import sys
import shutil
from datetime import datetime
import docx
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

TARGET_FILES = [
    r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx",
    r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable\BaoCao_QuanLyBanGiay_HSK.docx"
]

BACKUP_DIR = r"E:\Eclipse Java\_project_archive_2026-11-07"

HEADING_CONFIG = {
    'Heading 1': {'size': Pt(16), 'bold': True},
    'Heading 2': {'size': Pt(15), 'bold': True},
    'Heading 3': {'size': Pt(14), 'bold': True}
}

def clean_and_style_docx(file_path):
    print(f"\n==========================================")
    print(f"Đang xử lý: {file_path}")
    print(f"==========================================")

    if not os.path.exists(file_path):
        print(f"[CẢNH BÁO] Không tìm thấy file: {file_path}")
        return False

    doc = docx.Document(file_path)
    p_orig_count = len(doc.paragraphs)
    t_orig_count = len(doc.tables)
    d_orig_count = len(doc._element.xpath('.//w:drawing'))

    # 1. Cập nhật định nghĩa style cho Heading 1, 2, 3
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

    # 2. Cập nhật formatting cho các đoạn văn Heading 1, 2, 3
    heading_counts = {k: 0 for k in HEADING_CONFIG}
    for p in doc.paragraphs:
        style_name = p.style.name if p.style else ''
        if style_name in HEADING_CONFIG:
            heading_counts[style_name] += 1
            cfg = HEADING_CONFIG[style_name]
            for r in p.runs:
                r.font.size = cfg['size']
                r.font.bold = cfg['bold']
                r.font.color.rgb = RGBColor(0, 0, 0)

    # 3. Loại bỏ toàn bộ shading (w:shd) trong document.xml
    shd_elements = doc._element.xpath('.//w:shd')
    shd_count = len(shd_elements)
    for shd in shd_elements:
        parent = shd.getparent()
        if parent is not None:
            parent.remove(shd)

    # 4. Loại bỏ toàn bộ highlight (w:highlight) trong document.xml
    hl_elements = doc._element.xpath('.//w:highlight')
    hl_count = len(hl_elements)
    for hl in hl_elements:
        parent = hl.getparent()
        if parent is not None:
            parent.remove(hl)

    # 5. Đưa toàn bộ w:color về 000000 và xóa theme attributes
    color_elements = doc._element.xpath('.//w:color')
    color_count = len(color_elements)
    for color in color_elements:
        color.set(qn('w:val'), '000000')
        for attr in ['themeColor', 'themeShade', 'themeTint']:
            q_name = qn(f'w:{attr}')
            if q_name in color.attrib:
                del color.attrib[q_name]

    # Lưu file
    doc.save(file_path)
    print(f"Đã lưu thành công file: {file_path}")

    # Kiểm tra nghiệm thu (Verification)
    doc_check = docx.Document(file_path)
    p_new_count = len(doc_check.paragraphs)
    t_new_count = len(doc_check.tables)
    d_new_count = len(doc_check._element.xpath('.//w:drawing'))
    rem_shd = len(doc_check._element.xpath('.//w:shd'))
    rem_hl = len(doc_check._element.xpath('.//w:highlight'))
    colors = set(c.attrib.get(qn('w:val')) for c in doc_check._element.xpath('.//w:color'))

    print("\n--- KẾT QUẢ NGHIỆM THU ---")
    print(f"- Số đoạn văn: {p_new_count} (Gốc: {p_orig_count}) -> {'KHỚP 100%' if p_new_count == p_orig_count else 'LỖI'}")
    print(f"- Số bảng biểu: {t_new_count} (Gốc: {t_orig_count}) -> {'KHỚP 100%' if t_new_count == t_orig_count else 'LỖI'}")
    print(f"- Số hình ảnh/drawing: {d_new_count} (Gốc: {d_orig_count}) -> {'KHỚP 100%' if d_new_count == d_orig_count else 'LỖI'}")
    print(f"- Số w:shd đã xóa: {shd_count}, còn lại: {rem_shd}")
    print(f"- Số w:highlight đã xóa: {hl_count}, còn lại: {rem_hl}")
    print(f"- Số w:color đã chuẩn hóa: {color_count}")
    print(f"- Danh sách mã màu còn lại trong file: {colors}")
    print(f"- Thống kê Heading: {heading_counts}")

    assert p_new_count == p_orig_count, "Số đoạn văn bị thay đổi!"
    assert t_new_count == t_orig_count, "Số bảng bị thay đổi!"
    assert d_new_count == d_orig_count, "Số hình ảnh bị thay đổi!"
    assert rem_shd == 0, f"Vẫn còn {rem_shd} w:shd!"
    assert rem_hl == 0, f"Vẫn còn {rem_hl} w:highlight!"
    assert colors.issubset({'000000'}), f"Có màu khác ngoài 000000: {colors}"

    print(f"==> NGHIỆM THU THÀNH CÔNG: {os.path.basename(file_path)}\n")
    return True

def main():
    print("=== BẮT ĐẦU QUY TRÌNH CHUẨN HÓA V3 CHO BÁO CÁO WORD ===")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Tạo backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for target in TARGET_FILES:
        if os.path.exists(target):
            base = os.path.splitext(os.path.basename(target))[0]
            backup_path = os.path.join(BACKUP_DIR, f"{base}_backup_{timestamp}.docx")
            shutil.copyfile(target, backup_path)
            print(f"Đã sao lưu an toàn:\n  Từ: {target}\n  Đến: {backup_path}")

    # Thực hiện sửa định dạng
    for target in TARGET_FILES:
        clean_and_style_docx(target)

    print("=== HOÀN TẤT TOÀN BỘ NHIỆM VỤ V3 ===")

if __name__ == "__main__":
    main()

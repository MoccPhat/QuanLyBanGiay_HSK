import docx
import pymupdf
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

DOCX_FILE = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
PDF_FILE = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"

print("=== VERIFYING DOCX STRUCTURE ===")
doc = docx.Document(DOCX_FILE)

# 1. Table count
tbl_count = len(doc.tables)
print(f"Total tables: {tbl_count} (expected 22: reduced from 24 by Callout + Bảng 19)")
assert tbl_count == 22, f"Table count mismatch: {tbl_count} != 22"

# 2. Drawing count
draw_count = len(doc._body._element.xpath('.//w:drawing'))
print(f"Total drawings: {draw_count} (must remain 20/20)")
assert draw_count == 20, f"Drawing count mismatch: {draw_count} != 20"

# 3. Check callout box is removed from tables
has_callout = any("CHUỖI HÀNH ĐỘNG CỐT LÕI" in t.cell(0, 0).text.upper() for t in doc.tables)
print(f"Callout box in tables: {has_callout} (must be False)")
assert not has_callout, "Callout box still in tables!"

# 4. Check Bảng 19 is removed from tables
has_tbl19 = any("BẢNG 19" in t.cell(0, 0).text.upper() or "VERIFYALLSCENARIOS" in t.cell(0, 0).text.upper() for t in doc.tables)
print(f"Bảng 19 in tables: {has_tbl19} (must be False)")
assert not has_tbl19, "Bảng 19 still in tables!"

# 5. Check Section VI and VII in docx paragraphs
has_sec_vi = any("PHẦN VI: KẾT QUẢ KIỂM THỬ" in p.text.upper() for p in doc.paragraphs)
has_sec_vii = any("PHẦN VII: TÀI LIỆU THAM KHẢO" in p.text.upper() for p in doc.paragraphs)
print(f"PHẦN VI in paragraphs: {has_sec_vi} (must be False)")
print(f"PHẦN VII in paragraphs: {has_sec_vii} (must be False)")
assert not has_sec_vi, "PHẦN VI still in paragraphs!"
assert not has_sec_vii, "PHẦN VII still in paragraphs!"

# 6. Check StepUp in GUI section
gui_paras = [p.text for p in doc.paragraphs if "PHẦN IV" in p.text or ("Hình 5." in p.text) or ("Hình 6." in p.text)]
has_stepup_gui = any("StepUp" in text for text in gui_paras)
print(f"StepUp in GUI titles/captions: {has_stepup_gui} (must be False)")
assert not has_stepup_gui, "StepUp still in GUI section titles/captions!"

print("\n=== VERIFYING RENDERED PDF ===")
doc_pdf = pymupdf.open(PDF_FILE)
print(f"Total PDF pages: {len(doc_pdf)} (reduced from 49 to 42)")

# Verify last page text
last_page_text = doc_pdf[-1].get_text("text")
print("Last page preview text:")
for line in last_page_text.strip().split("\n")[-6:]:
    print("  ", line)

assert "PHẦN VI" not in last_page_text, "Phần VI found on last page!"
assert "PHẦN VII" not in last_page_text, "Phần VII found on last page!"
assert "Lời kết" in last_page_text, "Lời kết not on last page!"

print("\n=== ALL 6 CHECKS VERIFIED 100% SUCCEEDED! ===")

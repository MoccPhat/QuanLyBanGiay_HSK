import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import subprocess
import pymupdf
import shutil
import datetime
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
BACKUP_DIR = r"E:\Eclipse Java\project\_sync\backup_docx"
NEW_IMG_PATH = r"E:\Eclipse Java\project\_sync\vp_usecase_diagram.png"
OUT_DIR = r"E:\Eclipse Java\project\_sync"

assert os.path.exists(DOCX_PATH), "Docx file not found!"
assert os.path.exists(NEW_IMG_PATH), "New image file not found!"

# 1. Backup docx
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"BaoCao_QuanLyBanGiay_HSK_backup_{now_str}.docx")
shutil.copy2(DOCX_PATH, backup_file)
print(f"1. Backup created: {backup_file} ({os.path.getsize(backup_file):,} bytes)")

doc = docx.Document(DOCX_PATH)

# Check drawings before
drawings_before = 0
for p in doc.paragraphs:
    drawings_before += len(p._p.xpath('.//w:drawing'))
print(f"Drawings in paragraphs before: {drawings_before}")

# 2. Update StepUp Footwear POS (hit in P166)
p166 = doc.paragraphs[166]
print(f"P166 before: {p166.text[:80]}...")
assert "StepUp Footwear POS" in p166.text, "StepUp Footwear POS not found in P166!"
p166.text = p166.text.replace("Hệ thống StepUp Footwear POS", "Hệ thống Quản lý Bán hàng Giày dép")
p166.text = p166.text.replace("StepUp Footwear POS", "Hệ thống Quản lý Bán hàng Giày dép")
print(f"P166 after:  {p166.text[:80]}...")
for r in p166.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

# 3. Replace Image in P167 (Hình 1)
p167 = doc.paragraphs[167]
# Verify drawing exists in P167
assert len(p167._p.xpath('.//w:drawing')) > 0, "No drawing found in P167!"
# Clear existing runs in P167
for r in list(p167.runs):
    p167._p.remove(r._r)

# Add new run with new image
run167 = p167.add_run()
run167.add_picture(NEW_IMG_PATH, width=Cm(16))
p167.alignment = WD_ALIGN_PARAGRAPH.CENTER
p167.paragraph_format.space_before = Pt(6)
p167.paragraph_format.space_after = Pt(4)
print("3. Replaced image in P167 with vp_usecase_diagram.png (width=16cm, center)")

# 4. Update Caption in P168
p168 = doc.paragraphs[168]
new_caption = "Hình 1. Sơ đồ Use Case tổng thể hệ thống Quản lý bán giày thời trang (Visual Paradigm 18)"
print(f"P168 before: {p168.text}")
p168.text = new_caption
p168.alignment = WD_ALIGN_PARAGRAPH.CENTER
p168.paragraph_format.space_before = Pt(2)
p168.paragraph_format.space_after = Pt(8)
for r in p168.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.italic = True
    r.bold = False
print(f"P168 after:  {p168.text}")

# 5. Update Danh mục hình (P87)
p87 = doc.paragraphs[87]
print(f"P87 before: {p87.text}")
assert "Hình 1" in p87.text, "P87 does not mention Hình 1!"
# Check if page number exists after tab
parts = p87.text.split("\t")
page_str = parts[1] if len(parts) > 1 else "10"
p87.text = f"{new_caption}\t{page_str}"
for r in p87.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = True
print(f"P87 after:  {p87.text}")

# Check drawings after
drawings_after = 0
for p in doc.paragraphs:
    drawings_after += len(p._p.xpath('.//w:drawing'))
print(f"Drawings in paragraphs after: {drawings_after}")
assert drawings_before == drawings_after, f"Drawings mismatch: {drawings_before} vs {drawings_after}"

# Check StepUp Footwear POS hits across all paragraphs & tables
stepup_pos_hits = 0
for p in doc.paragraphs:
    if "StepUp Footwear POS" in p.text:
        stepup_pos_hits += 1
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            if "StepUp Footwear POS" in cell.text:
                stepup_pos_hits += 1
print(f"StepUp Footwear POS hits in document: {stepup_pos_hits}")
assert stepup_pos_hits == 0, f"Expected 0 hits, got {stepup_pos_hits}!"

# 6. Save docx
doc.save(DOCX_PATH)
print(f"4. Document saved to {DOCX_PATH} ({os.path.getsize(DOCX_PATH):,} bytes)")

# 7. Convert to PDF via LibreOffice headless
cmd = [r"C:\Program Files\LibreOffice\program\soffice.exe", "--headless", "--convert-to", "pdf", "--outdir", OUT_DIR, DOCX_PATH]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(f"5. LibreOffice convert code: {res.returncode}")

pdf_file = os.path.join(OUT_DIR, "BaoCao_QuanLyBanGiay_HSK.pdf")
doc_pdf = pymupdf.open(pdf_file)
total_pages = len(doc_pdf)
print(f"Total pages in PDF: {total_pages}")

# 8. Render 3 target pages: TOC, Hinh 1, Last page
# Find TOC page
toc_page_idx = None
hinh1_page_idx = None

for idx, page in enumerate(doc_pdf):
    txt = page.get_text("text")
    if "MỤC LỤC BÁO CÁO" in txt and toc_page_idx is None:
        toc_page_idx = idx
    if "Hình 1. Sơ đồ Use Case" in txt and idx > 6 and hinh1_page_idx is None:
        hinh1_page_idx = idx

last_page_idx = total_pages - 1

print(f"Target pages: TOC=Page {toc_page_idx+1}, Hinh 1=Page {hinh1_page_idx+1}, Last=Page {last_page_idx+1}")

mat = pymupdf.Matrix(2.0, 2.0)

# Render TOC
pix_toc = doc_pdf[toc_page_idx].get_pixmap(matrix=mat)
out_toc = os.path.join(OUT_DIR, "final_toc.png")
pix_toc.save(out_toc)
print(f"Rendered final_toc.png: {out_toc} ({os.path.getsize(out_toc):,} bytes, {pix_toc.width}x{pix_toc.height})")

# Render Hinh 1
pix_hinh1 = doc_pdf[hinh1_page_idx].get_pixmap(matrix=mat)
out_hinh1 = os.path.join(OUT_DIR, "final_hinh1.png")
pix_hinh1.save(out_hinh1)
print(f"Rendered final_hinh1.png: {out_hinh1} ({os.path.getsize(out_hinh1):,} bytes, {pix_hinh1.width}x{pix_hinh1.height})")

# Render Last page
pix_last = doc_pdf[last_page_idx].get_pixmap(matrix=mat)
out_last = os.path.join(OUT_DIR, "final_last.png")
pix_last.save(out_last)
print(f"Rendered final_last.png: {out_last} ({os.path.getsize(out_last):,} bytes, {pix_last.width}x{pix_last.height})")

print("=== ALL UPDATES & RENDERS COMPLETED SUCCESSFULLY ===")

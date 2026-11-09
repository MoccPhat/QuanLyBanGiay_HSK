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
FRAME_PNG = r"E:\Eclipse Java\project\_sync\cover_frame_a4.png"
OUT_DIR = r"E:\Eclipse Java\project\_sync"

# 1. Backup
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"BaoCao_QuanLyBanGiay_HSK_backup_{now_str}.docx")
shutil.copy2(DOCX_PATH, backup_file)
print(f"1. Backup created: {backup_file} ({os.path.getsize(backup_file):,} bytes)")

doc = docx.Document(DOCX_PATH)
s1 = doc.sections[0]

# 2. Update Header Frame image blob
with open(FRAME_PNG, "rb") as f:
    new_frame_bytes = f.read()

hdr = s1.header
hdr_p = hdr.paragraphs[0]
blips = hdr_p._p.xpath('.//a:blip')
assert len(blips) > 0, "No blip found in Section 1 header!"
rId = blips[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
rel = hdr.part.rels[rId]
rel.target_part._blob = new_frame_bytes
print(f"2. Updated Section 1 Header frame part ({rel.target_ref}): {len(new_frame_bytes):,} bytes")

# 3. Update Cover Page Bottom Date Line
# P8 is the bottom date line
p8 = doc.paragraphs[8]
print(f"Current P8 text: {repr(p8.text)}")
p8.text = "TP. Hồ Chí Minh, tháng 11 năm 2026"
p8.alignment = WD_ALIGN_PARAGRAPH.CENTER
p8.paragraph_format.space_before = Pt(28)
p8.paragraph_format.space_after = Pt(0)
for r in p8.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = True
    r.bold = False
print(f"3. Updated P8 text to: {repr(p8.text)}")

# Save docx
doc.save(DOCX_PATH)
print(f"4. Saved updated document to {DOCX_PATH}")

# 5. Convert to PDF with LibreOffice headless
cmd = [r"C:\Program Files\LibreOffice\program\soffice.exe", "--headless", "--convert-to", "pdf", "--outdir", OUT_DIR, DOCX_PATH]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print("5. LibreOffice convert return code:", res.returncode)

pdf_file = os.path.join(OUT_DIR, "BaoCao_QuanLyBanGiay_HSK.pdf")
doc_pdf = pymupdf.open(pdf_file)
print(f"Total pages in PDF: {len(doc_pdf)}")

# Render Page 1 preview -> cover_preview3.png
page1 = doc_pdf[0]
mat = pymupdf.Matrix(2.0, 2.0)
pix1 = page1.get_pixmap(matrix=mat)
out_png = os.path.join(OUT_DIR, "cover_preview3.png")
pix1.save(out_png)
print(f"6. Rendered cover preview: {out_png} ({os.path.getsize(out_png):,} bytes, {pix1.width}x{pix1.height})")

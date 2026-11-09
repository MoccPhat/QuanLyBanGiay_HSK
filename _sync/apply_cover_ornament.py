import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
import shutil
import datetime
import subprocess
import pymupdf
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
BACKUP_DIR = r"E:\Eclipse Java\project\_sync\backup_docx"
FRAME_PNG = r"E:\Eclipse Java\project\_sync\cover_frame_a4.png"
LOGO_PNG = r"E:\Eclipse Java\project\_sync\logo_iuh_trim.png"

# 1. Backup docx
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"BaoCao_QuanLyBanGiay_HSK_backup_{now_str}.docx")
shutil.copy2(DOCX_PATH, backup_file)
print(f"1. Backup created: {backup_file} ({os.path.getsize(backup_file):,} bytes)")

doc = docx.Document(DOCX_PATH)
s1 = doc.sections[0]
s2 = doc.sections[1] if len(doc.sections) > 1 else None

# 2. Remove old w:pgBorders from Section 1
pgBorders = s1._sectPr.xpath('.//w:pgBorders')
for b in pgBorders:
    b.getparent().remove(b)
print(f"2. Removed {len(pgBorders)} w:pgBorders from Section 1 (replaced with PNG frame)")

# 3. Insert frame into Section 1 header as background behind text
# Ensure s2 header is unlinked
if s2:
    s2.header.is_linked_to_previous = False

hdr = s1.header
hdr_p = hdr.paragraphs[0]
hdr_p.text = "" # clear

r_frame = hdr_p.add_run()
pic_frame = r_frame.add_picture(FRAME_PNG, width=Cm(21.0), height=Cm(29.7))

drawing = r_frame._r.xpath('.//w:drawing')[0]
inline = drawing.xpath('.//wp:inline')[0]

graphic = inline.xpath('.//a:graphic')[0]
docPr = inline.xpath('.//wp:docPr')[0]
cNvGraphicFramePr = inline.xpath('.//wp:cNvGraphicFramePr')[0]

anchor_xml = """
<wp:anchor xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
           xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
           distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="251658240"
           behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">
  <wp:simplePos x="0" y="0"/>
  <wp:positionH relativeFrom="page">
    <wp:posOffset>0</wp:posOffset>
  </wp:positionH>
  <wp:positionV relativeFrom="page">
    <wp:posOffset>0</wp:posOffset>
  </wp:positionV>
  <wp:extent cx="7560000" cy="10692000"/>
  <wp:effectExtent l="0" t="0" r="0" b="0"/>
  <wp:wrapNone/>
</wp:anchor>
"""
anchor = parse_xml(anchor_xml)
anchor.append(docPr)
anchor.append(cNvGraphicFramePr)
anchor.append(graphic)

drawing.remove(inline)
drawing.append(anchor)
print("3. Configured full A4 background frame in Section 1 Header (behindDoc=1, 21x29.7cm)")

# 4. Format Cover Page Paragraphs
# P0: TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP. HCM
p0 = doc.paragraphs[0]
p0.text = ""
p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
p0.paragraph_format.space_before = Pt(14)
p0.paragraph_format.space_after = Pt(2)
r0 = p0.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP. HCM")
r0.font.name = "Times New Roman"
r0.font.size = Pt(13)
r0.bold = True

# P1: Khoa Công nghệ Thông tin (with underline & centered bottom border)
p1 = doc.paragraphs[1]
p1.text = ""
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.paragraph_format.space_before = Pt(2)
p1.paragraph_format.space_after = Pt(12)
r1 = p1.add_run("Khoa Công nghệ Thông tin")
r1.font.name = "Times New Roman"
r1.font.size = Pt(13)
r1.bold = True
r1.underline = True

# Also add bottom border to paragraph
pPr1 = p1._p.get_or_add_pPr()
pBdr_xml = parse_xml(
    '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '  <w:bottom w:val="single" w:sz="8" w:space="3" w:color="000000"/>'
    '</w:pBdr>'
)
p1.paragraph_format.left_indent = Cm(5.75)
p1.paragraph_format.right_indent = Cm(5.75)
pPr1.append(pBdr_xml)

# P2: Logo IUH large (5.5 cm)
p2 = doc.paragraphs[2]
p2.text = ""
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_before = Pt(6)
p2.paragraph_format.space_after = Pt(12)
r2 = p2.add_run()
pic_logo = r2.add_picture(LOGO_PNG, width=Cm(5.5))
print("4. Logo IUH inserted at width = 5.5 cm (centered)")

# P3: BÁO CÁO MÔN HỌC
p3 = doc.paragraphs[3]
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p3.paragraph_format.space_before = Pt(6)
p3.paragraph_format.space_after = Pt(3)

# P4: LẬP TRÌNH HƯỚNG SỰ KIỆN VỚI CÔNG NGHỆ JAVA
p4 = doc.paragraphs[4]
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p4.paragraph_format.space_before = Pt(3)
p4.paragraph_format.space_after = Pt(12)

# P5: ĐỀ TÀI SỐ 3:
p5 = doc.paragraphs[5]
p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
p5.paragraph_format.space_before = Pt(6)
p5.paragraph_format.space_after = Pt(3)

# P6: HỆ THỐNG QUẢN LÝ BÁN HÀNG TẠI CỬA HÀNG GIÀY DÉP THỜI TRANG
p6 = doc.paragraphs[6]
p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
p6.paragraph_format.space_before = Pt(3)
p6.paragraph_format.space_after = Pt(16)

# P8: TP. Hồ Chí Minh, ngày ... tháng ... năm 2026
p8 = doc.paragraphs[8]
p8.text = "TP. Hồ Chí Minh, ngày ... tháng ... năm 2026"
p8.alignment = WD_ALIGN_PARAGRAPH.CENTER
p8.paragraph_format.space_before = Pt(28)
p8.paragraph_format.space_after = Pt(0)
for r in p8.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = True
    r.bold = False

# Save docx
doc.save(DOCX_PATH)
print(f"5. Saved updated document to {DOCX_PATH}")

# 6. Convert to PDF with LibreOffice headless
outdir = r"E:\Eclipse Java\project\_sync"
cmd = [r"C:\Program Files\LibreOffice\program\soffice.exe", "--headless", "--convert-to", "pdf", "--outdir", outdir, DOCX_PATH]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print("6. LibreOffice convert return code:", res.returncode)

pdf_file = os.path.join(outdir, "BaoCao_QuanLyBanGiay_HSK.pdf")
doc_pdf = pymupdf.open(pdf_file)
print(f"Total pages in PDF: {len(doc_pdf)}")

# Render Page 1 preview
page1 = doc_pdf[0]
mat = pymupdf.Matrix(2.0, 2.0)
pix1 = page1.get_pixmap(matrix=mat)
out_png1 = os.path.join(outdir, "cover_preview2.png")
pix1.save(out_png1)
print(f"Rendered cover preview: {out_png1} ({os.path.getsize(out_png1):,} bytes, {pix1.width}x{pix1.height})")

# Render Page 2 preview
page2 = doc_pdf[1]
pix2 = page2.get_pixmap(matrix=mat)
out_png2 = os.path.join(outdir, "page2_preview.png")
pix2.save(out_png2)
print(f"Rendered page 2 preview: {out_png2} ({os.path.getsize(out_png2):,} bytes, {pix2.width}x{pix2.height})")

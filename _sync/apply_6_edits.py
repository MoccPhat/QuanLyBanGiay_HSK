import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"

print(f"Loading {DOCX_PATH}...")
doc = docx.Document(DOCX_PATH)

init_paras = len(doc.paragraphs)
init_tables = len(doc.tables)
init_drawings = len(doc._body._element.xpath('.//w:drawing'))
print(f"Initial state: {init_paras} paragraphs, {init_tables} tables, {init_drawings} drawings")

# ==============================================================================
# EDIT 1 & EDIT 6: MỤC LỤC FONT WEIGHT, INDENTATION & XÓA MỤC VI, VII KHỎI MỤC LỤC
# ==============================================================================
print("\n=== EXECUTING EDIT 1 & TOC PART OF EDIT 6 ===")

# Identify TOC range: starts after P21 ("MỤC LỤC BÁO CÁO") until before P85 ("LỜI MỞ ĐẦU")
# First, find paragraphs belonging to Phần VI and VII in TOC to delete them
toc_remove_keywords = [
    "PHẦN VI",
    "I. Giới thiệu bộ kiểm thử",
    "II. Ma trận kết quả kiểm thử",
    "III. Đánh giá độ tin cậy",
    "PHẦN VII: TÀI LIỆU THAM KHẢO",
]

# We will scan paragraphs between "MỤC LỤC BÁO CÁO" and "LỜI MỞ ĐẦU"
toc_start = None
toc_end = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "MỤC LỤC BÁO CÁO" and toc_start is None:
        toc_start = i + 1 # First entry
    elif p.text.strip() == "LỜI MỞ ĐẦU" and toc_start is not None and toc_end is None:
        toc_end = i # End before LỜI MỞ ĐẦU
        break

print(f"TOC detected from paragraph {toc_start} to {toc_end}")

# Step A: Delete Phần VI and VII from TOC
removed_toc_count = 0
for i in range(toc_end - 1, toc_start - 1, -1):
    p = doc.paragraphs[i]
    if any(k.upper() in p.text.upper() for k in toc_remove_keywords):
        print(f"  Removing from TOC: P{i} -> {repr(p.text)}")
        p._p.getparent().remove(p._p)
        removed_toc_count += 1

print(f"Removed {removed_toc_count} TOC entries for Phần VI and VII")

# Re-detect TOC end after deletion
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "LỜI MỞ ĐẦU":
        toc_end = i
        break

print(f"New TOC range: {toc_start} to {toc_end} ({toc_end - toc_start} entries)")

def set_run_bold(r, bold=True):
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        if bold:
            rPr = OxmlElement('w:rPr')
            r.insert(0, rPr)
        else:
            return
    b_elems = rPr.findall(qn('w:b'))
    bCs_elems = rPr.findall(qn('w:bCs'))
    if bold:
        if not b_elems:
            rPr.append(OxmlElement('w:b'))
        if not bCs_elems:
            rPr.append(OxmlElement('w:bCs'))
    else:
        for el in b_elems:
            rPr.remove(el)
        for el in bCs_elems:
            rPr.remove(el)

# Format font weight & indentation
for i in range(toc_start, toc_end):
    p = doc.paragraphs[i]
    text = p.text.strip()
    if not text:
        continue
    
    # Determine level
    # Level 1: Starts with PHẦN, or major unnumbered sections
    is_level_1 = (
        text.startswith("PHẦN ")
        or text.startswith("DANH SÁCH THÀNH VIÊN")
        or text.startswith("LỜI CẢM ƠN")
        or text.startswith("NHẬN XÉT CỦA GIẢNG VIÊN")
        or text.startswith("MỤC LỤC BÁO CÁO")
        or text.startswith("LỜI MỞ ĐẦU")
        or text.startswith("DANH MỤC HÌNH ẢNH")
    )
    
    # Level 2: Roman numerals: I. II. III. IV. V. VI. VII. VIII. IX. X.
    is_level_2 = bool(re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s", text))
    
    # Level 3: Arabic numbers: 1. 2. 3. 4. ...
    is_level_3 = bool(re.match(r"^\d+\.\s", text))
    
    if is_level_1:
        # Bold, indent 0
        p.paragraph_format.left_indent = Cm(0)
        for r in p._p.xpath('.//w:r'):
            set_run_bold(r, True)
    elif is_level_2:
        # Bold, indent 0.5 cm
        p.paragraph_format.left_indent = Cm(0.5)
        for r in p._p.xpath('.//w:r'):
            set_run_bold(r, True)
    elif is_level_3:
        # Normal (not bold), indent 1.0 cm
        p.paragraph_format.left_indent = Cm(1.0)
        for r in p._p.xpath('.//w:r'):
            set_run_bold(r, False)
    else:
        # Fallback Level 2
        p.paragraph_format.left_indent = Cm(0.5)
        for r in p._p.xpath('.//w:r'):
            set_run_bold(r, True)

print("TOC font weight and indentation updated successfully.")


# ==============================================================================
# EDIT 2: KHỐI CHỮ KÝ GVHD THẲNG TRỤC, CĂN ĐỀU, KHOẢNG CÁCH DÒNG ĐỀU
# ==============================================================================
print("\n=== EXECUTING EDIT 2: KHỐI CHỮ KÝ GVHD ===")

# Find the signature paragraph on GVHD page
sig_p = None
for i, p in enumerate(doc.paragraphs[:35]):
    if "Thành phố Hồ Chí Minh, ngày" in p.text and "Trần Thị Anh Thi" in p.text:
        sig_p = p
        sig_idx = i
        break

assert sig_p is not None, "Could not find GVHD signature paragraph"
print(f"Found signature paragraph at P{sig_idx}: {repr(sig_p.text)}")

# Clear the old paragraph text and format it cleanly
# We will split into structured lines with exact formatting and center alignment on the right half (left_indent = 8.5 cm)
# To ensure perfect straight axis ("thẳng trục"), uniform spacing, and balanced left/right margins:
# Line 1: Thành phố Hồ Chí Minh, ngày ...... tháng ...... năm 2026 (Italic)
# Line 2: Chữ ký của Giảng viên hướng dẫn (Bold)
# Line 3: (Ký và ghi rõ họ tên) (Italic, 10pt)
# [Space for signature]
# Line 4: ThS. Trần Thị Anh Thi (Bold)

sig_p.text = "" # clear existing runs
sig_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_p.paragraph_format.left_indent = Cm(8.5)
sig_p.paragraph_format.space_before = Pt(18)
sig_p.paragraph_format.space_after = Pt(2)
sig_p.paragraph_format.line_spacing = 1.15

r1 = sig_p.add_run("Thành phố Hồ Chí Minh, ngày ...... tháng ...... năm 2026\n")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
r1.italic = True

r2 = sig_p.add_run("Chữ ký của Giảng viên hướng dẫn\n")
r2.font.name = "Times New Roman"
r2.font.size = Pt(12)
r2.bold = True

r3 = sig_p.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
r3.font.name = "Times New Roman"
r3.font.size = Pt(10)
r3.italic = True

r4 = sig_p.add_run("ThS. Trần Thị Anh Thi")
r4.font.name = "Times New Roman"
r4.font.size = Pt(13)
r4.bold = True

print("GVHD signature block redesigned with straight vertical axis and balanced margins.")


# ==============================================================================
# EDIT 3: BỎ HỘP CALLOUT "CHUỖI HÀNH ĐỘNG CỐT LÕI TẠI QUẦY"
# ==============================================================================
print("\n=== EXECUTING EDIT 3: BỎ HỘP CALLOUT CHUỖI HÀNH ĐỘNG CỐT LÕI ===")

# Find Table 3 (or the table containing CHUỖI HÀNH ĐỘNG CỐT LÕI TẠI QUẦY)
target_tbl = None
for t in doc.tables:
    if "CHUỖI HÀNH ĐỘNG CỐT LÕI" in t.cell(0, 0).text.upper():
        target_tbl = t
        break

assert target_tbl is not None, "Could not find callout table"

tbl_elem = target_tbl._tbl
parent = tbl_elem.getparent()
tbl_idx_in_parent = parent.index(tbl_elem)

# Create a clean replacement paragraph
rep_p_elem = OxmlElement('w:p')
rep_p = docx.text.paragraph.Paragraph(rep_p_elem, doc)
rep_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
rep_p.paragraph_format.space_before = Pt(4)
rep_p.paragraph_format.space_after = Pt(6)
rep_p.paragraph_format.line_spacing = 1.15

run_lead = rep_p.add_run("Quy trình 6 bước tại quầy được mô tả trực quan trong ")
run_lead.font.name = "Times New Roman"
run_lead.font.size = Pt(12)

run_fig = rep_p.add_run("Hình 7 – Sơ đồ tuần tự nghiệp vụ thanh toán POS")
run_fig.font.name = "Times New Roman"
run_fig.font.size = Pt(12)
run_fig.bold = True

run_tail = rep_p.add_run(", thể hiện đầy đủ luồng tương tác thời gian thực giữa nhân viên thu ngân, giao diện người dùng, tầng DAO xử lý giao dịch và cơ sở dữ liệu Microsoft SQL Server.")
run_tail.font.name = "Times New Roman"
run_tail.font.size = Pt(12)

# Insert replacement paragraph right before the table, then remove the table
parent.insert(tbl_idx_in_parent, rep_p_elem)
parent.remove(tbl_elem)

print("Callout table successfully removed and replaced with concise 2-3 line narrative.")


# ==============================================================================
# EDIT 4: BỎ CHỮ "STEPUP FOOTWEAR POS" KHỎI PHẦN GUI & CROP SCREENSHOTS
# ==============================================================================
print("\n=== EXECUTING EDIT 4: BỎ STEPUP FOOTWEAR POS KHỎI GUI & CROP SCREENSHOTS ===")

# Part A: Text cleanup in GUI section (Phần IV.I and IV.II)
gui_start = None
gui_end = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("PHẦN IV:"):
        gui_start = i
    elif p.text.strip().startswith("PHẦN V:") and gui_start is not None:
        gui_end = i
        break

print(f"Phần IV spans P{gui_start} to P{gui_end}")

stepup_replacements = [
    ("StepUp Footwear POS", "Hệ thống Quản lý Bán hàng Giày dép"),
    ("StepUp Footwear", "Hệ thống Quản lý Bán hàng Giày dép"),
    ("StepUp POS", "Hệ thống Quản lý Bán hàng Giày dép"),
    ("StepUp", "Hệ thống Quản lý Bán hàng Giày dép"),
]

text_replace_count = 0
for i in range(gui_start, gui_end):
    p = doc.paragraphs[i]
    for old_s, new_s in stepup_replacements:
        if old_s in p.text:
            print(f"  Replacing in P{i}: {old_s} -> {new_s}")
            p.text = p.text.replace(old_s, new_s)
            text_replace_count += 1

print(f"Replaced {text_replace_count} occurrences of StepUp in Phần IV text.")

# Part B: Crop screenshots
# 1. DangNhap screenshot (rId13 / image6.png)
rel13 = doc.part.rels['rId13']
img_dangnhap = Image.open(io.BytesIO(rel13.target_part.blob))
print(f"Original DangNhap image: {img_dangnhap.size}")
# Crop off top 31 pixels (window titlebar)
crop_dangnhap = img_dangnhap.crop((0, 31, img_dangnhap.width, img_dangnhap.height))
print(f"Cropped DangNhap image: {crop_dangnhap.size}")

buf13 = io.BytesIO()
crop_dangnhap.save(buf13, format='PNG')
rel13.target_part._blob = buf13.getvalue()

# Update drawing extent for DangNhap
# Find P containing rId13
for p in doc.paragraphs[gui_start:gui_start+20]:
    blips = p._p.xpath('.//a:blip')
    if any(b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') == 'rId13' for b in blips):
        # Update extent maintaining width
        extents = p._p.xpath('.//wp:extent')
        if extents:
            cx = int(extents[0].get('cx'))
            cy = int(cx * crop_dangnhap.height / crop_dangnhap.width)
            for ext in extents:
                ext.set('cy', str(cy))
            for ext in p._p.xpath('.//a:ext'):
                ext.set('cy', str(cy))
            print(f"Updated DangNhap drawing extent: cx={cx}, cy={cy}")
        break

# 2. BanHang screenshot (rId15 / image8.png)
rel15 = doc.part.rels['rId15']
img_banhang = Image.open(io.BytesIO(rel15.target_part.blob))
print(f"Original BanHang image: {img_banhang.size}")
# Crop off top 31 pixels (window titlebar)
crop_banhang = img_banhang.crop((0, 31, img_banhang.width, img_banhang.height))
print(f"Cropped BanHang image: {crop_banhang.size}")

buf15 = io.BytesIO()
crop_banhang.save(buf15, format='PNG')
rel15.target_part._blob = buf15.getvalue()

# Update drawing extent for BanHang
for p in doc.paragraphs[gui_start:gui_start+40]:
    blips = p._p.xpath('.//a:blip')
    if any(b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') == 'rId15' for b in blips):
        extents = p._p.xpath('.//wp:extent')
        if extents:
            cx = int(extents[0].get('cx'))
            cy = int(cx * crop_banhang.height / crop_banhang.width)
            for ext in extents:
                ext.set('cy', str(cy))
            for ext in p._p.xpath('.//a:ext'):
                ext.set('cy', str(cy))
            print(f"Updated BanHang drawing extent: cx={cx}, cy={cy}")
        break

print("Screenshots cropped and extents updated.")


# ==============================================================================
# EDIT 5 & EDIT 6: BỎ MA TRẬN HỒI QUY (BẢNG 19), PHẦN VI VÀ PHẦN VII
# ==============================================================================
print("\n=== EXECUTING EDIT 5 & BODY PART OF EDIT 6: BỎ PHẦN VI VÀ VII ===")

# In Document Body: locate start of Phần VI
p_vi_elem = None
for p in doc.paragraphs:
    if p.text.strip().startswith("PHẦN VI:"):
        p_vi_elem = p._p
        break

assert p_vi_elem is not None, "Could not find start of Phần VI in body"

body = doc._body._element
idx_vi = body.index(p_vi_elem)
print(f"PHẦN VI starts at body index {idx_vi} (total body elements: {len(body)})")

# Remove all elements from idx_vi to the end of body
# (Note: we leave the body's final sectPr intact if it's there)
elements_to_remove = []
for elem in body[idx_vi:]:
    if elem.tag.endswith('sectPr'):
        # Keep section properties at the end of body if present!
        continue
    elements_to_remove.append(elem)

print(f"Removing {len(elements_to_remove)} body elements (Phần VI and VII)...")
for elem in elements_to_remove:
    body.remove(elem)

# Also remove Bảng 19 from "Danh mục bảng biểu" in front matter!
# Find the line for Bảng 19 in paragraphs
removed_tbl_list = 0
for i in range(len(doc.paragraphs)-1, -1, -1):
    p = doc.paragraphs[i]
    if "BẢNG 19" in p.text.upper() and ("VERIFY" in p.text.upper() or "HỒI QUY" in p.text.upper()):
        print(f"Removing Bảng 19 entry from List of Tables: {repr(p.text)}")
        p._p.getparent().remove(p._p)
        removed_tbl_list += 1
    elif "Danh mục bao gồm 19 bảng biểu" in p.text:
        print(f"Updating technical note in List of Tables...")
        p.text = p.text.replace("19 bảng biểu", "18 bảng biểu").replace("Bảng 19", "Bảng 18").replace("23 bảng biểu", "22 bảng biểu")

print(f"Removed {removed_tbl_list} entries from List of Tables.")


# ==============================================================================
# SAVE AND VERIFY COUNTS
# ==============================================================================
doc.save(DOCX_PATH)
print(f"\nSaved updated document to {DOCX_PATH}")

final_doc = docx.Document(DOCX_PATH)
final_paras = len(final_doc.paragraphs)
final_tables = len(final_doc.tables)
final_drawings = len(final_doc._body._element.xpath('.//w:drawing'))

print("\n=== SUMMARY OF BEFORE / AFTER COUNTS ===")
print(f"Paragraphs: {init_paras} -> {final_paras} (reduced by {init_paras - final_paras})")
print(f"Tables:     {init_tables} -> {final_tables} (reduced by {init_tables - final_tables}: Callout Table 3 + Bảng 19)")
print(f"Drawings:   {init_drawings} -> {final_drawings} (maintained: exactly {final_drawings}/20)")

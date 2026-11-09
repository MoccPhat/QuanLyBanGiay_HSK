import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import subprocess
import pymupdf
from PIL import Image
import shutil
import datetime
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
BACKUP_DIR = r"E:\Eclipse Java\project\_sync\backup_docx"
SYNC_DIR = r"E:\Eclipse Java\project\_sync"

# 8 image mappings: (figure_id, caption_prefix, manual_file)
TARGETS = [
    ("Hình 1", "Hình 1. Sơ đồ Use Case", "manual_usecase.png"),
    ("Hình 3", "Hình 3. Sơ đồ lớp", "manual_class.png"),
    ("Hình 7", "Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán", "manual_seq_thanhtoan.png"),
    ("Hình 15", "Hình 15. Sơ đồ tuần tự nghiệp vụ Đăng nhập", "manual_seq_dangnhap.png"),
    ("Hình 16", "Hình 16. Sơ đồ tuần tự nghiệp vụ Quản lý sản phẩm", "manual_seq_sanpham.png"),
    ("Hình 17", "Hình 17. Sơ đồ tuần tự nghiệp vụ Quản lý khách hàng", "manual_seq_khachhang.png"),
    ("Hình 18", "Hình 18. Sơ đồ tuần tự nghiệp vụ Quản lý nhân sự", "manual_seq_nhanvien.png"),
    ("Hình 19", "Hình 19. Sơ đồ tuần tự nghiệp vụ Thống kê doanh thu", "manual_seq_thongke.png")
]

print("=== 1. VERIFYING SOURCE FILES ===")
source_sizes = {}
for fig_id, cap_prefix, filename in TARGETS:
    fpath = os.path.join(SYNC_DIR, filename)
    assert os.path.exists(fpath), f"File {fpath} not found!"
    size = os.path.getsize(fpath)
    source_sizes[filename] = size
    img = Image.open(fpath)
    print(f"  {fig_id}: {filename} ({size:,} bytes, {img.size[0]}x{img.size[1]} px)")

# 2. Backup docx
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"BaoCao_QuanLyBanGiay_HSK_backup_{now_str}.docx")
shutil.copy2(DOCX_PATH, backup_file)
print(f"\n2. Backup created: {backup_file} ({os.path.getsize(backup_file):,} bytes)")

doc = docx.Document(DOCX_PATH)

# Check drawings count before
drawings_before = 0
for p in doc.paragraphs:
    drawings_before += len(p._p.xpath('.//w:drawing'))
print(f"\nDrawings in body paragraphs before: {drawings_before}")

# 3. Process each target
print("\n=== 3. REPLACING 8 IMAGES ===")
old_rids_to_delete = []

for fig_id, cap_prefix, filename in TARGETS:
    fpath = os.path.join(SYNC_DIR, filename)
    
    # Find caption in body (index > 110 to avoid Table of Figures)
    cap_idx = None
    for i, p in enumerate(doc.paragraphs):
        if i > 110 and cap_prefix in p.text:
            cap_idx = i
            break
    
    assert cap_idx is not None, f"Caption for {fig_id} not found in body!"
    cap_p = doc.paragraphs[cap_idx]
    
    # Preceding paragraph is the drawing paragraph
    img_p = doc.paragraphs[cap_idx - 1]
    drawings = img_p._p.xpath('.//w:drawing')
    assert len(drawings) > 0, f"No drawing found in preceding paragraph P{cap_idx - 1} for {fig_id}!"
    
    # Extract old rId
    blip = drawings[0].xpath('.//a:blip')[0]
    old_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    old_part = doc.part.rels[old_rid].target_part
    print(f"\nReplacing {fig_id} at P{cap_idx - 1}:")
    print(f"  Caption: {cap_p.text}")
    print(f"  Old rId: {old_rid} -> {old_part.partname} ({len(old_part._blob):,} bytes)")
    
    # Remove old run(s) from img_p
    for r in list(img_p.runs):
        img_p._p.remove(r._r)
        
    # Insert new run with new image
    new_run = img_p.add_run()
    new_run.add_picture(fpath, width=Cm(16))
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.paragraph_format.space_before = Pt(6)
    img_p.paragraph_format.space_after = Pt(4)
    
    old_rids_to_delete.append(old_rid)
    print(f"  -> Inserted {filename} with width=Cm(16), center aligned")

# Delete old relationships so unreferenced watermark images are completely purged
for rid in old_rids_to_delete:
    if rid in doc.part.rels:
        del doc.part.rels[rid]
print(f"\nDeleted {len(old_rids_to_delete)} old relationships from doc.part.rels")

# Check drawings count after
drawings_after = 0
for p in doc.paragraphs:
    drawings_after += len(p._p.xpath('.//w:drawing'))
print(f"Drawings in body paragraphs after: {drawings_after}")
assert drawings_before == drawings_after, f"Drawings mismatch: {drawings_before} vs {drawings_after}!"

# 4. Save docx
doc.save(DOCX_PATH)
print(f"\n4. Document saved: {DOCX_PATH} ({os.path.getsize(DOCX_PATH):,} bytes)")

# 5. Check media inside saved docx
print("\n=== 5. CHECKING MEDIA IN SAVED DOCX ===")
doc_saved = docx.Document(DOCX_PATH)
saved_media_parts = [p for p in doc_saved.part.package.parts if 'media' in p.partname]
print(f"Total media parts in saved docx: {len(saved_media_parts)}")

# Verify 8 new images exist with matching sizes
found_new_sizes = []
for mp in saved_media_parts:
    size = len(mp._blob)
    for fn, src_sz in source_sizes.items():
        if size == src_sz:
            print(f"  MATCH: {mp.partname} ({size:,} bytes) matches {fn}")
            found_new_sizes.append(fn)

assert len(found_new_sizes) == 8, f"Expected 8 matched new images, found {len(found_new_sizes)}: {found_new_sizes}!"
print(f"All 8 manual images verified inside docx package!")

# 6. Convert to PDF via LibreOffice headless
print("\n=== 6. CONVERTING TO PDF VIA LIBREOFFICE ===")
cmd = [r"C:\Program Files\LibreOffice\program\soffice.exe", "--headless", "--convert-to", "pdf", "--outdir", SYNC_DIR, DOCX_PATH]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(f"LibreOffice return code: {res.returncode}")

pdf_file = os.path.join(SYNC_DIR, "BaoCao_QuanLyBanGiay_HSK.pdf")
doc_pdf = pymupdf.open(pdf_file)
total_pages = len(doc_pdf)
print(f"Total pages in PDF: {total_pages}")

# 7. Locate pages for Hình 1, Hình 7, Hình 19
p_hinh1 = None
p_hinh7 = None
p_hinh19 = None

for idx, page in enumerate(doc_pdf):
    # Only check body pages (idx >= 6)
    if idx < 6:
        continue
    txt = page.get_text("text")
    if "Hình 1. Sơ đồ Use Case" in txt and p_hinh1 is None:
        p_hinh1 = idx
    if "Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán" in txt and p_hinh7 is None:
        p_hinh7 = idx
    if "Hình 19. Sơ đồ tuần tự nghiệp vụ Thống kê" in txt and p_hinh19 is None:
        p_hinh19 = idx

print(f"\nTarget pages in PDF: Hình 1 = Page {p_hinh1+1}, Hình 7 = Page {p_hinh7+1}, Hình 19 = Page {p_hinh19+1}")
assert p_hinh1 is not None, "Page for Hình 1 not found!"
assert p_hinh7 is not None, "Page for Hình 7 not found!"
assert p_hinh19 is not None, "Page for Hình 19 not found!"

# 8. Render 3 pages to _sync\noWM_*.png
mat = pymupdf.Matrix(2.0, 2.0)

render_targets = [
    (p_hinh1, "noWM_hinh1.png", "Hình 1 (Use Case)"),
    (p_hinh7, "noWM_hinh7.png", "Hình 7 (Thanh toán POS)"),
    (p_hinh19, "noWM_hinh19.png", "Hình 19 (Thống kê doanh thu)")
]

print("\n=== 7. RENDERING PREVIEW PAGES ===")
for p_idx, fname, label in render_targets:
    pix = doc_pdf[p_idx].get_pixmap(matrix=mat)
    out_p = os.path.join(SYNC_DIR, fname)
    pix.save(out_p)
    print(f"  Rendered {label} -> {out_p} ({os.path.getsize(out_p):,} bytes, {pix.width}x{pix.height} px)")

print("\n=== COMPLETED SUCCESSFULLY ===")

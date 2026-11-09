import pymupdf
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

PDF_FILE = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"
OUT_DIR = r"E:\Eclipse Java\project\_sync"

doc = pymupdf.open(PDF_FILE)
print(f"Total pages: {len(doc)}")

targets = {}

# 1. Trang ký GVHD (Page 3)
targets["edit_gvhd_signature.png"] = (2, "Trang ký GVHD (Page 3)")

# 2. Mục lục
targets["edit_toc_page1.png"] = (3, "Mục lục trang 1 (Page 4)")
targets["edit_toc_page2.png"] = (4, "Mục lục trang 2 (Page 5)")

# 3. Callout replacement
for i, page in enumerate(doc):
    if "Quy trình 6 bước tại quầy được mô tả trực quan trong Hình 7" in page.get_text("text"):
        targets["edit_callout_replacement.png"] = (i, f"Đoạn thay thế Callout (Page {i+1})")
        break

# 4. Đăng nhập (Hình 5)
for i, page in enumerate(doc):
    if i >= 10 and "Hình 5. Giao diện Đăng nhập" in page.get_text("text"):
        targets["edit_gui_dangnhap.png"] = (i, f"GUI Đăng nhập cropped (Page {i+1})")
        break

# 5. Bán hàng & Hình 7 (Hình 6 & 7)
for i, page in enumerate(doc):
    if i >= 10 and "Hình 6. Giao diện Bán hàng" in page.get_text("text"):
        targets["edit_gui_banhang.png"] = (i, f"GUI Bán hàng cropped (Page {i+1})")
        break

for i, page in enumerate(doc):
    if i >= 10 and "Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS" in page.get_text("text"):
        targets["edit_hinh7_thanhtoan.png"] = (i, f"Hình 7 Tuần tự thanh toán (Page {i+1})")
        break

# 6. Trang cuối cùng
targets["edit_last_page.png"] = (len(doc) - 1, f"Trang cuối cùng của báo cáo (Page {len(doc)})")

for filename, (p_idx, label) in targets.items():
    page = doc[p_idx]
    mat = pymupdf.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    out_path = os.path.join(OUT_DIR, filename)
    pix.save(out_path)
    print(f"Rendered [{label}] -> {out_path} ({os.path.getsize(out_path):,} bytes, {pix.width}x{pix.height})")

print("\nAll target preview images exported successfully!")

import subprocess
import pymupdf
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
DOCX_FILE = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
OUT_DIR = r"E:\Eclipse Java\project\_sync"
PDF_FILE = os.path.join(OUT_DIR, "BaoCao_QuanLyBanGiay_HSK.pdf")

print("1. Converting docx to pdf with LibreOffice...")
cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", "--outdir", OUT_DIR, DOCX_FILE]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print("Return code:", res.returncode)
if res.stdout:
    print("Stdout:", res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

assert os.path.exists(PDF_FILE), f"PDF file does not exist: {PDF_FILE}"
print(f"PDF successfully created: {PDF_FILE} ({os.path.getsize(PDF_FILE):,} bytes)")

print("\n2. Opening PDF and searching for sequence diagram pages...")
doc = pymupdf.open(PDF_FILE)
print(f"Total pages: {len(doc)}")

targets = [
    {
        "search": "Hình 15.",
        "out_name": "preview_seq2_dangnhap.png",
        "label": "Đăng nhập",
    },
    {
        "search": "Hình 19.",
        "out_name": "preview_seq2_thongke.png",
        "label": "Thống kê",
    },
]

for t in targets:
    found_page_idx = None
    for p_idx, page in enumerate(doc):
        # Skip toc/list of figures (first 8 pages)
        if p_idx < 8:
            continue
        text = page.get_text("text")
        if t["search"] in text:
            found_page_idx = p_idx
            break
    
    if found_page_idx is not None:
        print(f"Found {t['search']} ({t['label']}) on PDF page {found_page_idx + 1}")
        page = doc[found_page_idx]
        mat = pymupdf.Matrix(2.0, 2.0) # 2x zoom for high quality
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(OUT_DIR, t["out_name"])
        pix.save(out_path)
        print(f"  Saved preview to: {out_path} ({os.path.getsize(out_path):,} bytes, {pix.width}x{pix.height})")
    else:
        print(f"WARNING: Could not find {t['search']} ({t['label']}) in PDF!")

print("\nDone rendering previews.")

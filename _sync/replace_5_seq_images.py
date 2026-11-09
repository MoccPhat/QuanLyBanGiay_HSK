import docx
from PIL import Image
import zipfile
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"

targets = [
    {
        "caption_prefix": "Hình 15.",
        "name": "dangnhap",
        "rid": "rId14",
        "file": r"E:\Eclipse Java\project\_sync\vp_seq_dangnhap.png",
        "expected_size": 118987,
    },
    {
        "caption_prefix": "Hình 16.",
        "name": "sanpham",
        "rid": "rId20",
        "file": r"E:\Eclipse Java\project\_sync\vp_seq_sanpham.png",
        "expected_size": 137568,
    },
    {
        "caption_prefix": "Hình 17.",
        "name": "khachhang",
        "rid": "rId23",
        "file": r"E:\Eclipse Java\project\_sync\vp_seq_khachhang.png",
        "expected_size": 128526,
    },
    {
        "caption_prefix": "Hình 18.",
        "name": "nhanvien",
        "rid": "rId25",
        "file": r"E:\Eclipse Java\project\_sync\vp_seq_nhanvien.png",
        "expected_size": 132563,
    },
    {
        "caption_prefix": "Hình 19.",
        "name": "thongke",
        "rid": "rId27",
        "file": r"E:\Eclipse Java\project\_sync\vp_seq_thongke.png",
        "expected_size": 126115,
    },
]

print(f"Opening {docx_path}...")
doc = docx.Document(docx_path)

cx_base = int(15.5 / 2.54 * 914400) # 15.5 cm

for item in targets:
    img_path = item["file"]
    actual_disk_size = os.path.getsize(img_path)
    print(f"\nProcessing {item['caption_prefix']} ({item['name']}): disk size={actual_disk_size:,} bytes")
    
    with open(img_path, "rb") as f:
        new_bytes = f.read()
    
    # Update media part blob
    rel = doc.part.rels[item["rid"]]
    rel.target_part._blob = new_bytes
    print(f"  Target ref: {rel.target_ref}, updated part blob size: {len(new_bytes):,} bytes")
    
    # Calculate cx and cy maintaining aspect ratio
    with Image.open(img_path) as img:
        w_px, h_px = img.size
    cy = int(cx_base * h_px / w_px)
    print(f"  Image dims: {w_px}x{h_px} -> cx={cx_base}, cy={cy} (~{cy/914400*2.54:.2f} cm)")
    
    # Locate drawing paragraph
    found = False
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith(item["caption_prefix"]) and "(Visual Paradigm 18)" in p.text:
            prev_p = doc.paragraphs[idx - 1]
            blips = prev_p._p.xpath('.//a:blip')
            matched_rids = [b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') for b in blips]
            if item["rid"] in matched_rids:
                found = True
                extents = prev_p._p.xpath('.//wp:extent')
                for ext in extents:
                    ext.set('cx', str(cx_base))
                    ext.set('cy', str(cy))
                a_exts = prev_p._p.xpath('.//a:ext')
                for ext in a_exts:
                    ext.set('cx', str(cx_base))
                    ext.set('cy', str(cy))
                print(f"  Updated extents in P{idx-1} (wp:extent: {len(extents)}, a:ext: {len(a_exts)})")
                break
    if not found:
        print(f"  WARNING: Could not find drawing paragraph for {item['caption_prefix']}")

doc.save(docx_path)
print(f"\nSuccessfully saved updated document to {docx_path}")

# Verification of zip archive
print("\n--- VERIFICATION OF DOCX ARCHIVE ---")
with zipfile.ZipFile(docx_path, "r") as z:
    media_files = [f for f in z.namelist() if f.startswith("word/media/")]
    print(f"Total media files in word/media/: {len(media_files)}")
    
    for item in targets:
        target_ref = doc.part.rels[item["rid"]].target_ref
        full_ref = "word/" + target_ref if not target_ref.startswith("word/") else target_ref
        info = z.getinfo(full_ref)
        match = "MATCH" if info.file_size == item["expected_size"] else "MISMATCH"
        print(f"  {item['caption_prefix']} -> {full_ref}: {info.file_size:,} bytes (expected {item['expected_size']:,}) [{match}]")

    doc_xml = z.read("word/document.xml").decode("utf-8")
    drawing_count = doc_xml.count("<w:drawing>")
    print(f"\nTotal <w:drawing> count in document.xml: {drawing_count} (must be 20)")

import os
import shutil
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

deliverable_dir = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable"
project_dir = r"E:\Eclipse Java\project"
sync_dir = os.path.join(project_dir, "_sync")
zip_target = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_FINAL_2026-11-09.zip"

print("=== 1. SYNCING FILES TO DELIVERABLE ===")

# 1. BaoCao docx
src_docx = os.path.join(project_dir, "BaoCao_QuanLyBanGiay_HSK.docx")
dst_docx = os.path.join(deliverable_dir, "BaoCao_QuanLyBanGiay_HSK.docx")
shutil.copy2(src_docx, dst_docx)
print(f"Copied docx: {dst_docx} ({os.path.getsize(dst_docx):,} bytes)")

# 2. Markdown docs
for doc_name in ["README.md", "HUONG_DAN_KIEN_TRUC_VA_CODE.md"]:
    src_md = os.path.join(project_dir, doc_name)
    dst_md = os.path.join(deliverable_dir, doc_name)
    if os.path.exists(src_md):
        shutil.copy2(src_md, dst_md)
        print(f"Copied markdown: {doc_name} ({os.path.getsize(dst_md):,} bytes)")

# 3. run.bat & db.properties.example
for f_name in ["run.bat", "db.properties.example"]:
    src_f = os.path.join(project_dir, f_name)
    dst_f = os.path.join(deliverable_dir, f_name)
    if os.path.exists(src_f):
        shutil.copy2(src_f, dst_f)
        print(f"Copied {f_name}")

# 4. Sync bin/
dst_bin = os.path.join(deliverable_dir, "bin")
src_bin = os.path.join(project_dir, "bin")
if os.path.exists(dst_bin):
    shutil.rmtree(dst_bin)
shutil.copytree(src_bin, dst_bin)
print(f"Synced bin directory ({len(os.listdir(dst_bin))} entries)")

# 5. Sync src/
dst_src = os.path.join(deliverable_dir, "src")
src_src = os.path.join(project_dir, "src")
if os.path.exists(dst_src):
    shutil.rmtree(dst_src)
shutil.copytree(src_src, dst_src)
print(f"Synced src directory")

# 6. Sync database/
dst_db = os.path.join(deliverable_dir, "database")
src_db = os.path.join(project_dir, "database")
if os.path.exists(dst_db):
    shutil.rmtree(dst_db)
shutil.copytree(src_db, dst_db)
print(f"Synced database directory")

# 7. Copy sequence diagrams
seq_diagrams = [
    "vp_seq_dangnhap.png",
    "vp_seq_sanpham.png",
    "vp_seq_khachhang.png",
    "vp_seq_nhanvien.png",
    "vp_seq_thongke.png",
]
for seq in seq_diagrams:
    s_path = os.path.join(sync_dir, seq)
    d_path = os.path.join(deliverable_dir, seq)
    if os.path.exists(s_path):
        shutil.copy2(s_path, d_path)
        print(f"Copied sequence diagram: {seq} ({os.path.getsize(d_path):,} bytes)")

# 8. Verify deliverable hygiene
forbidden = [
    os.path.join(deliverable_dir, "db.properties"),
    os.path.join(deliverable_dir, "hoadon"),
    os.path.join(deliverable_dir, "_sync"),
]
for p in forbidden:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
        print(f"Removed forbidden item: {p}")

# Also check for any .py files in deliverable
py_files = []
for root, dirs, files in os.walk(deliverable_dir):
    for f in files:
        if f.endswith(".py"):
            py_files.append(os.path.join(root, f))
for pf in py_files:
    os.remove(pf)
    print(f"Removed python file: {pf}")

print("\n=== 2. PACKAGING DELIVERABLE ZIP ===")
# Inspect existing zip structure if exists
if os.path.exists(zip_target):
    with zipfile.ZipFile(zip_target, "r") as z:
        sample_names = z.namelist()[:5]
        print(f"Existing zip sample entries: {sample_names}")

# Create new zip
total_files = 0
uncompressed_size = 0

with zipfile.ZipFile(zip_target, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(deliverable_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, os.path.dirname(deliverable_dir))
            z.write(full_path, rel_path)
            total_files += 1
            uncompressed_size += os.path.getsize(full_path)

zip_size = os.path.getsize(zip_target)

print(f"\nDeliverable packaging complete!")
print(f"Destination: {zip_target}")
print(f"Total files: {total_files}")
print(f"Uncompressed size: {uncompressed_size:,} bytes ({uncompressed_size / (1024*1024):.2f} MB)")
print(f"Zip size: {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")

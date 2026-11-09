import os
import shutil
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"E:\Eclipse Java\project"
DELIVERABLE_DIR = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_Deliverable"
ZIP_TARGET = r"E:\Eclipse Java\StepUp_QuanLyBanGiay_FINAL_2026-11-09.zip"

print("=== REPACKAGING DELIVERABLE: PACK-1109 ===")

# 1. Clean and recreate Deliverable directory
if os.path.exists(DELIVERABLE_DIR):
    shutil.rmtree(DELIVERABLE_DIR)
os.makedirs(DELIVERABLE_DIR, exist_ok=True)
print(f"1. Cleaned and initialized directory: {DELIVERABLE_DIR}")

# 2. Items to copy:
# Directories
dir_items = ["src", "bin", "lib", "database", ".settings"]
for d in dir_items:
    src_path = os.path.join(PROJECT_DIR, d)
    dst_path = os.path.join(DELIVERABLE_DIR, d)
    if os.path.exists(src_path):
        shutil.copytree(src_path, dst_path)
        print(f"  Copied directory: {d} ({len(os.listdir(dst_path))} entries)")
    else:
        print(f"  WARNING: Directory {d} not found in project!")

# Files
file_items = [
    "BaoCao_QuanLyBanGiay_HSK.docx",
    "SoDoLop_QuanLyBanGiay.png",
    "SoDoLop_QuanLyBanGiay.drawio",
    "HUONG_DAN_KIEN_TRUC_VA_CODE.md",
    "README.md",
    "run.bat",
    "db.properties.example",
    ".classpath",
    ".project",
    ".gitignore",
]

for f in file_items:
    src_path = os.path.join(PROJECT_DIR, f)
    dst_path = os.path.join(DELIVERABLE_DIR, f)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"  Copied file: {f} ({os.path.getsize(dst_path):,} bytes)")
    else:
        print(f"  WARNING: File {f} not found in project!")

# 3. Cleanliness & Deliverable hygiene check
print("\n=== HYGIENE CHECK (XÁC NHẬN KHÔNG CÓ FILE RÁC) ===")

forbidden_names = [".git", "_sync", "PHAN-BIEN", "hoadon", "db.properties"]
violations = []

all_files = []
for root, dirs, files in os.walk(DELIVERABLE_DIR):
    for d in dirs:
        if d in forbidden_names:
            violations.append(f"Forbidden directory found: {os.path.join(root, d)}")
    for f in files:
        full_f = os.path.join(root, f)
        all_files.append(full_f)
        if f in forbidden_names:
            violations.append(f"Forbidden file found: {full_f}")
        if f.endswith(".py"):
            violations.append(f"Python script found: {full_f}")
        if f.endswith(".tmp") or f.startswith("~") or f.startswith("_chk"):
            violations.append(f"Temp file found: {full_f}")

if violations:
    for v in violations:
        print("  ERROR:", v)
    raise RuntimeError(f"Hygiene check failed with {len(violations)} violations!")
else:
    print("  -> HYGIENE CHECK: 100% PASS!")
    print("     - 0 file .py")
    print("     - 0 file db.properties thật")
    print("     - 0 thư mục .git, _sync, PHAN-BIEN, hoadon")
    print("     - 0 file rác / temp file")

# 4. Verify bin/Main.class bytecode major version = 61
main_class = os.path.join(DELIVERABLE_DIR, "bin", "Main.class")
assert os.path.exists(main_class), "bin/Main.class not found in deliverable!"
with open(main_class, "rb") as f:
    f.seek(6)
    major = int.from_bytes(f.read(2), "big")
assert major == 61, f"Major version is {major}, expected 61 (Java 17)!"
print(f"\n  -> Bytecode Check: bin/Main.class major version = {major} (Java 17 - 100% PASS)")

# 5. Package zip
print("\n=== 4. PACKAGING DELIVERABLE ZIP ===")
if os.path.exists(ZIP_TARGET):
    os.remove(ZIP_TARGET)

total_files = 0
uncompressed_size = 0

with zipfile.ZipFile(ZIP_TARGET, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(DELIVERABLE_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, os.path.dirname(DELIVERABLE_DIR))
            z.write(full_path, rel_path)
            total_files += 1
            uncompressed_size += os.path.getsize(full_path)

zip_size = os.path.getsize(ZIP_TARGET)

print(f"\nDeliverable packaging complete!")
print(f"Destination: {ZIP_TARGET}")
print(f"Total files: {total_files}")
print(f"Uncompressed size: {uncompressed_size:,} bytes ({uncompressed_size / (1024*1024):.2f} MB)")
print(f"Zip size: {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")

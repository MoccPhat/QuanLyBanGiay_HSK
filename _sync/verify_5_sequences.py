import docx
import pymupdf
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

DOCX_FILE = r"E:\Eclipse Java\project\BaoCao_QuanLyBanGiay_HSK.docx"
PDF_FILE = r"E:\Eclipse Java\project\_sync\BaoCao_QuanLyBanGiay_HSK.pdf"

doc = docx.Document(DOCX_FILE)

print("=== 1. KIỂM TRA SỐ LƯỢNG DRAWINGS ===")
drawings = doc._body._element.xpath('.//w:drawing')
print(f"Tổng số w:drawing: {len(drawings)} (Kỳ vọng: 20)")
assert len(drawings) == 20, f"Lỗi: số drawing = {len(drawings)} != 20"

print("\n=== 2. KIỂM TRA DANH MỤC HÌNH ẢNH ===")
list_figures = []
for p in doc.paragraphs[:135]:
    text = p.text.strip()
    if text.startswith("Hình ") and "\t" in text:
        parts = text.split("\t")
        cap = parts[0].strip()
        pg = parts[1].strip()
        list_figures.append((cap, pg))

print(f"Tổng số mục trong Danh mục hình ảnh: {len(list_figures)} (Kỳ vọng: 19)")
assert len(list_figures) == 19, f"Lỗi: số mục danh mục = {len(list_figures)} != 19"

for cap, pg in list_figures:
    print(f"  {cap} -> Trang {pg}")

print("\n=== 3. KIỂM TRA 5 CAPTION MỚI TRONG THÂN BÁO CÁO ===")
expected_new_captions = [
    "Hình 15. Sơ đồ tuần tự nghiệp vụ Đăng nhập (Visual Paradigm 18)",
    "Hình 16. Sơ đồ tuần tự nghiệp vụ Quản lý sản phẩm (Visual Paradigm 18)",
    "Hình 17. Sơ đồ tuần tự nghiệp vụ Quản lý khách hàng (Visual Paradigm 18)",
    "Hình 18. Sơ đồ tuần tự nghiệp vụ Quản lý nhân sự (Visual Paradigm 18)",
    "Hình 19. Sơ đồ tuần tự nghiệp vụ Thống kê doanh thu (Visual Paradigm 18)"
]

found_captions = []
for p in doc.paragraphs:
    t = p.text.strip()
    if any(t == ec for ec in expected_new_captions):
        found_captions.append(t)
        print(f"  [FOUND] {t}")

print(f"Số caption mới tìm thấy: {len(found_captions)} / 5")
assert len(found_captions) == 5, f"Thiếu caption mới: {found_captions}"

print("\n=== 4. KIỂM TRA ĐỘ SẠCH ĐỊNH DẠNG ===")
shd_count = len(doc._body._element.xpath('.//w:shd'))
hl_count = len(doc._body._element.xpath('.//w:highlight'))
print(f"w:shd count: {shd_count}, w:highlight count: {hl_count}")
assert hl_count == 0, f"Có highlight tồn tại: {hl_count}"

print("\n=== 5. KIỂM TRA ẢNH PREVIEW ===")
previews = [
    r"E:\Eclipse Java\project\_sync\preview_seq_dangnhap.png",
    r"E:\Eclipse Java\project\_sync\preview_seq_sanpham.png",
    r"E:\Eclipse Java\project\_sync\preview_seq_thongke.png"
]
for p in previews:
    assert os.path.exists(p), f"Không tìm thấy ảnh: {p}"
    size = os.path.getsize(p)
    print(f"  [OK] {os.path.basename(p)} ({size:,} bytes)")

print("\n=== TẤT CẢ CÁC TIÊU CHÍ TỰ KIỂM ĐỀU ĐẠT 100% ===")

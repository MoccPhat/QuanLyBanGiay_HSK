import pymupdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"E:\Eclipse Java\project\_sync\test_cover_border.pdf"
doc = pymupdf.open(pdf_path)

page0 = doc[0]
page_w, page_h = page0.rect.width, page0.rect.height
print(f"Kích thước trang 1: width={page_w:.1f} pt, height={page_h:.1f} pt")

# 1. Kiểm tra khung viền (Page Border)
drawings = page0.get_drawings()
print(f"\n--- 1. Kiểm tra Khung viền (Drawings trên Trang 1: {len(drawings)}) ---")
# Các đường viền là rect hoặc lines
border_rects = []
for d in drawings:
    rect = d.get('rect')
    color = d.get('color')
    print(f"  Drawing: rect={rect}, color={color}")

# Lấy bounding box bao quanh tất cả các đường border
min_x = min(d['rect'].x0 for d in drawings)
max_x = max(d['rect'].x1 for d in drawings)
min_y = min(d['rect'].y0 for d in drawings)
max_y = max(d['rect'].y1 for d in drawings)

dist_left = min_x
dist_right = page_w - max_x
dist_top = min_y
dist_bottom = page_h - max_y

print(f"\nKhoảng cách viền đến mép trang:")
print(f"  Trái (Left):   {dist_left:.1f} pt")
print(f"  Phải (Right):  {dist_right:.1f} pt")
print(f"  Trên (Top):    {dist_top:.1f} pt")
print(f"  Dưới (Bottom): {dist_bottom:.1f} pt")

# 2. Kiểm tra Logo trên trang 1
print("\n--- 2. Kiểm tra Logo trên Trang 1 ---")
images = page0.get_images()
print(f"Số ảnh trên trang 1: {len(images)}")
# Lấy rect của ảnh logo
img_rects = []
for info in page0.get_image_info():
    r = info.get('bbox')
    w = r[2] - r[0]
    h = r[3] - r[1]
    center_x = (r[0] + r[2]) / 2
    print(f"  Logo bbox: x0={r[0]:.1f}, y0={r[1]:.1f}, x1={r[2]:.1f}, y1={r[3]:.1f} | rộng={w:.1f} pt ({w/72*2.54:.2f} cm), cao={h:.1f} pt ({h/72*2.54:.2f} cm) | center_x={center_x:.1f} pt (Trang mid={page_w/2:.1f} pt)")
    img_rects.append(r)

# 3. Kiểm tra nội dung không chạm khung
print("\n--- 3. Kiểm tra Nội dung không chạm khung ---")
words = page0.get_text("words")
content_min_x = min(w[0] for w in words)
content_max_x = max(w[2] for w in words)
content_min_y = min(w[1] for w in words)
content_max_y = max(w[3] for w in words)

print(f"Vùng nội dung text: x=[{content_min_x:.1f}, {content_max_x:.1f}], y=[{content_min_y:.1f}, {content_max_y:.1f}]")
print(f"Khoảng đệm từ nội dung đến khung viền:")
print(f"  Đệm trái:  {content_min_x - min_x:.1f} pt (> 0 -> không chạm)")
print(f"  Đệm phải:  {max_x - content_max_x:.1f} pt (> 0 -> không chạm)")
print(f"  Đệm trên:  {content_min_y - min_y:.1f} pt (> 0 -> không chạm)")
print(f"  Đệm dưới:  {max_y - content_max_y:.1f} pt (> 0 -> không chạm)")

# 4. Kiểm tra trang 2 và các trang sau KHÔNG có khung
print("\n--- 4. Kiểm tra các trang sau KHÔNG có khung ---")
for p_idx in range(1, min(6, len(doc))):
    p = doc[p_idx]
    # Lọc các drawing là page border (có kích thước lớn gần bằng trang)
    large_drawings = [d for d in p.get_drawings() if d['rect'].width > 400 and d['rect'].height > 600]
    print(f"  Trang {p_idx+1}: số large drawings (khung viền) = {len(large_drawings)}")
    assert len(large_drawings) == 0, f"Trang {p_idx+1} bị dính khung viền!"

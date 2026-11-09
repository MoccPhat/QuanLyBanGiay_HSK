from PIL import Image, ImageDraw
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

W = 2480
H = 3508
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

COLOR = (0, 0, 0, 255) # Pure black

# 1. Margins (strictly >= 60px from page edge)
m_out = 75   # outer border inset (>= 60px)
gap = 18     # gap between borders
m_in = m_out + gap  # 93px

# 2. Outer Border (thick: 8px)
t_out = 8
for i in range(t_out):
    draw.rectangle([m_out + i, m_out + i, W - m_out - i - 1, H - m_out - i - 1], outline=COLOR)

# 3. Inner Border (3px)
t_in = 3
for i in range(t_in):
    draw.rectangle([m_in + i, m_in + i, W - m_in - i - 1, H - m_in - i - 1], outline=COLOR)

# 4. Mid-edge Diamonds (24x24 px, stroke 3px, centered on each edge)
diamond_r = 12 # 24x24 total size
mid_border = (m_out + m_in) // 2

# Draw mid-edge diamond onto a small 60x60 tile, then paste/mirror
d_tile = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(d_tile)
cx_t, cy_t = 30, 30
for offset in range(3):
    pts = [
        (cx_t, cy_t - diamond_r + offset),
        (cx_t + diamond_r - offset, cy_t),
        (cx_t, cy_t + diamond_r - offset),
        (cx_t - diamond_r + offset, cy_t)
    ]
    d_draw.polygon(pts, outline=COLOR)

# Paste Top & Bottom (symmetric)
img.paste(d_tile, (W // 2 - 30, mid_border - 30), d_tile)
img.paste(d_tile, (W // 2 - 30, H - mid_border - 30), d_tile)

# Paste Left & Right (symmetric)
d_tile_side = d_tile.copy()
img.paste(d_tile_side, (mid_border - 30, H // 2 - 30), d_tile_side)
img.paste(d_tile_side, (W - mid_border - 30, H // 2 - 30), d_tile_side)

# 5. Corner Ornaments with PERFECT MIRROR SYMMETRY
# We construct the Top-Left corner tile of size (400, 400)
c_size = 400
corner_tile = Image.new("RGBA", (c_size, c_size), (0, 0, 0, 0))
c_draw = ImageDraw.Draw(corner_tile)

# A. Ô vuông nhỏ 60x60px ở góc trong (nối hai viền)
sq_x1, sq_y1 = m_out, m_out
sq_x2, sq_y2 = m_out + 60, m_out + 60

for i in range(3):
    c_draw.rectangle([sq_x1 + i, sq_y1 + i, sq_x2 - i, sq_y2 - i], outline=COLOR)

# Inner diagonal line across the 60x60 square
c_draw.line([(sq_x1, sq_y1), (sq_x2, sq_y2)], fill=COLOR, width=2)

# B. 3 chấm tròn nhỏ (bán kính 4px) xếp theo đường chéo
for d_step in [75, 90, 105]:
    dot_x = m_out + d_step
    dot_y = m_out + d_step
    r_dot = 4
    c_draw.ellipse([dot_x - r_dot, dot_y - r_dot, dot_x + r_dot, dot_y + r_dot], fill=COLOR)

# C. Đường xoắn ốc 2 vòng nằm chéo góc, nét 4px
sp_cx = m_out + 180
sp_cy = m_out + 180
total_angle = 4 * math.pi # 2 turns
steps = 300
spiral_pts = []

r_start = 70.0
r_end = 8.0

for s in range(steps + 1):
    t = s / steps
    theta = t * total_angle
    r_cur = r_start - t * (r_start - r_end)
    phi = math.pi * 1.25 + theta
    lx = sp_cx + r_cur * math.cos(phi)
    ly = sp_cy + r_cur * math.sin(phi)
    spiral_pts.append((lx, ly))

for i in range(len(spiral_pts) - 1):
    c_draw.line([spiral_pts[i], spiral_pts[i+1]], fill=COLOR, width=4)

end_pt = spiral_pts[-1]
c_draw.ellipse([end_pt[0] - 3, end_pt[1] - 3, end_pt[0] + 3, end_pt[1] + 3], fill=COLOR)

# Perfect Mirror symmetry pastes:
# 1. Top-Left
img.paste(corner_tile, (0, 0), corner_tile)
# 2. Top-Right (Mirror Horizontal)
tr_tile = corner_tile.transpose(Image.FLIP_LEFT_RIGHT)
img.paste(tr_tile, (W - c_size, 0), tr_tile)
# 3. Bottom-Left (Mirror Vertical)
bl_tile = corner_tile.transpose(Image.FLIP_TOP_BOTTOM)
img.paste(bl_tile, (0, H - c_size), bl_tile)
# 4. Bottom-Right (Mirror Both)
br_tile = corner_tile.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
img.paste(br_tile, (W - c_size, H - c_size), br_tile)

out_file = r"E:\Eclipse Java\project\_sync\cover_frame_a4.png"
img.save(out_file, format="PNG")
print(f"Generated clean academic cover frame: {out_file} ({os.path.getsize(out_file):,} bytes)")

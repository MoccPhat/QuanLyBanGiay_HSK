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

m1 = 90   # outer border inset
m2 = 130  # inner border inset

# 1. Outer Border (thick: 7px)
for i in range(7):
    draw.rectangle([m1 + i, m1 + i, W - m1 - i, H - m1 - i], outline=COLOR)

# 2. Inner Border (medium: 3px)
for i in range(3):
    draw.rectangle([m2 + i, m2 + i, W - m2 - i, H - m2 - i], outline=COLOR)

# 3. Running diamond pattern at corner junctions
def draw_corner(cx, cy, flip_x, flip_y):
    def pt(lx, ly):
        x = cx + (lx if not flip_x else -lx)
        y = cy + (ly if not flip_y else -ly)
        return (x, y)

    # Corner box between m1 and m2
    # Fill corner junction with an ornate diamond-and-cross motif
    c_mid = (m2 - m1) // 2
    # Diagonal line connecting outer to inner corner
    draw.line([pt(0, 0), pt(m2 - m1, m2 - m1)], fill=COLOR, width=3)
    
    # Diamond at (c_mid, c_mid)
    d = 12
    draw.polygon([
        pt(c_mid, c_mid - d),
        pt(c_mid + d, c_mid),
        pt(c_mid, c_mid + d),
        pt(c_mid - d, c_mid)
    ], fill=COLOR)

    ox = m2 - m1
    oy = m2 - m1

    # Concentric quarter-circles (thick smooth arcs)
    for r in [50, 90, 130, 170, 210]:
        bbox = [
            min(pt(ox - r, oy)[0], pt(ox + r, oy)[0]),
            min(pt(ox, oy - r)[1], pt(ox, oy + r)[1]),
            max(pt(ox - r, oy)[0], pt(ox + r, oy)[0]),
            max(pt(ox, oy - r)[1], pt(ox, oy + r)[1])
        ]
        if not flip_x and not flip_y:
            sa, ea = 180, 270
        elif flip_x and not flip_y:
            sa, ea = 270, 360
        elif not flip_x and flip_y:
            sa, ea = 90, 180
        else:
            sa, ea = 0, 90
        draw.arc(bbox, start=sa, end=ea, fill=COLOR, width=4)

    # Scalloped beads along the r=130 arc
    for deg in range(10, 81, 10):
        rad = math.radians(deg)
        bx = ox + 130 * math.cos(rad)
        by = oy + 130 * math.sin(rad)
        p = pt(bx, by)
        draw.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=COLOR)

    # Classic S-curve scroll flourish curving outward
    steps = 100
    curve = []
    for s in range(steps + 1):
        t = s / steps
        angle = t * math.pi / 2
        # Elegant logarithmic spiral curvature
        r_spiral = 240 + 35 * math.sin(t * math.pi * 2)
        lx = ox + r_spiral * math.cos(angle)
        ly = oy + r_spiral * math.sin(angle)
        curve.append(pt(lx, ly))

    for i in range(len(curve) - 1):
        draw.line([curve[i], curve[i+1]], fill=COLOR, width=5)

    # Spiral terminals (circles / scrolls)
    t1_p = curve[0]
    t2_p = curve[-1]
    draw.ellipse([t1_p[0]-10, t1_p[1]-10, t1_p[0]+10, t1_p[1]+10], fill=COLOR)
    draw.ellipse([t2_p[0]-10, t2_p[1]-10, t2_p[0]+10, t2_p[1]+10], fill=COLOR)

    # Flower / rosette in corner center along diagonal (45 degrees)
    diag_r = 170
    fx = ox + diag_r * math.cos(math.pi / 4)
    fy = oy + diag_r * math.sin(math.pi / 4)
    fp = pt(fx, fy)
    # 8-petal rosette
    draw.ellipse([fp[0]-12, fp[1]-12, fp[0]+12, fp[1]+12], fill=COLOR)
    for p_ang in range(0, 360, 45):
        prad = math.radians(p_ang)
        px = fp[0] + 16 * math.cos(prad)
        py = fp[1] + 16 * math.sin(prad)
        draw.ellipse([px-5, py-5, px+5, py+5], fill=COLOR)

    # Border extension dashes/scrolls along the frames
    for dist in [120, 220, 320, 420]:
        # Horizontal accent
        p_hx = ox + dist
        draw.line([pt(p_hx, -10), pt(p_hx, 10)], fill=COLOR, width=3)
        draw.ellipse([pt(p_hx, 0)[0]-4, pt(p_hx, 0)[1]-4, pt(p_hx, 0)[0]+4, pt(p_hx, 0)[1]+4], fill=COLOR)
        
        # Vertical accent
        p_vy = oy + dist
        draw.line([pt(-10, p_vy), pt(10, p_vy)], fill=COLOR, width=3)
        draw.ellipse([pt(0, p_vy)[0]-4, pt(0, p_vy)[1]-4, pt(0, p_vy)[0]+4, pt(0, p_vy)[1]+4], fill=COLOR)

# Draw all 4 corners
draw_corner(m1, m1, False, False)
draw_corner(W - m1, m1, True, False)
draw_corner(m1, H - m1, False, True)
draw_corner(W - m1, H - m1, True, True)

out_path = r"E:\Eclipse Java\project\_sync\cover_frame_a4.png"
img.save(out_path, format="PNG")
print(f"Generated enhanced ornate cover frame: {out_path} ({os.path.getsize(out_path):,} bytes)")

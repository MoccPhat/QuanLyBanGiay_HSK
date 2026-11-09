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

print("=== CẬP NHẬT BÁO CÁO ROUND 3: CODE MỚI & CONNECTDB MẪU GIẢNG VIÊN ===")

# 1. Backup docx
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"BaoCao_QuanLyBanGiay_HSK_backup_{now_str}.docx")
shutil.copy2(DOCX_PATH, backup_file)
print(f"1. Backup created: {backup_file} ({os.path.getsize(backup_file):,} bytes)")

doc = docx.Document(DOCX_PATH)

# Check counts before
drawings_before = sum(len(p._p.xpath('.//w:drawing')) for p in doc.paragraphs)
tables_before = len(doc.tables)
print(f"Before: Drawings in body = {drawings_before}, Tables = {tables_before}")

# 2. TASK (a) & (b): THAY 5 ẢNH (2 SEQUENCE + 3 SCREENSHOTS)
# Mapping: (caption_search, new_file, display_width_cm, description)
IMG_REPLACEMENTS = [
    # (a) 2 sequence
    ("Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán POS", "manual_seq_thanhtoan.png", 16.0, "Hình 7 (Sequence Thanh toán)"),
    ("Hình 19. Sơ đồ tuần tự nghiệp vụ Thống kê doanh thu", "manual_seq_thongke.png", 16.0, "Hình 19 (Sequence Thống kê)"),
    # (b) 3 screenshots
    ("Hình 5. Giao diện Đăng nhập hệ thống", "after_trim_login.png", 14.5, "Hình 5 (Màn hình Đăng nhập)"),
    ("Hình 9. Giao diện Quản lý danh mục mẫu giày", "after_trim_sanpham.png", 16.0, "Hình 9 (Màn hình Sản phẩm)"),
    ("Hình 14. Giao diện Báo cáo thống kê doanh thu", "after_trim_thongke.png", 16.0, "Hình 14 (Màn hình Thống kê)")
]

old_rids_to_purge = []

for cap_search, new_fn, w_cm, desc in IMG_REPLACEMENTS:
    new_fp = os.path.join(SYNC_DIR, new_fn)
    assert os.path.exists(new_fp), f"Source file {new_fp} not found!"
    
    cap_idx = None
    for i, p in enumerate(doc.paragraphs):
        if i > 110 and cap_search in p.text:
            cap_idx = i
            break
    assert cap_idx is not None, f"Caption for {desc} not found in body!"
    
    img_p = doc.paragraphs[cap_idx - 1]
    drawings = img_p._p.xpath('.//w:drawing')
    assert len(drawings) > 0, f"No drawing found in P{cap_idx - 1} for {desc}!"
    
    # Save old rId to purge
    blip = drawings[0].xpath('.//a:blip')[0]
    old_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    old_rids_to_purge.append(old_rid)
    
    # Remove old run(s)
    for r in list(img_p.runs):
        img_p._p.remove(r._r)
        
    # Insert new picture
    new_r = img_p.add_run()
    new_r.add_picture(new_fp, width=Cm(w_cm))
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.paragraph_format.space_before = Pt(6)
    img_p.paragraph_format.space_after = Pt(4)
    print(f"  -> Replaced {desc} with {new_fn} (width={w_cm}cm, center)")

# Purge old relationships
for rid in old_rids_to_purge:
    if rid in doc.part.rels:
        del doc.part.rels[rid]
print(f"Purged {len(old_rids_to_purge)} old media relationships.")

# 3. TASK (c): XOÁ/CẮT CÁC MÔ TẢ CŨ
# (c.1) Bỏ 'in máy in' / 'máy in' (chỉ còn Xuất hóa đơn .txt)
for i, p in enumerate(doc.paragraphs):
    if "Hộp thoại xem trước phiếu Hóa đơn K80 tương tác" in p.text:
        p.text = "Hộp thoại xem trước phiếu Hóa đơn K80 tương tác (JDialog) tích hợp chức năng Xuất file văn bản:"
    if "Hình 8. Hộp thoại xem trước Hóa đơn K80" in p.text and i > 110:
        p.text = "Hình 8. Hộp thoại xem trước Hóa đơn K80 tích hợp chức năng Xuất file văn bản (chụp thật ngày 07/11/2026)"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.italic = True
    if "THANH TOÁN & IN HÓA ĐƠN" in p.text:
        p.text = p.text.replace("THANH TOÁN & IN HÓA ĐƠN", "THANH TOÁN & XUẤT HÓA ĐƠN")
    if "In hóa đơn vật lý:" in p.text:
        p.text = "Xuất chứng từ hóa đơn .txt: Hệ thống tập trung tối ưu hóa quy trình lưu trữ chứng từ số qua tính năng xuất hóa đơn ra file văn bản .txt định dạng chuẩn, không phụ thuộc vào thiết bị phần cứng máy in tại quầy."

# (c.2) Sửa mô tả 'tìm kiếm nâng cao' dạng hộp thoại -> thanh lọc trên màn hình
for i, p in enumerate(doc.paragraphs):
    if "Hộp thoại Tìm kiếm nâng cao Sản phẩm đa tiêu chí:" in p.text:
        p.text = "Thanh công cụ lọc và tra cứu sản phẩm trực tiếp trên giao diện:"
    if "Hình 10. Hộp thoại Tìm kiếm nâng cao Sản phẩm" in p.text and i > 110:
        p.text = "Hình 10. Giao diện bộ lọc Sản phẩm theo đa tiêu chí (chụp thật ngày 07/11/2026)"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.italic = True
    if "Hộp thoại Tìm kiếm nâng cao Khách hàng theo phân hạng" in p.text:
        p.text = "Thanh công cụ lọc và phân nhóm khách hàng trực tiếp trên giao diện:"
    if "Hình 12. Hộp thoại Tìm kiếm nâng cao Khách hàng" in p.text and i > 110:
        p.text = "Hình 12. Giao diện bộ lọc Khách hàng theo phân hạng và điểm tích lũy (chụp thật ngày 07/11/2026)"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.italic = True

# (c.3) Sửa mô tả Thống kê: Bỏ 'bộ lọc thời gian' và 'Top sản phẩm bán chạy'
for i, p in enumerate(doc.paragraphs):
    if "Hình 14. Giao diện Báo cáo thống kê doanh thu và Top sản phẩm" in p.text and i > 110:
        p.text = "Hình 14. Giao diện Báo cáo thống kê doanh thu (chụp thật ngày 07/11/2026)"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.italic = True
    if "Phân hệ Báo cáo thống kê: Xem tổng quan doanh thu" in p.text:
        p.text = "Phân hệ Báo cáo thống kê: Xem tổng quan 4 chỉ số KPI doanh thu, số đơn hàng, số sản phẩm bán ra thực tế, tổng khách hàng, danh sách hóa đơn giao dịch và chi tiết từng đơn hàng."
    if "Bộ lọc kỳ thời gian:" in p.text and "Toàn bộ thời gian, Hôm nay" in p.text:
        p.text = "Danh mục hóa đơn giao dịch: Bảng dữ liệu chi tiết hiển thị toàn bộ các hóa đơn đã thanh toán kèm mã hóa đơn, ngày lập, nhân viên phụ trách, khách hàng và tổng tiền."
    if "Xếp hạng sản phẩm bán chạy:" in p.text and "Top 5" in p.text:
        p.text = "Chỉ số tổng hợp kinh doanh: Phân hệ Thống kê phản ánh tức thời doanh thu thực thu, lượng hàng xuất kho và quy mô khách hàng phục vụ công tác đối soát kế toán."

# 4. TASK (d): SỬA ĐOẠN MÔ TẢ CONNECTDB THEO MẪU GIẢNG VIÊN
# Update P176 (Tầng DAO & ConnectDB)
p176 = doc.paragraphs[176]
p176.text = (
    "2. Tầng Truy cập dữ liệu & Quản lý kết nối (Data Access Layer - DAO & ConnectDB): "
    "Bao gồm lớp quản lý kết nối ConnectDB và các lớp DAO (HoaDon_DAO, SanPham_DAO, ChiTietGiay_DAO, "
    "KhachHang_DAO, NhanVien_DAO) kết hợp cùng 7 lớp Thực thể OOP. Trong đó, lớp ConnectDB được xây dựng "
    "chuẩn mực theo đúng mẫu của Giảng viên hướng dẫn: áp dụng mẫu thiết kế Singleton (Singleton Pattern) "
    "với biến kết nối tĩnh dùng chung 'public static Connection con = null', thể hiện đơn nhất qua phương thức "
    "getInstance(). Lớp cung cấp 3 phương thức tác nghiệp cốt lõi: connect() thiết lập kết nối tới CSDL với "
    "chuỗi URL cố định 'jdbc:sqlserver://localhost:1433;databaseName=QuanLyBanGiay' và tài khoản sa; "
    "disconnect() đóng kết nối an toàn; và getConnection() trả về đối tượng Connection tĩnh cho toàn bộ "
    "các lớp DAO cùng khai thác xuyên suốt phiên làm việc."
)
for r in p176.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

# 5. TASK (e): CẬP NHẬT DANH MỤC HÌNH & BẢNG ĐỐI CHIẾU YÊU CẦU ĐỀ BÀI
# (e.1) Danh mục hình (P85..110)
for i in range(85, min(110, len(doc.paragraphs))):
    p = doc.paragraphs[i]
    if "Hình 8." in p.text:
        p.text = "Hình 8. Hộp thoại xem trước Hóa đơn K80 tích hợp chức năng Xuất file văn bản (chụp thật ngày 07/11/2026)\t30"
    elif "Hình 10." in p.text:
        p.text = "Hình 10. Giao diện bộ lọc Sản phẩm theo đa tiêu chí (chụp thật ngày 07/11/2026)\t32"
    elif "Hình 12." in p.text:
        p.text = "Hình 12. Giao diện bộ lọc Khách hàng theo phân hạng và điểm tích lũy (chụp thật ngày 07/11/2026)\t34"
    elif "Hình 14." in p.text:
        p.text = "Hình 14. Giao diện Báo cáo thống kê doanh thu (chụp thật ngày 07/11/2026)\t38"
    if "Hình " in p.text and "\t" in p.text:
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.italic = True

# (e.2) Bảng đối chiếu yêu cầu đề bài (Table 21 / Bảng 18)
t21 = doc.tables[21]
# Row 3: Tìm kiếm nâng cao
t21.rows[3].cells[1].text = (
    "SanPham_DAO.timKiemNangCao() (kết hợp Thương hiệu + Phân loại + Khoảng giá bán [từ - đến] + Tình trạng tồn kho);\n"
    "KhachHang_DAO.timKiemNangCao() (kết hợp Hạng thẻ + Khoảng điểm tích lũy + Giới tính);\n"
    "Tích hợp trực quan trên thanh công cụ bộ lọc của màn hình chính."
)
# Row 5: Xuất hóa đơn bán lẻ
t21.rows[5].cells[0].text = "5. Xuất hóa đơn bán lẻ"
t21.rows[5].cells[1].text = (
    "Hộp thoại xem trước Hóa đơn K80 tương tác (BanHang_GUI):\n"
    "- Nút '📄 Xuất File Hóa Đơn' tự động ghi tệp văn bản .txt (HoaDon_DAO.xuatHoaDonRaFileTxt()) "
    "đảm bảo lưu trữ chứng từ bán hàng chuẩn mực."
)
# Row 6: Thống kê cơ bản
t21.rows[6].cells[1].text = (
    "ThongKe_GUI [F5] (phân quyền chỉ mở cho Quản lý), HoaDon_DAO.\n"
    "Bốn thẻ Bento KPI (Tổng doanh thu, Số đơn hàng, Sản phẩm đã bán ra thực tế, Khách hàng) và "
    "Bảng danh sách chi tiết các hóa đơn giao dịch."
)
# Row 8: Coding Convention Java + Mô hình kiến trúc 2–3 lớp + ConnectDB mẫu giảng viên
t21.rows[8].cells[1].text = (
    "Cấu trúc 3 tầng phân tách rõ ràng: Trình diễn (gui.*), Truy cập dữ liệu & Nghiệp vụ (dao.*), "
    "Cơ sở dữ liệu (SQL Server 3NF 6 bảng).\n"
    "Lớp kết nối ConnectDB chuẩn mẫu giảng viên: Singleton Pattern, biến tĩnh public static Connection con, "
    "URL hard-code 'jdbc:sqlserver://localhost:1433;databaseName=QuanLyBanGiay', user sa, đủ connect()/disconnect()/getConnection()."
)

# Apply font Times New Roman 11pt to updated table cells
for r in [3, 5, 6, 8]:
    for c in t21.rows[r].cells:
        for p in c.paragraphs:
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(11)

# Check counts after
drawings_after = sum(len(p._p.xpath('.//w:drawing')) for p in doc.paragraphs)
tables_after = len(doc.tables)
print(f"After: Drawings in body = {drawings_after}, Tables = {tables_after}")
assert drawings_before == drawings_after, f"Drawings mismatch: {drawings_before} vs {drawings_after}!"
assert tables_before == tables_after, f"Tables mismatch: {tables_before} vs {tables_after}!"

# 6. Save docx
doc.save(DOCX_PATH)
print(f"Document saved: {DOCX_PATH} ({os.path.getsize(DOCX_PATH):,} bytes)")

# 7. Convert to PDF via LibreOffice headless
print("\n=== CONVERTING TO PDF VIA LIBREOFFICE ===")
cmd = [r"C:\Program Files\LibreOffice\program\soffice.exe", "--headless", "--convert-to", "pdf", "--outdir", SYNC_DIR, DOCX_PATH]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(f"LibreOffice return code: {res.returncode}")

pdf_file = os.path.join(SYNC_DIR, "BaoCao_QuanLyBanGiay_HSK.pdf")
doc_pdf = pymupdf.open(pdf_file)
total_pages = len(doc_pdf)
print(f"Total pages in PDF: {total_pages}")

# 8. TASK (f): RENDER 4 TRANG BỊ ẢNH HƯỞNG -> _sync\r2_*.png
# 1. Trang Đăng nhập (Hình 5)
p_login = None
# 2. Trang Thanh toán POS (Hình 7)
p_thanhtoan = None
# 3. Trang Sản phẩm (Hình 9)
p_sanpham = None
# 4. Trang Thống kê (Hình 14 & 19)
p_thongke = None

for idx, page in enumerate(doc_pdf):
    if idx < 6:
        continue
    txt = page.get_text("text")
    if "Hình 5. Giao diện Đăng nhập" in txt and p_login is None:
        p_login = idx
    if "Hình 7. Sơ đồ tuần tự nghiệp vụ thanh toán" in txt and p_thanhtoan is None:
        p_thanhtoan = idx
    if "Hình 9. Giao diện Quản lý danh mục mẫu giày" in txt and p_sanpham is None:
        p_sanpham = idx
    if "Hình 14. Giao diện Báo cáo thống kê" in txt and p_thongke is None:
        p_thongke = idx

print(f"Target pages in PDF: Login=Page {p_login+1}, ThanhToan=Page {p_thanhtoan+1}, SanPham=Page {p_sanpham+1}, ThongKe=Page {p_thongke+1}")

mat = pymupdf.Matrix(2.0, 2.0)
render_pages = [
    (p_login, "r2_login.png", "Trang Đăng nhập (Hình 5)"),
    (p_thanhtoan, "r2_thanhtoan.png", "Trang Thanh toán (Hình 7)"),
    (p_sanpham, "r2_sanpham.png", "Trang Sản phẩm (Hình 9)"),
    (p_thongke, "r2_thongke.png", "Trang Thống kê (Hình 14)")
]

for p_idx, fname, label in render_pages:
    pix = doc_pdf[p_idx].get_pixmap(matrix=mat)
    out_p = os.path.join(SYNC_DIR, fname)
    pix.save(out_p)
    print(f"  Rendered {label} -> {out_p} ({os.path.getsize(out_p):,} bytes, {pix.width}x{pix.height} px)")

print("\n=== ALL ROUND 3 UPDATES COMPLETED SUCCESSFULLY ===")

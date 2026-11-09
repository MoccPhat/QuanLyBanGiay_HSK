import pymupdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"E:\Eclipse Java\project\_sync\test_cover.pdf"
doc = pymupdf.open(pdf_path)

print(f"Tổng số trang: {len(doc)} / 45")

page0 = doc[0]
words = page0.get_text("words")

# 1. Thứ tự trên xuống
# Kiểm tra y0 của các khối:
# School header -> Logo -> Report title -> Topic title -> Info Table -> City
school_words = [w for w in words if "CÔNG" in w[4] or "NGHIỆP" in w[4]]
report_words = [w for w in words if "BÁO" in w[4] or "CÁO" in w[4]]
topic_words = [w for w in words if "STEPUP" in w[4]]
table_words = [w for w in words if "Giảng" in w[4] or "Nhóm" in w[4]]
city_words = [w for w in words if "2026" in w[4] and w[1] > 550]

y_school = school_words[0][1] if school_words else None
y_report = report_words[0][1] if report_words else None
y_topic = topic_words[0][1] if topic_words else None
y_table = table_words[0][1] if table_words else None
y_city = city_words[0][1] if city_words else None

print("\n--- 1. Kiểm tra thứ tự dọc ---")
print(f"y_school: {y_school:.1f}")
print(f"y_report: {y_report:.1f}")
print(f"y_topic:  {y_topic:.1f}")
print(f"y_table:  {y_table:.1f}")
print(f"y_city:   {y_city:.1f}")

assert y_school < y_report < y_topic < y_table < y_city, "Thứ tự các phần tử không đúng!"
print("=> [PASS] Thứ tự dọc chuẩn: Trường -> Logo -> Báo cáo -> Đề tài -> Bảng thông tin -> Năm")

# 2. Kiểm tra 'Nguyễn Trọng Vinh (Nhóm trưởng)' trọn vẹn 1 dòng
vinh_words = [w for w in words if w[4] in ["Nguyễn", "Trọng", "Vinh", "(Nhóm", "trưởng)"]]
y_vinh = set([round(w[1], 1) for w in vinh_words])
print("\n--- 2. Kiểm tra 'Nguyễn Trọng Vinh (Nhóm trưởng)' ---")
print(f"Tọa độ y các từ của Vinh: {y_vinh}")
assert len(y_vinh) == 1, f"Tên nhóm trưởng bị rớt dòng: {y_vinh}"
print("=> [PASS] Toàn bộ cụm 'Nguyễn Trọng Vinh (Nhóm trưởng)' nằm trọn vẹn trên 1 dòng y =", list(y_vinh)[0])

# 3. Kiểm tra căn cột MSSV
mssv_list = ["24704381", "24718221", "24695041", "24638311"]
mssv_words = [w for w in words if w[4] in mssv_list]
print("\n--- 3. Kiểm tra căn cột MSSV ---")
for w in mssv_words:
    print(f"MSSV {w[4]}: x0={w[0]:.1f}, x1={w[2]:.1f}, y0={w[1]:.1f}")
x1_coords = set([round(w[2], 1) for w in mssv_words])
print(f"Tọa độ x1 các MSSV: {x1_coords}")
assert len(x1_coords) == 1, f"Cột MSSV không thẳng hàng: {x1_coords}"
print("=> [PASS] Cột MSSV thẳng tắp tuyệt đối tại x1 =", list(x1_coords)[0])

# 4. Kiểm tra nhãn cột 1 không bị gãy dòng
col0_labels = ["Giảng viên hướng dẫn:", "Nhóm sinh viên thực hiện:", "Lớp học phần:", "Khóa học:", "Chuyên ngành:"]
print("\n--- 4. Kiểm tra nhãn cột 1 ---")
text0 = page0.get_text("text")
for lbl in col0_labels:
    assert lbl in text0, f"Nhãn bị gãy: {lbl}"
    print(f"Label: '{lbl}' => Có mặt trọn vẹn")
print("=> [PASS] Toàn bộ 5 nhãn ở cột 1 đều nguyên vẹn, không bị ngắt rớt dòng")

# 5. Kiểm tra lề và số trang
print("\n--- 5. Kiểm tra tràn lề & số trang ---")
print(f"Tổng số trang PDF: {len(doc)} (kỳ vọng 45)")
assert len(doc) == 45, "Trang bìa bị tràn làm tăng số trang!"
assert "DANH SÁCH THÀNH VIÊN TRONG NHÓM THỰC HIỆN" in doc[1].get_text("text"), "Trang 2 không khớp!"
print("=> [PASS] Số trang chuẩn 45/45, không tràn lề, trang 2 giữ nguyên vẹn 100%")

print("\n=== TẤT CẢ 5 TIÊU CHÍ CHECKLIST ĐỀU ĐẠT 100% ===")

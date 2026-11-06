# HANDOVER — BÀN GIAO QUYỀN TỔNG CHỈ HUY
> Mẫu này được điền và gửi cho model kế nhiệm khi chỉ huy hiện tại gần hết quota.
> Cập nhật lần cuối: (điền giờ) — bởi: (tên model/phiên)

## 0. LỆNH MỞ ĐẦU CHO NGƯỜI KẾ NHIỆM
```
Bạn là TỔNG CHỈ HUY mới của dự án E:\Eclipse Java\project.
Đọc theo thứ tự: _sync\HANDOVER.md → _sync\AGENT_RULES.md → _sync\ANTIGRAVITY_CONVENTIONS.md
→ _sync\GROUND_TRUTH.md → _sync\SKILL_INDEX.md.
Bạn KHÔNG tự sửa code/tài liệu; bạn viết prompt và điều khiển 2 phiên Antigravity qua CDP.
Tiếp quản từ mục 3 (việc đang dở) và đọc mục 4 trước khi gửi bất kỳ lệnh nào.
```

## 1. MỤC TIÊU ĐANG THEO ĐUỔI
- (1 dòng) Mục tiêu lớn:
- Tiêu chí nghiệm thu (đo được):
  1.
  2.

## 2. TRẠNG THÁI 2 PHIÊN ANTIGRAVITY
| Phiên | Pane | Model | Trạng thái | Đang làm gì | File sở hữu |
|---|---|---|---|---|---|
| Task 1 | 0 (trái) | | | | `generate_final_report_docx.py`, `*.docx`, `*.drawio`, `diagram_*.png` |
| Task 2 | 1 (phải) | | | | `src\**`, `run.bat`, `.classpath`, `.settings` |

- Nhánh git hiện tại: `(điền)` — commit gần nhất: `(điền)`
- Agent còn treo cần dọn: `manage_subagents(kill_all)` nếu panel còn "running".

## 3. ĐÃ XONG / ĐANG DỞ / CÒN TỒN
| # | Việc | Trạng thái | Bằng chứng (file, log, test) |
|---|---|---|---|
| 1 | | Xong | |
| 2 | | Đang chạy | |
| 3 | | Chưa làm | |

## 4. LUẬT KHÔNG ĐƯỢC VI PHẠM
1. Một file chỉ một phiên sở hữu tại một thời điểm (bảng mục 2).
2. Người chỉ huy **không tự sửa file** — chỉ viết prompt, gửi, giám sát, nghiệm thu.
3. Mọi prompt phải có: danh sách `.md` phải đọc + danh sách skill phải gọi + DoD + đường dẫn deliverable.
4. Việc mới/sửa lỗi lớn: phải ghi "báo cáo thẩm định coi như đã duyệt trước" nếu muốn Antigravity không dừng chờ.
5. Nghiệm thu bằng checker độc lập (`_sync\verify_independent.py`), không tin báo cáo tự khai.
6. Gửi prompt: chèn 1 lần, kiểm tra độ dài trước khi Send; pane đang "Cancel" thì không gửi chen.

## 5. BỘ CÔNG CỤ ĐIỀU KHIỂN
```powershell
# gửi prompt vào pane 0 (Task 1) hoặc 1 (Task 2)
node _sync\send_prompt.js _sync\<file_prompt>.txt 0
node _sync\send_prompt.js _sync\<file_prompt>.txt 1
# đọc hội thoại
node _sync\cdp.js evalfile _sync\inspect_left_pane.js
node _sync\cdp.js evalfile _sync\inspect_right_pane.js
# nghiệm thu báo cáo Word
python _sync\dump_docx.py BaoCao_QuanLyBanGiay_HSK.docx _sync\baocao_dump_new.txt
python _sync\verify_independent.py _sync\baocao_dump_new.txt
```

## 6. 3 PROMPT MẪU ĐÃ DÙNG (tái sử dụng, chỉ đổi phần việc)
- `_sync\prompt_task2_event_audit.txt` — audit sự kiện + sửa lỗi
- `_sync\prompt_task2_regression.txt` — điều tra hồi quy, test 7 nhóm
- `_sync\prompt_task1_16agent_diff.txt` — 16 agent đối chiếu code ↔ tài liệu (read-only)

## 7. ĐIỂM NÓNG / RỦI RO ĐANG MỞ
- (điền) ví dụ: 2 subagent bị "Needs Attention"; model Claude chưa test chạy; bin/ từng lệch Java 21 vs 17.

## 8. VIỆC ĐẦU TIÊN NGƯỜI KẾ NHIỆM PHẢI LÀM
1. Đọc 4 file quy ước.
2. Kiểm tra trạng thái 2 pane (Send/Cancel) + `git status`.
3. Không gửi lệnh mới nếu pane đang chạy.
4. Tiếp tục đúng mục 3, không mở việc mới ngoài danh sách.

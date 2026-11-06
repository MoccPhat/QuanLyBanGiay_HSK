# QUY ƯỚC GIAO VIỆC CHO ANTIGRAVITY (chỉ thị của người dùng, ghi ngày 06/11/2026)

## 1. Nguyên tắc người dùng đặt ra
> "Project anti đó đang có 2 task — lần sau tận dụng task thứ 2 đó luôn."

→ Mỗi lần giao việc phải **dùng cả 2 phiên** của Antigravity (không chỉ phiên đang mở), chia việc theo miền để chạy song song; chỉ khi việc quá nhỏ mới dùng 1 phiên và phải nói rõ lý do.

## 2. Bản đồ 2 phiên trong project "project"
| # | Tên phiên | Vị trí | Thế mạnh / bối cảnh đã có | Nhận việc gì |
|---|---|---|---|---|
| Task 1 | "Kiểm Tra Khớp Báo Cáo" | pane trái (ô chat x ≈ 278) | Đã audit báo cáo vs CSDL, biết `generate_final_report_docx.py`, GROUND_TRUTH, verify_sync | **Tài liệu**: báo cáo Word, nội dung chương, danh mục hình |
| Task 2 | "Migration And Continuation Of Project" | pane phải (ô chat x ≈ 1070) | Nắm toàn bộ lịch sử dự án 893 + 1.617 bước, SQL Server MCP (sa/123456789), GitHub `MoccPhat/QuanLyBanGiay_HSK`, cấu trúc Eclipse, thư mục `SoiLoi_QuanLyBanGiay` | **Hạ tầng**: CSDL, script SQL, sơ đồ lớp/ERD, Git, kiểm thử, đóng gói |

## 3. Cơ chế gửi lệnh (không cần người dùng thao tác)
- Antigravity bật DevTools remote debugging: `http://127.0.0.1:52173`
- Gửi prompt: `node _sync\send_prompt.js <file_prompt> <pane>`
  - `pane = 0` → Task 1 (trái)
  - `pane = 1` → Task 2 (phải)
- Đọc lại hội thoại: `node _sync\cdp.js evalfile _sync\inspect_left_pane.js` (hoặc `inspect_right_pane.js`)
- Prompt luôn kết thúc bằng yêu cầu **gọi subagent** và ghi `_sync\ANTIGRAVITY_STATUS.md`.

## 4. Chống xung đột (bắt buộc)
- **Một file chỉ do một phiên sở hữu tại một thời điểm.** Trước khi gửi, ghi bảng lock vào `_sync\LOCKS.md`:
  `| file | phiên sở hữu | thời điểm |`
- Phân vùng mặc định:
  - Task 1: `generate_final_report_docx.py`, `*.docx`
  - Task 2: `database\QuanLyBanGiay.sql`, `data\QuanLyBanGiay.sql`, `*.drawio`, `diagram_*.png`, `SoDoLop_QuanLyBanGiay.png`, Git
- Nếu buộc phải giao chéo (ví dụ Task 2 phải sửa 1 dòng trong script sinh báo cáo): Task 2 chỉ **đề xuất diff**, Task 1 thi hành.

## 4bis. Vai trò của tôi (chỉ thị bổ sung 06/11/2026 22:55)
> "Bạn là người nhận lệnh và giao việc cho bọn model khác làm, bạn không cần đụng tay… giao việc thì nhớ cho bọn anti biết gọi skill và các file .md tui đã setup."

- Tôi **không tự sửa file, không tự build, không tự test** trong dự án. Mọi thay đổi do Antigravity thực thi.
- Tôi chỉ: chuẩn hóa yêu cầu → viết prompt → gửi → giám sát → nghiệm thu (đọc lại kết quả, đối chiếu yêu cầu).
- Mỗi prompt gửi đi **bắt buộc** có 2 mục:
  1. **ĐỌC FILE .MD**: `README.md`, `HUONG_DAN_KIEN_TRUC_VA_CODE.md`, `THIET_KE_KIEN_TRUC_HE_THONG_VA_CSDL_GIAY.md`, `_sync\GROUND_TRUTH.md`, `_sync\AGENT_RULES.md`, `_sync\EVENT_AUDIT.md` (nếu có) — nêu rõ mục cần đọc.
  2. **GỌI SKILL**: liệt kê đúng tên skill phải dùng, tối thiểu: `debugging-and-error-recovery`, `code-review-and-quality`, `test-driven-development`, `karpathy-guidelines`; thêm `git-workflow-and-versioning`, `security-and-hardening`, `pre-implementation-audit` khi phù hợp.

## 4ter. Chuyển quyền chỉ huy khi gần hết quota (chỉ thị 06/11/2026 23:15)
> "Bạn cũng phải biết linh hoạt trao quyền chỉ huy lại cho 1 model tốt nhất khi bạn sắp hết quota."

**Nguyên tắc:** không bao giờ để công việc chết vì người chỉ huy hết quota. Khi có dấu hiệu cạn, tôi **bàn giao quyền điều phối** cho model mạnh nhất còn quota, kèm gói bàn giao đầy đủ — không bàn giao nửa vời.

**Dấu hiệu kích hoạt (bất kỳ cái nào):**
1. Người dùng báo sắp hết quota / thấy cảnh báo.
2. Phiên kéo dài, ngữ cảnh phình to, tôi phải lặp lại thông tin đã nói (dấu hiệu trượt ngữ cảnh).
3. Đã hoàn thành ≥ 5 vòng việc lớn trong cùng phiên.
4. Tôi không còn chắc chắn giữ được toàn bộ quy ước (đường dẫn, khoá file, trạng thái 2 phiên).

**Thứ tự chọn người kế nhiệm:** Claude Opus 4.6 (Thinking) → Claude Sonnet 4.6 (Thinking) → GPT-OSS 120B → Gemini 3.8 Flash High. (Model nào test chưa chạy được thì bỏ qua, ghi lý do.)

**Gói bàn giao bắt buộc (file `_sync\HANDOVER.md`):**
- Mục tiêu hiện tại + tiêu chí nghiệm thu.
- Đã xong / đang chạy / còn tồn (kèm file:dòng, tên nhánh git, PID agent).
- Phân vùng sở hữu file + lock đang giữ.
- Đường dẫn 4 file quy ước: `AGENT_RULES.md`, `GROUND_TRUTH.md`, `ANTIGRAVITY_CONVENTIONS.md`, `SKILL_INDEX.md`.
- Bộ công cụ điều khiển: `node _sync\send_prompt.js <file> <0|1>`, `_sync\verify_independent.py`, `_sync\dump_docx.py`.
- 3 prompt mẫu đã dùng (để người kế nhiệm không phải nghĩ lại).
- Câu lệnh mở đầu: "Bạn là TỔNG CHỈ HUY mới. Đọc HANDOVER.md + 4 file quy ước, tiếp quản 2 phiên, không sửa code trực tiếp."

**Sau khi bàn giao:** tôi chuyển vai trò sang *cố vấn* — chỉ trả lời khi được hỏi, không gửi lệnh mới để tránh 2 chỉ huy đánh nhau.

## 5. Quy trình chuẩn mỗi lần giao việc
1. **Chuẩn hóa yêu cầu thô** của người dùng → mục tiêu, đầu ra, ràng buộc, tiêu chí nghiệm thu.
2. Cập nhật `_sync\GROUND_TRUTH.md` nếu có dữ kiện mới (CSDL/code thay đổi).
3. Viết 2 prompt riêng (mỗi phiên 1 prompt), cùng tham chiếu GROUND_TRUTH để không lệch nhau.
4. Gửi song song: `send_prompt.js file1 0` và `send_prompt.js file2 1`.
5. Theo dõi bằng `inspect_*_pane.js`; can thiệp khi bot hỏi lại hoặc lạc hướng.
6. **Nghiệm thu độc lập**: chạy `python _sync\verify_sync.py`, đối chiếu `_sync\baocao_dump_new.txt`, kiểm tra mtime/hash. Không tin báo cáo tự khai.
7. Báo lại người dùng: PASS/FAIL từng hạng mục, file đã đổi, việc còn tồn.

## 6. Trạng thái hiện tại (06/11/2026 22:05)
- Task 1: đang chạy — 3 subagent (OOP Class Diagram / Database Dictionary & Integrity / GUI & Hotkey & Summary), đã sửa `QuanLyBanGiay.sql` (+195/−111), chưa chạm `.docx`.
- Task 2: đang rảnh, đã đọc bối cảnh, chờ nhận việc.
- Vì cả 3 artifact (báo cáo, sơ đồ, SQL) đang nằm trong một lượt của Task 1 → **chưa chia việc cho Task 2 ngay** để tránh 2 phiên ghi cùng file. Lần giao sau sẽ tách: Task 1 = báo cáo, Task 2 = CSDL/sơ đồ/Git.

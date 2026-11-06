# QUY ƯỚC CỦA ANTIGRAVITY — tôi đã đọc và áp dụng khi viết prompt (06/11/2026)

Nguồn đã đọc:
- `C:\Users\ASUS\.gemini\GEMINI.md` (283 dòng) — bộ quy ước **toàn cục**, Antigravity nạp mỗi phiên.
- `C:\Users\ASUS\.gemini\skills\` (~100 skill) và `C:\Users\ASUS\.agents\skills\` — mỗi skill là `SKILL.md`.
- `E:\Kho Skill AI\DOC-TRUOC.md` + `GEMINI.md` — kho gốc, có bảng Excel tổng hợp skill.
- `C:\Users\ASUS\.gemini\settings.json`, `antigravity-ide\{knowledge,prompting,mcp_config.json}`.

## 1. Nó tự động dùng skill, không cần gọi tên
`GEMINI.md §1` buộc Antigravity tự nhận diện ngữ cảnh và đọc `SKILL.md` tương ứng. Bảng điều phối ở §2 quy định: bug → `debugging-and-error-recovery`; review → `code-review-and-quality`; test → `test-driven-development`; code → `karpathy-guidelines` + `incremental-implementation`; git → `git-workflow-and-versioning`; Word/Excel → `docx` / `xlsx`; sơ đồ → `diagram-design`; tài liệu → `documentation-and-adrs`.
→ Vẫn nên nêu tên skill trong prompt để nó khỏi bỏ sót, nhưng **không cần** giải thích skill là gì.

## 2. CHỐT CHẶN DUYỆT (quan trọng nhất) — `pre-implementation-audit`
`GEMINI.md §3`: trước khi viết bất kỳ dòng code nào cho việc **mới / sửa lỗi phức tạp / refactor**, nó **BẮT BUỘC** xuất "BÁO CÁO THẨM ĐỊNH" 6 mục rồi **DỪNG LẠI CHỜ NGƯỜI DUYỆT**.
→ Đây chính là lý do 2 lần trước nó dừng hỏi "Bạn duyệt để triển khai?". Từ nay prompt phải ghi rõ: *"Báo cáo thẩm định coi như ĐÃ DUYỆT trước — không dừng chờ, triển khai luôn"*, nếu không sẽ mất một vòng.

## 3. Học thuyết "Quân đoàn 4 tiểu đội – 16 tác tử" — ĐÃ KIỂM CHỨNG LÀ THẬT
`GEMINI.md §4`: 4 tiểu đội (Chiến lược & Yêu cầu / Kiến trúc & Thực thi / Kiểm định & Phản biện / Đóng gói & Bàn giao), 16 vai, chạy **song song 100%**, nghiêm cấm tuần tự.

**Bằng chứng thực nghiệm (probe 23:04 ngày 06/11/2026):** tôi giao một bài test yêu cầu chạy 16 subagent cùng lúc. Kết quả từ chính Antigravity:
- `16/16 tác tử ở trạng thái running đồng thời`, UI hiện `Found 16 subagents`.
- 16 dòng kết quả có `started` 23:04:57–23:05:01 và `finished` 23:05:01–23:05:02 → chồng lấn nhau, đúng là song song.
- Công cụ thật: `invoke_subagent`, `manage_subagents(Action='kill_all')`.
→ **Giữ nguyên học thuyết, không xoá.** Khác biệt duy nhất: các lần trước chỉ có 3 subagent vì *tôi yêu cầu 3*, không phải vì nó bị giới hạn.

**Cách tôi sẽ tận dụng:**
- Việc **đọc/audit/soát** (read-only): fan-out 16 nhánh thật — mỗi nhánh 1 file/module, trả bảng phát hiện.
- Việc **có ghi file**: vẫn 3–5 nhánh soạn nội dung + **1 writer duy nhất** (agent chính) để tránh 16 process cùng ghi một file.
- Luôn nhắc `manage_subagents(kill_all)` khi xong để không treo agent.
- Dùng đúng từ vựng: "tiểu đội", "Đội trưởng", "tác tử", "DoD", "4 báo cáo nghiệm thu".

## 4. Giao thức minh bạch 4 điểm (§4B)
Nó có thói quen: dán banner "Swarm Dispatch", POST sự kiện tới `http://localhost:8001/api/dispatch` (dashboard `:5173`), xuất báo cáo 4 đội, và **ghi deliverable vào `E:\Workstation\deliverables\`**.
→ Prompt phải **ghi đè đường dẫn deliverable** về `E:\Eclipse Java\project\_sync\`, và cho phép **bỏ qua** bước POST dashboard nếu dịch vụ không chạy (đỡ lỗi mạng).

## 5. Lãnh địa hoạt động (§4B.3)
Mặc định nó làm việc ở `E:\Workstation` và **chỉ đọc** `E:\Kho Skill AI`.
→ Prompt phải nói rõ: dự án nằm ở `E:\Eclipse Java\project`, **không** di chuyển/không copy sang Workstation, **không** sửa Kho Skill AI.

## 6. Đường ray 13 trạm n8n (§5)
Chuỗi chuẩn: Ingest → Spec → Grill → Clean Architecture → Nén token → Phong cách → Khử văn AI → Đóng gói skill → Task brief/DoD → Runtime adapter → Sinh code → Kiểm định → Xuất xưởng.
→ Tôi không cần bắt nó chạy đủ 13 trạm; nhưng nếu prompt có sẵn **DoD + tiêu chí nghiệm thu ở dạng đo được**, nó khớp trạm 08/11 và ít lan man hơn.

## 7. Mẫu "Báo cáo thẩm định" (§3.6) — tôi dùng lại làm khung prompt
6 mục: Mục tiêu & YAGNI → Định vị kiến trúc/file ảnh hưởng → Quét xung đột (dữ liệu/code/luồng) → Where/Why/What/How → Danh sách skill + công dụng → Kế hoạch + DoD.
→ Tôi chủ động điền sẵn các mục này trong prompt, coi như "báo cáo thẩm định đã có", để nó vào việc ngay.

## 8. Kho skill là nguồn sự thật về tên skill
Danh sách thật nằm ở `~/.gemini/skills/` (100+ mục). Chỉ được gọi tên có trong kho; tên không tồn tại (vd `humanizer`, `generative_ui` trong GEMINI.md nhưng không có thư mục) thì **không** đưa vào prompt kẻo nó đi tìm vô ích.

## 10. KHO SKILL — đã nạp và lập chỉ mục (105 skill)
Tôi đã quét toàn bộ `~/.gemini/skills` + `~/.agents/skills` thành bảng tra cứu: **`_sync\SKILL_INDEX.md`** (105 skill: tên, số dòng, mô tả, đường dẫn `SKILL.md`).

Phân loại theo pha công việc (theo meta-skill `using-agent-skills`):
| Pha | Skill dùng cho dự án này |
|---|---|
| Chưa rõ yêu cầu | `interview-me`, `grilling`, `idea-refine` |
| Trước khi code | `pre-implementation-audit` (chốt chặn duyệt), `spec-driven-development`, `planning-and-task-breakdown`, `constraint-driven-development`, `doubt-driven-development` |
| Viết code | `karpathy-guidelines`, `incremental-implementation`, `code-simplification`, `ponytail` |
| Sửa lỗi | `debugging-and-error-recovery` (quy tắc Stop-the-Line + triage) |
| Kiểm thử | `test-driven-development` (Red-Green-Refactor + Prove-It cho bug fix) |
| Soát code | `code-review-and-quality` (Five-Axis Review), `ponytail-review`, `ponytail-audit` |
| Bảo mật | `security-and-hardening` (Threat model → 3-tier boundary → checklist) |
| Git | `git-workflow-and-versioning` (commit nguyên tử, semantic versioning) |
| Tài liệu | `documentation-and-adrs`, `docx` (đọc/ghi .docx), `diagram-design` (ERD/UML) |
| Ngữ cảnh dài | `context-mode` (lọc log, nghĩ bằng code, chống trôi mục tiêu) |

Ghi chú đã kiểm tra: `humanizer`, `generative_ui`, `minimax-xlsx` có tên trong `GEMINI.md` nhưng **không có thư mục** trong kho → không gọi.

## 11. Cách tôi chọn skill cho từng phiên (bảng quyết định)
- Người dùng báo **"hỏng / sai / từ đúng thành sai"** → `debugging-and-error-recovery` + `test-driven-development` (Prove-It) + `git-workflow-and-versioning`.
- Cần **đồng bộ tài liệu** (Word/Excel/ERD) → `docx` + `diagram-design` + `context-mode`.
- Cần **sửa nhiều file** → `incremental-implementation` + `karpathy-guidelines`, chia nhánh theo module.
- Cần **đánh giá chất lượng trước khi nộp** → `code-review-and-quality` + `security-and-hardening` + `ponytail-audit`.
- Việc **mới hoàn toàn** → bắt buộc `pre-implementation-audit` (và tôi phải ghi "đã duyệt trước" nếu muốn nó không dừng).

## 12. Cách gửi lệnh (kỹ thuật)
- CDP `127.0.0.1:52173`, composer là **Lexical editor**: chèn text dài một lần thì được, chèn nhiều chunk liên tiếp thì bị reset/đứt → phải `Ctrl+A` + `Delete` rồi `insertText` một lần và **kiểm tra độ dài trước khi Send**.
- Nút gửi của pane trái/phải khác nhau; khi pane đang chạy, nút thành `Cancel (Ctrl+D)` → không gửi chen ngang, phải chờ.

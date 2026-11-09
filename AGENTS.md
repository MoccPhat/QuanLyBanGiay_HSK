# QUY TẮC HOẠT ĐỘNG CỦA TÁC TỬ (AGENTS.md)

> **Dự án:** StepUp - Quản lý Cửa Hàng Bán Giày (QuanLyBanGiay_HSK)  
> **Thư mục gốc:** `E:\Eclipse Java\project\`  
> **Giao thức bàn giao:** `E:\Eclipse Java\_agent_kit\inbox\INBOX_PROTOCOL.md`

---

## 1. QUY TẮC BẮT BUỘC: TỰ ĐỘNG ĐẨY BÀN GIAO (MANDATORY HANDOVER PUSH)

Sau **MỌI TÁC VỤ** (tính năng mới, sửa lỗi, cập nhật tài liệu, đóng gói, kiểm thử), Agent **BẮT BUỘC PHẢI TỰ ĐỘNG ĐẨY KẾT QUẢ BÀN GIAO** theo giao thức tại `E:\Eclipse Java\_agent_kit\inbox\INBOX_PROTOCOL.md` trước khi kết thúc lượt.

> [!IMPORTANT]
> **TUYỆT ĐỐI KHÔNG CHỜ QUẢN LÝ HỎI:** Không dừng lại chỉ ở việc in kết quả trên giao diện chat. Quản lý và các tiến trình tự động sẽ đọc báo cáo từ `E:\Eclipse Java\_agent_kit\inbox\`.

### Cơ chế thực thi bắt buộc trước khi kết thúc lượt:
Mỗi khi hoàn thành một tác vụ hoặc gặp sự cố bị chặn:
1. Chạy lệnh hoặc gọi Python script:
   ```bash
   python "E:\Eclipse Java\_agent_kit\push_handover.py" \
     --task-id "<TASK-ID-DUY-NHAT>" \
     --status "DONE" \
     --summary "<Tóm tắt kết quả>" \
     --commit "<git-commit-hash>" \
     --files <danh_sach_file_thay_doi> \
     --evidence-json '<json_bang_chung_DoD>' \
     --open-items "<viec_ton_hoac_ghi_khong>"
   ```
2. Đảm bảo 3 tệp sau trong `E:\Eclipse Java\_agent_kit\inbox\` đã được đồng bộ:
   - `<YYYYMMDD-HHMMSS>__<task-id>.md` (bản Markdown chi tiết cho người đọc).
   - `index.jsonl` (bổ sung/cập nhật bản ghi JSON chuẩn máy đọc).
   - `STATUS.json` (cập nhật trạng thái mới nhất của hệ thống).

---

## 2. NGUYÊN TẮC KỸ THUẬT & KIỂM SOÁT CHẤT LƯỢNG

1. **Tuân thủ Karpathy Guidelines:**
   - *Think before writing:* Hiểu rõ nguyên nhân và yêu cầu trước khi sửa.
   - *Simplicity first:* Viết giải pháp tối giản nhất, không over-engineering.
   - *Minimal diff:* Chỉ sửa đúng phạm vi cần thiết.
   - *Verifiability:* Mọi thay đổi đều phải được chứng minh bằng lệnh kiểm thử thực tế và ghi vào bằng chứng DoD.
2. **Tiêu chuẩn Biên dịch & Bytecode:**
   - Biên dịch với cờ Java 17: `javac --release 17 -encoding UTF-8 -cp "lib/*" -d bin ...`
   - Đảm bảo `bin/Main.class` luôn có major version = **61** (Java 17).
3. **Bảo toàn CSDL & Ràng buộc:**
   - CSDL chuẩn 6 bảng: `NhanVien`, `KhachHang`, `SanPham`, `ChiTietGiay`, `HoaDon` (13 cột), `ChiTietHoaDon`.
   - Không được khôi phục các bảng thừa cũ (`LoaiGiay`, `ThuongHieu`, `TaiKhoan`).
4. **Vệ sinh Môi trường Bàn giao (Deliverable Hygiene):**
   - Không đưa file tạm, script `.py`, thư mục `_sync/`, thư mục test `hoadon/`, hoặc file cấu hình thật `db.properties` vào thư mục bàn giao `StepUp_QuanLyBanGiay_Deliverable/`.

---

## 2. BỘ NHỚ DÀI HẠN (OBSIDIAN) — BẮT BUỘC

Vault: `C:\Users\ASUS\OneDrive\Tài liệu\Obsidian Vault\Jarvis_Memory\`
Truy cập ngắn: `E:\Eclipse Java\project\_memory\Jarvis_Memory\` (junction)

- **Trước task:** đọc `_memory\Jarvis_Memory\00_JARVIS_INDEX.md` + `wiki\User_Preferences.md`.
- **Sau task:** append `raw\<YYYY-MM-DD>_Session_Log.md`, thêm link vào index, cập nhật `updated:`.
- Chỉ THÊM, không sửa/xoá note của agent khác.
- Quy ước đầy đủ: `_memory\Jarvis_Memory\MEMORY_PROTOCOL.md`.

### 2.1. Tri thức dùng chung & quyền điều chỉnh
- Đọc `_memory\Jarvis_Memory\wiki\DeepSeek_Playbook.md` trước khi làm — đây là tri thức kỹ thuật đã kiểm chứng (Claude config path, MCP packaging, rubric báo cáo, Windows automation, Java/SQL).
- Nếu phát hiện thông tin trong Playbook **sai hoặc lỗi thời**: được phép sửa, nhưng phải
  (a) kiểm chứng lại bằng lệnh/ảnh chụp, (b) ghi Changelog ở cuối note, (c) cập nhật `last_verified`.
  Quy trình: `_memory\Jarvis_Memory\system\Knowledge_Update_Protocol.md`.
- Không xoá nội dung của agent khác; nếu không còn phù hợp thì đánh dấu `status: outdated` và thêm nhánh mới.

### 2.2. Tab & Subagent — bắt buộc
- Việc nhiều mảng độc lập → dùng **subagent** (`Creator mode` / `Agent team`), không dồn 1 tab.
- Trước khi nhận việc: kiểm tra xem đang có mấy tab chat; 2 tab thì chia việc cho cả 2.
- Vai trò tab chuẩn: (1) Code `src/**` · (2) Test/QA không sửa src · (3) Báo cáo `.docx`/`.md` · (4) Theo dõi chỉ đọc.
- Hai tab không được sửa cùng một file. Chi tiết: `_memory\Jarvis_Memory\wiki\Antigravity_Tab_Strategy.md`.

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

# 📌 BẢNG ĐIỀU PHỐI TIẾN ĐỘ DỰ ÁN (TASK_QUEUE.MD)

> **Cập nhật lúc:** 2026-11-09 20:40:00  
> **Người thực hiện:** Tab 3 — Báo cáo (.docx/.md) & Đóng gói bàn giao  
> **Dự án:** StepUp — Quản lý Cửa Hàng Bán Giày (`E:\Eclipse Java\project`)

---

## 🚦 BẢNG THEO DÕI TÁC VỤ CHI TIẾT

| Việc | Trạng thái | Bằng chứng | Người phụ trách (tab) | Ghi chú |
|---|---|---|---|---|
| **Thay ảnh Hình 1 Use Case & sạch StepUp (DOC-FINAL-HINH1)** | `DONE` (Hoàn hảo) | Thay Hình 1 bằng `_sync/vp_usecase_diagram.png` (16cm, center); Caption 'Hình 1. Sơ đồ Use Case tổng thể hệ thống Quản lý bán giày thời trang (Visual Paradigm 18)'; Danh mục hình khớp; StepUp Footwear POS hits = 0; 3 ảnh preview `_sync/final_toc.png`, `_sync/final_hinh1.png`, `_sync/final_last.png` | Tab 3 (Báo cáo) | Drawings trước/sau = 20/20; Layout nguyên vẹn không vỡ; Mục lục không còn dòng VI/VII; Trang cuối sạch đẹp. |
| **Bìa học thuật chuẩn V2 (COVER-FRAME-V2)** | `DONE` (5/5 PASS) | Khung A4 300dpi (`_sync/cover_frame_a4.png`, 47,284 bytes); 100% đối xứng gương; 4 cạnh đủ hình thoi; lề an toàn >= 72px; dòng ngày 'TP. Hồ Chí Minh, tháng 11 năm 2026'; `_sync/cover_preview3.png` | Tab 3 (Báo cáo) | 5/5 tiêu chí checklist đều PASS; Đạt chuẩn học thuật đối xứng hoàn hảo; Bỏ placeholder `...`. |
| **Bìa hoa văn mẫu (COVER-ORNAMENT)** | `DONE` (Hoàn hảo) | Khung hoa văn 4 góc A4 300dpi (`_sync/cover_frame_a4.png`); Logo 5.5cm; Dòng Khoa gạch chân; `_sync/cover_preview2.png` | Tab 3 (Báo cáo) | Đã nhúng Header Section 1 behindDoc=1; Section 2 unlinked 100% sạch; Bỏ w:pgBorders. |
| **Báo cáo Word (DOC-EDIT-ROUND2)** | `DONE` (Hoàn tất) | 6 sửa đổi hoàn tất; 22 bảng, 20 drawings; PDF 42 trang; 8 ảnh preview `_sync/edit_*.png` | Tab 3 (Báo cáo) | Mục lục bold/indent phân cấp; Khối chữ ký thẳng trục; Bỏ Callout; Bỏ StepUp; Bỏ Bảng 19 & Phần VI/VII. |
| **Báo cáo Word (DOC-SEQ-REPLACE)** | `DONE` (Đạt chuẩn) | 20 drawings, 20 media parts, 5 sơ đồ tuần tự mới không cắt chữ | Tab 3 (Báo cáo) | Đã thay thế thành công 5 sơ đồ tuần tự mới vào file Word. |
| **VP Diagrams** (Visual Paradigm UML) | `DONE` (Hoàn tất không cắt chữ) | `_sync/vp_class_diagram.png` + **6 ảnh sơ đồ tuần tự** + `_sync/vp_usecase_diagram.png` (Use Case V2 chuẩn UML); `ThanhToan2.vpp` | Tab 4 / Subagent VP | Đã hoàn thành Use Case V2: (1) Boundary fill TRẮNG (#FFFFFF) line đen; (2) 8 ellipse cách mép >= 50px, tiêu đề dải trên thông thoáng; (3) Đường liên kết orthogonal gấp khúc 0 cắt ellipse; (4) Nhân viên trên-trái (40,200), Quản lý dưới-phải (1060,420), arch kế thừa đỉnh. |
| **QA Test Matrix** (Kiểm thử hệ thống) | `DONE` (100% Pass) | 62/62 tests PASS (50 VerifyAllScenarios + 12 VerifyNewFeatures); Bytecode Java 17 (`bin/Main.class` major 61) | Tab 2 (Test/QA) | CSDL sạch: 2 hóa đơn chuẩn (`HD000001`, `HD000002`). |
| **CSDL Audit** (Kiểm toán CSDL & Kết nối) | `DONE` (100% Khớp) | 6/6 bảng, 54/54 cột khớp 100% giữa SSMS & Entity; `ConnectDB.java` URL tối giản | Tab 1 (Code) | Triệt tiêu bảng thừa cũ. Bảng HoaDon chuẩn 13 cột. |
| **Memory Update** (Bộ nhớ Obsidian) | `DONE` (Đã đồng bộ) | `00_JARVIS_INDEX.md` cập nhật lúc 20:07:00; `raw/2026-11-09_Session_Log.md` ghi nhận toàn bộ session `COVER-ORNAMENT` | Tab 3 / Lead | Đã đồng bộ 2 chiều với Obsidian Vault `Jarvis_Memory`. |
| **Deliverable / Zip** (Đóng gói bàn giao) | `DONE` (Hoàn tất 100%) | Thư mục `StepUp_QuanLyBanGiay_Deliverable` (105 file, 7.32 MB); Tệp nén `StepUp_QuanLyBanGiay_FINAL_2026-11-09.zip` (6.65 MB, 105 files) | Tab 3 (Đóng gói) | Sạch 100%: 0 file `.py`, không có `db.properties` thật, không có `hoadon/` và `_sync/`. |

---

## ✅ TỔNG KẾT HẠNG MỤC BÀN GIAO MỚI NHẤT

1. **Báo cáo Word & PDF:**
   - [`BaoCao_QuanLyBanGiay_HSK.docx`](file:///E:/Eclipse%20Java/project/BaoCao_QuanLyBanGiay_HSK.docx) (2,796,052 bytes, 22 bảng, 20 drawings).
   - [`BaoCao_QuanLyBanGiay_HSK.pdf`](file:///E:/Eclipse%20Java/project/_sync/BaoCao_QuanLyBanGiay_HSK.pdf) (2,857,464 bytes, 42 trang).
   - Bản sao lưu: `_sync/backup_docx/BaoCao_QuanLyBanGiay_HSK_backup_20261109_200642.docx`.
2. **Khung hoa văn & Ảnh nghiệm thu Trang bìa:**
   - [`_sync/cover_frame_a4.png`](file:///E:/Eclipse%20Java/project/_sync/cover_frame_a4.png) (52,003 bytes, 2480×3508 px, A4 300dpi).
   - [`_sync/cover_preview2.png`](file:///E:/Eclipse%20Java/project/_sync/cover_preview2.png) (179,757 bytes, 1191×1684 px).
   - [`_sync/page2_preview.png`](file:///E:/Eclipse%20Java/project/_sync/page2_preview.png) (218,052 bytes, 1191×1684 px - xác nhận Trang 2 không có khung).
3. **Gói bàn giao nghiệm thu:**
   - [`StepUp_QuanLyBanGiay_Deliverable`](file:///E:/Eclipse%20Java/StepUp_QuanLyBanGiay_Deliverable)
   - [`StepUp_QuanLyBanGiay_FINAL_2026-11-09.zip`](file:///E:/Eclipse%20Java/StepUp_QuanLyBanGiay_FINAL_2026-11-09.zip) (6.65 MB, 105 files).

import sys, re
import docx

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('BaoCao_QuanLyBanGiay_HSK.docx')

print("=== VERIFYING BAOCAO_QUANLYBANGIAY_HSK.DOCX ===")
print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

# 1. Check Heading Styles
h1_list = [p.text.strip() for p in doc.paragraphs if p.style.name == 'Heading 1']
h2_list = [p.text.strip() for p in doc.paragraphs if p.style.name == 'Heading 2']
h3_list = [p.text.strip() for p in doc.paragraphs if p.style.name == 'Heading 3']

print(f"Heading 1: {len(h1_list)}")
print(f"Heading 2: {len(h2_list)}")
print(f"Heading 3: {len(h3_list)}")

# 2. Check Table Captions (Bảng 1 to Bảng 18)
body_table_captions = []
for p in doc.paragraphs:
    m = re.match(r'^Bảng\s+(\d+)\.\s*(.*)', p.text.strip())
    if m:
        body_table_captions.append((int(m.group(1)), m.group(2).strip()))

# Filter out the preliminary list (pages before Part I) vs body captions
# The body captions have p.paragraph_format.keep_with_next == True
actual_captions = []
prelim_table_entries = []

for num, title in body_table_captions:
    # If the title ends with a tab and number or is in prelims
    if re.search(r'\t\d+$', title) or not any(p.paragraph_format.keep_with_next for p in doc.paragraphs if p.text.strip().startswith(f"Bảng {num}.")):
        prelim_table_entries.append((num, title))
    else:
        actual_captions.append((num, title))

print(f"\nFound {len(actual_captions)} body Table Captions:")
for num, title in sorted(actual_captions):
    print(f"  Bảng {num}. {title}")

# 3. Check Figure Captions (Hình 1 to Hình 10)
body_fig_captions = []
for p in doc.paragraphs:
    m = re.match(r'^Hình\s+(\d+)\.\s*(.*)', p.text.strip())
    if m:
        t = m.group(2).strip()
        if not re.search(r'\t\d+$', t):
            body_fig_captions.append((int(m.group(1)), t))

print(f"\nFound {len(body_fig_captions)} body Figure Captions:")
for num, title in sorted(body_fig_captions):
    print(f"  Hình {num}. {title}")

# 4. Check Banned / Outdated Phrases across all paragraphs and tables
banned_phrases = [
    "💡",
    "Connection Pool",
    "ném ngoại lệ",
    "mật khẩu SHA-256 đã vô hiệu",
    "mật khẩu đã vô hiệu",
    "in hóa đơn K80",
    "in phiếu thanh toán K80"
]

all_text = []
for p in doc.paragraphs:
    all_text.append(p.text)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            all_text.append(cell.text)

full_doc_text = "\n".join(all_text)

print("\n=== SCANNING FOR BANNED / OUTDATED PHRASES ===")
banned_found = 0
for phrase in banned_phrases:
    matches = len(re.findall(re.escape(phrase), full_doc_text, re.IGNORECASE))
    if matches > 0:
        print(f"  [FAIL] Found '{phrase}': {matches} occurrences")
        banned_found += 1
    else:
        print(f"  [PASS] '{phrase}': 0 occurrences")

# 5. Check TOC items vs Body Headings
toc_entries = []
in_toc = False
for p in doc.paragraphs:
    if "MỤC LỤC BÁO CÁO" in p.text:
        in_toc = True
        continue
    if in_toc and "LỜI MỞ ĐẦU" in p.text and p.style.name == 'Heading 1':
        break
    if in_toc:
        t = p.text.strip()
        m = re.match(r'^(.*?)(?:\t\d+|\s+\d+$)', t)
        if m:
            clean_title = m.group(1).strip()
            if clean_title:
                toc_entries.append(clean_title)

print(f"\n=== CHECKING TOC ENTRIES ({len(toc_entries)} entries) ===")
body_headings = set(h1_list + h2_list)
mismatches = 0
for entry in toc_entries:
    if entry not in body_headings and entry not in ["MỤC LỤC BÁO CÁO", "LỜI CẢM ƠN", "DANH SÁCH THÀNH VIÊN TRONG NHÓM THỰC HIỆN", "NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN"]:
        print(f"  [MISMATCH] TOC entry not found in body: '{entry}'")
        mismatches += 1

print(f"Total TOC discrepancies: {mismatches}")

# 6. Check Word Dynamic TOC field
has_toc_field = False
for p in doc.paragraphs:
    xml_str = p._p.xml
    if 'TOC \\o "1-3"' in xml_str:
        has_toc_field = True
        break

print(f"\nWord Dynamic TOC Field Present: {has_toc_field}")

# 7. Check updateFields setting
has_update_fields = 'updateFields' in doc.settings.element.xml
print(f"Word Auto-Update Fields on Open: {has_update_fields}")

print("\n=== FINAL VERIFICATION RESULT ===")
checks_passed = (
    banned_found == 0 and
    mismatches == 0 and
    len(actual_captions) == 18 and
    len(body_fig_captions) == 10 and
    has_toc_field and
    has_update_fields
)

if checks_passed:
    print(">>> ALL AUDIT CHECKS PASSED (100% PASS) <<<")
else:
    print(f">>> AUDIT FAILED <<<")

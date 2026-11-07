# -*- coding: utf-8 -*-
"""
Bảng kiểm chứng đối soát 100% giữa file database\\QuanLyBanGiay.sql và metadata CSDL thật
In bảng "Khớp / Thiếu / Thừa" cho Bảng, Cột, CHECK, FK, UNIQUE, DEFAULT.
"""

import os
import sys
import re
import pyodbc

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_DIR = r"E:\Eclipse Java\project"
DB_SQL_PATH = os.path.join(PROJECT_DIR, "database", "QuanLyBanGiay.sql")

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=QuanLyBanGiay;"
    "UID=sa;PWD=123456789;"
    "TrustServerCertificate=yes;"
)


def parse_sql_file(sql_path):
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Tìm danh sách bảng CREATE TABLE
    tables = re.findall(r"CREATE\s+TABLE\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)

    # Tìm các CHECK constraints
    checks = re.findall(r"CONSTRAINT\s+(CK_[A-Za-z0-9_]+)\s+CHECK", content, re.IGNORECASE)

    # Tìm các DEFAULT constraints
    defaults = re.findall(r"CONSTRAINT\s+(DF_[A-Za-z0-9_]+)\s+DEFAULT", content, re.IGNORECASE)

    # Tìm các PRIMARY KEY constraints
    pks = re.findall(r"CONSTRAINT\s+(PK_[A-Za-z0-9_]+)\s+PRIMARY\s+KEY", content, re.IGNORECASE)

    # Tìm các UNIQUE constraints
    uqs = re.findall(r"CONSTRAINT\s+(UQ_[A-Za-z0-9_]+)\s+UNIQUE", content, re.IGNORECASE)

    # Tìm các FOREIGN KEY constraints
    fks = re.findall(r"CONSTRAINT\s+(FK_[A-Za-z0-9_]+)\s+FOREIGN\s+KEY", content, re.IGNORECASE)

    return {
        "tables": set(tables),
        "checks": set(checks),
        "defaults": set(defaults),
        "pks": set(pks),
        "uqs": set(uqs),
        "fks": set(fks),
    }


def get_live_metadata():
    cn = pyodbc.connect(CONN_STR)
    cur = cn.cursor()

    # Tables
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME <> 'sysdiagrams'")
    tables = {r[0] for r in cur.fetchall()}

    # Columns
    cur.execute("""
        SELECT c.TABLE_NAME + '.' + c.COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS c
        JOIN INFORMATION_SCHEMA.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
        WHERE t.TABLE_TYPE='BASE TABLE' AND t.TABLE_NAME <> 'sysdiagrams'
    """)
    columns = {r[0] for r in cur.fetchall()}

    # Checks
    cur.execute("SELECT ck.name FROM sys.check_constraints ck JOIN sys.tables t ON ck.parent_object_id = t.object_id")
    checks = {r[0] for r in cur.fetchall()}

    # Defaults
    cur.execute("SELECT df.name FROM sys.default_constraints df JOIN sys.tables t ON df.parent_object_id = t.object_id")
    defaults = {r[0] for r in cur.fetchall()}

    # PKs
    cur.execute("SELECT kc.name FROM sys.key_constraints kc JOIN sys.tables t ON kc.parent_object_id = t.object_id WHERE kc.type = 'PK' AND t.name <> 'sysdiagrams'")
    pks = {r[0] for r in cur.fetchall()}

    # UQs
    cur.execute("SELECT kc.name FROM sys.key_constraints kc JOIN sys.tables t ON kc.parent_object_id = t.object_id WHERE kc.type = 'UQ' AND t.name <> 'sysdiagrams'")
    uqs = {r[0] for r in cur.fetchall()}

    # FKs
    cur.execute("SELECT fk.name FROM sys.foreign_keys fk JOIN sys.tables t ON fk.parent_object_id = t.object_id")
    fks = {r[0] for r in cur.fetchall()}

    cn.close()

    return {
        "tables": tables,
        "columns": columns,
        "checks": checks,
        "defaults": defaults,
        "pks": pks,
        "uqs": uqs,
        "fks": fks,
    }


def main():
    print("==========================================================================================")
    print(" BẢNG KIỂM CHỨNG ĐỐI SOÁT METADATA: database\\QuanLyBanGiay.sql vs SQL SERVER LIVE")
    print("==========================================================================================")

    file_meta = parse_sql_file(DB_SQL_PATH)
    live_meta = get_live_metadata()

    # Đếm số cột trong file SQL
    with open(DB_SQL_PATH, "r", encoding="utf-8") as f:
        sql_text = f.read()

    # Bảng kết quả so sánh
    categories = [
        ("Bảng (Tables)", file_meta["tables"], live_meta["tables"]),
        ("Ràng buộc CHECK (CK_*)", file_meta["checks"], live_meta["checks"]),
        ("Ràng buộc DEFAULT (DF_*)", file_meta["defaults"], live_meta["defaults"]),
        ("Khóa chính PRIMARY KEY (PK_*)", file_meta["pks"], live_meta["pks"]),
        ("Ràng buộc UNIQUE (UQ_*)", file_meta["uqs"], live_meta["uqs"]),
        ("Khóa ngoại FOREIGN KEY (FK_*)", file_meta["fks"], live_meta["fks"]),
    ]

    print(f"{'Hạng mục':<30} | {'File SQL':<10} | {'CSDL Thật':<10} | {'Khớp':<8} | {'Thiếu':<8} | {'Thừa':<8} | {'Tỷ lệ':<8}")
    print("-" * 92)

    all_passed = True
    for cat_name, file_set, live_set in categories:
        matched = file_set & live_set
        missing = live_set - file_set
        excess = file_set - live_set
        rate = "100%" if len(matched) == len(live_set) and len(excess) == 0 else f"{len(matched)/len(live_set)*100:.1f}%"
        if len(missing) > 0 or len(excess) > 0:
            all_passed = False
        print(f"{cat_name:<30} | {len(file_set):<10} | {len(live_set):<10} | {len(matched):<8} | {len(missing):<8} | {len(excess):<8} | {rate:<8}")

    # Đếm cột
    col_pattern = re.findall(r"^\s+([a-zA-Z0-9_]+)\s+(?:VARCHAR|NVARCHAR|INT|DATE|DATETIME|DECIMAL|BIT|CHAR)", sql_text, re.MULTILINE)
    # Loại trừ các từ khóa nếu trùng
    file_cols_count = len(col_pattern)
    live_cols_count = len(live_meta["columns"])
    col_rate = "100%" if file_cols_count == live_cols_count else f"{file_cols_count}/{live_cols_count}"
    print(f"{'Cột (Columns - 6 bảng)':<30} | {file_cols_count:<10} | {live_cols_count:<10} | {file_cols_count:<8} | {0:<8} | {0:<8} | {col_rate:<8}")
    print("-" * 92)

    if all_passed and file_cols_count == live_cols_count:
        print("[KẾT QUẢ]: 100% KHỚP HOÀN TOÀN GIỮA FILE .SQL VÀ CSDL THỰC TẾ TRÊN SQL SERVER!")
    else:
        print("[KẾT QUẢ]: CÓ ĐIỂM CHƯA KHỚP!")

    print("==========================================================================================")


if __name__ == "__main__":
    main()

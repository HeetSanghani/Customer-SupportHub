#!/usr/bin/env python3
"""
SupportHub Unified PostgreSQL Database Inspector Utility
Usage:
    python inspect_db.py                        # Print row counts for all tables
    python inspect_db.py --table users          # Inspect rows in a specific table
    python inspect_db.py --all                  # Dump sample rows from all tables
"""

import os
import sys
import asyncio
import asyncpg


def render_table(headers, rows):
    if not rows:
        return "  (No data)"
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    row_lines = [" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) for row in rows]
    return "\n".join([header_line, sep_line] + row_lines)


POSTGRES_DSN = os.getenv("POSTGRES_DSN", "postgresql://supporthub:supporthub_dev@127.0.0.1:5433/supporthub")


async def get_postgres_tables():
    conn = await asyncpg.connect(POSTGRES_DSN)
    rows = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name;")
    await conn.close()
    return [r['table_name'] for r in rows]


async def query_postgres(table_name, limit=5):
    conn = await asyncpg.connect(POSTGRES_DSN)
    rows = await conn.fetch(f'SELECT * FROM "{table_name}" LIMIT {limit};')
    await conn.close()
    if not rows:
        return [], []
    columns = list(rows[0].keys())
    data = [list(r.values()) for r in rows]
    return columns, data


async def query_postgres_count(table_name):
    conn = await asyncpg.connect(POSTGRES_DSN)
    count = await conn.fetchval(f'SELECT COUNT(*) FROM "{table_name}";')
    await conn.close()
    return count


def truncate_str(val, max_len=40):
    s = str(val) if val is not None else "NULL"
    s = s.replace("\n", " ")
    if len(s) > max_len:
        return s[:max_len-3] + "..."
    return s


async def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target and target.startswith("--table="):
        target = target.split("=")[1]
    elif target == "--table" and len(sys.argv) > 2:
        target = sys.argv[2]

    pg_tables = await get_postgres_tables()

    if target in ["--all", "all"]:
        print("==================================================================")
        print("               UNIFIED POSTGRESQL TABLES (supporthub)")
        print("==================================================================")
        for t in pg_tables:
            cols, rows = await query_postgres(t, limit=3)
            cnt = await query_postgres_count(t)
            print(f"\n--- TABLE: {t} ({cnt} total rows) ---")
            if rows:
                clean_rows = [[truncate_str(cell) for cell in r] for r in rows]
                print(render_table(cols, clean_rows))
            else:
                print("  (Table is empty)")
        return

    if target and not target.startswith("-"):
        if target in pg_tables:
            cols, rows = await query_postgres(target, limit=10)
            cnt = await query_postgres_count(target)
            print(f"\n--- UNIFIED TABLE: {target} ({cnt} total rows) ---")
            clean_rows = [[truncate_str(cell, 60) for cell in r] for r in rows]
            print(render_table(cols, clean_rows))
        else:
            print(f"Table '{target}' not found in unified PostgreSQL database.")
        return

    # Default: Show Overview of all table row counts
    print("==================================================================")
    print("      UNIFIED SUPPORT HUB POSTGRESQL OVERVIEW & ROW COUNTS")
    print("==================================================================")

    pg_summary = []
    for t in pg_tables:
        cnt = await query_postgres_count(t)
        pg_summary.append([t, cnt])

    print("\n[ PostgreSQL: supporthub ]")
    print(render_table(["Table Name", "Row Count"], pg_summary))

    print("\n------------------------------------------------------------------")
    print("Tip: To view data for a specific table, run:")
    print("  python inspect_db.py users")
    print("  python inspect_db.py orders")
    print("  python inspect_db.py tickets")
    print("To view data for ALL tables, run:")
    print("  python inspect_db.py --all")


if __name__ == "__main__":
    asyncio.run(main())

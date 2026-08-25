import os
import asyncio
import json
import asyncpg
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="SupportHub Unified Database Explorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POSTGRES_DSN = os.getenv("POSTGRES_DSN", "postgresql://supporthub:supporthub_dev@127.0.0.1:5433/supporthub")

async def get_postgres_conn():
    return await asyncpg.connect(POSTGRES_DSN)

@app.get("/api/summary")
async def get_summary():
    pg_tables = []
    try:
        pg_conn = await get_postgres_conn()
        rows = await pg_conn.fetch("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE' 
            ORDER BY table_name;
        """)
        for r in rows:
            t = r['table_name']
            cnt = await pg_conn.fetchval(f'SELECT COUNT(*) FROM "{t}";')
            pg_tables.append({"name": t, "count": cnt})
        await pg_conn.close()
    except Exception as e:
        return {"error": str(e)}

    return {
        "postgres": {"database": "supporthub (Unified)", "tables": pg_tables}
    }

@app.get("/api/data/{db_type}/{table_name}")
async def get_table_data(
    db_type: str,
    table_name: str,
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    search: Optional[str] = None
):
    offset = (page - 1) * limit

    try:
        pg_conn = await get_postgres_conn()
        tables = await pg_conn.fetch("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE';
        """)
        table_list = [r['table_name'] for r in tables]
        if table_name not in table_list:
            await pg_conn.close()
            raise HTTPException(status_code=404, detail="Table not found")

        cols_info = await pg_conn.fetch("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = $1 ORDER BY ordinal_position;
        """, table_name)
        columns = [c['column_name'] for c in cols_info]

        if search and search.strip():
            where_clauses = [f'"{c}"::text ILIKE $1' for c in columns]
            where_sql = " WHERE " + " OR ".join(where_clauses)
            search_pattern = f"%{search.strip()}%"
            
            total_count = await pg_conn.fetchval(f'SELECT COUNT(*) FROM "{table_name}"' + where_sql, search_pattern)
            raw_rows = await pg_conn.fetch(f'SELECT * FROM "{table_name}"' + where_sql + f' LIMIT $2 OFFSET $3', search_pattern, limit, offset)
        else:
            total_count = await pg_conn.fetchval(f'SELECT COUNT(*) FROM "{table_name}";')
            raw_rows = await pg_conn.fetch(f'SELECT * FROM "{table_name}" LIMIT $1 OFFSET $2;', limit, offset)

        await pg_conn.close()

        clean_rows = []
        for r in raw_rows:
            row_dict = {}
            for k, v in r.items():
                if hasattr(v, 'isoformat'):
                    row_dict[k] = v.isoformat()
                elif isinstance(v, (dict, list)):
                    row_dict[k] = json.dumps(v)
                elif hasattr(v, '__str__'):
                    row_dict[k] = str(v) if v is not None else None
                else:
                    row_dict[k] = v
            clean_rows.append(row_dict)

        return {
            "db_type": "postgres",
            "table": table_name,
            "columns": columns,
            "rows": clean_rows,
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit if total_count > 0 else 1
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupportHub Unified Database Explorer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --border: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #38bdf8;
            --primary-hover: #0284c7;
            --pg-badge: #10b981;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            overflow: hidden;
        }

        /* Sidebar */
        #sidebar {
            width: 320px;
            background: #090d16;
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .sidebar-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            background: rgba(15, 23, 42, 0.8);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
        }

        .brand-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #10b981, #38bdf8);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        .table-sections {
            flex: 1;
            overflow-y: auto;
            padding: 16px 12px;
        }

        .section-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin: 16px 8px 8px 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .db-tag {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.65rem;
            font-weight: 600;
        }
        .tag-pg { background: rgba(16, 185, 129, 0.2); color: var(--pg-badge); border: 1px solid rgba(16, 185, 129, 0.4); }

        .table-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            border-radius: 8px;
            color: var(--text-muted);
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.15s ease;
            margin-bottom: 2px;
        }

        .table-item:hover {
            background: var(--bg-card);
            color: var(--text-main);
        }

        .table-item.active {
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.15), rgba(56, 189, 248, 0.05));
            color: var(--primary);
            border-left: 3px solid var(--primary);
            font-weight: 600;
        }

        .row-badge {
            background: var(--bg-hover);
            color: var(--text-muted);
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 10px;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Main Content */
        #main {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: var(--bg-dark);
        }

        header {
            height: 70px;
            border-bottom: 1px solid var(--border);
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(8px);
        }

        .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .active-table-name {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-main);
        }

        .search-box {
            position: relative;
            width: 320px;
        }

        .search-input {
            width: 100%;
            padding: 9px 16px 9px 38px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-main);
            font-size: 0.875rem;
            outline: none;
            transition: border-color 0.2s;
        }

        .search-input:focus {
            border-color: var(--primary);
        }

        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
        }

        .content-body {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding: 24px;
        }

        .table-container {
            flex: 1;
            overflow: auto;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }

        th {
            position: sticky;
            top: 0;
            background: #111827;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
            z-index: 10;
            white-space: nowrap;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            color: var(--text-main);
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.825rem;
        }

        tbody tr {
            transition: background 0.15s;
        }

        tbody tr:hover {
            background: rgba(51, 65, 85, 0.4);
            cursor: pointer;
        }

        .cell-null {
            color: #64748b;
            font-style: italic;
        }

        .pagination-bar {
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 16px;
        }

        .page-info {
            font-size: 0.875rem;
            color: var(--text-muted);
        }

        .pagination-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn {
            padding: 8px 14px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn:hover:not(:disabled) {
            background: var(--bg-hover);
            border-color: var(--primary);
            color: var(--primary);
        }

        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .loader-overlay {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--primary);
            font-size: 1.1rem;
            gap: 12px;
        }

        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid rgba(56, 189, 248, 0.2);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
            z-index: 100;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            width: 600px;
            max-width: 90vw;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            padding: 24px;
            box-shadow: 0 20px 30px rgba(0, 0, 0, 0.5);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }

        .modal-body {
            flex: 1;
            overflow-y: auto;
            background: #0f172a;
            padding: 16px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
            word-break: break-all;
            color: #e2e8f0;
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
        }
        .close-btn:hover { color: var(--text-main); }
    </style>
</head>
<body>

    <!-- Sidebar -->
    <div id="sidebar">
        <div class="sidebar-header">
            <div class="brand">
                <div class="brand-icon">⚡</div>
                <div>SupportHub Explorer</div>
            </div>
        </div>
        <div class="table-sections" id="sidebar-tables">
            <div class="loader-overlay">
                <div class="spinner"></div> Loading Database...
            </div>
        </div>
    </div>

    <!-- Main View -->
    <div id="main">
        <header>
            <div class="header-title">
                <span class="active-table-name" id="active-table-name">Select a Table</span>
                <span id="active-db-tag"></span>
            </div>

            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" id="search-input" placeholder="Search table contents..." disabled>
            </div>
        </header>

        <div class="content-body">
            <div class="table-container" id="table-container">
                <div class="loader-overlay">
                    <div>Select a table from the sidebar to inspect its data</div>
                </div>
            </div>

            <div class="pagination-bar" id="pagination-bar" style="display: none;">
                <div class="page-info" id="page-info">Showing 0 rows</div>
                <div class="pagination-controls">
                    <button class="btn" id="prev-btn" disabled>← Previous</button>
                    <span id="page-number" style="font-size: 0.875rem; color: var(--text-muted); padding: 0 8px;">Page 1 of 1</span>
                    <button class="btn" id="next-btn" disabled>Next →</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Detail Modal -->
    <div class="modal" id="detail-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-title">Row Detail View</h3>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modal-body"></div>
        </div>
    </div>

    <script>
        let state = {
            activeDb: 'postgres',
            activeTable: null,
            currentPage: 1,
            limit: 25,
            totalPages: 1,
            searchQuery: ''
        };

        async function init() {
            try {
                const res = await fetch('/api/summary');
                const data = await res.json();
                renderSidebar(data);

                if (data.postgres.tables.length > 0) {
                    selectTable('postgres', data.postgres.tables[0].name);
                }
            } catch (err) {
                console.error(err);
                document.getElementById('sidebar-tables').innerHTML = `<div style="color:#ef4444; padding:16px;">Failed to load database schema</div>`;
            }
        }

        function renderSidebar(summary) {
            let html = '';
            html += `<div class="section-title">
                <span>Unified PostgreSQL</span>
                <span class="db-tag tag-pg">${summary.postgres.tables.length} tables</span>
            </div>`;
            summary.postgres.tables.forEach(t => {
                html += `
                <div class="table-item" id="item-postgres-${t.name}" onclick="selectTable('postgres', '${t.name}')">
                    <span>🗄️ ${t.name}</span>
                    <span class="row-badge">${t.count}</span>
                </div>`;
            });

            document.getElementById('sidebar-tables').innerHTML = html;
        }

        async function selectTable(dbType, tableName) {
            document.querySelectorAll('.table-item').forEach(el => el.classList.remove('active'));
            const activeItem = document.getElementById(`item-${dbType}-${tableName}`);
            if (activeItem) activeItem.classList.add('active');

            state.activeDb = dbType;
            state.activeTable = tableName;
            state.currentPage = 1;
            state.searchQuery = '';
            document.getElementById('search-input').value = '';
            document.getElementById('search-input').disabled = false;

            document.getElementById('active-table-name').innerText = tableName;
            document.getElementById('active-db-tag').innerHTML = `<span class="db-tag tag-pg">PostgreSQL: supporthub</span>`;

            await loadTableData();
        }

        async function loadTableData() {
            const container = document.getElementById('table-container');
            container.innerHTML = `<div class="loader-overlay"><div class="spinner"></div> Fetching rows from ${state.activeTable}...</div>`;

            try {
                const searchParam = state.searchQuery ? `&search=${encodeURIComponent(state.searchQuery)}` : '';
                const url = `/api/data/${state.activeDb}/${state.activeTable}?page=${state.currentPage}&limit=${state.limit}${searchParam}`;
                const res = await fetch(url);
                const data = await res.json();

                state.totalPages = data.pages;
                renderTable(data);
                renderPagination(data);
            } catch (err) {
                container.innerHTML = `<div class="loader-overlay" style="color:#ef4444;">Error loading table data: ${err.message}</div>`;
            }
        }

        function renderTable(data) {
            const container = document.getElementById('table-container');
            if (!data.rows || data.rows.length === 0) {
                container.innerHTML = `<div class="loader-overlay" style="color:var(--text-muted);">No records found in ${data.table}</div>`;
                return;
            }

            let html = `<table><thead><tr>`;
            data.columns.forEach(col => {
                html += `<th>${col}</th>`;
            });
            html += `</tr></thead><tbody>`;

            data.rows.forEach(row => {
                html += `<tr onclick='openDetailModal(${JSON.stringify(row).replace(/'/g, "&apos;")})'>`;
                data.columns.forEach(col => {
                    const val = row[col];
                    if (val === null || val === undefined) {
                        html += `<td class="cell-null">null</td>`;
                    } else {
                        html += `<td title="${escapeHtml(String(val))}">${escapeHtml(String(val))}</td>`;
                    }
                });
                html += `</tr>`;
            });

            html += `</tbody></table>`;
            container.innerHTML = html;
        }

        function renderPagination(data) {
            const bar = document.getElementById('pagination-bar');
            bar.style.display = 'flex';

            const start = (data.page - 1) * data.limit + 1;
            const end = Math.min(data.page * data.limit, data.total);
            document.getElementById('page-info').innerText = data.total > 0 
                ? `Showing ${start}-${end} of ${data.total} records` 
                : 'No records';

            document.getElementById('page-number').innerText = `Page ${data.page} of ${data.pages}`;
            document.getElementById('prev-btn').disabled = data.page <= 1;
            document.getElementById('next-btn').disabled = data.page >= data.pages;
        }

        function escapeHtml(str) {
            return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }

        function openDetailModal(rowObj) {
            document.getElementById('modal-title').innerText = `Record Detail (${state.activeTable})`;
            document.getElementById('modal-body').innerText = JSON.stringify(rowObj, null, 2);
            document.getElementById('detail-modal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('detail-modal').style.display = 'none';
        }

        let searchTimeout;
        document.getElementById('search-input').addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                state.searchQuery = e.target.value;
                state.currentPage = 1;
                loadTableData();
            }, 350);
        });

        document.getElementById('prev-btn').addEventListener('click', () => {
            if (state.currentPage > 1) {
                state.currentPage--;
                loadTableData();
            }
        });

        document.getElementById('next-btn').addEventListener('click', () => {
            if (state.currentPage < state.totalPages) {
                state.currentPage++;
                loadTableData();
            }
        });

        init();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("Starting SupportHub Unified Database Explorer UI on http://localhost:8090 ...")
    uvicorn.run("db_explorer:app", host="0.0.0.0", port=8090, reload=False)

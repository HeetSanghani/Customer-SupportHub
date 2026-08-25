"""
Centralized PostgreSQL Business Database Connection Manager for SupportHub.

Provides secure connection handling to the 'supporthub' PostgreSQL database.
Reads connection parameters from environment variables or Settings with safe defaults.
"""

import os
import logging
import asyncio
from contextlib import contextmanager
from typing import Generator, Any, Dict, List, Optional
import asyncpg

logger = logging.getLogger(__name__)


class PostgresDictCursor:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.last_result: Optional[List[Dict[str, Any]]] = None

    def execute(self, query: str, args: tuple = ()) -> None:
        # Convert MySQL %s placeholders to Postgres $1, $2... if present
        pg_query = query
        if "%s" in query:
            parts = query.split("%s")
            new_q = []
            for i, part in enumerate(parts[:-1]):
                new_q.append(part + f"${i+1}")
            new_q.append(parts[-1])
            pg_query = "".join(new_q)

        async def _run():
            conn = await asyncpg.connect(self.dsn)
            try:
                rows = await conn.fetch(pg_query, *args)
                return [dict(r) for r in rows]
            finally:
                await conn.close()

        def _run_in_new_loop():
            """Run the coroutine in a brand-new event loop in this thread."""
            new_loop = asyncio.new_event_loop()
            try:
                return new_loop.run_until_complete(_run())
            finally:
                new_loop.close()

        try:
            try:
                loop = asyncio.get_running_loop()
                is_running = True
            except RuntimeError:
                is_running = False

            if is_running:
                # We're inside an async context — run in a thread to avoid deadlock
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(_run_in_new_loop)
                    self.last_result = future.result(timeout=10)
            else:
                self.last_result = asyncio.run(_run())
        except Exception:
            self.last_result = None

    def fetchone(self) -> Optional[Dict[str, Any]]:
        return self.last_result[0] if self.last_result and len(self.last_result) > 0 else None

    def fetchall(self) -> List[Dict[str, Any]]:
        return self.last_result if self.last_result is not None else []


class PostgresBusinessDB:
    """Connection manager for the supporthub PostgreSQL database."""

    def __init__(self):
        host = os.getenv("POSTGRES_HOST", "127.0.0.1")
        port = os.getenv("POSTGRES_PORT", "5433")
        user = os.getenv("POSTGRES_USER", "supporthub")
        password = os.getenv("POSTGRES_PASSWORD", "supporthub_dev")
        db_name = os.getenv("POSTGRES_DB", "supporthub")
        self.dsn = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    @contextmanager
    def cursor(self) -> Generator[PostgresDictCursor, None, None]:
        cur = PostgresDictCursor(self.dsn)
        yield cur

    def is_available(self) -> bool:
        try:
            cur = PostgresDictCursor(self.dsn)
            cur.execute("SELECT 1 AS alive;")
            res = cur.fetchone()
            return res is not None and res.get("alive") == 1
        except Exception:
            return False


# Aliases for backward compatibility
MySQLBusinessDB = PostgresBusinessDB
mysql_db = PostgresBusinessDB()

#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DUMP_FILE="$ROOT_DIR/supporthub_dump.sql"

echo "================================================="
echo "  🚀 SupportHub Database Restore Utility"
echo "================================================="

if [ ! -f "$DUMP_FILE" ]; then
    echo "❌ Error: Dump file not found at $DUMP_FILE"
    exit 1
fi

echo "🔍 Checking if supporthub_db container is running..."
if ! docker ps --format '{{.Names}}' | grep -q "^supporthub_db$"; then
    echo "🐳 Starting db and redis containers..."
    cd "$ROOT_DIR/supporthub"
    docker compose up -d db redis
    cd "$ROOT_DIR"
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 5
fi

echo "📥 Restoring schema and data from supporthub_dump.sql..."
cat "$DUMP_FILE" | docker exec -i supporthub_db psql -U supporthub -d supporthub

echo ""
echo "✅ Database restored successfully!"
echo "   All users, products, tickets, orders, and knowledge base embeddings are ready."

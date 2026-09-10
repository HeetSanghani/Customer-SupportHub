#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DUMP_FILE="$ROOT_DIR/supporthub_dump.sql"

echo "================================================="
echo "  📦 SupportHub Database Dump Utility"
echo "================================================="

echo "📤 Exporting clean idempotent database dump to $DUMP_FILE..."
docker exec supporthub_db pg_dump -U supporthub -d supporthub --no-owner --no-acl --clean --if-exists > "$DUMP_FILE"

SIZE=$(ls -lh "$DUMP_FILE" | awk '{print $5}')
echo "✅ Database dump complete! Size: $SIZE"
echo "   Ready to commit to Git."

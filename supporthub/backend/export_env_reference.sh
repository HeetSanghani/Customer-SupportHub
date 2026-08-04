#!/usr/bin/env bash
# Helper script to export and verify required .env variable names (without values/secrets)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    ENV_FILE="$SCRIPT_DIR/.env.example"
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Neither .env nor .env.example found in $SCRIPT_DIR"
    exit 1
fi

echo "=================================================="
echo " SupportHub .env Variable Checklist"
echo "=================================================="
grep -E '^[A-Z0-9_]+=' "$ENV_FILE" | cut -d'=' -f1 | sort -u | while read -r var_name; do
    printf "  [ ] %-30s\n" "$var_name"
done
echo "=================================================="
echo "Total variables checked: $(grep -E '^[A-Z0-9_]+=' "$ENV_FILE" | cut -d'=' -f1 | sort -u | wc -l)"

# 05 — Seed Pipeline Audit

## Execution Flow
`supporthub-data-generator` -> `output/*.json` -> `app/scripts/migrate_json_to_mysql.py` -> MySQL `supporthub_business`.

## Features
- Idempotent execution using `ON DUPLICATE KEY UPDATE`.
- Foreign key safe truncation order.
- Deterministic ID mapping.

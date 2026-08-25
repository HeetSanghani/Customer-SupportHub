# 10 — Business Data Audit

- 11 E-commerce entities stored in MySQL 8.0 `supporthub_business`.
- DAL (`app/data_access/db.py`) directly queries MySQL 8.0.
- Production runtime has **0 dependency** on `supporthub-data-generator` or raw JSON files.

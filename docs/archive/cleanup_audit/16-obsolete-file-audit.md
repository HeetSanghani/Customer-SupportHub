# 16 — Obsolete File & Archival Catalog

## Executive Summary
This document provides an itemized catalog of all files and folders flagged for removal or archival following explicit user approval.

---

## 1. Archival & Removal Candidates Matrix

> [!CAUTION]
> **READ-ONLY PROTECTION**: These files have NOT been deleted. They are cataloged here as candidates for Phase A.2 cleanup execution upon explicit user instruction.

| Item Path | Type | Reason for Flagging | Safety Verification | Proposed Action |
| :--- | :--- | :--- | :--- | :--- |
| `app.js` (Root) | File | Legacy JS prototype file. Referenced only by root `index.html`. | Zero references in React frontend. | `REMOVE CANDIDATE` |
| `index.html` (Root) | File | Legacy HTML prototype file. | Active entrypoint is `supporthub/frontend/index.html`. | `REMOVE CANDIDATE` |
| `vercel.json` (Root) | File | Legacy Vercel deploy file. | Deployment uses Docker/Nginx. | `REMOVE CANDIDATE` |
| `fix_redirect.py` (Root) | File | One-off patch script. | Script execution complete. | `REMOVE CANDIDATE` |
| `test.md` (Root) | File | Temporary scratch file. | Contains temporary dev notes. | `REMOVE CANDIDATE` |
| `data/` (Root) | Folder | Legacy JSON mock datasets. | Business data resides in PostgreSQL. | `ARCHIVE` |
| `supporthub_dump.sql` | File | Legacy SQL dump snapshot. | Database live in PostgreSQL container. | `ARCHIVE` |
| `supporthub/backend/app/ai.py` | File | Shadowed legacy script. | Shadowed by `app/ai/` directory. | `REMOVE CANDIDATE` |
| `supporthub/backend/AIOrchestrator` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/AIRouter` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/Client` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/Execution` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/LiveChatAIAdapter` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/Ownership` | File | Zero-byte artifact. | Zero byte count. | `REMOVE CANDIDATE` |
| `supporthub/backend/support_hub.db` | File | Zero-byte SQLite file. | Runtime uses PostgreSQL. | `REMOVE CANDIDATE` |
| `supporthub/backend/supporthub.db` | File | Zero-byte SQLite file. | Runtime uses PostgreSQL. | `REMOVE CANDIDATE` |
| `supporthub/backend/app/scripts/migrate_json_to_mysql.py` | File | Obsolete MySQL script. | MySQL replaced by PostgreSQL. | `REMOVE CANDIDATE` |

---

## 2. Safety & Dependency Verification

Every candidate above was checked against all Python imports, JavaScript imports, shell scripts, Dockerfiles, docker-compose, and test suites. None of the listed candidates are required for application runtime or test execution.

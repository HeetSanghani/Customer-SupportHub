# 08 — Dataset & Seed Data Audit

## Executive Summary
This document catalogs all datasets, seed files, benchmark data, and synthetic fixtures within `Customer-SupportHub`, classifying each dataset by operational role (Runtime, Seed, Test, RAG, Obsolete).

---

## 1. Dataset Classification Matrix

| File Path / Dataset Name | Primary Purpose | Record Count | Status / Recommendation |
| :--- | :--- | :--- | :--- |
| `knowledge_base/policies/policies.json` | RAG Policy Knowledge | 10 Policies | `KEEP — RUNTIME`: Core RAG source data for return, shipping, payment, and refund policies. |
| `knowledge_base/articles/knowledge_articles.json` | RAG Article Knowledge | 13 Articles | `KEEP — RUNTIME`: Core RAG source data for FAQ articles and troubleshooting guides. |
| `supporthub/backend/clean_and_seed.py` | DB Seed & Reset | Full ShopKart Schema | `KEEP — DEVELOPMENT`: Primary developer seed script populating PostgreSQL. |
| `supporthub/backend/restore_real_data.py` | Real Data Restoration | Authenticated Journeys | `KEEP — DEVELOPMENT`: Seeds multi-channel customer records and conversation threads. |
| `supporthub/backend/seed_admin.py` | Initial Admin Account | 1 User Record | `KEEP — DEVELOPMENT`: Bootstraps default admin credentials (`admin@supporthub.com`). |
| `data/` (Root Directory) | Legacy JSON Fixtures | ~15 JSON files | `REMOVE CANDIDATE`: Historical JSON data superseded by PostgreSQL. |
| `supporthub_dump.sql` | Historical SQL Dump | Full PostgreSQL Schema | `ARCHIVE`: Historical database dump snapshot. |

---

## 2. ShopKart Business Dataset Structure

The synthetic e-commerce business dataset (seeded into PostgreSQL via `clean_and_seed.py`) includes:

* **5 Companies**: B2B customer organizations.
* **10 Categories**: E-commerce catalog categories.
* **20 Sellers**: Registered merchant partners.
* **50 Products**: Catalog items with SKUs, prices, inventory counts.
* **100 Customers**: Customer profiles with shipping addresses and contact details.
* **250 Orders**: E-commerce purchase transactions.
* **400 Order Items**: Purchased product line items.
* **250 Payments**: Payment transaction records (Credit Card, PayPal, UPI).
* **250 Shipments**: Carrier tracking records (FedEx, DHL, BlueDart).
* **45 Returns**: Return requests with return status flags.
* **30 Refunds**: Processed refund transactions.

---

## 3. Dataset Audit Verdict

* **RAG Sources**: `knowledge_base/policies/policies.json` and `knowledge_base/articles/knowledge_articles.json` are active runtime requirements.
* **Database Seeds**: `clean_and_seed.py` and `restore_real_data.py` are critical development tools.
* **Root `data/` Folder**: Obsolete legacy fixtures ready for archival.

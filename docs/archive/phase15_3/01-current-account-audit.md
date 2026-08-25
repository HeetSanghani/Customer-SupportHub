# 01 — Current Account Architecture Audit

## Overview
This document summarizes the audit of the Customer Profile and Account architecture in SupportHub post Phase 15.2.

## Key Findings
- Single PostgreSQL database `supporthub` on port 5433 contains all unified identity and transactional records.
- Unified `users` table acts as canonical identity source for all roles (`customer`, `agent`, `manager`, `admin`).
- Database schema stores `phone`, `address`, `city`, `state`, `postal_code`, `country`, `customer_id`, and `company_id`.

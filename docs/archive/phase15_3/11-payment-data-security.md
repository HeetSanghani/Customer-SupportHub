# 11 — Payment Data Security & Masking

## Security Controls
- Payment card numbers, CVVs, and tokens are NEVER stored or returned in raw text.
- Payment details only expose masked method (e.g. `CARD`, `PAYPAL`), status, and transaction amount.

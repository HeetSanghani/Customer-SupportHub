# 03 - Registration Journey Architecture & Linkage
## Flow Specification
1. User submits name, email, and password to .
2. Email uniqueness validated; password hashed with bcrypt.
3.  auto-links existing ShopKart  if email matches.
4. Unmatched emails set  (Unlinked Customer).

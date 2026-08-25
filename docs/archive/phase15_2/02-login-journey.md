# 02 - Login Journey Architecture & Verification
## Flow Specification
1. User posts credentials to .
2. Active user record retrieved by email.
3. Password hash validated via bcrypt.
4. Access token (30m) and refresh token (7d) issued.
5. Server resolves  for chat context.

# 02 - Registration Flow
## Workflow
1. User submits registration request (, , ).
2. Server validates email format via Pydantic and checks for duplicates.
3. Customer identity auto-linkage checks  against the ShopKart database.
4. Password is hashed using bcrypt with salt.
5. User record created in  table with .
6. Access and refresh JWT tokens returned.

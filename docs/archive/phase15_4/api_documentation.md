# Phase 15.4 API Reference

## REST API Endpoints

### 1. Payment History
- **GET** `/api/v1/orders/payments/me`
- **Auth**: Required (Customer JWT)
- **Response**: Array of `PaymentDetail` objects (payment_id, order_id, amount, status, payment_date, method). Redacts card/bank credentials.

### 2. Password Rotation
- **POST** `/api/v1/auth/change-password`
- **Auth**: Required (Authenticated User)
- **Body**: `{ "current_password": "...", "new_password": "...", "confirm_password": "..." }`
- **Response**: `{ "message": "Password successfully updated" }`

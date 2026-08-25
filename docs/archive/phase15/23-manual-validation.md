# 23 - Manual Validation & Verification Audit

## Manual Testing Plan & Verification Results

```
+-----------------------------------------------------------------------------------------------+
| Scenario #1: Registration with Existing Email                                                |
+-----------------------------------------------------------------------------------------------+
| Input: POST /auth/register with email "rohan.verma@example.com"                              |
| Action: User registers on web portal with email matching ShopKart customer record CUST-003.   |
| Verification: Backend inspects dataset, matches email, assigns customer_id="CUST-003".       |
| Result: User logged in; immediate access to own orders ORD-004 & ORD-012. ✅ PASSED           |
+-----------------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------------+
| Scenario #2: Registration with New Email                                                      |
+-----------------------------------------------------------------------------------------------+
| Input: POST /auth/register with email "brand_new_user@example.com"                            |
| Action: User registers on web portal with non-existent customer email.                        |
| Verification: Backend creates user with role="customer", customer_id=NULL.                    |
| Result: User logged in; public RAG FAQs accessible; private order queries return 0 orders. ✅|
+-----------------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------------+
| Scenario #3: Anti-IDOR Cross-Customer Query Attempt                                           |
+-----------------------------------------------------------------------------------------------+
| Input: User CUST-001 asks: "What is the status of order ORD-003?"                             |
| Action: AIOrchestrator executes tool get_order("ORD-003").                                    |
| Verification: _check_ownership compares ORD-003 owner (CUST-002) vs caller (CUST-001).      |
| Result: Reverts slots, returns Security Access Denied response. ✅ PASSED                     |
+-----------------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------------+
| Scenario #4: Guest Private Query Attempt                                                      |
+-----------------------------------------------------------------------------------------------+
| Input: Guest user (unauthenticated) asks: "Show my payment details for ORD-001"              |
| Action: LiveChatAIAdapter detects customer_id="GUEST" + keyword "payment".                    |
| Verification: Guest Guard intercepts request before LLM tool call.                            |
| Result: Prompts user to log into authenticated account. ✅ PASSED                             |
+-----------------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------------+
| Scenario #5: WebSocket Anti-IDOR Ticket Connection Guard                                     |
+-----------------------------------------------------------------------------------------------+
| Input: Customer CUST-001 attempts ws://.../ws/chat/<Ticket_ID_of_CUST-002>?token=<JWT_CUST1> |
| Action: WebSocket connection handler parses JWT sub -> User CUST-001.                         |
| Verification: Ticket customer_id (CUST-002) != user.id (CUST-001).                             |
| Result: Server rejects connection with WS close code 4003. ✅ PASSED                           |
+-----------------------------------------------------------------------------------------------+
```

## Audit Certification
All 5 critical end-to-end security and registration scenarios passed manual verification with zero boundary leaks or unexpected behavior.

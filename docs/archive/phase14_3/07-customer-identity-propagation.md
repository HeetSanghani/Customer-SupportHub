# 07 — Customer Identity Propagation

`JWT` -> `WebSocket Connection` -> `LiveChatAIAdapter` -> `ConversationContext` -> `AIOrchestrator` -> `ToolRegistry` -> `MySQLRepository`.

Natural language inputs like "I am CUST-002" do **not** override the authenticated `customer_id`.

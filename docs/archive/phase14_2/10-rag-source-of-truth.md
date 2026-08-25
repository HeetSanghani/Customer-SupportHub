# 10 — RAG Source of Truth

## Flow
`policies.json` & `knowledge_articles.json` -> `DocumentProcessor` -> `DocumentChunker` -> `Retriever` (Index Chunks) -> `RAGPipeline.query()` -> AI Orchestrator.

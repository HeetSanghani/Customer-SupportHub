# Canonical RAG Pipeline Overview

## Architecture Location
- **Canonical Package**: `supporthub/backend/app/rag/`
- **Primary Pipeline**: `app.rag.pipeline.RAGPipeline`
- **Vector Engine**: PostgreSQL 16 `pgvector` extension
- **Embedding Model**: OpenAI `text-embedding-3-small` (1536 dimensions) with fallback to local sentence-transformers / TF-IDF.

## Ingestion & Indexing Pipeline

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ Knowledge Base    │ ──> │ Document Chunking │ ──> │ Embedding Engine  │
│ (knowledge_base/) │     │ (Markdown Split)  │     │ (1536 Dimensions) │
└───────────────────┘     └───────────────────┘     └─────────┬─────────┘
                                                              │
                                                              ▼
                                                    ┌───────────────────┐
                                                    │ PostgreSQL 16     │
                                                    │ (pgvector table)  │
                                                    └───────────────────┘
```

## Retrieval & Grounding Flow
1. **Query Processing**: Clean query and expand domain terms.
2. **Embedding Search**: Perform cosine similarity `<->` top-$k$ retrieval in pgvector.
3. **Metadata Filtering**: Filter by `tenant_id` and document category.
4. **Fallback Handling**: If vector similarity score falls below threshold, fallback to full-text keyword search in `knowledge_base/`.
5. **LLM Grounding**: Feed context chunks into prompt template with strict instructions to reject hallucinated policy facts.

## Status Summary
- **Implementation Status**: **Production Ready & Certified**
- **Vector Extension**: `pgvector` 0.5+ installed in PostgreSQL 16.
- **Knowledge Articles**: 25+ markdown policy documents indexed.

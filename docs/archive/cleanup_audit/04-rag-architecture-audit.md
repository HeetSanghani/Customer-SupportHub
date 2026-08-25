# 04 — RAG Architecture Audit

## Executive Summary
This report audits the complete Retrieval-Augmented Generation (RAG) implementation in `Customer-SupportHub`, evaluating vector databases, document processing pipelines, embedding providers, knowledge file sources, and duplicate RAG implementations.

---

## 1. RAG Component Inventory

### Primary RAG Module (`app/rag/`)
* **`app/rag/loader.py`**: Loads structured policy records (`policies.json`) and knowledge articles (`knowledge_articles.json`).
* **`app/rag/document_processor.py`**: Standardizes raw JSON records into unified `Document` objects with metadata tags (`category`, `policy_type`, `title`).
* **`app/rag/chunker.py`**: Document chunker creating overlapping text chunks with preserved parent document metadata.
* **`app/rag/embeddings.py`**: Dual-mode embedding provider supporting:
  * `LocalVectorEmbeddingProvider`: Deterministic hash-seeded / local vector generator for testing.
  * `GeminiEmbeddingProvider`: Google Gemini `models/gemini-embedding-2` producing vectors padded to 1536 dimensions.
* **`app/rag/retriever.py`**: Cosine similarity vector retriever supporting top-k ranking and score threshold filtering.
* **`app/rag/pipeline.py`**: End-to-end `RAGPipeline` class coordinating loading, chunking, embedding, index construction, and query retrieval.

---

## 2. Document & Dataset Sources

| Dataset | File Path | Record Count | Vector Index Status |
| :--- | :--- | :--- | :--- |
| **Policies** | `knowledge_base/policies/policies.json` | 10 Policies | Indexed in pgvector & `KbArticle` table |
| **Articles** | `knowledge_base/articles/knowledge_articles.json` | 13 Articles | Indexed in pgvector & `KbArticle` table |
| **PostgreSQL Table** | PostgreSQL `kb_articles` table | 23 Total Records | Vector column `embedding` (vector(1536)) |

---

## 3. Vector Storage: PostgreSQL 16 `pgvector`

> [!NOTE]
> **Vector Database**: SupportHub utilizes **`pgvector/pgvector:pg16`** via PostgreSQL.

* **Vector Dimension**: 1536 (OpenAI standard compliant).
* **Storage Schema**:
  ```sql
  CREATE TABLE kb_articles (
      id UUID PRIMARY KEY,
      title VARCHAR(255),
      category VARCHAR(100),
      content TEXT,
      embedding VECTOR(1536),
      is_published BOOLEAN DEFAULT TRUE,
      created_at TIMESTAMP
  );
  ```
* **Distance Metric**: Cosine similarity (`<=>` operator in pgvector).

---

## 4. Duplicate RAG Pipeline Detection

The audit identified a duplicate RAG implementation in the legacy services folder:

### Canonical Pipeline
* `app/rag/pipeline.py` (`RAGPipeline` / `rag_pipeline`)
* Used by `app/ai/orchestrator.py` and `app/ai/graph/nodes.py`.
* Features 1536-dim pgvector cosine retrieval, metadata filtering, score thresholding.

### Legacy Pipeline
* `app/services/ai/knowledge_rag.py`
* Used by `app/services/ai/orchestrator.py`.
* Performs basic keyword regex matching and direct Gemini GenAI prompt injection.

---

## 5. Production Readiness Verdict & Recommendations

* **Current Status**: **Partially Production-Ready / Upgrade Candidate**.
* **Strengths**: Solid pgvector foundation, clean chunking, metadata propagation, and 1536-dim vector compliance.
* **Action Required**: Retain and upgrade `app/rag/` as the single RAG engine. Deprecate `app/services/ai/knowledge_rag.py` during backend consolidation.

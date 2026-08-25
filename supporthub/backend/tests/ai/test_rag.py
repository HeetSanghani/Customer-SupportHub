"""Unit tests for Ground-Truth RAG Pipeline."""
import unittest
from app.rag.document_processor import DocumentProcessor
from app.rag.chunker import DocumentChunker
from app.rag.embeddings import LocalVectorEmbeddingProvider, cosine_similarity
from app.rag.pipeline import rag_pipeline


class TestRAGPipeline(unittest.TestCase):
    """Test RAG ingestion, chunking, embedding, and semantic retrieval."""

    @classmethod
    def setUpClass(cls):
        rag_pipeline.initialize()

    def test_document_processing(self):
        processor = DocumentProcessor()
        docs = processor.process_all_documents()
        self.assertGreater(len(docs), 0)
        
        # Check metadata
        for d in docs:
            self.assertTrue(len(d.source_id) > 0)
            self.assertTrue(len(d.title) > 0)
            self.assertTrue(len(d.content) > 0)

    def test_chunking(self):
        processor = DocumentProcessor()
        docs = processor.process_all_documents()
        chunker = DocumentChunker(chunk_size=400, chunk_overlap=30)
        chunks = chunker.chunk_all(docs)
        self.assertGreater(len(chunks), len(docs))
        
        first_chunk = chunks[0]
        self.assertIsNotNone(first_chunk.text)
        self.assertIsNotNone(first_chunk.source_id)
        self.assertIsNotNone(first_chunk.title)

    def test_vector_embeddings(self):
        provider = LocalVectorEmbeddingProvider()
        corpus = [
            "What is the return policy of ShopKart for electronics?",
            "How long do refunds take for UPI transactions?",
            "How can I reset my password if I forgot it?"
        ]
        provider.fit(corpus)
        vecs = provider.embed_batch(corpus)
        self.assertEqual(len(vecs), 3)

        # Same query similarity
        q_vec = provider.embed_text("return policy for electronics")
        sim_return = cosine_similarity(q_vec, vecs[0])
        sim_pwd = cosine_similarity(q_vec, vecs[2])
        self.assertGreater(sim_return, sim_pwd)

    def test_semantic_retrieval(self):
        # Query return policy
        res1 = rag_pipeline.query("What is the return policy for electronics?")
        self.assertTrue(res1["has_knowledge"])
        self.assertGreater(len(res1["citations"]), 0)
        self.assertTrue(any("Return" in c["title"] or "POL-001" in c["source_id"] for c in res1["citations"]))

        # Query UPI refunds
        res2 = rag_pipeline.query("How long does a UPI refund take?")
        self.assertTrue(res2["has_knowledge"])
        self.assertGreater(len(res2["citations"]), 0)

        # Query Password Reset
        res3 = rag_pipeline.query("I forgot my ShopKart password. How to reset?")
        self.assertTrue(res3["has_knowledge"])
        self.assertGreater(len(res3["citations"]), 0)


if __name__ == "__main__":
    unittest.main()

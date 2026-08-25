"""Embedding Provider abstractions and local vector implementation."""
import math
import re
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from collections import Counter
from app.ai.config import settings


class BaseEmbeddingProvider(ABC):
    """Abstract interface for text embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate a dense or weighted vector representation for a single text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate vector representations for a batch of texts."""
        pass


class LocalVectorEmbeddingProvider(BaseEmbeddingProvider):
    """Local, dependency-free TF-IDF and n-gram keyword vectorizer."""

    STOPWORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
        "to", "was", "were", "will", "with", "i", "you", "my", "your",
        "what", "where", "how", "when", "can", "do", "does", "please", "me"
    }

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self._is_fitted: bool = False

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase words and bigrams."""
        tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())
        meaningful = [t for t in tokens if t not in self.STOPWORDS and len(t) > 1]
        
        # Add bigrams for compound phrases like "return_policy", "refund_timeline"
        bigrams = []
        for i in range(len(meaningful) - 1):
            bigrams.append(f"{meaningful[i]}_{meaningful[i+1]}")
        return meaningful + bigrams

    def fit(self, corpus: List[str]) -> None:
        """Fit vocabulary and compute Inverse Document Frequency (IDF)."""
        doc_count = len(corpus)
        df_counts: Counter = Counter()

        for doc in corpus:
            unique_tokens = set(self._tokenize(doc))
            for t in unique_tokens:
                df_counts[t] += 1

        self.vocabulary = {token: idx for idx, (token, _) in enumerate(df_counts.items())}
        self.idf = {
            token: math.log((doc_count + 1) / (count + 1)) + 1.0
            for token, count in df_counts.items()
        }
        self._is_fitted = True

    def embed_text(self, text: str) -> List[float]:
        """Convert a text string into a normalized TF-IDF vector."""
        if not self._is_fitted:
            tokens = self._tokenize(text)
            self.vocabulary = {token: idx for idx, token in enumerate(set(tokens))}
            self.idf = {token: 1.0 for token in self.vocabulary}
            self._is_fitted = True

        tokens = self._tokenize(text)
        tf_counts = Counter(tokens)
        vector = [0.0] * len(self.vocabulary)

        for token, count in tf_counts.items():
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                tf = count / max(len(tokens), 1)
                idf = self.idf.get(token, 1.0)
                vector[idx] = tf * idf

        # L2 Normalize
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Compute embeddings for a batch of texts."""
        if not self._is_fitted:
            self.fit(texts)
        return [self.embed_text(t) for t in texts]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two normalized vectors."""
    min_len = min(len(vec_a), len(vec_b))
    if min_len == 0:
        return 0.0
    dot = sum(vec_a[i] * vec_b[i] for i in range(min_len))
    return float(dot)


def get_embedding_provider() -> BaseEmbeddingProvider:
    """Factory function for embedding providers."""
    return LocalVectorEmbeddingProvider()

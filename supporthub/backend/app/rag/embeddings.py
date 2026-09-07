"""Embedding Provider abstractions and local vector implementation."""
import math
import re
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
from collections import Counter
from app.ai.config import settings

logger = logging.getLogger(__name__)


class BaseEmbeddingProvider(ABC):
    """Abstract interface for text embedding providers."""

    @property
    @abstractmethod
    def embedding_method(self) -> str:
        """Name/identifier of the active embedding method."""
        pass

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

    @property
    def embedding_method(self) -> str:
        return "local_tfidf"

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
    try:
        return GoogleEmbeddingProvider()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("[Embeddings] Falling back to LocalVectorEmbeddingProvider due to: %s", e)
        return LocalVectorEmbeddingProvider()


def _make_fallback_vector(text_str: str) -> List[float]:
    """Generate a deterministic 768-dim feature hashing vector for local fallback."""
    import math, re, zlib
    if not text_str or not text_str.strip():
        return [0.0] * 768

    tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text_str.lower())
    stopwords = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "in", "is", "it", "of", "on", "that", "the", "to", "what",
        "where", "how", "when", "can", "do", "does", "please", "me", "you", "your"
    }
    meaningful = [t for t in tokens if t not in stopwords and len(t) > 1]
    bigrams = [f"{meaningful[i]}_{meaningful[i+1]}" for i in range(len(meaningful) - 1)]
    all_terms = meaningful + bigrams

    vector = [0.0] * 768
    if not all_terms:
        return vector

    for term in all_terms:
        bucket = zlib.crc32(term.encode("utf-8")) % 768
        vector[bucket] += 1.0

    norm = math.sqrt(sum(v * v for v in vector)) or 1.0
    return [v / norm for v in vector]

def get_seconds_until_utc_midnight() -> float:
    """Calculate remaining seconds until 00:00 UTC daily quota reset."""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    tomorrow_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(300.0, (tomorrow_midnight - now).total_seconds())


class GoogleEmbeddingProvider(BaseEmbeddingProvider):
    """Production Google Generative AI Embedding Provider using text-embedding-004 / gemini-embedding-001."""

    PRIMARY_MODEL = "models/gemini-embedding-001"
    FALLBACK_MODEL = "models/gemini-embedding-001"
    MAX_BATCH_SIZE = 15

    def __init__(self, api_key: Optional[str] = None):
        import os
        from app.config import get_settings

        self.api_key = (
            api_key
            or get_settings().gemini_api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )
        if not self.api_key or not self.api_key.strip():
            raise ValueError(
                "[ERROR] GEMINI_API_KEY is missing. GoogleEmbeddingProvider requires a valid Gemini API key configured in .env."
            )

        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self._genai = genai
        self.active_model = self.PRIMARY_MODEL
        self._quota_cooldown_until: float = 0.0
        self._query_cache: Dict[Tuple[str, str], List[float]] = {}

    @property
    def quota_exceeded(self) -> bool:
        import time
        return time.time() < getattr(self, "_quota_cooldown_until", 0.0)

    @property
    def embedding_method(self) -> str:
        if self.quota_exceeded:
            return "feature_hash_fallback"
        return getattr(self, "active_model", "gemini-embedding-001")

    def _call_embed_with_retry(
        self,
        content: str | List[str],
        task_type: str,
        title: Optional[str] = None,
        max_retries: int = 5,
    ) -> dict:
        import time

        kwargs = {
            "model": self.active_model,
            "content": content,
            "task_type": task_type,
            "output_dimensionality": 768,
        }
        if title and isinstance(content, str):
            kwargs["title"] = title

        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
        last_error = None

        def _do_call(kw):
            return self._genai.embed_content(**kw)

        def _trigger_fallback(reason: str, cooldown_seconds: float = 20.0):
            was_exceeded = self.quota_exceeded
            self._quota_cooldown_until = time.time() + cooldown_seconds
            if not was_exceeded:
                content_preview = str(content)[:200] if content else "N/A"
                logger.error(
                    "[Embeddings ERROR] Google Gemini API rate limit fallback triggered (%s). "
                    "Entering %.1fs temporary cooldown; falling back to local feature hashing. Affected content preview: '%s'",
                    reason,
                    cooldown_seconds,
                    content_preview
                )
                try:
                    from app.rag.pipeline import rag_pipeline
                    if rag_pipeline.chunks:
                        logger.error("[Embeddings ERROR] Updating pgvector storage with feature hashing fallback vectors for %d chunks...", len(rag_pipeline.chunks))
                        rag_pipeline.retriever.index_chunks(rag_pipeline.chunks)
                except Exception as e:
                    logger.error("[Embeddings ERROR] Failed to update fallback database vectors: %s", e)

        for attempt in range(1, max_retries + 1):
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    fut = executor.submit(_do_call, kwargs)
                    return fut.result(timeout=15.0)
            except FutureTimeoutError:
                _trigger_fallback("Timeout > 15.0s", cooldown_seconds=15.0)
                if isinstance(content, list):
                    return {"embeddings": [_make_fallback_vector(str(txt)) for txt in content]}
                else:
                    return {"embedding": _make_fallback_vector(str(content))}
            except Exception as exc:
                err_msg = str(exc)
                if "404" in err_msg and self.active_model == self.PRIMARY_MODEL:
                    import logging
                    logging.getLogger(__name__).info(
                        "[Embeddings] Primary model %s unavailable (404), switching to fallback %s",
                        self.PRIMARY_MODEL,
                        self.FALLBACK_MODEL,
                    )
                    self.active_model = self.FALLBACK_MODEL
                    kwargs["model"] = self.FALLBACK_MODEL
                    kwargs["output_dimensionality"] = 768
                    try:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            fut = executor.submit(_do_call, kwargs)
                            return fut.result(timeout=3.0)
                    except Exception as fallback_exc:
                        last_error = fallback_exc
                else:
                    last_error = exc

                err_str = str(last_error or exc)
                if "429" in err_str or "Quota" in err_str or "ResourceExhausted" in err_str or "timeout" in err_str.lower():
                    # Differentiate between Daily Quota Exhaustion (PerDay) vs Transient Rate Limits (PerMinute)
                    is_daily_quota = (
                        "PerDay" in err_str
                        or "free_tier_requests" in err_str
                        or "EmbedContentRequestsPerDay" in err_str
                    )
                    if is_daily_quota:
                        cooldown = get_seconds_until_utc_midnight()
                        hours_left = cooldown / 3600.0
                        reason_msg = f"Daily Quota Exhausted (limit: 1000/day, reset in {hours_left:.2f}h)"
                    else:
                        import re
                        match = re.search(r"retry in (\d+(?:\.\d+)?)s", err_str, re.IGNORECASE)
                        cooldown = float(match.group(1)) + 2.0 if match else 20.0
                        reason_msg = f"Transient Rate Limit ({last_error or exc})"

                    _trigger_fallback(reason_msg, cooldown_seconds=cooldown)
                    if isinstance(content, list):
                        return {"embeddings": [_make_fallback_vector(str(txt)) for txt in content]}
                    else:
                        return {"embedding": _make_fallback_vector(str(content))}

                if attempt < max_retries:
                    time.sleep(2 * attempt)

        _trigger_fallback("Max retries exceeded", cooldown_seconds=30.0)
        if isinstance(content, list):
            return {"embeddings": [_make_fallback_vector(str(txt)) for txt in content]}
        else:
            return {"embedding": _make_fallback_vector(str(content))}

    def embed_text(
        self,
        text: str,
        task_type: str = "retrieval_query",
        title: Optional[str] = None,
    ) -> List[float]:
        """Embed a single text string (default task_type: retrieval_query) with memoization."""
        if not text or not text.strip():
            return [0.0] * 768

        if getattr(self, "quota_exceeded", False):
            return _make_fallback_vector(text)

        cache_key = (text.strip(), task_type)
        if cache_key in self._query_cache:
            return self._query_cache[cache_key]

        res = self._call_embed_with_retry(content=text, task_type=task_type, title=title)
        if isinstance(res, dict):
            embedding = res.get("embedding")
        elif hasattr(res, "embedding"):
            embedding = res.embedding
        elif hasattr(res, "__getitem__"):
            try:
                embedding = res["embedding"]
            except Exception:
                embedding = None
        else:
            embedding = None

        if not embedding:
            embedding = _make_fallback_vector(text)

        if not self.quota_exceeded:
            self._query_cache[cache_key] = embedding
        return embedding

    def embed_batch(
        self,
        texts: List[str],
        titles: Optional[List[str]] = None,
        task_type: str = "retrieval_document",
    ) -> List[List[float]]:
        """Embed a list of text strings in batches (default task_type: retrieval_document)."""
        if not texts:
            return []

        if getattr(self, "quota_exceeded", False):
            return [_make_fallback_vector(txt) for txt in texts]

        import time
        embeddings: List[List[float]] = []

        for i in range(0, len(texts), self.MAX_BATCH_SIZE):
            batch_texts = texts[i : i + self.MAX_BATCH_SIZE]
            batch_titles = titles[i : i + self.MAX_BATCH_SIZE] if titles else None

            # Format titles into text if provided for batch calls
            if batch_titles:
                formatted_batch = [
                    f"{t}\n{txt}".strip() if t else txt
                    for txt, t in zip(batch_texts, batch_titles)
                ]
            else:
                formatted_batch = [txt if txt and txt.strip() else " " for txt in batch_texts]

            res = self._call_embed_with_retry(
                content=formatted_batch,
                task_type=task_type,
            )
            batch_embeds = res.get("embedding") or res.get("embeddings")
            if not batch_embeds:
                # If single vector returned for batch, wrap it
                if "embedding" in res and isinstance(res["embedding"], list) and len(res["embedding"]) == 768:
                    batch_embeds = [res["embedding"]] * len(batch_texts)
                else:
                    raise ValueError(f"Empty batch embedding response from Google API for batch starting at index {i}")

            embeddings.extend(batch_embeds)
            if i + self.MAX_BATCH_SIZE < len(texts):
                time.sleep(1.0)

        return embeddings




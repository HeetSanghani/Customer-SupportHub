"""RAG Document Loader for ShopKart policies and knowledge articles."""
from typing import List, Dict, Any, Optional
from pathlib import Path
class RAGLoader:
    """Loads unstructured and semi-structured knowledge files for RAG processing."""

    def __init__(self, data_loader_instance: Optional[Any] = None):
        if data_loader_instance is None:
            from app.data_access.loader import data_loader
            self.data_loader = data_loader
        else:
            self.data_loader = data_loader_instance
        try:
            self._kb_dir = Path(__file__).resolve().parents[4] / "knowledge_base"
        except IndexError:
            self._kb_dir = Path("/app/knowledge_base")

    def load_raw_policies(self) -> List[Dict[str, Any]]:
        """Load raw policy records from knowledge_base or policies.json."""
        kb_policy_file = self._kb_dir / "policies" / "policies.json"
        if kb_policy_file.exists():
            import json
            with open(kb_policy_file, "r", encoding="utf-8") as f:
                return json.load(f)

        self.data_loader.load()
        return self.data_loader.policies_raw

    def load_raw_knowledge_articles(self) -> List[Dict[str, Any]]:
        """Load raw article records from knowledge_base or knowledge_articles.json."""
        kb_article_file = self._kb_dir / "articles" / "knowledge_articles.json"
        if kb_article_file.exists():
            import json
            with open(kb_article_file, "r", encoding="utf-8") as f:
                return json.load(f)

        self.data_loader.load()
        return self.data_loader.knowledge_articles_raw

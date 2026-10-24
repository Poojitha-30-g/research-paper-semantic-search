from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


REQUIRED_COLUMNS = ["paper_id", "title", "abstract", "authors", "year", "url"]


class PaperSearchEngine:
    """Keyword and semantic search over a local CSV of research-paper records."""

    def __init__(self, papers: pd.DataFrame, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        missing = [column for column in REQUIRED_COLUMNS if column not in papers.columns]
        if missing:
            raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

        self.papers = papers.copy().fillna("")
        self.papers["search_text"] = (
            self.papers["title"].astype(str) + ". " + self.papers["abstract"].astype(str)
        ).str.strip()

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.papers["search_text"])

        self.model = SentenceTransformer(model_name)
        self.paper_embeddings = self.model.encode(
            self.papers["search_text"].tolist(),
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def keyword_search(self, query: str, top_k: int = 5) -> pd.DataFrame:
        """Rank papers using TF-IDF keyword matching."""
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.tfidf_matrix).ravel()
        return self._format_results(scores, top_k)

    def semantic_search(self, query: str, top_k: int = 5) -> pd.DataFrame:
        """Rank papers using sentence embeddings and cosine similarity."""
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        scores = cosine_similarity(query_embedding, self.paper_embeddings).ravel()
        return self._format_results(scores, top_k)

    def _format_results(self, scores, top_k: int) -> pd.DataFrame:
        results = self.papers.copy()
        results["score"] = scores
        results = results.sort_values("score", ascending=False).head(top_k)
        results = results[results["score"] > 0].copy()
        columns = ["paper_id", "title", "abstract", "authors", "year", "url", "score"]
        return results[columns].reset_index(drop=True)

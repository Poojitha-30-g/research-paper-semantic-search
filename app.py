from pathlib import Path

import pandas as pd
import streamlit as st

from src.search_engine import PaperSearchEngine

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "papers.csv"

st.set_page_config(page_title="Research Paper Semantic Search", page_icon="🔎", layout="wide")

@st.cache_resource(show_spinner="Loading the text-embedding model (first run may take a minute)...")
def load_engine():
    papers = pd.read_csv(DATA_PATH).fillna("")
    return PaperSearchEngine(papers)

st.title("🔎 Research Paper Semantic Search Engine")
st.write(
    "Search a collection of research papers retrieved from arXiv "
    "using keyword matching or semantic similarity. "
    "This collection contains 100 records and is not a comprehensive academic search service."
)

with st.sidebar:
    st.header("Search settings")
    mode = st.radio("Search method", ["Semantic search", "Keyword search"])
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)
    st.caption("Semantic search downloads a pretrained embedding model the first time it runs.")

query = st.text_input(
    "What research topic are you looking for?",
    placeholder="e.g. finding misinformation on social media using neural networks",
)

try:
    engine = load_engine()
except Exception as exc:
    st.error("The search engine could not load. Check the installation instructions in README.md.")
    st.exception(exc)
    st.stop()

st.caption(f"Dataset contains {len(engine.papers)} research-paper records retrieved from arXiv.")

if query.strip():
    with st.spinner("Searching papers..."):
        if mode == "Semantic search":
            results = engine.semantic_search(query, top_k=top_k)
        else:
            results = engine.keyword_search(query, top_k=top_k)

    if results.empty:
        st.info("No results found. Try a broader query or switch search method.")
    else:
        st.subheader("Search results")
        for _, row in results.iterrows():
            with st.container(border=True):
                st.markdown(f"### {row['title']}")
                st.write(f"**Authors:** {row['authors'] or 'Not specified'}")
                st.write(f"**Year:** {row['year'] or 'Not specified'}")
                st.write(row["abstract"])
                score_label = "Similarity score" if mode == "Semantic search" else "Keyword relevance score"
                st.caption(f"{score_label}: {row['score']:.3f}")
                if row["url"]:
                    st.link_button("Open paper / source", row["url"])
                st.caption(f"Paper ID: {row['paper_id']}")

with st.expander("About this project"):
    st.markdown(
        """
        **Methods**
        - Keyword baseline: TF-IDF vectors and cosine similarity.
        - Semantic search: pretrained Sentence Transformers embeddings and cosine similarity.
        - Results are ranked by the selected method's score.

        **Limitations**
        - The dataset contains 100 records retrieved from arXiv and is not a live index of all research papers.
        - Similarity scores are ranking signals, not probabilities or proof that a result is relevant.
        - The quality of the search should be evaluated with a labelled query set before making performance claims.
        """
    )

st.divider()
st.caption("Built with Python, Pandas, scikit-learn, Sentence Transformers, and Streamlit.")

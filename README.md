# Research Paper Semantic Search Engine

A beginner-friendly demonstration app that searches a small local collection of research-paper-style records using either lexical keyword matching or semantic similarity.

## Features

- Search by meaning with a pretrained Sentence Transformers model.
- Compare semantic search with a TF-IDF keyword-search baseline.
- Rank results by cosine similarity.
- Streamlit interface.
- Small CSV dataset that can be replaced with a properly sourced collection.

## Important dataset note

The included `data/papers.csv` records are **synthetic demonstration records**, not real research papers. Several URLs point to general resource pages rather than individual papers. Do not describe these records as a real academic corpus, and do not use this demo dataset to make claims about retrieval performance on real research literature.

For a research-grade version, replace the sample records with real metadata and abstracts from a permitted source such as the Semantic Scholar API or arXiv metadata, follow that source's terms, and create a manually checked query/relevance set for evaluation.

## Requirements

- Ubuntu, Python 3.10 or 3.11 recommended
- Internet access on first run to download the pretrained embedding model
- Approximately a few GB of free disk space is recommended for Python packages and model cache

## Run on Ubuntu

Open a terminal in this project directory.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit should print a local URL, usually `http://localhost:8501`. Open it in your browser.

The first run downloads `sentence-transformers/all-MiniLM-L6-v2`. Subsequent runs use the local model cache unless it is cleared.

## Try these queries

- `finding misinformation on social media`
- `models that understand the meaning of text`
- `neural networks for medical scans`
- `retrieving documents for a question answering system`

Try each query with both search methods and compare the results. Semantic scores are similarity signals, not probabilities.

## How it works

1. Loads records from `data/papers.csv` with Pandas.
2. Joins each title and abstract into searchable text.
3. Builds a TF-IDF matrix for keyword search.
4. Encodes each record with a pretrained sentence-embedding model.
5. Encodes a query and ranks records by cosine similarity.
6. Displays the highest-scoring records in Streamlit.

## Repository structure

```text
research-paper-semantic-search/
├── app.py
├── data/
│   └── papers.csv
├── src/
│   ├── __init__.py
│   └── search_engine.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Evaluation plan for a research-grade extension

Do not claim that semantic search is better without testing it. To evaluate fairly:

1. Create at least 15–30 representative queries.
2. Have a human label which papers are relevant to each query.
3. Use the same corpus and query set for both methods.
4. Calculate Precision@K, Recall@K, and nDCG@K.
5. Report results, examples of failures, and limitations.
6. Keep a fixed version of the dataset and document how it was collected.

## Limitations

- The included data is synthetic and tiny.
- Search quality depends on the data, query, and embedding model.
- The app does not crawl the web or download full papers.
- Similarity does not establish factual correctness or scientific quality.
- No performance result is claimed by this repository.

## Responsible use

Use real datasets only when permitted, respect API terms and licensing, and cite the original paper metadata source. Do not upload API keys or private data to GitHub.

## Resume wording

After you have installed and tested it, you can describe the work accurately, for example:

> Built a Streamlit-based research text search prototype with TF-IDF keyword retrieval and Sentence Transformers embeddings; compared ranked outputs qualitatively and documented dataset limitations.

Only say you evaluated metrics or used a real paper corpus after you have actually done those things.

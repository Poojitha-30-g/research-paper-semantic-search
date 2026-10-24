# Research Paper Semantic Search Engine

A Python-based application that helps users discover relevant research papers using keyword matching and semantic search.

## Overview

Finding relevant research papers can be time-consuming when searching through large collections of academic publications. This project provides an interactive interface to search research paper titles and abstracts using two approaches: traditional keyword search and semantic search.

The application uses a dataset of 100 research paper records collected from arXiv.

## Features

- **Keyword Search:** Uses TF-IDF to represent text and cosine similarity to rank relevant papers.
- **Semantic Search:** Uses Sentence Transformers to generate text embeddings and identify papers with similar meanings.
- **Interactive Interface:** Built with Streamlit.
- **Ranked Results:** Displays relevant papers according to their similarity scores.
- **Paper Information:** Shows paper titles, abstracts, authors, publication years, and arXiv links.
- **Data Collection Script:** Includes a Python script to retrieve research paper metadata from arXiv.

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Sentence Transformers
- TF-IDF
- Cosine Similarity
- arXiv API

## Project Structure

```text
research-paper-semantic-search/
├── app.py
├── fetch_arxiv.py
├── requirements.txt
├── constraints.txt
├── README.md
├── data/
│   └── papers.csv
└── src/
    ├── __init__.py
    └── search_engine.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Poojitha-30-g/research-paper-semantic-search.git
cd research-paper-semantic-search
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If PyTorch installation causes problems on a CPU-only Linux system, install a compatible CPU-only PyTorch build before installing the remaining dependencies.

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use the application.

## How It Works

### Keyword Search

1. Converts paper text into numerical TF-IDF vectors.
2. Converts the user's query into the same vector representation.
3. Calculates cosine similarity between the query and paper vectors.
4. Ranks papers by their similarity scores.

### Semantic Search

1. Converts paper text into embeddings using the `all-MiniLM-L6-v2` Sentence Transformer model.
2. Converts the search query into an embedding.
3. Compares the query embedding with paper embeddings using cosine similarity.
4. Ranks papers according to their semantic similarity.

Semantic search can identify related concepts even when the query and paper use different words.

## Dataset

The project includes 100 research paper records collected from arXiv. The CSV file contains paper identifiers, titles, abstracts, authors, publication years, and links.

The collection is limited in size and should not be considered a comprehensive index of academic research.

To retrieve paper metadata again, run:

```bash
python fetch_arxiv.py
```

This script requires an internet connection.

## Current Limitations

- The current dataset contains only 100 papers.
- Search quality depends on the dataset and the relevance of the retrieved text.
- The search methods have not yet been evaluated using a formal benchmark.
- The application does not index the full arXiv collection.

## Future Improvements

- Expand the research paper dataset.
- Evaluate retrieval quality using Precision@K and Recall@K.
- Add filters for publication year and research topics.
- Improve the user interface and search experience.
- Explore more advanced information retrieval techniques.

## Author

**G. Siva Sai Poojitha**

B.Tech Computer Science and Engineering

GitHub: https://github.com/Poojitha-30-g

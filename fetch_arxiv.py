import csv
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

API_URL = "https://export.arxiv.org/api/query"

params = {
    "search_query": "cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
    "start": 0,
    "max_results": 100,
    "sortBy": "relevance",
    "sortOrder": "descending",
}

url = API_URL + "?" + urllib.parse.urlencode(params)

request = urllib.request.Request(
    url,
    headers={"User-Agent": "ResearchPaperSemanticSearch/1.0"}
)

print("Connecting to the arXiv API...")

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        xml_data = response.read()

except Exception as error:
    print("Could not download paper data:", error)
    print("Your original dataset has not been changed.")
    raise SystemExit(1)

namespace = {
    "atom": "http://www.w3.org/2005/Atom"
}

root = ET.fromstring(xml_data)
entries = root.findall("atom:entry", namespace)

papers = []

for entry in entries:
    title_element = entry.find("atom:title", namespace)
    abstract_element = entry.find("atom:summary", namespace)
    id_element = entry.find("atom:id", namespace)
    published_element = entry.find("atom:published", namespace)

    if (
        title_element is None
        or abstract_element is None
        or id_element is None
        or published_element is None
    ):
        continue

    paper_url = id_element.text.strip()
    paper_id = paper_url.rsplit("/", 1)[-1]

    title = " ".join(title_element.text.split())
    abstract = " ".join(abstract_element.text.split())

    authors = [
        author.find("atom:name", namespace).text
        for author in entry.findall("atom:author", namespace)
        if author.find("atom:name", namespace) is not None
    ]

    published_date = published_element.text[:10]
    year = datetime.strptime(published_date, "%Y-%m-%d").year

    papers.append({
        "paper_id": paper_id,
        "title": title,
        "abstract": abstract,
        "authors": ", ".join(authors),
        "year": year,
        "url": f"https://arxiv.org/abs/{paper_id}",
    })

if not papers:
    print("No papers were returned. Your original dataset is unchanged.")
    raise SystemExit(1)

output_file = Path("data/papers.csv")
temporary_file = output_file.with_suffix(".tmp")

with temporary_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "paper_id", "title", "abstract",
            "authors", "year", "url"
        ],
    )
    writer.writeheader()
    writer.writerows(papers)

temporary_file.replace(output_file)

print(f"\nSuccessfully saved {len(papers)} real paper records.")
print(f"Dataset: {output_file}")
print("\nFirst five paper titles:")

for paper in papers[:5]:
    print("-", paper["title"])

print("\nOriginal paper links are included in the CSV.")

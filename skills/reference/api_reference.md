# API Reference: Academic Databases

> **Universal Reference**: Used by both Claude (SKILL.md) and Codex (AGENTS.md)

---

## Overview

ScholaRAG uses 3 academic databases for automated paper retrieval:
1. **Semantic Scholar** (~40% open access PDF availability)
2. **OpenAlex** (~50% open access)
3. **arXiv** (~100% PDF access for preprints)

**Why these databases?**
- All provide **REST APIs** with generous rate limits
- All offer **PDF URLs** (direct download, no manual intervention)
- **No API keys required** (Semantic Scholar, arXiv)
- **No institutional subscriptions** needed

---

## 1. Semantic Scholar API

### Base URL
```
https://api.semanticscholar.org/graph/v1/paper/search
```

### Authentication
- ❌ **No API key required** for basic usage
- ✅ **Optional API key** for higher rate limits (1,000 requests/5 min → 5,000 requests/5 min)

### Rate Limits
- **Free tier**: 100 requests/5 minutes
- **With API key**: 1,000 requests/5 minutes

### Request Parameters (Used by ScholaRAG)

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string | Search query | `"chatbot language learning"` |
| `year` | string | Publication year filter | `"2015-2025"` |
| `fields` | string | Comma-separated fields | `"title,abstract,authors,year,openAccessPdf"` |
| `limit` | integer | Results per request (max 100) | `100` |
| `offset` | integer | Pagination offset | `0`, `100`, `200`, ... |

### Example Request (Bash)
```bash
curl -X GET \
  'https://api.semanticscholar.org/graph/v1/paper/search?query=chatbot+language+learning&year=2015-2025&fields=title,abstract,authors,year,openAccessPdf&limit=100&offset=0'
```

### Example Response (JSON)
```json
{
  "total": 2456,
  "offset": 0,
  "next": 100,
  "data": [
    {
      "paperId": "abc123",
      "title": "AI Chatbots for Speaking Practice in EFL",
      "abstract": "This study investigates...",
      "year": 2023,
      "authors": [
        {"authorId": "xyz789", "name": "Jane Doe"}
      ],
      "openAccessPdf": {
        "url": "https://arxiv.org/pdf/2301.12345.pdf",
        "status": "GREEN"
      }
    }
  ]
}
```

### Key Fields

**`openAccessPdf.url`**: Direct PDF download URL (40% of papers have this)

**`openAccessPdf.status`**:
- `GREEN`: Free to read (publisher-hosted)
- `GOLD`: Open access (journal policy)
- `BRONZE`: Free on publisher site (no license)
- `null`: No open access PDF available

### ScholaRAG Usage
```python
# scripts/01_fetch_papers.py, line ~46-100
response = requests.get(
    "https://api.semanticscholar.org/graph/v1/paper/search",
    params={
        'query': config['search_query'],
        'year': f"{config['year_start']}-{config['year_end']}",
        'fields': 'title,abstract,authors,year,openAccessPdf,externalIds',
        'limit': 100,
        'offset': offset
    },
    timeout=30
)
```

### Official Docs
https://api.semanticscholar.org/api-docs/graph

---

## 2. OpenAlex API

### Base URL
```
https://api.openalex.org/works
```

### Authentication
- ❌ **No API key required**
- ✅ **Polite pool access**: Add `mailto` parameter for higher rate limits

### Rate Limits
- **Standard**: 10 requests/second
- **Polite pool** (with `mailto`): 100 requests/second

### Request Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search query | `chatbot language learning` |
| `filter` | string | Filters (year, OA status) | `publication_year:2015-2025,is_oa:true` |
| `per_page` | integer | Results per request (max 200) | `200` |
| `page` | integer | Pagination (1-indexed) | `1`, `2`, `3`, ... |
| `mailto` | string | Your email (polite pool) | `yourname@example.com` |

### Example Request (Bash)
```bash
curl -X GET \
  'https://api.openalex.org/works?search=chatbot+language+learning&filter=publication_year:2015-2025&per_page=200&mailto=researcher@university.edu'
```

### Example Response (JSON)
```json
{
  "meta": {
    "count": 3245,
    "per_page": 200,
    "page": 1
  },
  "results": [
    {
      "id": "https://openalex.org/W1234567890",
      "title": "Conversational Agents in Language Education",
      "publication_year": 2022,
      "open_access": {
        "is_oa": true,
        "oa_url": "https://repository.edu/paper.pdf",
        "oa_status": "green"
      },
      "authorships": [
        {"author": {"display_name": "John Smith"}}
      ],
      "abstract_inverted_index": {
        "This": [0],
        "study": [1],
        "explores": [2],
        ...
      }
    }
  ]
}
```

### Key Fields

**`open_access.oa_url`**: Direct PDF URL (50% of papers)

**`open_access.oa_status`**:
- `green`: Repository-hosted (arXiv, PubMed Central)
- `gold`: Open access journal
- `hybrid`: Paid journal, OA option selected
- `bronze`: Free on publisher site
- `closed`: Not open access

**`abstract_inverted_index`**: Reconstructed into full abstract by ScholaRAG

### ScholaRAG Usage
```python
# scripts/01_fetch_papers.py, line ~120-180
response = requests.get(
    "https://api.openalex.org/works",
    params={
        'search': config['search_query'],
        'filter': f"publication_year:{config['year_start']}-{config['year_end']}",
        'per_page': 200,
        'mailto': 'scholarag@example.com'  # Polite pool
    },
    timeout=30
)
```

### Official Docs
https://docs.openalex.org/

---

## 3. arXiv API

### Base URL
```
http://export.arxiv.org/api/query
```

### Authentication
- ❌ **No API key required**

### Rate Limits
- **Standard**: 1 request/3 seconds (enforced by ScholaRAG `time.sleep(3)`)
- **Burst**: Allowed for small queries (<100 results)

### Request Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search_query` | string | Query with field specifiers | `all:chatbot AND all:language` |
| `start` | integer | Pagination offset (0-indexed) | `0`, `100`, `200`, ... |
| `max_results` | integer | Results per request (recommended <100) | `100` |
| `sortBy` | string | Sort order | `submittedDate`, `relevance` |
| `sortOrder` | string | Ascending/descending | `descending` |

### Example Request (Bash)
```bash
curl -X GET \
  'http://export.arxiv.org/api/query?search_query=all:chatbot+AND+all:language&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
```

### Example Response (Atom XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title type="html">ArXiv Query: chatbot language</title>
  <totalResults>456</totalResults>
  <entry>
    <id>http://arxiv.org/abs/2301.12345v1</id>
    <title>Neural Chatbots for L2 Speaking</title>
    <summary>This paper presents...</summary>
    <published>2023-01-15T00:00:00Z</published>
    <author>
      <name>Alice Johnson</name>
    </author>
    <link href="http://arxiv.org/abs/2301.12345v1" />
    <link title="pdf" href="http://arxiv.org/pdf/2301.12345v1" type="application/pdf"/>
  </entry>
</feed>
```

### Key Fields

**`<id>`**: arXiv ID (e.g., `2301.12345v1`)

**`<link title="pdf">`**: **100% guaranteed PDF URL** 🎉

**PDF URL format**: `https://arxiv.org/pdf/{arxiv_id}.pdf`

### ScholaRAG Usage
```python
# scripts/01_fetch_papers.py, line ~200-260
response = requests.get(
    "http://export.arxiv.org/api/query",
    params={
        'search_query': f"all:{query_term1} AND all:{query_term2}",
        'start': offset,
        'max_results': 100,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    },
    timeout=30
)

# Rate limiting (required by arXiv)
time.sleep(3)
```

### Official Docs
https://arxiv.org/help/api/

---

## Common Workflows

### Workflow 1: Fetch Papers from All 3 Databases

**Stage 1: Fetch (scripts/01_fetch_papers.py)**
```python
# Semantic Scholar
semantic_scholar_papers = fetch_semantic_scholar(
    query="chatbot language learning",
    year_start=2015,
    year_end=2025,
    limit=1000
)

# OpenAlex
openalex_papers = fetch_openalex(
    query="chatbot language learning",
    year_start=2015,
    year_end=2025,
    limit=2000
)

# arXiv
arxiv_papers = fetch_arxiv(
    query="chatbot AND language",
    limit=500
)

# Combine and save
all_papers = semantic_scholar_papers + openalex_papers + arxiv_papers
pd.DataFrame(all_papers).to_csv("data/01_identification/combined.csv")
```

**Expected result**:
- Total papers: ~3,500-4,000
- PDF availability: ~50-60% (weighted average)

---

### Workflow 2: Filter for Open Access Only

**Semantic Scholar filter**:
```python
# Only keep papers with openAccessPdf
papers_with_pdf = [
    p for p in papers
    if p.get('openAccessPdf') and p['openAccessPdf'].get('url')
]
```

**OpenAlex filter**:
```python
# Add filter to API request
params = {
    'search': query,
    'filter': 'publication_year:2015-2025,is_oa:true'  # ← Open access only
}
```

**arXiv** (no filter needed, 100% have PDFs):
```python
# All arXiv papers have PDFs by default
```

---

## Error Handling

### Common Errors

**Error 1: Semantic Scholar Rate Limit (429)**
```python
if response.status_code == 429:
    print("Rate limit exceeded. Waiting 60 seconds...")
    time.sleep(60)
    # Retry request
```

**Error 2: OpenAlex Timeout**
```python
try:
    response = requests.get(url, params=params, timeout=30)
except requests.exceptions.Timeout:
    print("OpenAlex timeout. Retrying with smaller batch...")
    params['per_page'] = 100  # Reduce from 200 to 100
```

**Error 3: arXiv Invalid Query**
```python
# arXiv requires proper field specifiers
# Bad: "chatbot language learning"
# Good: "all:chatbot AND all:language AND all:learning"

query_formatted = "all:" + " AND all:".join(query.split())
```

---

## Integration with ScholaRAG Scripts

### scripts/01_fetch_papers.py
- Calls all 3 APIs
- Saves to `data/01_identification/{database}_results.csv`
- Returns: title, abstract, authors, year, doi, arxiv_id, pdf_url

### scripts/04_download_pdfs.py
- Reads `pdf_url` from CSV
- Downloads to `data/pdfs/{paper_id}.pdf`
- Retry logic (3 attempts with backoff)
- Success rate tracking (expected 40-60%)

---

## Performance Benchmarks

| Database | Papers/Request | Requests/Min | Papers/Hour | PDF Success |
|----------|----------------|--------------|-------------|-------------|
| Semantic Scholar | 100 | 20 | ~12,000 | 40% |
| OpenAlex (polite) | 200 | 60 | ~72,000 | 50% |
| arXiv | 100 | 20 (3s delay) | ~12,000 | 100% |

**Total throughput**: ~30,000 papers/hour (if running all 3 in parallel)

---

## FAQ

### Q1: Which database should I prioritize?
**A**: Depends on your domain:
- **CS/AI/ML**: arXiv (100% PDF, preprints)
- **Education/Social Science**: Semantic Scholar + OpenAlex (broader coverage)
- **Medicine/Health**: OpenAlex (includes PubMed Central)

### Q2: Why not use PubMed/Scopus/Web of Science?
**A**: Those APIs **do not provide PDF URLs**. You'd need:
1. Institutional subscription ($$)
2. Manual PDF download (defeats automation purpose)
3. Copyright restrictions (can't redistribute)

ScholaRAG prioritizes **automation** → Only use APIs with direct PDF access.

### Q3: How to get Semantic Scholar API key?
Visit: https://www.semanticscholar.org/product/api#api-key

Add to `.env`:
```bash
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```

Use in script:
```python
headers = {'x-api-key': os.getenv('SEMANTIC_SCHOLAR_API_KEY')}
response = requests.get(url, params=params, headers=headers)
```

---

**Maintained by**: ScholaRAG Core Team
**Last Updated**: 2025-10-24
**Status**: Universal Reference (Claude + Codex)

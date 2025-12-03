# API Reference: Academic Databases

> **Universal Reference**: Used by both Claude (SKILL.md) and Codex (AGENTS.md)

---

## Overview

ScholaRAG supports **5 academic databases** for paper retrieval:

### Open Access Databases (PDF URLs available)
1. **Semantic Scholar** (~40% open access PDF availability)
2. **OpenAlex** (~50% open access)
3. **arXiv** (~100% PDF access for preprints)

### Institutional Databases (Metadata only - NO PDF URLs)
4. **Scopus** (Elsevier) - Requires API key + institutional access
5. **Web of Science** (Clarivate) - Requires API key

**Open Access vs Institutional:**
| Feature | Open Access (SS, OA, arXiv) | Institutional (Scopus, WoS) |
|---------|---------------------------|---------------------------|
| API Keys | Free/Optional | Required (institutional) |
| PDF URLs | Yes (40-100%) | **NO** (metadata only) |
| Rate Limits | Generous | Moderate |
| Coverage | CS, Engineering, Biomedical | Comprehensive, all fields |

**Why this distinction?**
- Open access databases provide **automated PDF retrieval**
- Institutional databases provide **metadata** but require manual PDF download
- For full-text RAG analysis, open access databases are preferred

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

## 4. Scopus API (Elsevier)

> ⚠️ **INSTITUTIONAL DATABASE**: Provides metadata only - NO PDF URLs

### Base URL
```
https://api.elsevier.com/content/search/scopus
```

### Authentication
- ✅ **API key REQUIRED**: `SCOPUS_API_KEY`
- ✅ **Optional**: `SCOPUS_INST_TOKEN` (for full institutional access)

### How to Get API Key
1. Visit: https://dev.elsevier.com/
2. Create an account or sign in
3. Request API access (requires institutional affiliation)
4. Add to `.env`:
   ```bash
   SCOPUS_API_KEY=your_key_here
   SCOPUS_INST_TOKEN=your_inst_token  # Optional
   ```

### Rate Limits
- **Standard**: 6 requests/second
- **With Inst Token**: Higher limits available

### Request Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string | Scopus search query | `TITLE-ABS-KEY(chatbot)` |
| `start` | integer | Pagination offset | `0`, `25`, `50`, ... |
| `count` | integer | Results per request (max 25) | `25` |
| `sort` | string | Sort order | `-coverDate` (newest first) |
| `view` | string | Response detail level | `COMPLETE` |

### Example Request (Bash)
```bash
curl -X GET \
  'https://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY(chatbot)%20AND%20PUBYEAR%20>%202015&start=0&count=25&sort=-coverDate&view=COMPLETE' \
  -H 'X-ELS-APIKey: YOUR_API_KEY' \
  -H 'Accept: application/json'
```

### Key Fields
- `dc:title`: Paper title
- `dc:description`: Abstract
- `prism:coverDate`: Publication date
- `prism:doi`: DOI
- `citedby-count`: Citation count
- **NO `pdf_url`**: Scopus does NOT provide PDF URLs

### ScholaRAG Usage
```python
# scripts/01_fetch_papers.py
response = requests.get(
    "https://api.elsevier.com/content/search/scopus",
    params={
        'query': f"TITLE-ABS-KEY({query}) AND PUBYEAR >= {year_start}",
        'start': offset,
        'count': 25,
        'sort': '-coverDate',
        'view': 'COMPLETE'
    },
    headers={
        'X-ELS-APIKey': os.getenv('SCOPUS_API_KEY'),
        'Accept': 'application/json'
    }
)
```

### Official Docs
https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl

---

## 5. Web of Science API (Clarivate)

> ⚠️ **INSTITUTIONAL DATABASE**: Provides metadata only - NO PDF URLs

### Base URL
```
https://api.clarivate.com/apis/wos-starter/v1/documents
```

### Authentication
- ✅ **API key REQUIRED**: `WOS_API_KEY`

### How to Get API Key
1. Visit: https://developer.clarivate.com/apis
2. Sign up for Web of Science Starter API
3. Get API key (requires institutional subscription)
4. Add to `.env`:
   ```bash
   WOS_API_KEY=your_key_here
   ```

### Rate Limits
- **Starter API**: 5 requests/second, 50 results/request

### Request Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | WoS search query | `TS=(chatbot AND learning)` |
| `page` | integer | Page number (1-indexed) | `1`, `2`, `3`, ... |
| `limit` | integer | Results per page (max 50) | `50` |
| `sortField` | string | Sort field | `PY` (publication year) |
| `order` | string | Sort order | `desc` |

### Example Request (Bash)
```bash
curl -X GET \
  'https://api.clarivate.com/apis/wos-starter/v1/documents?q=TS=(chatbot%20AND%20learning)%20AND%20PY=2015-2024&page=1&limit=50&sortField=PY&order=desc' \
  -H 'X-ApiKey: YOUR_API_KEY' \
  -H 'Accept: application/json'
```

### Key Fields
- `source.title`: Paper title
- `source.abstract`: Abstract
- `source.publishYear`: Publication year
- `identifiers.doi`: DOI
- `citations.count`: Citation count
- **NO `pdf_url`**: WoS does NOT provide PDF URLs

### ScholaRAG Usage
```python
# scripts/01_fetch_papers.py
response = requests.get(
    "https://api.clarivate.com/apis/wos-starter/v1/documents",
    params={
        'q': f"TS=({query}) AND PY={year_start}-{year_end}",
        'page': page,
        'limit': 50,
        'sortField': 'PY',
        'order': 'desc'
    },
    headers={
        'X-ApiKey': os.getenv('WOS_API_KEY'),
        'Accept': 'application/json'
    }
)
```

### Official Docs
https://developer.clarivate.com/apis/wos-starter/swagger

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

### Open Access Databases
| Database | Papers/Request | Requests/Min | Papers/Hour | PDF Success |
|----------|----------------|--------------|-------------|-------------|
| Semantic Scholar | 100 | 20 | ~12,000 | 40% |
| OpenAlex (polite) | 200 | 60 | ~72,000 | 50% |
| arXiv | 100 | 20 (3s delay) | ~12,000 | 100% |

### Institutional Databases (Metadata Only)
| Database | Papers/Request | Requests/Min | Papers/Hour | PDF Success |
|----------|----------------|--------------|-------------|-------------|
| Scopus | 25 | 120 | ~30,000 | **0%** ⚠️ |
| Web of Science | 50 | 120 | ~60,000 | **0%** ⚠️ |

**Open Access throughput**: ~30,000 papers/hour (if running all 3 in parallel)
**Total with institutional**: ~120,000 papers/hour (metadata only for Scopus/WoS)

---

## FAQ

### Q1: Which database should I prioritize?
**A**: Depends on your domain:
- **CS/AI/ML**: arXiv (100% PDF, preprints)
- **Education/Social Science**: Semantic Scholar + OpenAlex (broader coverage)
- **Medicine/Health**: OpenAlex (includes PubMed Central)

### Q2: When should I use Scopus/Web of Science?
**A**: Use institutional databases when:
1. **Comprehensive coverage is critical** (e.g., systematic review for publication)
2. **Your institution provides API access** (check with your library)
3. **You can manually download PDFs** from your institution's portal

**Trade-offs**:
- ✅ **Pro**: More comprehensive coverage than open access alone
- ❌ **Con**: No automated PDF download (metadata only)
- ❌ **Con**: Requires API keys + institutional subscription

**Recommendation**: Start with open access (semantic_scholar, openalex, arxiv). Add Scopus/WoS if coverage is insufficient.

### Q3: How do I enable Scopus or Web of Science?
**A**:
1. Get API keys from your institution
2. Add to `.env`:
   ```bash
   SCOPUS_API_KEY=your_key
   SCOPUS_INST_TOKEN=your_token  # Optional
   WOS_API_KEY=your_key
   ```
3. Initialize with: `scholarag init --databases semantic_scholar openalex arxiv scopus wos`

### Q4: How to get Semantic Scholar API key?
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

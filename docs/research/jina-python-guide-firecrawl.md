# Using Jina Programmatically with Python

> A comprehensive guide to programmatically utilizing Jina AI services via Python, compiled from multiple sources using Firecrawl MCP search and scrape capabilities.

## Overview

Jina AI provides several APIs that can be accessed programmatically via Python:
- **Reader API** - Convert URLs to LLM-friendly markdown
- **Embeddings API** - Generate text/image embeddings
- **Reranker API** - Rank documents by relevance
- **Search API** - Web search with SERP results
- **DeepSearch** - Advanced search with reasoning
- **Classifier API** - Train and use classifiers
- **Segmenter API** - Tokenize and segment long text

## Reader API

### Basic Usage

The Reader API (`r.jina.ai`) extracts main content from webpages and converts it to clean, LLM-friendly markdown.

#### Simple GET Request

```python
import requests

# Basic usage - prepend r.jina.ai to any URL
url = "https://r.jina.ai/https://www.example.com"
response = requests.get(url)
content = response.text
print(content)
```

#### With API Key for Higher Rate Limits

```python
import requests

url = "https://r.jina.ai/https://www.example.com"
headers = {
    "X-Return-Format": "markdown",
    "Authorization": "Bearer YOUR_JINA_API_KEY"
}
response = requests.get(url, headers=headers)
content = response.text
```

#### Advanced Options

```python
import requests

url = "https://r.jina.ai/https://www.example.com"
headers = {
    "Authorization": "Bearer YOUR_JINA_API_KEY",
    "X-Return-Format": "markdown",
    "X-Token-Budget": "10000",  # Limit token usage
    "X-Timeout": "30",  # Maximum wait time in seconds
}

response = requests.get(url, headers=headers)
content = response.text
```

### Reader API Features

- **PDF Support**: Natively supports PDF reading
- **Image Captioning**: Automatically captions images on webpages
- **Multilingual**: Returns content in original language
- **Caching**: Caches content for 5 minutes
- **Rate Limits**:
  - Without API key: 20 RPM
  - With API key: 500 RPM
  - With Premium API key: 5000 RPM

## Search API (SERP)

The Search API (`s.jina.ai`) searches the web and returns top results with clean content.

```python
import requests

# Search the web
query = "Python machine learning tutorials"
search_url = f"https://s.jina.ai/?q={query}"

headers = {
    "Authorization": "Bearer YOUR_JINA_API_KEY"
}

response = requests.get(search_url, headers=headers)
results = response.text  # Returns markdown with top 5 results
```

## Embeddings API

Generate embeddings for text or images.

```python
import requests
import json

url = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_JINA_API_KEY"
}

data = {
    "model": "jina-embeddings-v2-base-en",
    "input": ["Your text here"]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
embeddings = result["data"][0]["embedding"]
```

### Multimodal Embeddings

```python
import requests
import json

url = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_JINA_API_KEY"
}

data = {
    "model": "jina-clip-v2",
    "input": [
        "text: A beautiful sunset over mountains",
        "image: https://example.com/image.jpg"
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
```

## Reranker API

Rank documents by relevance to a query.

```python
import requests
import json

url = "https://api.jina.ai/v1/rerank"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_JINA_API_KEY"
}

data = {
    "model": "jina-reranker-v3",
    "query": "Organic skincare products for sensitive skin",
    "top_n": 3,
    "documents": [
        "Document 1 content here...",
        "Document 2 content here...",
        "Document 3 content here..."
    ],
    "return_documents": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
ranked_docs = result["results"]
```

### Reranker Features

- **Multilingual**: Supports 100+ languages
- **Code Search**: Ranks code snippets based on natural language queries
- **Function Calling**: Supports agentic RAG applications
- **Tabular Data**: Ranks relevant tables before SQL generation
- **Max Documents**: Can rerank up to 2048 documents per query

## Python SDK (jinaai-py)

The official Python SDK provides a convenient interface for Jina AI services.

### Installation

```bash
pip install jinaai
```

### Usage

```python
from jinaai import JinaAI

jinaai = JinaAI(
    secrets={
        'promptperfect-secret': 'XXXXXX',
        'scenex-secret': 'XXXXXX',
        'rationale-secret': 'XXXXXX',
        'jinachat-secret': 'XXXXXX',
        'bestbanner-secret': 'XXXXXX',
    }
)

# Describe images
descriptions = jinaai.describe('https://picsum.photos/200')

# Optimize prompts
prompts = jinaai.optimize('Write an Hello World function in Python')

# Generate answers
output = jinaai.generate('Give me a recipe for a pizza with pineapple')

# Create images from text
output = jinaai.imagine('A controversial fusion of sweet pineapple and savory pizza.')
```

## Rate Limits

Rate limits are tracked by **RPM** (requests per minute) and **TPM** (tokens per minute):

| Product | Endpoint | w/o API Key | w/ API Key | w/ Premium Key |
|---------|----------|-------------|------------|----------------|
| Reader API | `r.jina.ai` | 20 RPM | 500 RPM | 5000 RPM |
| Search API | `s.jina.ai` | Blocked | 100 RPM | 1000 RPM |
| Embeddings API | `api.jina.ai/v1/embeddings` | Blocked | 500 RPM & 1M TPM | 2000 RPM & 5M TPM |
| Reranker API | `api.jina.ai/v1/rerank` | Blocked | 500 RPM & 1M TPM | 2000 RPM & 5M TPM |

## Pricing

- **Free Trial**: 10 million tokens for new API keys
- **Prototype Development**: $50 for 1 billion tokens ($0.050/1M tokens)
- **Production Deployment**: $500 for 11 billion tokens ($0.045/1M tokens)

## Best Practices

### Error Handling

```python
import requests
from requests.exceptions import RequestException

def fetch_with_jina(url, api_key=None):
    try:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.get(f"https://r.jina.ai/{url}", headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
```

### Rate Limit Management

```python
import time
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests=500, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def wait_if_needed(self):
        now = datetime.now()
        # Remove requests outside time window
        while self.requests and (now - self.requests[0]).seconds > self.time_window:
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0]).seconds
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.requests.append(now)

# Usage
limiter = RateLimiter(max_requests=500, time_window=60)

for url in urls:
    limiter.wait_if_needed()
    content = fetch_with_jina(url, api_key)
```

### Batch Processing

```python
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(f"https://r.jina.ai/{url}", headers=headers, timeout=30)
        return url, response.text
    except Exception as e:
        return url, None

def batch_fetch(urls, api_key, max_workers=5):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_url, url, api_key): url for url in urls}
        for future in as_completed(futures):
            url, content = future.result()
            results[url] = content
    return results
```

## Example: AI-Powered Web Scraper

Here's a complete example combining Jina Reader API with an LLM for intelligent data extraction:

```python
import requests
import json
from groq import Groq
import time

JINA_READER_PREFIX = "https://r.jina.ai/"

def get_markdown_from_url(url: str, api_key: str = None) -> str | None:
    """Fetch clean markdown content from URL using Jina Reader API."""
    full_url = f"{JINA_READER_PREFIX}{url}"
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    time.sleep(0.5)  # Rate limiting
    try:
        response = requests.get(full_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {full_url}: {e}")
        return None

def extract_with_groq(groq_client: Groq, prompt: str, context: str) -> dict | None:
    """Extract structured data using Groq LLM."""
    if not context:
        return None

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert assistant extracting structured data. Respond ONLY with the requested JSON object."},
                {"role": "user", "content": f"{prompt}\n\nHere is the text:\n\n{context}"}
            ],
            model='llama3-8b-8192',
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        content = chat_completion.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error extracting with Groq: {e}")
        return None

# Example usage
groq_client = Groq(api_key="your-groq-api-key")
jina_api_key = "your-jina-api-key"

# Get clean content
url = "https://example-store.com/products"
markdown_content = get_markdown_from_url(url, jina_api_key)

# Extract product information
prompt = """
From the provided text representing a product listing page, extract the primary products shown.
For each product, identify its:
1. `name`: The main product name/title.
2. `product_url`: The relative or absolute URL to the product's detail page.
3. `image_url`: The URL of the main product image shown in the listing.
4. `price`: The displayed price text (e.g., "$99.99", "£25.00").

Respond ONLY with a single valid JSON object with one key "products" whose value is a JSON list of these product objects.
"""

products = extract_with_groq(groq_client, prompt, markdown_content)
print(json.dumps(products, indent=2))
```

## Resources

- **Official Documentation**: https://jina.ai/reader
- **Python SDK**: https://github.com/jina-ai/jinaai-py
- **API Dashboard**: https://jina.ai/api-dashboard
- **Status Page**: https://status.jina.ai/
- **MCP Server**: https://github.com/jina-ai/MCP

## Source

This guide was compiled using Firecrawl MCP Server's `firecrawl_search` and `firecrawl_scrape` tools to gather information from multiple sources including:
- Official Jina AI documentation
- GitHub repositories
- Tutorial articles and blog posts
- API reference documentation

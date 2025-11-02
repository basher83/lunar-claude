# Python

> Firecrawl Python SDK is a wrapper around the Firecrawl API to help you easily turn websites into markdown.

Example useage can be found at <https://github.com/firecrawl/firecrawl/blob/main/apps/python-sdk/>

## Installation

To install the Firecrawl Python SDK, you can use pip:

```python Python theme={null}
# pip install firecrawl-py

from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
```

## Usage

1. Get an API key from [firecrawl.dev](https://firecrawl.dev)
2. Set the API key as an environment variable named `FIRECRAWL_API_KEY` or pass it as a parameter to the `Firecrawl`
   class.

Here's an example of how to use the SDK:

```python Python theme={null}
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_status = firecrawl.scrape(
  'https://firecrawl.dev',
  formats=['markdown', 'html']
)
print(scrape_status)

# Crawl a website:
crawl_status = firecrawl.crawl(
  'https://firecrawl.dev',
  limit=100,
  scrape_options={
    'formats': ['markdown', 'html']
  }
)
print(crawl_status)
```

### Scraping a URL

To scrape a single URL, use the `scrape` method. It takes the URL as a parameter and returns the scraped document.

```python Python theme={null}
# Scrape a website:
scrape_result = firecrawl.scrape('firecrawl.dev', formats=['markdown', 'html'])
print(scrape_result)
```

### Crawl a Website

To crawl a website, use the `crawl` method. It takes the starting URL and optional options as arguments. The options
allow you to specify additional settings for the crawl job, such as the maximum number of pages to crawl, allowed
domains, and the output format. See [Pagination](#pagination) for auto/manual pagination and limiting.

```python Python theme={null}
job = firecrawl.crawl(url="https://docs.firecrawl.dev", limit=5, poll_interval=1, timeout=120)
print(job)
```

### Start a Crawl

<Tip>Prefer non-blocking? Check out the [Async Class](#async-class) section below.</Tip>

Start a job without waiting using `start_crawl`. It returns a job `ID` you can use to check status. Use `crawl` when
you want a waiter that blocks until completion. See [Pagination](#pagination) for paging behavior and limits.

```python Python theme={null}
job = firecrawl.start_crawl(url="https://docs.firecrawl.dev", limit=10)
print(job)
```

### Checking Crawl Status

To check the status of a crawl job, use the `get_crawl_status` method. It takes the job ID as a parameter and returns
the current status of the crawl job.

```python Python theme={null}
status = firecrawl.get_crawl_status("<crawl-id>")
print(status)
```

### Cancelling a Crawl

To cancel an crawl job, use the `cancel_crawl` method. It takes the job ID of the `start_crawl` as a parameter and
returns the cancellation status.

```python Python theme={null}
ok = firecrawl.cancel_crawl("<crawl-id>")
print("Cancelled:", ok)
```

### Map a Website

Use `map` to generate a list of URLs from a website. The options let you customize the mapping process, including
excluding subdomains or utilizing the sitemap.

```python Python theme={null}
res = firecrawl.map(url="https://firecrawl.dev", limit=10)
print(res)
```

### Crawling a Website with WebSockets

To crawl a website with WebSockets, start the job with `start_crawl` and subscribe using the `watcher` helper. Create a
watcher with the job ID and attach handlers (e.g., for page, completed, failed) before calling `start()`.

```python Python theme={null}
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    firecrawl = AsyncFirecrawl(api_key="fc-YOUR-API-KEY")

    # Start a crawl first
    started = await firecrawl.start_crawl("https://firecrawl.dev", limit=5)

    # Watch updates (snapshots) until terminal status
    async for snapshot in firecrawl.watcher(started.id, kind="crawl", poll_interval=2, timeout=120):
        if snapshot.status == "completed":
            print("DONE", snapshot.status)
            for doc in snapshot.data:
                print("DOC", doc.metadata.source_url if doc.metadata else None)
        elif snapshot.status == "failed":
            print("ERR", snapshot.status)
        else:
            print("STATUS", snapshot.status, snapshot.completed, "/", snapshot.total)

asyncio.run(main())
```

### Pagination

Firecrawl endpoints for crawl and batch return a `next` URL when more data is available. The Python SDK auto-paginates
by default and aggregates all documents; in that case `next` will be `None`. You can disable auto-pagination or set
limits.

#### Crawl

Use the waiter method `crawl` for the simplest experience, or start a job and page manually.

##### Simple crawl (auto-pagination, default)

* See the default flow in [Crawl a Website](#crawl-a-website).

##### Manual crawl with pagination control (single page)

* Start a job, then fetch one page at a time with `auto_paginate=False`.

```python Python theme={null}
crawl_job = client.start_crawl("https://example.com", limit=100)

status = client.get_crawl_status(crawl_job.id, pagination_config=PaginationConfig(auto_paginate=False))
print("crawl single page:", status.status, "docs:", len(status.data), "next:", status.next)
```

##### Manual crawl with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `max_pages`, `max_results`, or `max_wait_time`.

```python Python theme={null}
status = client.get_crawl_status(
    crawl_job.id,
    pagination_config=PaginationConfig(max_pages=2, max_results=50, max_wait_time=15),
)
print("crawl limited:", status.status, "docs:", len(status.data), "next:", status.next)
```

#### Batch Scrape

Use the waiter method `batch_scrape`, or start a job and page manually.

##### Simple batch scrape (auto-pagination, default)

* See the default flow in [Batch Scrape](/features/batch-scrape).

##### Manual batch scrape with pagination control (single page)

* Start a job, then fetch one page at a time with `auto_paginate=False`.

```python Python theme={null}
batch_job = client.start_batch_scrape(urls)
status = client.get_batch_scrape_status(batch_job.id, pagination_config=PaginationConfig(auto_paginate=False))
print("batch single page:", status.status, "docs:", len(status.data), "next:", status.next)
```

##### Manual batch scrape with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `max_pages`, `max_results`, or `max_wait_time`.

```python Python theme={null}
status = client.get_batch_scrape_status(
    batch_job.id,
    pagination_config=PaginationConfig(max_pages=2, max_results=100, max_wait_time=20),
)
print("batch limited:", status.status, "docs:", len(status.data), "next:", status.next)
```

## Error Handling

The SDK handles errors returned by the Firecrawl API and raises appropriate exceptions. If an error occurs during a
request, an exception will be raised with a descriptive error message.

## Async Class

For async operations, use the `AsyncFirecrawl` class. Its methods mirror `Firecrawl`, but they don't block the main
thread.

```python Python theme={null}
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    firecrawl = AsyncFirecrawl(api_key="fc-YOUR-API-KEY")

    # Scrape
    doc = await firecrawl.scrape("https://firecrawl.dev", formats=["markdown"])  # type: ignore[arg-type]
    print(doc.get("markdown"))

    # Search
    results = await firecrawl.search("firecrawl", limit=2)
    print(results.get("web", []))

    # Crawl (start + status)
    started = await firecrawl.start_crawl("https://docs.firecrawl.dev", limit=3)
    status = await firecrawl.get_crawl_status(started.id)
    print(status.status)

    # Batch scrape (wait)
    job = await firecrawl.batch_scrape([
        "https://firecrawl.dev",
        "https://docs.firecrawl.dev",
    ], formats=["markdown"], poll_interval=1, timeout=60)
    print(job.status, job.completed, job.total)

asyncio.run(main())
```

import gzip
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

CRAWL = "CC-MAIN-2026-43"
MAX_URLS = 1_000_000
SHARDS = 250
QUOTA = MAX_URLS // SHARDS
EXTRA = QUOTA // 10
WORKERS = 4
MAX_PER_HOST = 25
MAX_LINES_PER_SHARD = 1_000_000
URLS_PATH = "tests/test_data/1m_urls.txt.gz"

def line_count(path):
    count = 0
    with gzip.open(path, "rt", encoding="utf-8") as file:
        for line in file:
            count += 1
    return count

if os.path.exists(URLS_PATH):
    if line_count(URLS_PATH) != MAX_URLS:
        raise RuntimeError(f"{URLS_PATH} is incomplete, delete it and run again")
    print(f"{URLS_PATH} already exists, delete it to download again")
    sys.exit(0)

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "shortly-test-data-fetcher"})
    for attempt in range(5):
        try:
            return urllib.request.urlopen(request, timeout=60)
        except urllib.error.HTTPError as error:
            if error.code != 503 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))

with fetch(f"https://data.commoncrawl.org/crawl-data/{CRAWL}/cc-index.paths.gz") as response:
    paths = gzip.decompress(response.read()).decode().split()

all_shards = []
for path in paths:
    if "/cdx-" in path:
        all_shards.append(path)

shards = []
for i in range(SHARDS):
    index = i * len(all_shards) // SHARDS
    shards.append(all_shards[index])

def read_shard(shard):
    urls = []
    host_counts = {}

    with fetch("https://data.commoncrawl.org/" + shard) as response, gzip.GzipFile(fileobj=response) as lines:
        for count, line in enumerate(lines):
            if count >= MAX_LINES_PER_SHARD or len(urls) >= QUOTA + EXTRA:
                break

            host = line.split(b")", 1)[0]
            host_count = host_counts.get(host, 0)
            if host_count >= MAX_PER_HOST:
                continue
            host_counts[host] = host_count + 1

            urls.append(json.loads(line.split(b" ", 2)[2])["url"])

    return urls

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(read_shard, shards))

selected = []
missing = MAX_URLS
for urls in results:
    selected.append(urls[:QUOTA])
    missing -= len(selected[-1])

for i in range(len(results)):
    if missing <= 0:
        break
    extra = results[i][QUOTA:QUOTA + missing]
    selected[i].extend(extra)
    missing -= len(extra)

url_count = 0
with gzip.open(URLS_PATH, "wt", encoding="utf-8") as file:
    for urls in selected:
        for url in urls:
            file.write(url + "\n")
            url_count += 1

if url_count != MAX_URLS:
    os.remove(URLS_PATH)
    raise RuntimeError(f"expected {MAX_URLS} URLs, got {url_count}")

print(f"done: {url_count} URLs")

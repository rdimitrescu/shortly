import gzip
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "src")
from hash import hash_url, validate_url

CRAWL = "CC-MAIN-2026-43"
MAX_URLS = 100_000
SHARDS = 100
QUOTA = MAX_URLS // SHARDS
WORKERS = 4
MAX_PER_HOST = 10
MAX_LINES_PER_SHARD = 200_000
RAW_PATH = "tests/test_data/100k_urls_raw.txt.gz"
CLEAN_PATH = "tests/test_data/100k_urls_clean.txt.gz"

def line_count(path):
    count = 0
    with gzip.open(path, "rt", encoding="utf-8") as file:
        for line in file:
            count += 1
    return count

if os.path.exists(RAW_PATH) and os.path.exists(CLEAN_PATH):
    if line_count(RAW_PATH) != MAX_URLS or line_count(CLEAN_PATH) != MAX_URLS:
        raise RuntimeError(f"{RAW_PATH} or {CLEAN_PATH} is incomplete, delete them and run again")
    print(f"{RAW_PATH} and {CLEAN_PATH} already exist, delete them to download again")
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
    raw_urls = []
    clean_urls = []
    seen = set()
    host_counts = {}

    with fetch("https://data.commoncrawl.org/" + shard) as response, gzip.GzipFile(fileobj=response) as lines:
        for count, line in enumerate(lines):
            if count >= MAX_LINES_PER_SHARD:
                break
            if len(raw_urls) >= QUOTA and len(clean_urls) >= QUOTA:
                break

            host = line.split(b")", 1)[0]
            host_count = host_counts.get(host, 0)
            if host_count >= MAX_PER_HOST:
                continue
            host_counts[host] = host_count + 1

            url = json.loads(line.split(b" ", 2)[2])["url"]

            if len(raw_urls) < QUOTA:
                raw_urls.append(url)

            if len(clean_urls) < QUOTA:
                try:
                    url = validate_url(url)
                    hash_url(url)
                except (ValueError, KeyError):
                    continue
                if url not in seen:
                    seen.add(url)
                    clean_urls.append(url)

    return raw_urls, clean_urls

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(read_shard, shards))

raw_count = 0
seen = set()
with gzip.open(RAW_PATH, "wt", encoding="utf-8") as raw, gzip.open(CLEAN_PATH, "wt", encoding="utf-8") as clean:
    for raw_urls, clean_urls in results:
        for url in raw_urls:
            raw.write(url + "\n")
            raw_count += 1
        for url in clean_urls:
            if url not in seen:
                seen.add(url)
                clean.write(url + "\n")

if raw_count != MAX_URLS or len(seen) != MAX_URLS:
    raise RuntimeError(f"expected {MAX_URLS} URLs, got {raw_count} raw and {len(seen)} clean")

print(f"done: {raw_count} raw, {len(seen)} clean")

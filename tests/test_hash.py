from hash import *
import os
import pytest
import gzip
from hash_alphabet import HASH_SPACE
import math

def test_invalid_urls():
    succeses = 0
    total_tested = 0
    with open("tests/test_data/invalid_urls.txt", encoding="utf-8") as invalid_urls:
        for line in invalid_urls:
            bad_url = line.strip()
            if not bad_url or bad_url[0] == '#':
                continue

            try:
                validate_url(bad_url)
            except ValueError as error:
                succeses += 1
            else:
                print("FAIL: DIDN'T STOP INVALID URL:", bad_url)
            finally:
                total_tested += 1

    assert succeses == total_tested, f"{total_tested - succeses} invalid URLs got through"

def test_valid_urls():
    succeses = 0
    total_tested = 0
    with open("tests/test_data/valid_urls.txt", encoding="utf-8") as valid_urls:
        for line in valid_urls:
            good_url = line.strip()
            if not good_url or good_url[0] == '#':
                continue

            try:
                validate_url(good_url)
            except ValueError as error:
                print("FAIL: GOOD URL DIDN'T PASS VALIDATION:", good_url, "with error code", error)
            else:
                succeses += 1
            finally:
                total_tested += 1

    assert succeses == total_tested, f"{total_tested - succeses} valid URLs were allowed to pass"

@pytest.mark.parametrize("url_amount", [10_000, 25_000, 50_000, 75_000, 100_000])
def test_url_colissions(url_amount:int):
    data_path = "tests/test_data/100k_urls_clean.txt.gz"
    
    if os.path.exists(data_path) == False:
        print("FAIL: CANNOT SOLVE FOR FILE: ", data_path)
        raise FileNotFoundError

    hash_map = {}
    collisions = 0
    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for url in f:
            try:
                url  = validate_url(url)
            except ValueError:
                continue

            hashed_url = hash_url(url)
            if hashed_url in hash_map and hash_map[hashed_url] != url:
                collisions += 1
            hash_map[hashed_url] = url

            if len(hash_map) >= url_amount:
                break

    # Calculated based on birthday paradox
    expected_colissions = len(hash_map) ** 2 / (2 * HASH_SPACE)
    # Aim to be within 10% of the expected colission calculation
    expected_colissions = math.ceil(expected_colissions * 1.10)

    if collisions <= expected_colissions:
        error = 0
    else:
        error = (collisions - expected_colissions) / expected_colissions

    print(f"\nFor {url_amount:,} URLs: expected collisions: {expected_colissions:.2f}, actual collisions: {collisions}")
    
    assert collisions <= expected_colissions, f"Error of {error:.0%} above expected collisions"
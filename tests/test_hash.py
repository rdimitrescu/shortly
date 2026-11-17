from hash import *

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
                print("SUCCESS: CAUGHT INVALID URL:", bad_url, "with error code", error)
                succeses += 1
            else:
                print("FAIL: DIDN'T STOP INVALID URL:", bad_url)
            finally:
                total_tested += 1

    print("--------------------------------")
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
                succeses += 1
            else:
                print("SUCCESS: GOOD URL PASSSED CHECKS:", good_url)
                succeses += 1
            finally:
                total_tested += 1

    print("--------------------------------")
    assert succeses == total_tested, f"{total_tested - succeses} valid URLs were allowed to pass"

def run_test_hash():
    test_invalid_urls()
    test_valid_urls()

if __name__ == "__main__":
    run_test_hash()
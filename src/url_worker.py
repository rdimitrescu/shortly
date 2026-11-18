from hash import *
SHORTLY_URL = "https://example.com/"

def get_hash(url:str) -> str:
    try:
        url = validate_url(url)
        hash_result = hash_url(url)
    except ValueError as error:
        print("HASH FAILED:", error)
    else:
        print("HASH_SUCCESFUL:", hash_url(url))

    return SHORTLY_URL + hash_result

def run_worker() -> None:
    print(get_hash("https://github.com/rdimitrescu/shortly"))

if __name__ == "__main__":
    run_worker()
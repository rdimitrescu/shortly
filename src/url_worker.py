from hash import *
from repository import db_single_write
from psycopg import Error
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
    for i in range(1,5):
        try:
            hash = get_hash("https://example.com/")
            db_single_write("https://example.com/", hash)

            hash = get_hash("https://github.com/")
            db_single_write("https://github.com/", hash)

            break
        except psycopg.Error as e:
            print("DB WRITE FAILED")

if __name__ == "__main__":
    run_worker()
from hash import *

def get_hash(url:str) -> str:
    try:
        url = validate_url(url)
        hash_result = hash_url(url)
    except ValueError as error:
        print("HASH FAILED:", error)
    else:
        print("HASH_SUCCESFUL:", hash_url(url))

    return hash_result
from hash_alphabet import *
from urllib.parse import urlparse

def hash_url(long_url:str) -> str:
    # Postional weight hash number calculation
    hash_number = 0
    for char in long_url:
        hash_number = (hash_number * URL_ALPHABET_LEN + 1 + URL_CHAR_TO_INDEX[char]) % HASH_SPACE

    # Base conversion step
    hash = ''
    for i in range(HASH_SIZE):
        hash += HASH_INDEX_TO_CHAR[hash_number % HASH_ALPHABET_LEN] 
        hash_number = hash_number // HASH_ALPHABET_LEN

    return hash

print(hash_url("https://github.com/"))

from hash_alphabet import *
from urllib.parse import urlsplit
import validators

def hash_url(url:str) -> str:
    # Postional weight hash number calculation
    hash_number = 0
    for char in url:
        hash_number = (hash_number * URL_ALPHABET_LEN + 1 + URL_CHAR_TO_INDEX[char]) % HASH_SPACE

    # Base conversion step
    hash = ''
    for i in range(HASH_SIZE):
        hash += HASH_INDEX_TO_CHAR[hash_number % HASH_ALPHABET_LEN] 
        hash_number = hash_number // HASH_ALPHABET_LEN

    return hash

# Make sure that provided links can be accessed
def validate_url(url:str) -> str:
    url = url.strip()

    if "://" not in url:
        url = "https://" + url

    if not validators.url(url):
        raise ValueError("Not a real URL")

    split_url = urlsplit(url)

    # Make it so only https links are allowed
    if split_url.scheme != "https":
        raise ValueError("HTTP protocol not allowed")

    if split_url.username != None:
        raise ValueError("Credentials in URL not allowed")

    hostname = split_url.hostname.strip(":\n ").rpartition(".")
    if hostname[-1] not in VALID_TLDS:
        raise ValueError("Not an accepted TLD")

    return url

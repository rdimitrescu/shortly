from hash_alphabet import *
from urllib.parse import urlparse

# No matter the imput format always return something in the form of www.example.com/page?id=gg
def strip_url(long_url:str) -> str:
    url_sections = urlparse(long_url)
    stripped_url = url_sections.netloc + url_sections.path + url_sections.query

# Postional weight hash
def hash_url(long_url:str) -> str:
    hash_number = 0
    index = 1
    for char in long_url:
        hash_number += (URL_CHAR_TO_INDEX[char] * index) % URL_ALPHABET_LEN
        index += 1

    hash = ''
    for i in range(HASH_SIZE):
        hash += HASH_INDEX_TO_CHAR[hash_number % HASH_ALPHABET_LEN] 
        hash_number = hash_number // HASH_ALPHABET_LEN

    return hash

print(hash_url("www.ae3070703363.com"))

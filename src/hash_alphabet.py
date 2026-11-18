import string

# URL's only contain these charachters
URL_ALPHABET = string.ascii_letters + string.digits + '.' + '-' + '_' + '~' + ':' + '?' +'/'
URL_ALPHABET_LEN = len(URL_ALPHABET)
MAX_URL_SIZE = 2048

URL_CHAR_TO_INDEX = {}
for index, char in enumerate(URL_ALPHABET):
    URL_CHAR_TO_INDEX[char] = index

# Hashes and should only contain these charachters
HASH_ALPHABET = string.ascii_letters + string.digits
HASH_ALPHABET_LEN = len(HASH_ALPHABET)
HASH_SIZE = 6
HASH_SPACE = HASH_ALPHABET_LEN ** HASH_SIZE

HASH_INDEX_TO_CHAR = {}
for index, char in enumerate(HASH_ALPHABET):
    HASH_INDEX_TO_CHAR [index] = char

HASH_CHAR_TO_INDEX = {}
for index, char in enumerate(HASH_ALPHABET):
    HASH_CHAR_TO_INDEX[char] = index

VALID_TLDS = set()
TLD_FILE_PATH = "./data/valid_tlds.txt"
with open(TLD_FILE_PATH, encoding="utf-8") as tld_file:
    for line in tld_file:
        VALID_TLDS.add(line.strip().lower())
        
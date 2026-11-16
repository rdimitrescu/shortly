import string

# URL's only contain these charachters
URL_ALPHABET = string.ascii_letters + string.digits + '.' + '-' + '_' + '~'
URL_ALPHABET_LEN = len(URL_ALPHABET)

URL_CHAR_TO_INDEX = {}
for index, char in enumerate(URL_ALPHABET):
    URL_CHAR_TO_INDEX[char] = index

# Hashes and should only contain these charachters
HASH_ALPHABET = string.ascii_letters + string.digits
HASH_ALPHABET_LEN = len(HASH_ALPHABET)
HASH_SIZE = 6

HASH_INDEX_TO_CHAR = {}
for index, char in enumerate(HASH_ALPHABET):
    HASH_INDEX_TO_CHAR [index] = char

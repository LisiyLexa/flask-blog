import string
import random

# Use the same alphabet as before
ALPHABET = string.digits + string.ascii_letters
CODE_LENGTH = 7


def random_code(length=CODE_LENGTH):
    return "".join(random.choices(ALPHABET, k=length))

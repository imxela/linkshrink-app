from hashids import Hashids
from sys import maxsize


def hash_string_to_int(str):
    # Adds the lower bounds of an integer to the hash to
    # ensure that the resulting number is non-negative
    return hash(str) + maxsize


# FIXME: The generated hashids are a little too long,
#        most likely because of how large numbers
#        hash_string_to_int() generates.
def generate_url_hash(target):
    return Hashids().encode(hash_string_to_int(target))

from flask import request
from . import hash
from . import database
from urllib.parse import urlparse


# Returns False if 'url' is not a valid URL.
# Otherwise a valid URL is returned.
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Shrinks the specified 'target_url'.
# If 'targer_url' isn't a valid URL, None is returned.
# If the 'target_url' already exists in the database,
# a link to the existing URL-hash is returned.
# If not, one is generated and added to the database,
# and then returned as a shortened link.
def shrink_url(target_url):
    is_valid = validate_url(target_url)
    if is_valid is False:
        print('{} is not a valid target URL'.format(target_url))
        return None

    print('Shrinking \'{}\'!'.format(target_url))

    url_hash = ''
    if database.exists_target(target_url):
        # The target URL already exists,
        # return shrunk URL instead of creating a new one
        url_hash = database.query_shrunk_url(target_url)
        print('\'{}\' already exists in database, using associated hash: \'{}\'!'.format(target_url, url_hash))
    else:
        url_hash = hash.generate_url_hash(target_url)
        database.insert_pair(url_hash, target_url)
        print('Successfully shrunk \'{}\' to hash \'{}\'.'.format(target_url, url_hash))

    # Below gives an actual URL for the url_hash, e.g:
    # https://www.linkshrink.app/Nk9XBq5VN4186
    return request.url_root + url_hash

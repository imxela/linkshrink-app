from flask import request
from . import hash
from . import database
from urllib.parse import urlparse
from werkzeug.utils import secure_filename


def validate_url(url):
    validated_url = secure_filename(url)
    validated_url = urlparse(validated_url)

    if not validated_url.scheme:
        validated_url = validated_url._replace(**{"scheme": "http"}).geturl()
    else:
        validated_url = validated_url.geturl()

    validated_url = validated_url.replace('///', '//')

    print('Validated \'{}\'')
    return validated_url


# Shrinks the specified 'target_url'.
# If the 'target_url' already exists in the database,
# a link to the existing URL-hash is returned.
# Oterwise, one is generated and added to the database,
# and then returned as a link.
def shrink_url(target_url):
    validated_url = validate_url(target_url)

    print('Shrinking \'{}\'!'.format(target_url))

    url_hash = ''
    if database.exists_target(validated_url):
        # The target URL already exists,
        # return shrunk URL instead of creating a new one
        url_hash = database.query_shrunk_url(validated_url)
        print('\'{}\' already exists in database, using associated hash: \'{}\'!'.format(validated_url, url_hash))
    else:
        url_hash = hash.generate_url_hash(validated_url)
        database.insert_pair(url_hash, validated_url)
        print('Successfully shrunk \'{}\' to hash \'{}\'.'.format(validated_url, url_hash))

    # Below gives an actual URL for the url_hash, e.g:
    # https://www.linkshrink.app/Nk9XBq5VN4186
    return request.url_root + url_hash

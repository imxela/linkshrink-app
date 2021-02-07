from flask import request, redirect, abort, current_app, g
from . import database


@current_app.route('/')
@current_app.route('/index')
def index_route():
    return 'Hello, World!'

# Responsible for redirecting the user to the target_url
# associated with the specified shrunk_url.
# Aborts a 404 if the speicifed shrunk_url does not exist.
@current_app.route('/<shrunk_url>')
def redirect_route(shrunk_url):
    url = database.query_target_url(shrunk_url)

    if url is not None:
        return redirect(url, code=302)
    else:
        print('Error: Invalid route or URL: "{}"'.format(request.path))
        abort(404)

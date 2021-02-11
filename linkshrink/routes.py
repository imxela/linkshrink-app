from flask import request, redirect, abort, current_app, g, render_template

from . import shortener
from . import database


@current_app.route('/', methods=['POST', 'GET'])
def index_route():
    if (request.method == 'POST'):
        print('POSTing @ index -- starting shrinking process')

        target_url = request.form.get('target_url')

        with current_app.app_context():
            shrunk_url = shortener.shrink_url(target_url)

        return render_template(
            'index.html',
            shrunk_url=shrunk_url,
            target_url=target_url
        )
    else:
        return render_template('index.html')

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

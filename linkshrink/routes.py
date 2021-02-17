from flask import request, redirect, abort, session, url_for
from flask import current_app, render_template

from . import shortener
from . import database


@current_app.route('/', methods=['POST', 'GET'])
def index_route():
    if (request.method == 'POST'):
        print('POSTing @ index -- starting shrinking process')

        target_url = request.form.get('url-input')

        with current_app.app_context():
            shrunk_url = shortener.shrink_url(target_url)

        # Store shortened URL in session to save it when redirecting
        session['url_input_value'] = shrunk_url
        # Redirect to same page to prevent form resubmission
        return redirect(url_for('index_route'), 303)
    else:
        # If user has generated a URL previously,
        # retrieve it from session and display it
        if 'url_input_value' in session:
            return render_template(
                'index.html',
                url_input_value=session.pop('url_input_value')
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

from flask import request, redirect, abort, session, url_for, flash
from flask import current_app, render_template

from . import shortener
from . import database

from urllib.parse import urlparse


@current_app.route('/', methods=['POST', 'GET'])
def index_route():
    if (request.method == 'POST'):
        print('POSTing @ index -- starting shrinking process')

        target_url = request.form.get('url-input')

        if not target_url:
            flash('You can not shrink an empty URL; please enter a valid URL in the input field below!', 'danger')
            return redirect(url_for('index_route'), 303)

        # Make sure the user isn't trying to
        # shorten a linkto the current domain
        parsed = urlparse(target_url)
        if parsed.netloc in request.url:
            flash('Shrinking links belonging to the linkshrink domain is not allowed!', 'danger')
            return redirect(url_for('index_route'), 303)

        with current_app.app_context():
            url_hash = shortener.shrink_url(target_url)

        # Store shortened URL in session to save it when redirecting
        session['url_input_value'] = url_hash
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
# associated with the specified url_hash.
# Aborts a 404 if the speicifed url_hash does not exist.
@current_app.route('/<url_hash>')
def redirect_route(url_hash):
    url = database.query_target_url(url_hash)

    if url is not None:
        return redirect(url, code=302)
    else:
        print('Error: Invalid route or URL: "{}"'.format(request.path))
        abort(404)

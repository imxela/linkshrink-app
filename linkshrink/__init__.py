import os

from flask import Flask, request, redirect, abort


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


# Factory function for creation and configuration of the app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Default development config
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'linkshrink.sqlite'),
    )

    # Differentiate between production and testing configs
    if test_config is None:
        # Load the production config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the passed test config
        app.config.from_mapping(test_config)

    # Create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Intercepts all incoming URLs to check if they match a
    # registered route or a shortened URL. (Or none, in which case 404)
    @app.before_request
    def shrunk_redirect():
        print('Requested path: {}'.format(request.path))

        # Ensure the current URL doesn't match any registered route
        url_routes = []
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and has_no_empty_params(rule):
                url_routes.append(rule.rule)

        for route in url_routes:
            if route == request.path:
                # Returning none will continue normal flow
                return None

        from linkshrink.db import get_db

        # Query for target url and redirect
        target_url = ''
        stripped_url = request.path.strip('/')

        db = get_db()

        row = db.execute(
            'SELECT target_url FROM url WHERE shrunk_url = ?',
            (stripped_url,)
        ).fetchone()

        if row is not None:
            # success, get row value target_url!
            return redirect(row['target_url'], code=302)
        else:
            # Failed to find matching route or shrunk url
            print('Error: Invalid route or url: "{}"'.format(request.path))
            abort(404)

        return redirect(target_url, code=302)

    @app.route('/')
    @app.route('/index')
    def index():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    return app

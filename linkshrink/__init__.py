import os

from flask import Flask, request, redirect, abort, g

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, select, exists


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


# Factory function for creation and configuration of the app
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration values are loaded from environment values
    # or in some cases set to a development default value
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        DATABASE_URL=os.environ.get('DATABASE_URL'),
    )

    print(app.config['DATABASE_URL'])

    # Create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import database
        database.create_database()
        db = g.database

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

        # Query for target url and redirect
        stripped_url = request.path.strip('/')

        from . import database
        database.create_database()
        db = g.database

        query = select([database.url.c.target_url]).where(database.url.c.shrunk_url == stripped_url)
        result = db.execute(query).fetchone()

        if result is not None:
            # success, get row value target_url!
            return redirect(result[0], code=302)
        else:
            # Failed to find matching route or shrunk url
            print('Error: Invalid route or url: "{}"'.format(request.path))
            abort(404)

    @app.route('/')
    @app.route('/index')
    def index():
        return 'Hello, World!'

    return app

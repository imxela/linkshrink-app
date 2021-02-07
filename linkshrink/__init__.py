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
        from . import routes

    return app

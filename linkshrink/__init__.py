import os

from flask import Flask


# Factory function for creation and configuration of the app
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration values are loaded from environment values
    # or in some cases set to a development default value
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        DATABASE_URL=os.environ.get('DATABASE_URL'),
    )

    print('Database URI: '.format(app.config['DATABASE_URL']))

    # Create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import database
        from . import routes
        from . import commands

    return app

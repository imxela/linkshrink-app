
from flask import g, current_app

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import select, exists


db_meta = MetaData()

url = Table(
            'urls', db_meta,
            Column('id', Integer, primary_key=True),
            Column('shrunk_url', String(35), unique=True, nullable=False),
            Column('target_url', String(2048), unique=True, nullable=False),
        )


# Creates a shortened URL entry in the database for testing
def create_testing_defaults():
    default_shrunk_url = 'test'
    default_target_url = 'https://www.google.com/'

    exists_query = select([url.c.target_url]).where(
        url.c.shrunk_url == default_shrunk_url
    )

    s = exists(exists_query).select()
    result = get_db().execute(s).fetchone()[0]

    # Only add them if they do not exist
    if result is False:
        print('Database defaults created!')
        insert_test = url.insert().values(
            shrunk_url=default_shrunk_url, 
            target_url=default_target_url
        )
        result = get_db().execute(insert_test)
    else:
        print('Database defaults already exist.')


# Creates a database connection
def create_database():
    db_engine = create_engine(current_app.config['DATABASE_URL'])
    db_meta.create_all(db_engine)
    g.database = db_engine.connect()

    create_testing_defaults()

    print('Database created!')


# Creates a database connection if one does not exist and returns it
def get_db():
    if 'database' not in g:
        create_database()

    return g.database

@current_app.teardown_appcontext
def close_db(e):
    if 'database' in g:
        g.database.close()


# Returns the 'target_url' associated with the specified 'shrunk_url'.
# Returns 'default' if 'shrunk_url' does not exist in the database.
def get_target_url(shrunk_url, default=None):
    query = select([url.c.target_url]).where(url.c.shrunk_url == shrunk_url)
    result = get_db().execute(query).fetchone()
    # TODO: g.database does not exist here, why?

    if result is not None:
        return result[0]

    return default

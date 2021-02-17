
from flask import g, current_app

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import select, exists


db_meta = MetaData()

url = Table(
            'urls', db_meta,
            Column('id', Integer, primary_key=True),
            Column('url_hash', String(35), unique=True, nullable=False),
            Column('target_url', String(2048), unique=True, nullable=False),
        )


# Creates a database connection
def create_database():
    db_engine = create_engine(current_app.config['DATABASE_URL'])
    db_meta.create_all(db_engine)
    g.database = db_engine.connect()

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


# Returns the 'target_url' associated with the specified 'url_hash'.
# Returns 'default' if 'url_hash' does not exist in the database.
def query_target_url(url_hash, default=None):
    query = select([url.c.target_url]).where(url.c.url_hash == url_hash)
    result = get_db().execute(query).fetchone()

    if result is not None:
        return result[0]

    return default


# Returns the 'url_hash' associated with the specified 'target_url'.
# Returns 'default' if 'target_url' does not exist in the database.
def query_url_hash(target_url, default=None):
    query = select([url.c.url_hash]).where(url.c.target_url == target_url)
    result = get_db().execute(query).fetchone()

    if result is not None:
        return result[0]

    return default


# Returns True if the 'target_url' exists in the database, False otherwise.
def exists_target(target_url):
    query = select([exists().where(url.c.target_url == target_url)])
    result = get_db().execute(query).fetchone()
    return result[0]


# Returns True if the 'url_hash' exists in the database, False otherwise.
def exists_shrunk(url_hash):
    query = select([exists().where(url.c.url_hash == url_hash)])
    result = get_db().execute(query).fetchone()
    return result[0]


# Inserts a shortened URL associated with a target URL into the database.
# Returns True on success or False if it already exists.
def insert_pair(url_hash, target_url):
    exists = exists_shrunk(url_hash)
    if exists is True:
        print('Attempted to insert pair, but the url_hash \'{}\' already exists.'.format(url_hash))
        return False

    exists = exists_target(target_url)
    if exists is True:
        print('Attempted to insert pair, but the target_url \'{}\' already exists.'.format(target_url))
        return False

    query = url.insert().values(
            url_hash=url_hash,
            target_url=target_url
        )

    get_db().execute(query)
    print('Successfully inserted new pair ({}, {}) into database.'.format(url_hash, target_url))
    return True


# Deletes a the specified shortened URL and its associated target URL from the database.
# Returns True on success or False if 'url_hash' does not exist in database.
def delete_shrunk(url_hash):
    result = exists_shrunk(url_hash)

    if result is not True:
        print('Failed to delete target \'{}\': Value does not exist in database.'.format(url_hash))
        return False

    query = url.delete().where(url.c.url_hash == url_hash)
    result = get_db().execute(query)
    print('Deleted pair \'{}\''.format(url_hash))
    return True


# Deletes a the specified target URL and its associated shortened URL from the database.
# Returns True on success or False if 'target_url' does not exist in database.
def delete_target(target_url):
    result = exists_target(target_url)

    if result is not True:
        print('Failed to delete target \'{}\': Value does not exist in database.'.format(target_url))
        return False

    query = url.delete().where(url.c.target_url == target_url)
    result = get_db().execute(query)
    print('Deleted pair \'{}\''.format(target_url))
    return True

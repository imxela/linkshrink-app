from flask import current_app

import click

from . import database

@current_app.cli.command('delete-shrunk')
@click.argument('url_hash')
def delete_shrunk_command(url_hash):
    """Deletes a URL pair associated with the specified shortened URL."""
    database.delete_shrunk(url_hash)

@current_app.cli.command('delete-target')
@click.argument('target_url')
def delete_target_command(target_url):
    """Deletes a URL pair associated with the specified target URL."""
    database.delete_target(target_url)

@current_app.cli.command('insert-pair')
@click.argument('url_hash')
@click.argument('target_url')
def insert_pair_command(url_hash, target_url):
    """Inserts the specified URL pair into the database."""
    database.insert_pair(url_hash, target_url)

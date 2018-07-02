from itemcatalog.db import db
from itemcatalog.dbmodels import Category

import click
from flask.cli import with_appcontext


@click.command('init-data')
@with_appcontext
def init_data_command():
    """Add the categories to the catalog."""
    create_data()
    click.echo("Initialized the database data")


def init_app(app):
    app.cli.add_command(init_data_command)


def create_data():
    categories = [
        "Sports",
        "Holiday",
        "Clothes",
        "Weapons",
        "Accessories",
        "Laptops",
        "Phones",
        "Watches",
        "Shoes",
        "Tablets",
        "Jewelry"
        ]

    for x in categories:
        cat = Category(name=x)
        db.session.add(cat)
        db.session.commit()

from itemcatalog.db import db
from itemcatalog.dbmodels import User, Item, Category, Like, Comment, Password


def create_test_data():
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

from flask import Blueprint, render_template

from dbmodels import Category, Item

bp = Blueprint("catalog", __name__)


@bp.route("/")
@bp.route("/catalog/")
def show_catalog():
    categories = Category.query.all()
    latest_items = Item.query.order_by(Item.pubdate.desc()).limit(6)
    return render_template("catalog/cataloghome.html", categories=categories,
                           items=latest_items)


@bp.route("/catalog/<int:categoryid>/")
def show_category(categoryid):
    # get items in this category
    items = Item.query.filter_by(categoryid=categoryid).all()

    # get the category
    category = Category.query.filter_by(id=categoryid).first()
    categories = Category.query.all()

    num = len(items)

    return render_template("catalog/category.html", items=items,
                           category=category, num=num, categories=categories)


@bp.route("/errormessage/<string:error>/")
def error(error):
    return render_template("error.html", error=error)

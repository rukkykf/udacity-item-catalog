from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from db import db
from dbmodels import Category, Item

bp = Blueprint("catalog", __name__)


@bp.route("/")
@bp.route("/catalog/")
def show_catalog():
    categories = Category.query.all()
    latest_items = Item.query.order_by(Item.pubdate.desc())[0:6]
    return render_template("cataloghome.html", categories=categories,
                           items=latest_items)


@bp.route("/catalog/<int:categoryid>/")
def show_category(categoryid):
    return "hello"

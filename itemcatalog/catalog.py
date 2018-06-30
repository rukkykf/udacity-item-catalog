from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from db import db
from dbmodels import Category

bp = Blueprint("catalog", __name__)

@bp.route("/")
@bp.route("/catalog/")
def show_catalog():
    categories = Category.query.all()
    return render_template("cataloghome.html", categories=categories)


@bp.route("/catalog/<int:categoryid>/")
def show_category(categoryid):
    return "hello"

from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from forms import newItemForm
from dbmodels import User, Item, Comment, Category

from auth import login_required

bp = Blueprint("items", __name__)


@bp.route("/item/new/", methods=["GET", "POST"])
@login_required
def create_item():
    form = newItemForm()
    form.category.choices = [(g.id, g.name) for g in Category.query.order_by("name")]

    return render_template("items/newitem.html", form=form)

from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from forms import ItemForm
from dbmodels import User, Item, Comment, Category
from db import db

from auth import login_required

bp = Blueprint("items", __name__)


@bp.route("/item/new/", methods=["GET", "POST"])
@login_required
def create_item():
    form = ItemForm()
    form.category.choices = [(b.id, b.name)
                             for b in Category.query.order_by("name")]

    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        name = form.name.data
        description = form.description.data

        item = Item(name=name, description=description,
                    user=g.user, category=category)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('user.profile'))

    return render_template("items/newitem.html", form=form)


@bp.route("/item/<int:itemid>/")
def show_item(itemid):
    return "hello"

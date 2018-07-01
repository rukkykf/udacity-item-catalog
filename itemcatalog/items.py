from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from forms import ItemForm, DeleteItemForm, EditItemForm
from dbmodels import User, Item, Comment, Category, Like
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
    item = Item.query.filter_by(id=itemid).first()

    # get the number of likes this item has
    num = len(Like.query.filter_by(itemid=itemid).all())
    return render_template("items/item.html", item=item, num=num)


@bp.route("/item/like/<int:itemid>/")
@login_required
def like_item(itemid):
    like = Like(userid=g.user.id, itemid=itemid)
    db.session.add(like)
    db.session.commit()
    return redirect(url_for("items.show_item", itemid=itemid))


@bp.route("/item/unlike/<int:itemid>/")
@login_required
def unlike_item(itemid):
    like = Like.query.filter_by(userid=g.user.id, itemid=itemid).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for("items.show_item", itemid=itemid))


@bp.route("/item/delete/<int:itemid>/", methods=["GET", "POST"])
@login_required
def delete_item(itemid):

    form = DeleteItemForm()
    form.itemid = itemid

    item = Item.query.filter_by(id=itemid).first()

    if form.validate_on_submit():
        error = None

        # ensure the user is not trying to edit the wrong item
        if form.itemid.data != itemid:
            error = "You're trying to edit the wrong item, please try again"

        # ensure the user is authorized to edit this item
        if g.user.id != item.user.id:
            error = "You are not authorized to edit this item"

        if error is not None:
            return redirect(url_for("catalog.error", error=error))

        # delete all likes for the item
        likes = Like.query.filter_by(itemid=itemid).all()
        for like in likes:
            db.session.delete(like)
            db.session.commit()

        # delete the item
        db.session.delete(item)
        db.session.commit()

        return redirect(url_for("user.profile"))

    return render_template("items/deleteitem.html", item=item, form=form)


@bp.route("/item/edit/<int:itemid>/", methods=["GET", "POST"])
@login_required
def edit_item(itemid):
    form = EditItemForm()

    item = Item.query.filter_by(id=itemid).first()

    if request.method == "GET":
        form.itemid = itemid
        form.name.data = item.name
        form.description.data = item.description

    form.category.choices = [(b.id, b.name)
                             for b in Category.query.order_by("name")]

    if form.validate_on_submit():
        error = None

        if form.itemid.data != itemid:
            error = "You're trying to edit the wrong item, please try again"

        if g.user.id != item.user.id:
            error = "You are not authorized to edit this item"

        if error is not None:
            return redirect(url_for("catalog.error", error=error))

        item.name = form.name.data
        item.description = form.description.data

        item.category = Category.query.filter_by(id=form.category.data).first()

        db.session.add(item)
        db.session.commit()
        return redirect(url_for("items.show_item", itemid=itemid))

    return render_template("items/edititem.html", form=form, item=item)


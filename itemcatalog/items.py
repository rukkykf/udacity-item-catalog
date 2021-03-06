from flask import (Blueprint, redirect,
                   render_template, request, url_for, g)

from forms import ItemForm, DeleteItemForm, EditItemForm
from dbmodels import Item, Category, Like
from db import db
from validate_item_ud import ValidateItemUD
from auth import login_required

bp = Blueprint("items", __name__)
ud_validator = ValidateItemUD()


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

    item = Item.query.filter_by(id=itemid).first()

    if request.method == "GET":
        ud_validator.item = item
        ud_validator.user = g.user

    if form.validate_on_submit():
        error = None

        error = ud_validator.is_valid(item)

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
        ud_validator.item = item
        ud_validator.user = g.user
        form.name.data = item.name
        form.description.data = item.description

    form.category.choices = [(b.id, b.name)
                             for b in Category.query.order_by("name")]

    if form.validate_on_submit():
        error = ud_validator.is_valid(item)

        if error is not None:
            return redirect(url_for("catalog.error", error=error))

        item.name = form.name.data
        item.description = form.description.data

        item.category = Category.query.filter_by(id=form.category.data).first()

        db.session.add(item)
        db.session.commit()
        return redirect(url_for("items.show_item", itemid=itemid))

    return render_template("items/edititem.html", form=form, item=item)

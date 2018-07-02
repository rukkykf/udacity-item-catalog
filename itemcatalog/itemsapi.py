from flask import Blueprint, jsonify
from dbmodels import Item

bp = Blueprint("api", __name__)


@bp.route("/items/json/")
def itemsJSON():
    items = Item.query.all()
    return jsonify(items=[item.serialize for item in items])

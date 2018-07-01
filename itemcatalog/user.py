from flask import Blueprint, render_template, g
from itemcatalog.auth import login_required
from dbmodels import Item
bp = Blueprint('user', __name__)


@bp.route('/profile/')
@login_required
def profile():
    items = Item.query.filter_by(userid=g.user.id)
    return render_template("user/profile.html", items=items)

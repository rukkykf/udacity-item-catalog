from flask import Blueprint, render_template
from itemcatalog.auth import login_required

bp = Blueprint('user', __name__)

@bp.route('/profile/')
@login_required
def profile():
    return render_template("user/profile.html")
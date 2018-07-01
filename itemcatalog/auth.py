import functools

from db import db
from dbmodels import User, Password, Like
from forms import RegistrationForm, LoginForm
from passwordmng import set_password, check_password

from flask import (Blueprint, redirect,
                   render_template, request, session, url_for, jsonify, g)

from flask_dance.contrib.google import make_google_blueprint, google

bp = Blueprint('auth', __name__)
gbp = make_google_blueprint(
    client_id="421504894578-8kvmfrgrpbibbppnumcvn6nm1hkqk670.apps.googleusercontent.com",
    client_secret="e1regt3-GhiMbI-dmIhJjEQ9",
    scope=["openid", "email"],
    redirect_url="/gconnect/"
)


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print "Receiving post method"
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()

        pswh = set_password(form.password.data)
        psw = Password(userid=user.id, pw_hash=pswh)
        db.session.add(psw)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ""

    if form.validate_on_submit():
        # Get the user
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        # Get the user's password
        psw = Password.query.filter_by(userid=user.id).first()

        # Check the password
        is_valid = check_password(psw.pw_hash, form.password.data)

        if is_valid:
            session["user_id"] = user.id
            return redirect(url_for('user.profile'))

        error = "Invalid login"
    return render_template('auth/login.html', form=form, error=error)


@gbp.route('/gconnect/')
def gconnect():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")

    email = resp.json()["email"]
    name = resp.json()["given_name"]

    # Check if this user already exists.
    user = User.query.filter_by(email=email).first()

    if user is not None:
        session["user_id"] = user.id
    else:
        # create a new user and then log user in
        user = User(username=name, email=email)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('user.profile'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
        likes = Like.query.filter_by(userid=g.user.id).all()
        g.userlikes = []
        for like in likes:
            g.userlikes.append(like.itemid)


@bp.route('/logout/')
def logout():
    session.clear()
    g.userlikes = None
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

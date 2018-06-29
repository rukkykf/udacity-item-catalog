from db import db
from dbmodels import User, Password
from forms import RegistrationForm
from passwordmng import set_password, check_password

from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)

bp = Blueprint('auth', __name__)

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
    return "hello"

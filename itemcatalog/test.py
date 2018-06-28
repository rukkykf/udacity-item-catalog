from db import db
import dbmodels

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

bp = Blueprint('auth', __name__)

@bp.route('/testdb/')
def testingdb():
    admin = dbmodels.User(email='rukkykofi@gmail.com', username='rukky')

    db.session.add(admin)
    db.session.commit()

    return "done"
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    x = "sqlite:///" + app.instance_path + "/itemcat.db"
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=x,
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    if test_config is None:
        # load the instance config, if it exists when not testing
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return x

    from . import db
    db.init_app(app)

    from . import data
    data.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(auth.gbp)

    from . import user
    app.register_blueprint(user.bp)

    from . import catalog
    app.register_blueprint(catalog.bp)

    from . import items
    app.register_blueprint(items.bp)

    from . import itemsapi
    app.register_blueprint(itemsapi.bp)

    return app

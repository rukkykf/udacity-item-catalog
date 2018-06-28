import os
import tempfile

import pytest
from itemcatalog import create_app
from itemcatalog.db import init_db
import testdata

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    x = "sqlite:///" + db_path + "/test.db"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": x
    })

    with app.app_context():
        init_db()
        testdata.create_test_data()


    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()


import os
import datetime
import tempfile

import pytest

from backend.app import create_app
from backend.extensions import db


@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    # create the db and load test data
    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    # close and remove the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def _db():
    """Create and configure a new db instance for pytest-flask-sqlalchemy."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    with app.app_context():
        db.init_app(app)
        db.create_all()

        yield db

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def new_user():
    user = {
        'username': 'TestName',
        'password': 'TestPassword'
    }
    return user


@pytest.fixture
def new_participant():
    participant = {
        'name': 'Jon',
        'lastname': 'Doe',
        'email': 'test@test.com',
        'phone': '123456789'
    }
    return participant


@pytest.fixture
def new_hacknight():
    hacknight = {'date': datetime.date(2000, 10, 10)}
    return hacknight

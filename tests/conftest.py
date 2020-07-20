import os
import tempfile
from flask.globals import session

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db, create_user
from flaskr.db_for_test import fill_db



@pytest.fixture
def app():
    file, path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///' + path
    })

    with app.app_context():
        init_db()
        with get_db() as session:
            fill_db(session)
        create_user('LOGIN', 'PASSWORD', 'Team')

    yield app

    os.close(file)
    os.unlink(path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_client(client):
    response = client.post('/team/login',
        data= {
                'userlogin': 'LOGIN',
                'userpassword': 'PASSWORD',
                })
    assert response.status_code == 302
    return client

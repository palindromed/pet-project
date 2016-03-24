import os
import pytest
import webtest
from passlib.apps import custom_app_context as blogger_pwd_context

def test_access_to_view(app):
    response = app.get('/create')
    assert response.status_code == 200


def test_no_access_to_view(app):
    response = app.get('/create', status=403)
    assert response.status_code == 403


@pytest.fixture()
def auth_env():
    os.environ['AUTH_PASSWORD'] = 'secret'
    os.environ['AUTH_USERNAME'] == 'admin'


def test_uname_and_pwd_exist(app):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exists(app):
    assert os.environ.get('AUTH_USERNAME', None) is not None

def test_check_pw_success(auth_env):
    # from learning-journal.security import check_pw
    password = 'secret'
    assert check_pw(password)


# def test_auth_env()

# -*- coding: utf-8 -*-OLD
from __future__ import unicode_literals

import pytest
import os

from pyramid.paster import get_appsettings
from sqlalchemy import create_engine
from webtest import TestApp

from ..models import DBSession, Base, Post, User

TEST_DATABASE_URL = os.environ.get("TEST_DB_URL")
AUTH_DATA = {'username': 'admin', 'password': 'secret'}


def pytest_addoption(parser):
    parser.addoption("--ini", action="store", metavar="INI_FILE")


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope='session')
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


# use fixture
# noinspection PyUnusedLocal,PyShadowingNames
@pytest.fixture()
def app(dbtransaction, request):
    from learning_journal import main
    settings = get_appsettings(request.config.option.ini)
    settings['sqlalchemy.url'] = TEST_DATABASE_URL
    app = main({}, **settings)
    return TestApp(app)


@pytest.fixture(scope='function')
def new_post(request):
    """Return a fresh new Entry and flush to the database."""
    post = Post(title="test post title", text="This is only a test")
    DBSession.add(post)
    DBSession.flush()

    def teardown():

        DBSession.delete(post)
        DBSession.flush()

    request.addfinalizer(teardown)
    return post


@pytest.fixture()
def new_user(request, app):
    user = User(username='hannah', password='banana')
    DBSession.add(user)
    DBSession.flush()

    def teardown():
        DBSession.delete(user)
        DBSession.flush()

    request.addfinalizer(teardown)
    return user


@pytest.fixture()
def authenticated_app(app):
    res = app.get('/register')
    form = res.forms['register']
    form.set('username', 'admin')
    form.set('password', 'secret')
    res = form.submit()
    res.follow()

    return app

# -*- coding: utf-8 -*-OLD
from __future__ import unicode_literals

import pytest
import os

from pyramid.paster import get_appsettings
from sqlalchemy import create_engine
from webtest import TestApp

from ..models import DBSession, Base, Post

TEST_DATABASE_URL = os.environ.get("TEST_DB_URL")


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

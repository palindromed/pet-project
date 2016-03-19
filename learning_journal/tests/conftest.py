# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import os


from sqlalchemy import create_engine
#from webtest import TestApp

from ..models import DBSession, Base, Post

# TEST_DATABASE_URL = os.environ.get("TEST_DB_URL")
# PARENT_DIR = os.path.dirname(__file__)
# GPARENT_DIR = os.path.join(PARENT_DIR, '..')
# GGPARENT_DIR = os.path.join(GPARENT_DIR, '..')
# CONFIG_URI = os.path.join(GGPARENT_DIR, 'development.ini')

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
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


# use fixture
# noinspection PyUnusedLocal,PyShadowingNames
@pytest.fixture()
def app(dbtransaction):
    from learning_journal import main
    from webtest import TestApp
    from pyramid.paster import get_appsettings
    settings = get_appsettings(CONFIG_URI)
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

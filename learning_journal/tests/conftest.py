# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine

from ..models import DBSession, Base


#TEST_DATABASE_URL = 'postgres:////tmp/test_db.sqlite'
TEST_DATABASE_URL = 'postgresql://hannahkrager@localhost:5432/author'

@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
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

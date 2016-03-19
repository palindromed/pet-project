# coding=utf-8
from __future__ import unicode_literals

import datetime
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(length=128), unique=True)
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)

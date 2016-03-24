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
from passlib.apps import custom_app_context as blogger_pwd_context
from zope.sqlalchemy import ZopeTransactionExtension
# from passlib.hash import sha256_crypt

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(length=128), unique=True)
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        return blogger_pwd_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = blogger_pwd_context.encrypt(password)
        self.password = password_hash

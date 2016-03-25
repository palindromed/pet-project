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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Post(Base):
    """Class for modeling a single blog post."""

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(length=128), unique=True)
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    """Create user class so individuals can register and login."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        """Check for cleartext password, verify that provided pw is valid."""
        # is it cleartext?
        if password == self.password:
            self.set_password(password)
        return blogger_pwd_context.verify(password, self.password)

    def set_password(self, password):
        """Hash provided password to compare to user provided value later."""
        password_hash = blogger_pwd_context.encrypt(password)
        self.password = password_hash

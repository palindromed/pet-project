import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    String
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
    title = Column(String(length=128, convert_unicode=True), unique=True)
    text = Column(Text(convert_unicode=True))
    created = Column(DateTime, default=datetime.datetime.utcnow)

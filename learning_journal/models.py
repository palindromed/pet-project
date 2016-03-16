from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
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


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(Text(length=128, convert_unicode=True), unique=True)
    text = Column(Text(convert_unicode=True))
    created = Column(DateTime(timezone=True))

#Index('my_index', Post.title, unique=True, mysql_length=128)

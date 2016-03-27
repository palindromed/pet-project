from .models import User, Post, Comment, DBSession

class UserService(object):

    @classmethod
    def by_name(cls, username):
        return DBSession.query(User).filter(User.username == username).first()


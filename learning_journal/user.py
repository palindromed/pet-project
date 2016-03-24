from .models import User, DBSession

class UserService(object):

    @classmethod
    def by_name(cls, username):
        return DBSession.query(User).filter(User.username == username).first()

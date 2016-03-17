# coding=utf-8
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Post,
    )


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning-journal'}
#     pass


@view_config(route_name='list', renderer='templates/list.jinja')
def list_view(request):
    try:
        posts = DBSession.query(Post).all()
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    # return {
    #     'posts': [
    #         {'title': post.title, 'text': post.text, 'created': post.created}
    #         for post in posts
    #     ]
    # }
    return posts


@view_config(route_name='detail', renderer='templates/detail.jinja')
def detail_view(request):
    try:
        post = DBSession.query(Post).filter(Post.id == request.matchdict['post_id'])
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    # return {
    #     'title': post.title,
    #     'text': post.text,
    #     'created': post.created,
    # }
    return post


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning-journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


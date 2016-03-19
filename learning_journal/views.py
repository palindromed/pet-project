# coding=utf-8
from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from wtforms import Form, StringField, validators, TextAreaField

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


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    try:
        posts = DBSession.query(Post).all()
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'posts': posts}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    try:
        post = DBSession.query(Post).filter(Post.id == int(request.matchdict['post_id'])).first()
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'post': post}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    try:
        post = DBSession.query(Post).filter(Post.id == request.matchdict['post_id']).first()
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'post': post}


@view_config(route_name='add_entry', renderer="templates/add_entry.jinja2")
def create_view(request):
    class PostForm(Form):
        title = StringField('Title', [validators.Length(min=4, max=128)])
        text = TextAreaField('Text', [validators.Length(min=6)])
    form = PostForm(request.POST)
    print("~~FORM~~", form.title.data, form.text.data)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, text=form.text.data)
        try:
            DBSession.add(post)
            DBSession.flush()
            return HTTPFound(request.route_url('detail', post_id=post.id))
        except DBAPIError:
            # request.session.flash("Can't make that post!")
            form.errors.setdefault('error', []).append('Title must be unique!')
    return {'form': form}


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

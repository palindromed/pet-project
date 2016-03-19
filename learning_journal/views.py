# coding=utf-8
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Post,
    )
from .post_form import PostForm


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
        post = DBSession.query(Post).filter(Post.id == request.matchdict['post_id']).first()
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'post': post}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    try:
        post_to_edit = DBSession.query(Post).filter(Post.id == request.matchdict['post_id']).first()
        form = PostForm(request.POST, post_to_edit)
        if request.method == 'POST' and form.validate():
            form.populate_obj(post_to_edit)
            post_to_edit.title = request.params['title']
            post_to_edit.text = request.params['text']
            post_id = post_to_edit.id
            re_route = request.route_url('detail', post_id=post_id)
            return HTTPFound(location=re_route)
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'form': form}


@view_config(route_name='add_entry', renderer="templates/add_entry.jinja2")
def create_view(request):
    form = PostForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_post = Post(title=form.title.data, text=form.text.data)
        DBSession.add(new_post)
        DBSession.flush()
        detail_id = new_post.id
        re_route = request.route_url('detail', post_id=detail_id)
        return HTTPFound(location=re_route)
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

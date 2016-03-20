# coding=utf-8
from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Post,
    )

from .post_form import ModifyPostForm


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
        post = DBSession.query(Post).get(request.matchdict['post_id'])
    except DBAPIError:
        return Response("error!", content_type='text/plain', status_int=500)
    return {'post': post}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    print("editing post numero", request.matchdict['post_id'])
    post_to_edit = DBSession.query(Post).filter(Post.id == int(request.matchdict['post_id'])).first()
    print(post_to_edit)
    print("available postids:", list(DBSession.query(Post).all()))
    # TODO: as you can see from the above debug printout, the new_post in our tests does not actually show up here
    form = ModifyPostForm(request.POST, post_to_edit)
    if not post_to_edit:
        form.errors.setdefault('error', []).append('That post does not exist!')
    elif request.method == 'POST' and form.validate():
        try:
            form.populate_obj(post_to_edit)
            re_route = request.route_url('detail', post_id=post_to_edit.id)
            return HTTPFound(location=re_route)
        except DBAPIError:
            form.errors.setdefault('error', []).append('Title must be unique!')
        # return Response("error!", content_type='text/plain', status_int=500)
    return {'form': form, 'use_case': 'Edit'}


@view_config(route_name='add_entry', renderer="templates/edit.jinja2")
def create_view(request):
    form = ModifyPostForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_post = Post(title=form.title.data, text=form.text.data)
        try:
            DBSession.add(new_post)
            DBSession.flush()
            detail_id = new_post.id
            re_route = request.route_url('detail', post_id=detail_id)
            return HTTPFound(location=re_route)
        except DBAPIError:
            form.errors.setdefault('error', []).append('Title must be unique!')
    return {'form': form, 'use_case': 'Create'}


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

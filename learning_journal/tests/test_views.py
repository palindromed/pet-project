# coding=utf-8
from __future__ import unicode_literals

from pyramid.testing import DummyRequest

from learning_journal.models import DBSession, Post
from learning_journal.views import (
    list_view,
    detail_view,
    create_view,
    edit_view
)


def test_list_view(dbtransaction, new_post):
    response_data = list_view(DummyRequest())
    posts = response_data['posts']
    assert posts == [new_post]


def test_list_route(app, dbtransaction, new_post):
    response = app.get("/")
    assert response.status_code == 200
    # assert new_post.text.encode('utf-8') in response.body


def test_detail_view(dbtransaction, new_post):
    request = DummyRequest()
    request.matchdict = {'post_id': new_post.id}
    response_data = detail_view(request)
    assert response_data['post'] == new_post


def test_detail_route(app, dbtransaction, new_post):
    response = app.get('/post/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body

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
    test_view = DummyRequest()
    response_data = list_view(test_view)
    posts = response_data['posts']
    assert new_post in posts


def test_list_route(app, dbtransaction, new_post):
    response = app.get("/")
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_detail_view(dbtransaction, new_post):
    request = DummyRequest()
    request.matchdict = {'post_id': new_post.id}
    response_data = detail_view(request)
    assert response_data['post'] == new_post


def test_detail_route(app, dbtransaction, new_post):
    response = app.get('/post/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_add_view(dbtransaction, app):
    """Test that create view creates a new Entry in database."""
    results = DBSession.query(Post).filter(
        Post.title == 'TEST Title' and Post.text == 'TEST Text')
    assert results.count() == 0
    params = {
        'title': 'This is a title',
        'text': 'Here is some text'
    }
    app.post('/create', params=params, status='3*')
    results = DBSession.query(Post).filter(
        Post.title == 'This is a title' and Post.text == 'Here is some text')
    assert results.count() == 1


def test_add_route(app, dbtransaction):
    """Test that the create view works"""
    response = app.get("/create")
    assert response.status_code == 200


def test_edit_view(dbtransaction, app, new_post):
    """Test that edit can successfully update existing post"""
    new_post.title = new_post.title + "I'm new"
    new_post.text = new_post.text + "I'm new too"
    params = {
        'title': new_post.title,
        'text': new_post.text
    }
    app.post('/edit/{}'.format(new_post.id), params=params, status='3*')
    results = DBSession.query(Post).filter(
        Post.title == new_post.title and Post.text == new_post.text)
    assert results.count() == 1


def test_edit_route(app, dbtransaction, new_post):
    response = app.get('/post/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body

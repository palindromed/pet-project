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
    # why did they call this 'params'? it should be called 'data' or 'body' : /
    app.post('/create', params=params, status='3*')
    results = DBSession.query(Post).filter(
        Post.title == 'This is a title' and Post.text == 'Here is some text')
    assert results.count() == 1


def test_add_view_collide(dbtransaction, app, new_post):
    params = {
        'title': 'test post title',
        'text': 'Here is some text'
    }
    # ensure that it fails to create successfully
    app.post('/create', params=params, status='200 *')


def test_add_route(app, dbtransaction):
    """Test that the create view works"""
    response = app.get("/create")
    assert response.status_code == 200


def test_edit_view(dbtransaction, app, new_post):
    """Test that edit can successfully update existing post"""
    # new_post.title = new_post.title + "I'm new"
    # new_post.text = new_post.text + "I'm new too"
    params = {
        'title': "I'm new",
        'text': "I'm also new"
    }
    print("editing post numero", new_post.id)
    response = app.post('/edit/{}'.format(new_post.id), params=params)
    print(response.body.decode('utf-8'))
    assert 300 <= response.status_code < 400
    results = DBSession.query(Post).filter(
        Post.title == params['title'] and Post.text == params['text'])
    assert results.count() == 1


# def test_edit_view_collide(dbtransaction, app, new_post):



def test_edit_route(app, dbtransaction, new_post):
    response = app.get('/edit/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body

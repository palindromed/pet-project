# coding=utf-8
from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.testing import DummyRequest
import pytest
from webob.multidict import MultiDict

from learning_journal.models import DBSession, Post
from learning_journal.views import (
    list_view,
    detail_view,
    create_view,
    edit_view
)


def test_list_view(dbtransaction, new_post, dummy_request):
    dummy_request = DummyRequest()
    response_data = list_view(dummy_request)
    posts = response_data['posts']
    assert new_post in posts


def test_list_route(app, dbtransaction, new_post):
    response = app.get("/")
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_detail_view(dbtransaction, new_post, dummy_request):
    dummy_request.matchdict = {'post_id': new_post.id}
    response_data = detail_view(dummy_request)
    assert response_data['post'] == new_post


def test_detail_view_fail(dbtransaction, dummy_request):
    dummy_request.matchdict = {'post_id': 0}
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_detail_route(app, dbtransaction, new_post):
    response = app.get('/post/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_detail_route_fail(app, dbtransaction):
    app.get('/post/{}'.format(0), status="404*")


def test_create_view(dbtransaction, dummy_request):
    response_data = create_view(dummy_request)
    assert not (response_data['form'].title.data or response_data['form'].text.data)


def test_create_view_post(dbtransaction, dummy_request):
    dummy_request.method = 'POST'
    dummy_request.POST = MultiDict([('title', "Test Title"), ('text', "Test text")])
    response_data = create_view(dummy_request)
    assert isinstance(response_data, HTTPFound)


def test_create_view_post_fail(dbtransaction, dummy_request, new_post):
    dummy_request.method = 'POST'
    dummy_request.POST = MultiDict([('title', new_post.title), ('text', "this post has the same title")])
    response_data = create_view(dummy_request)
    assert type(response_data) is dict
    assert response_data['form'].title.data == new_post.title
    assert response_data['form'].text.data == "this post has the same title"


def test_create_route(dbtransaction, app):
    """Test that the create view works"""
    response = app.get("/create")
    assert response.status_code == 200


def test_create_route_post(dbtransaction, app):
    """Test that create view creates a new Entry in database."""
    params = {
        'title': 'This is a title',
        'text': 'Here is some text'
    }
    # why did they call this 'params'? it should be called 'data' or 'body' : /
    response = app.post('/create', params=params, status='3*')
    results = DBSession.query(Post).filter(Post.title == 'This is a title').all()
    assert len(results) == 1
    assert response.location.endswith(app.app.routes_mapper.generate('detail', {'post_id': results[0].id}))


def test_create_route_post_fail(dbtransaction, app, new_post):
    params = {
        'title': 'test post title',
        'text': 'Here is some text'
    }
    # ensure that it fails to create successfully
    app.post('/create', params=params, status='200 *')


def test_edit_view(dbtransaction, new_post, dummy_request):
    dummy_request.matchdict['post_id'] = new_post.id
    response_data = edit_view(dummy_request)
    assert response_data['form'].title.data == new_post.title
    assert response_data['form'].text.data == new_post.text


def test_edit_view_nonexistent(dbtransaction, dummy_request):
    dummy_request.matchdict['post_id'] = -1
    with pytest.raises(HTTPNotFound):
        edit_view(dummy_request)


def test_edit_view_post(dbtransaction, new_post, dummy_request):
    dummy_request.matchdict['post_id'] = new_post.id
    dummy_request.method = 'POST'
    dummy_request.POST = MultiDict([('title', "new post title"), ('text', "new post text")])
    response_data = edit_view(dummy_request)
    assert isinstance(response_data, HTTPFound)


def test_edit_view_post_fail(dbtransaction, new_post, another_post, dummy_request):
    dummy_request.matchdict['post_id'] = new_post.id
    dummy_request.method = 'POST'
    dummy_request.POST = MultiDict([('title', another_post.title), ('text', "this post wants to have the same title")])
    response_data = edit_view(dummy_request)
    assert type(response_data) is dict
    assert response_data['form'].title.data == another_post.title
    assert response_data['form'].text.data == "this post wants to have the same title"


def test_edit_route(app, dbtransaction, new_post):
    response = app.get('/edit/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_edit_route_nonexistent(app, dbtransaction):
    app.get("/edit/-1", status="404*")


def test_edit_route_post(dbtransaction, app, new_post):
    """Test that edit can successfully update existing post"""
    params = {
        'title': "I'm new",
        'text': "I'm also new",
    }
    response = app.post('/edit/{}'.format(new_post.id), params=params)
    assert 300 <= response.status_code < 400
    results = DBSession.query(Post).filter(Post.title == params['title']).all()
    assert len(results) == 1
    assert response.location.endswith(app.app.routes_mapper.generate('detail', {'post_id': results[0].id}))


def test_edit_route_post_fail(dbtransaction, new_post, another_post, app):
    params = {
        'title': another_post.title,
        'text': "this text can be whatever",
    }
    response = app.post("/edit/{}".format(new_post.id), params=params)
    assert response.status_code == 200
    assert params['title'].encode('utf-8') in response.body
    assert params['text'].encode('utf-8') in response.body

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


def test_detail_view_fail():
    pass  # TODO: test that a GET to detail_view for a nonexistent post yields 404 response info


def test_detail_route(app, dbtransaction, new_post):
    response = app.get('/post/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_detail_route_fail():
    pass  # TODO: test hitting the detail route for a nonexistent post fails with 404


def test_create_view():
    pass  # TODO: test a GET to create_view provides data for an empty page (to match create_route)


def test_create_view_post():
    pass  # TODO: test a POST to create_view functions (to match create_route_post)


def test_create_view_post_fail():
    pass  # TODO: test a POST to create_view fails when creating a post with a duplicate title


def test_create_route(app, dbtransaction):
    """Test that the create view works"""
    response = app.get("/create")
    assert response.status_code == 200


def test_create_route_post(dbtransaction, app):
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


def test_create_route_post_fail(dbtransaction, app, new_post):
    params = {
        'title': 'test post title',
        'text': 'Here is some text'
    }
    # ensure that it fails to create successfully
    app.post('/create', params=params, status='200 *')


def test_edit_view():
    pass  # TODO: test the edit_view provides data for an edit page, to match test_edit_route


def test_edit_view_post():
    pass  # TODO: test a POST to edit_view creates a post


def test_edit_view_post_fail():
    pass  # TODO: test a POST to edit_view fails when editing a view to have the same title as another


def test_edit_route(app, dbtransaction, new_post):
    response = app.get('/edit/{}'.format(new_post.id))
    assert response.status_code == 200
    assert new_post.text.encode('utf-8') in response.body


def test_edit_route_post(dbtransaction, app, new_post):
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
    # TODO: new_post is not seen by the view, test fails here; see views.py/edit_view
    results = DBSession.query(Post).filter(
        Post.title == params['title'] and Post.text == params['text'])
    assert results.count() == 1


def test_edit_route_post_fail(dbtransaction, new_post):
    pass  # TODO: test editing a post to have the same title as an existing post

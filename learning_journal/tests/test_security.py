# coding=utf-8
from __future__ import unicode_literals

from pyramid.testing import DummyRequest

from webob.multidict import MultiDict

from learning_journal.views import (
    list_view,
    detail_view,
    create_view,
    edit_view,
    login_view,
    register,
)

from webob.multidict import MultiDict


def test_access_to_view(app):
    """Make sure that everyone can read the blog posts."""
    response = app.get('/')
    assert response.status_code == 200


# def test_access_to_view(authenticated_app, new_post):
#     """Make sure that everyone can read the blog posts."""
#     response = authenticated_app.get('/detail/{}'.format(new_post.id))
#     assert response.status_code == 200


def test_access_to_create_view(authenticated_app):
    """
    Use the logged in app to show that this view is available
    only to the admin user.
    """
    response = authenticated_app.get('/create')
    assert response.status_code == 200

# TODO: make test not blow up when I get the result I want
# def test_no_access_to_view(app):
#     response = app.get('/create')
#     assert response.status_code == 403


def test_login(app):
    """Test that a sucessful login is possible."""
    res = app.get('/login')
    form = res.forms['login']
    form.set('username', 'admin')
    form.set('password', 'secret')
    res = form.submit()
    res.follow()
    assert res.status_code == 302


def test_registration(app):
    """Test that registration form succeeds as expected."""
    res = app.get('/register')
    form = res.forms['register']
    form.set('username', 'tester')
    form.set('password', 'testing')
    res = form.submit()
    res.follow()
    assert res.status_code == 302


def test_list_view(app, new_post):
    dummy_request = DummyRequest()
    response_data = list_view(dummy_request)
    posts = response_data['posts']
    assert new_post in posts


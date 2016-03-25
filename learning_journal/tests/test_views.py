# # coding=utf-8
# from __future__ import unicode_literals

# from pyramid.httpexceptions import HTTPFound, HTTPNotFound
# import pytest
# from webob.multidict import MultiDict

# from learning_journal.models import DBSession, Post
# from learning_journal.views import (
#     list_view,
#     detail_view,
#     create_view,
#     edit_view
# )


# def test_list_view(dbtransaction, new_post, dummy_request):
#     response_data = list_view(dummy_request)
#     posts = [p for p in response_data['posts'] if p.id == new_post.id]
#     assert posts
#     post, = posts
#     assert post.title == new_post.title
#     assert post.text == new_post.text
#     assert post.created == new_post.created


# def test_list_route(dbtransaction, app, new_post):
#     response = app.get("/")
#     assert response.status_code == 200
#     assert new_post.text.encode('utf-8') in response.body


# def test_detail_view(dbtransaction, new_post, dummy_request):
#     dummy_request.matchdict = {'post_id': new_post.id}
#     response_data = detail_view(dummy_request)
#     post = response_data['post']
#     assert post.title == new_post.title
#     assert post.text == new_post.text
#     assert post.created == new_post.created


# def test_detail_view_fail(dbtransaction, dummy_request):
#     dummy_request.matchdict = {'post_id': 0}
#     with pytest.raises(HTTPNotFound):
#         detail_view(dummy_request)


# def test_detail_route(dbtransaction, app, new_post):
#     response = app.get('/post/{}'.format(new_post.id))
#     assert response.status_code == 200
#     assert new_post.text.encode('utf-8') in response.body


# def test_detail_route_fail(dbtransaction, app):
#     app.get('/post/{}'.format(0), status="404*")


# def test_create_view(dbtransaction, dummy_request):
#     response_data = create_view(dummy_request)
#     assert not (response_data['form'].title.data or response_data['form'].text.data)


# def test_create_view_post(dbtransaction, dummy_request):
#     dummy_request.method = 'POST'
#     dummy_request.POST = MultiDict([('title', "Test Title"), ('text', "Test text")])
#     response_data = create_view(dummy_request)
#     assert isinstance(response_data, HTTPFound)
#     qp = DBSession.query(Post).filter(Post.title == "Test Title").all()
#     assert qp  # got some
#     post, = qp  # only one
#     assert post.text == "Test text"


# def test_create_view_post_fail(dbtransaction, dummy_request, new_post):
#     dummy_request.method = 'POST'
#     dummy_request.POST = MultiDict([('title', new_post.title), ('text', "this post has the same title")])
#     response_data = create_view(dummy_request)
#     assert type(response_data) is dict  # not a redirect
#     assert response_data['form'].title.data == new_post.title
#     assert response_data['form'].text.data == "this post has the same title"


# def test_create_route(dbtransaction, app):
#     """Test that the create view works"""
#     response = app.get("/create")
#     assert response.status_code == 200


# def test_create_route_post(dbtransaction, app):
#     """Test that create view creates a new Entry in database."""
#     params = {
#         'title': 'This is a title',
#         'text': 'Here is some text'
#     }
#     # why did they call this 'params'? it should be called 'data' or 'body' : /
#     response = app.post('/create', params=params, status='3*')
#     qp = DBSession.query(Post).filter(Post.title == 'This is a title').all()
#     assert qp  # got some
#     post, = qp  # only one
#     assert post.text == "Here is some text"
#     assert response.location.endswith(app.app.routes_mapper.generate('detail', {'post_id': qp[0].id}))


# def test_create_route_post_fail(dbtransaction, app, new_post):
#     params = {
#         'title': new_post.title,
#         'text': 'fails because the title is not unique'
#     }
#     # ensure that it fails to create successfully
#     response = app.post('/create', params=params, status='200 *')
#     assert params['title'].encode('utf-8') in response.body
#     assert params['text'].encode('utf-8') in response.body


# def test_edit_view(dbtransaction, new_post, dummy_request):
#     dummy_request.matchdict['post_id'] = new_post.id
#     response_data = edit_view(dummy_request)
#     assert response_data['form'].title.data == new_post.title
#     assert response_data['form'].text.data == new_post.text


# def test_edit_view_nonexistent(dbtransaction, dummy_request):
#     dummy_request.matchdict['post_id'] = 0
#     with pytest.raises(HTTPNotFound):
#         edit_view(dummy_request)


# def test_edit_view_post(dbtransaction, new_post, dummy_request):
#     dummy_request.matchdict['post_id'] = new_post.id
#     dummy_request.method = 'POST'
#     dummy_request.POST = MultiDict([('title', "new post title"), ('text', "new post text")])
#     response_data = edit_view(dummy_request)
#     assert isinstance(response_data, HTTPFound)
#     assert response_data.location.endswith(dummy_request.route_url('detail', post_id=new_post.id))
#     post = DBSession.query(Post).get(new_post.id)
#     assert post.title == "new post title"
#     assert post.text == "new post text"


# def test_edit_view_post_fail(dbtransaction, new_post, another_post, dummy_request):
#     dummy_request.matchdict['post_id'] = new_post.id
#     dummy_request.method = 'POST'
#     dummy_request.POST = MultiDict([
#         ('title', another_post.title),
#         ('text', "this post wants to have the same title")
#     ])
#     response_data = edit_view(dummy_request)
#     assert type(response_data) is dict
#     assert response_data['form'].title.data == another_post.title
#     assert response_data['form'].text.data == "this post wants to have the same title"


# def test_edit_route(dbtransaction, app, new_post):
#     response = app.get('/edit/{}'.format(new_post.id))
#     assert response.status_code == 200
#     assert new_post.text.encode('utf-8') in response.body


# def test_edit_route_nonexistent(dbtransaction, app):
#     app.get("/edit/0", status="404*")


# def test_edit_route_post(dbtransaction, app, new_post):
#     """Test that edit can successfully update existing post"""
#     params = {
#         'title': "I'm new",
#         'text': "I'm also new",
#     }
#     response = app.post('/edit/{}'.format(new_post.id), params=params)
#     assert 300 <= response.status_code < 400
#     qp = DBSession.query(Post).filter(Post.title == params['title']).all()
#     assert qp
#     post, = qp
#     assert post.id == new_post.id
#     assert post.text == params['text']
#     assert response.location.endswith(app.app.routes_mapper.generate('detail', {'post_id': qp[0].id}))


# def test_edit_route_post_fail(dbtransaction, new_post, another_post, app):
#     params = {
#         'title': another_post.title,
#         'text': "this text can be whatever",
#     }
#     response = app.post("/edit/{}".format(new_post.id), params=params)
#     assert response.status_code == 200
#     assert params['title'].encode('utf-8') in response.body
#     assert params['text'].encode('utf-8') in response.body

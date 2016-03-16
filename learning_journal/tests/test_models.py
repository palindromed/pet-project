from learning_journal.models import DBSession, Post


def test_models(dbtransaction):
    new_post = Post(title="title", text='text')
    assert new_post.id is None
    assert new_post.created is None
    DBSession.add(new_post)
    DBSession.flush()
    assert new_post.id is not None
    assert new_post.created is not None


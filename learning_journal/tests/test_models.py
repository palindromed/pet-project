from learning_journal.models import MyModel, DBSession, Post


def test_models(dbtransaction):
    new_post = Post(title="title", text='text')
    assert new_post.id is None
    DBSession.add(new_post)
    DBSession.flush()
    assert new_post.id is not None


def test_create_my_model(dbtransaction):
    new_model = MyModel(name='Jill', value=42)
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None

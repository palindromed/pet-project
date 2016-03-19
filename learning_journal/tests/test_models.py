# coding=utf-8
from __future__ import unicode_literals
from learning_journal.models import DBSession, Post


def test_models(dbtransaction):
    new_post = Post(title="\u1555( \u141b )\u1557", text='( \u0361\xb0 \u035c\u0296 \u0361\xb0)')
    assert new_post.id is None
    assert new_post.created is None
    DBSession.add(new_post)
    DBSession.flush()
    assert new_post.id is not None
    assert new_post.created is not None

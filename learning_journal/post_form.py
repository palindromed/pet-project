# coding=utf-8
from __future__ import unicode_literals

from wtforms import Form, StringField, validators, TextAreaField


class ModifyPostForm(Form):
    """Create class for form to edit/create a post"""

    title = StringField('title', [validators.Length(min=4, max=128)])
    text = TextAreaField('text', [validators.Length(min=6)])


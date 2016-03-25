# coding=utf-8
from __future__ import unicode_literals

from wtforms import (Form, StringField, validators,
                    TextAreaField, PasswordField, )


class ModifyPostForm(Form):
    """Create class for form to edit/create a post"""

    title = StringField('title', [validators.Length(min=4, max=128)])
    text = TextAreaField('text', [validators.Length(min=6)])


class UserForm(Form):
    """Create class for a form to create a user and login."""

    username = StringField('username', [validators.Length(min=2, max=128)])
    password = PasswordField('password', [validators.Length(min=5, max=128)])

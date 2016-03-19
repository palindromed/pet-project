from wtforms import Form, StringField, validators, TextAreaField


class PostForm(Form):
    """Create class for form to edit/create a post"""

    title = StringField('Title', [validators.Length(min=4, max=128)])
    text = TextAreaField('Text', [validators.Length(min=6)])

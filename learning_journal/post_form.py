from wtforms import Form, StringField, validators, TextAreaField

class PostForm(Form):
        title = StringField('Title', [validators.Length(min=4, max=128)])
        text = TextAreaField('Text', [validators.Length(min=6)])

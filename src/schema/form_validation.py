from wtforms import Form, StringField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(
        min=4, max=25), validators.InputRequired()])
    password = StringField('Password', [validators.InputRequired(), 
    validators.Length(min=5)])
    email = StringField('Email Address', [validators.Email()])
    secret_key = StringField('Secret Key')

class LoginForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = StringField('Password', [validators.InputRequired()])



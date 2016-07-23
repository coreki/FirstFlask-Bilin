from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,BooleanField,SelectField,TextAreaField,PasswordField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo,ValidationError
from ..models import Role,User
from flask.ext.pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('Whar is your name?',validators=[Required()])
    submit = SubmitField('Submit')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[Required()])
    new_password = PasswordField('New Password', validators=[Required(),EqualTo('new_password2','Passwords must match')])
    new_password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('Name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = StringField('About Me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username', validators=[Required(), Length(4, 26), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                    'Usernames must have only letters,'
                                                                                  'numbers,dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = StringField('About me', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class PostForm(Form):
    body = PageDownField('What is on your mind?',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = TextAreaField('Enter your comment',validators=[Required()])
    submit = SubmitField('Submit')
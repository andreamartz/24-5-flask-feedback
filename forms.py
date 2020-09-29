from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length


class RegisterUserForm(FlaskForm):
    """Form to enter registration information for a new user."""

    username = StringField("Username", validators=[
                           InputRequired(message="Username cannot be blank."),
                           Length(min=1, max=20, message="Username must be between 1 and 20 characters long.")])

    password = PasswordField("Password", validators=[
                             InputRequired(message="Password cannot be blank.")])

    email = EmailField("Email", validators=[
                       InputRequired(message="Email cannot be blank."),
                       Length(min=1, max=50, message="Email address must be between 1 and 50 characters long.")])

    first_name = StringField("First Name", validators=[
                             InputRequired(
                                 message="First name cannot be blank."),
                             Length(min=1, max=30, message="First name must be between 1 and 30 characters long.")])

    last_name = StringField("Last Name", validators=[
                            InputRequired(
                                message="Last name cannot be blank."),
                            Length(min=1, max=30, message="Last name must be between 1 and 30 characters long.")])


class LoginUserForm(FlaskForm):
    """Form to enter username and password."""

    username = StringField("Username", validators=[
                           InputRequired(message="Username cannot be blank."),
                           Length(min=1, max=20, message="Username must be between 1 and 30 characters long.")])

    password = PasswordField("Password", validators=[
                             InputRequired(message="Password cannot be blank.")])


class UserFeedbackForm(FlaskForm):
    """Form to enter username and password."""

    title = StringField("Feedback Title", validators=[InputRequired()])
    content = TextAreaField("Feedback Text",
                            render_kw={"rows": 15, "cols": 11},
                            validators=[InputRequired(),
                                        Length(min=1, max=500, message="Message must be between 1 and 500 characters long.")])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

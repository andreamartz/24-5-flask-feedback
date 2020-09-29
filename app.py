"""Flask app for Users"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import db, connect_db, User, Post
from forms import RegisterUserForm, LoginUserForm, UserFeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized

from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors by showing custom 404 page."""

    return render_template('404.html'), 404


@app.route('/')
def root():
    """Redirect to registration page."""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register a user by rendering registration form template and handling form submission."""

    form = RegisterUserForm()

    # if the CSRF token is validated after the form is submitted
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
            session['username'] = new_user.username
            flash("Welcome! Your account was successfully created!", "success")
            return redirect(f'/users/{new_user.username}')
        except IntegrityError:
            form.username.errors.append(
                "That username is taken. Please choose another username.")

    # if the form validation fails
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Render login form or handle login."""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate method will return the user object found or False
        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back, { user.username }', 'primary')
            session["username"] = user.username  # keep logged in
            # return redirect("/secret")
            return redirect(f'/users/{ user.username }')

        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


# Step 6: Let's change /secret to /users/<username>
@app.route('/users/<username>')
def show_user(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user = User.query.get_or_404(username)
        form = DeleteForm()
        return render_template("/users/show.html", user=user, form=form)


# Step 8: Add user account deletion route
@app.route('/users/<username>/delete', methods=["POST"])
def delete(username):
    """Delete user account and redirect to root."""

    # NOT DONE
    if "username" not in session or username != session['username']:
        # flash("Please login first!", "danger")
        # return redirect('/login')
        raise Unauthorized()

    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        # session.pop('username')
        return redirect('/logout')

# NOT DONE: give_feedback route


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def give_feedback(username):
    """Show a feedback form and handle feedback submission."""

    form = UserFeedbackForm()

    if "username" not in session or username != session["username"]:
        flash("Please login first!", "danger")

        return redirect('/login')

    user = User.query.get_or_404(username)

    # if the CSRF token is validated after the form is submitted
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = username

        # Create new post instance
        new_post = Post(username=username, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{ user.username }')

    # if the form validation fails
    else:
        return render_template('/feedback/add.html', form=form, user=user)


@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete a specific piece of feedback and redirect to /users/<username>."""
    # There is no logged in user
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    post = Post.query.get_or_404(feedback_id)
    # Logged in user does NOT own the feedback post
    if session['username'] != post.username:
        flash("You don't have permission to do that!", "danger")
        return redirect('/')
    # Logged in user owns the feedback post
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("Feedback deleted!", "info")
        return redirect(f'/users/{post.username}')


# @app.route("/feedback/<int:post_id>/delete", methods=["POST"])
# def delete_feedback(post_id):
#     """Delete feedback."""

#     post = Post.query.get_or_404(post_id)
#     if "username" not in session or post.username != session['username']:
#         raise Unauthorized()

#     form = DeleteForm()

#     if form.validate_on_submit():
#         db.session.delete(post)
#         db.session.commit()

#     return redirect(f"/users/{post.username}")


# Step 5: Log out users


@app.route('/logout')
def logout_user():
    """Log the user out."""

    session.pop('username')
    flash("Goodbye!", "info")

    return redirect('/')

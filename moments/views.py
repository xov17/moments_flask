# coding:utf-8

from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from moments import moments, login_manager, db
from .forms import SignUpForm, SignInForm, PostForm
from .models import User, Post
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==user_id).first()

@moments.before_request
def before_request():
    g.user = current_user


@moments.route("/", methods=['GET', 'POST'])
def index(name=None):
    """
    Landing page, later merge with login and create account
    Also with posts and recent posts if logged in
    """
    if not g.user.is_authenticated:
        # should redirect to login
        return login_manager.unauthorized()
    form = PostForm()
    if form.validate_on_submit():
        new_post = form.post.data
        new_post_list = new_post.split()
        for i in range(len(new_post_list)):
            if new_post_list[i][0] == "#":
                new_post_list[i] = '<a href="/tag/%s">%s</a>' % (str(new_post_list[i][1:]) , new_post_list[i])
        new_post = (" ").join(new_post_list)
        post = Post(body=new_post, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        # without the redirect, the last request is the POST request
        # that submitted the form, so a refresh action will resubmit
        # the form, causing a second Post record that is identical to the first
        # to the first to be written to the database. not good.
        return redirect(url_for('index'))
    posts = g.user.posts
    return render_template('dashboard.html', form=form, posts=posts)

@moments.route("/signin", methods=['GET', 'POST'])
def signin():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    flash('Before validate_on_submit')
    if form.validate_on_submit():
        flash('In validate_on_submit')
        user = User.query.filter_by(username=form.username.data).first()
        if (user != None) and user.is_correct_password(form.password.data):
            login_user(user, remember=True)

            return redirect(url_for('signin'))
        else:
            flash('User and password not found')

    return render_template('signin.html', form=form)


@moments.route("/signup", methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    password=form.password.data, 
                    firstname=form.firstname.data, 
                    email=form.email.data)
        username_query = User.query.filter_by(username=form.username.data).first()
        if (username_query != None):
            message = "Username taken %s" % user
            flash(message)
            return redirect(url_for('signup'))

        email_query = User.query.filter_by(username=form.username.data).first()
        if (email_query != None):
            message = "Email already used %s" % user
            flash(message)
            return redirect(url_for('signup'))
        flash('Valid signup inputs!')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        flash('Signed in after signup!')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@moments.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))

# Error handlers
@moments.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@moments.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

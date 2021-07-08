from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Review, Restaurant
from app.auth.forms import SignUpForm, LoginForm
from app import bcrypt

# Import app and db from app package so that we can run app
from app import app, db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("inside login route")
    form = LoginForm()
    if form.validate_on_submit():
        print("inside login form")
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True, force=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('api.display_categories'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

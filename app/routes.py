import sqlalchemy as sa

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from app import app, forms, db, prediction_model
from app.forms import ChoiceObj
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', username=current_user.username)
    else:
        return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegistrationForm()
    form.genres.choices = [(x, x) for x in prediction_model.genres]
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.set_genres(form.genres.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/liked', methods=['GET', 'POST'])
def liked():
    choices = current_user.get_liked_tracks()
    form = forms.LikedForm(obj=ChoiceObj('liked', [x[0] for x in choices]))
    form.liked.choices = choices
    if form.is_submitted():
        current_user.update_liked_tracks(form.liked.data, replace=True)
        return redirect(url_for('liked'))
    return render_template('liked.html', title='Likes', form=form)

@app.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():
    form = forms.PredictionForm()
    choices = prediction_model.get_prediction(current_user.liked_tracks_ids, current_user.genres)
    form.recommendation.choices = choices
    if form.is_submitted():
        current_user.update_liked_tracks(form.recommendation.data)
        return redirect(url_for('recommendations'))
    return render_template('recommendations.html', title='Recommendations', form=form)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', default=None)

    if query is None:
        return jsonify([])

    return jsonify(prediction_model.search(query))

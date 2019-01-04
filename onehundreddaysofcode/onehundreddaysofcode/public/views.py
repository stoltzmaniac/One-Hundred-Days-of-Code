# -*- coding: utf-8 -*-
import json

"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from onehundreddaysofcode.extensions import csrf_protect
from onehundreddaysofcode.database import mdb
from onehundreddaysofcode.extensions import login_manager
from onehundreddaysofcode.public.forms import LoginForm
from onehundreddaysofcode.user.forms import RegisterForm
from onehundreddaysofcode.user.models import User
from onehundreddaysofcode.utils import flash_errors, twtr
from onehundreddaysofcode.public.mongo_forms import RandomForm
from onehundreddaysofcode.public.mongo_models import RandomData

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@csrf_protect.exempt
@blueprint.route("/mongo", methods=["GET", "POST"])
def mongo():
    """Testing mongo"""
    if request.method == "GET":
        data = mdb.db.songs.find_one({"name": "hello"})
        return jsonify(data), 200
    if request.method == "POST":
        data = request.data
        d = json.loads(data.decode('utf-8'))
        mdb.db.songs.insert_one(d)
        return jsonify({'ok': True, 'message': 'Song created successfully!'}), 200


@blueprint.route("/twitter/<query>/<count>", methods=["GET", "POST"])
def twitter(query, count):
    """Testing twitter"""
    tweets = mdb.db.tweets
    search_query = f"q={query}&count={str(count)}"
    results = twtr.GetSearch(raw_query=search_query)
    for r in results:
        tweets.insert_one(r.AsDict())
    return jsonify({'yes': 'did it'})


@blueprint.route("/add_random_data", methods=["GET", "POST"])
def twitter_lookup():
    """Home page."""
    form = RandomForm(request.form)
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = request.form
            random_data = RandomData(
                username=form_data['username'],
                text=form_data['text'])
            random_data.save()
            return jsonify({'yes': 'you did it'})
        else:
            flash_errors(form)
    return render_template("public/about2.html", myform=form)

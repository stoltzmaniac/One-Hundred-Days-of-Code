# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import pandas as pd
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
from flask_login import login_required

from onehundreddaysofcode.database import mdb
from onehundreddaysofcode.utils import flash_errors, twtr
from onehundreddaysofcode.twitter.mongo_forms import TwitterForm
from onehundreddaysofcode.twitter.utils import twitter_search
from onehundreddaysofcode.stoltzmaniac.utils import analyze_tweet_sentiment


blueprint = Blueprint("stoltzmaniac", __name__, url_prefix="/stoltzmaniac", static_folder="../static")


@blueprint.route("/", methods=["GET"])
@login_required
def index():
    return jsonify({'add': 'a stoltzmaniac index page'})


@blueprint.route("/twitter", methods=["GET", "POST"])
@login_required
def stoltzmaniac_twitter():
    form = TwitterForm(request.form)
    if request.method == "GET":
        return render_template("stoltzmaniac/twitter_sentiment.html",
                               myform=form,
                               chart_data={})

    elif request.method == "POST" and form.validate_on_submit():
        chart_data = []
        data = twitter_search(request)
        sentiment = analyze_tweet_sentiment(data)
        return render_template("stoltzmaniac/twitter_sentiment.html",
                               myform=form,
                               chart_data=sentiment)



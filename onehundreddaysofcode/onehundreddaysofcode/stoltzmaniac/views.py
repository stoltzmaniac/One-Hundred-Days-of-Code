# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import pandas as pd
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    session,
)
from flask_login import login_required

from onehundreddaysofcode.database import mdb
from onehundreddaysofcode.utils import flash_errors, twtr
from onehundreddaysofcode.twitter.mongo_forms import TwitterForm
from onehundreddaysofcode.twitter.utils import twitter_search
from onehundreddaysofcode.stoltzmaniac.utils import analyze_tweet_sentiment, analyze_csv, altair_plot


blueprint = Blueprint(
    "stoltzmaniac", __name__, url_prefix="/stoltzmaniac", static_folder="../static"
)


@blueprint.route("/")
@login_required
def home():
    return render_template("stoltzmaniac/home.html")


@blueprint.route("/csv_example")
@login_required
def csv_example():
    data = analyze_csv()
    return data.to_html()


@blueprint.route("/altair_example")
@login_required
def altair_example():
    plot = altair_plot()
    return render_template("stoltzmaniac/altair_plot.html", plot=plot.to_html())


@blueprint.route("/twitter", methods=["GET", "POST"])
@login_required
def twitter_sentiment():
    form = TwitterForm(request.form)
    if request.method == "GET":
        return render_template(
            "stoltzmaniac/twitter_sentiment.html", myform=form
        )

    elif request.method == "POST" and form.validate_on_submit():
        chart_data = []
        data = twitter_search(request)
        sentiment = analyze_tweet_sentiment(data)
        return render_template(
            "stoltzmaniac/twitter_sentiment.html", myform=form,
            chart_data=sentiment[1], tweets=sentiment[0]
        )


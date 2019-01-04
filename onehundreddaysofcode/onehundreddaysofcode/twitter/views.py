# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
from flask_login import login_required

from onehundreddaysofcode.database import mdb
from onehundreddaysofcode.utils import flash_errors, twtr
from onehundreddaysofcode.twitter.mongo_forms import TwitterForm


blueprint = Blueprint("twitter", __name__, url_prefix="/twitter", static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def twitter():
    """Adding Twitter data to Mongo database via form"""
    user_id = str(session['user_id'])
    form = TwitterForm(request.form)
    tweets = mdb.db.tweets
    data = tweets.find({'one_hundred_id': user_id})
    output = [i for i in data]
    if request.method == "GET":
        return render_template("twitter/index.html", myform=form, output=output)

    elif request.method == "POST" and form.validate_on_submit():
        form_data = request.form
        search_query = f"q={form_data['search_term']}&count={str(form_data['count'])}"
        results = twtr.GetSearch(raw_query=search_query)
        for r in results:
            rd = r.AsDict()
            rd['one_hundred_id'] = user_id
            tweets.insert_one(rd)
        return render_template("twitter/index.html", myform=form, output=output)

    else:
        return jsonify({'something': 'went wrong'})

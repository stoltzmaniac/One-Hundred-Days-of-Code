# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import time
from urllib.parse import quote_plus

import pandas as pd
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
    chart_data = []
    for i in output:
        chart_data.append({'timestamp': i['timestamp'], 'text': i['text'], 'screen_name': i['user']['screen_name']})

    chart_df = pd.DataFrame(chart_data)
    chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'])
    chart_df['Date'] = chart_df['timestamp'].dt.hour
    chart_df = chart_df.groupby(['Date']).count()
    chart_df = chart_df.reset_index()
    chart_df = chart_df.sort_values('Date', ascending=True)
    # chart_df['Date'] = chart_df['Date'].apply(lambda x: str(x))
    chart_df['Tweets'] = chart_df['text']
    chart_df = chart_df[['Date', 'Tweets']]
    chart_data = chart_df.to_dict(orient='records')
    chart_dates = ['Date']
    chart_tweets = ['Tweets']
    for i in chart_data:
        chart_dates.append(i['Date'])
        chart_tweets.append(i['Tweets'])
    if request.method == "GET":
        return render_template("twitter/index.html", myform=form, output=output,
                               chart_dates=chart_dates, chart_tweets=chart_tweets)

    elif request.method == "POST" and form.validate_on_submit():
        form_data = request.form
        search_query = f"q={quote_plus(form_data['search_term'])}&count={str(form_data['count'])}"
        results = twtr.GetSearch(raw_query=search_query)
        for r in results:
            rd = r.AsDict()
            rd['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(rd['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            rd['one_hundred_id'] = user_id
            tweets.insert_one(rd)
        return redirect(url_for("twitter.twitter"))

    else:
        return jsonify({'something': 'went wrong'})

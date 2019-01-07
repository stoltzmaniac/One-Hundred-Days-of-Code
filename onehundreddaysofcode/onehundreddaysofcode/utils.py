# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import json
import datetime
from bson.objectid import ObjectId
from flask import flash
import twitter

from onehundreddaysofcode.settings import (
    TWTR_CONSUMER_KEY,
    TWTR_CONSUMER_SECRET,
    TWTR_TOKEN_KEY,
    TWTR_TOKEN_SECRET,
)


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


twtr = twitter.Api(
    consumer_key=TWTR_CONSUMER_KEY,
    consumer_secret=TWTR_CONSUMER_SECRET,
    access_token_key=TWTR_TOKEN_KEY,
    access_token_secret=TWTR_TOKEN_SECRET,
)

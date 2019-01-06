# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import pandas as pd
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
from flask_login import login_required

from onehundreddaysofcode.database import mdb
from onehundreddaysofcode.utils import flash_errors, twtr
from onehundreddaysofcode.twitter.mongo_forms import TwitterForm

from onehundreddaysofcode.data_science.stoltzmaniac import run_analysis


blueprint = Blueprint("data_science", __name__, url_prefix="/data_science", static_folder="../static")


@blueprint.route("/", methods=["GET"])
@login_required
def index():
    return jsonify({'add': 'a data_science index page'})


@blueprint.route("/stoltzmaniac", methods=["GET"])
@login_required
def stoltzmaniac_run_analysis():
    data = run_analysis.hello()
    return jsonify(data)



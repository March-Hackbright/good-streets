import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
# from model import User, Trip, UserTrip, Comment, CheckList, Geodata, GeodataTrip, Route, connect_to_db, db
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
# app.jinja_env.undefined = StrictUndefined

google_maps_key = os.environ['GOOGLE_MAPS_ACCESS_TOKEN']


@app.route('/map')
def display_map():
    return render_template("map.html", google_maps_key=google_maps_key)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

    

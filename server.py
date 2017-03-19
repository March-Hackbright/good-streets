import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
# from model import User, Trip, UserTrip, Comment, CheckList, Geodata, GeodataTrip, Route, connect_to_db, db
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import connect_to_db, db, Crime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
# app.jinja_env.undefined = StrictUndefined

google_maps_key = os.environ['GOOGLE_MAPS_ACCESS_TOKEN']


@app.route('/map')
def display_map():
    return render_template("map.html", google_maps_key=google_maps_key)


@app.route('/markers.json')
def crimes_in_box():
    """Query this endpoint with parameters NE-lat, NE-lng, SW-lat, SW-lng.
    Returns all crimes in that bounding box."""

    max_lat = float(request.form.get('NE-lat', 38))
    max_lng = float(request.form.get('NE-lng', -122))

    min_lat = float(request.form.get('SW-lat', 37))
    min_lng = float(request.form.get('SW-lng', -123))

    print min_lat, min_lng, max_lat, max_lng

    crimes = Crime.query.filter(Crime.lat >= min_lat,
                                Crime.lat <= max_lat,
                                Crime.lng >= min_lng,
                                Crime.lng <= max_lng,
                                ).all()
    print crimes

    list_to_send = []
    print "Number of crimes:", len(crimes)

    for crime in crimes:
        data = {'lat': float(crime.lat),
                'lng': float(crime.lng),
                'category': crime.category,
                'specific': crime.specific,
                'datetime': crime.date.isoformat()
                }
        list_to_send.append(data)
    return jsonify(list_to_send)


@app.route("/green-markers.json", methods=["POST"])
def show_resources():
    """Get resources from Amanda's Yelp file.  Query this with latitude and longitude bounding boxes."""

    min_lat = request.form.get('SW-lat')
    max_lat = request.form.get('NE-lat')
    min_lng = request.form.get('SW-lng')
    max_lng = request.form.get('NE-lng')

    if min_lat and max_lat and min_lng and max_lng:
        min_lat = float(min_lat)
        max_lat = float(max_lat)
        min_lng = float(min_lng)
        max_long = float(max_lng)

        kilometers_lat = 55.5*(max_lat - min_lat)
        kilometers_lng = 44.5*(max_lng - min_lng)
        radius = max(kilometers_lng+kilometers_lat, 100)
        center_lng = (max_lng + min_lng)/2
        center_lat = (max_lat + min_lat)/2

        depts = yelp.get_police_departments(center_lat, center_lng, radius)
        self_defense = yelp.get_self_defense(center_lat, center_lng, radius)

    else:
        depts = yelp.get_police_departments()
        self_defense = yelp.get_self_defense()
    
    return jsonify(depts + self_defense)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
    import yelp

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')


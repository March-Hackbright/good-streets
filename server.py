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


@app.route('/markers.json', methods=["POST"])
def crimes_in_box():
    """Query this endpoint with parameters NE-lat, NE-lng, SW-lat, SW-lng.
    Returns all crimes in that bounding box."""

    my_first_data = request.form.get('first')
    if my_first_data:
        first = json.loads(my_first_data)
    else:
        first = {'lat': 37, 'lng': -123}
    my_second_data = request.form.get('second')
    if my_second_data:
        second = json.loads(my_second_data)
        print type(second)
        print second
    else:
        second = {'lat': 38, 'lng': -122}


    max_lat = max(first['lat'], second['lat'])
    min_lat = min(first['lat'], second['lat'])

    max_lng = max(first['lng'], second['lng'])
    min_lng = min(first['lng'], second['lng'])

    # print my_first_data

    # max_lat = float(request.args.get('NE-lat', 38))
    # max_lng = float(request.args.get('NE-lng', -122))

    # min_lat = float(request.args.get('SW-lat', 37))
    # min_lng = float(request.args.get('SW-lng', -123))

    print min_lat, min_lng, max_lat, max_lng

    crimes = Crime.query.filter(Crime.lat >= min_lat, 
                                Crime.lat <= max_lat,
                                Crime.lng >= min_lng,
                                Crime.lng <= max_lng,
                                ).all()

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
    write_log("Result list", str(list_to_send))
    return json.dumps(list_to_send)

def write_log(*args):
    with open("server.log", 'a') as log_file:
        log_file.write('\n'.join(args))

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')


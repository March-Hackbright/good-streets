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


def process_form(my_first_data, my_second_data):

    if my_first_data:
        first = json.loads(my_first_data)
    else:
        first = {'lat': 37, 'lng': -123}
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
    return {'min_lng': min_lng, 'max_lng': max_lng, 'min_lat': min_lat, 'max_lat': max_lat}


@app.route('/markers.json', methods=["POST"])
def crimes_in_box():
    """Query this endpoint with parameters NE-lat, NE-lng, SW-lat, SW-lng.
    Returns all crimes in that bounding box."""

    my_first_data = request.form.get('first')
    my_second_data = request.form.get('second')

    bounds = process_form(my_first_data, my_second_data)

    min_lat = bounds['min_lat']
    max_lat = bounds['max_lat']
    min_lng = bounds['min_lng']
    max_lng = bounds['max_lng']

    print min_lat, min_lng, max_lat, max_lng

    crimes = Crime.query.filter(Crime.lat >= min_lat, 
                                Crime.lat <= max_lat,
                                Crime.lng >= min_lng,
                                Crime.lng <= max_lng,
                                ).order_by(Crime.date.desc()).limit(100).all()

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
    write_log("Result list", str(list_to_send)[:200])
    return json.dumps(list_to_send)

def write_log(*args):
    with open("server.log", 'a') as log_file:
        log_file.write('\n'.join(args))


@app.route("/green-markers.json", methods=["POST"])
def show_resources():
    """Get resources from Amanda's Yelp file.  Query this with latitude and longitude bounding boxes."""

    my_first_data = request.form.get('first')
    my_second_data = request.form.get('second')

    if my_second_data and my_first_data:
        bounds = process_form(my_first_data, my_second_data)

        min_lat = bounds['min_lat']
        max_lat = bounds['max_lat']
        min_lng = bounds['min_lng']
        max_lng = bounds['max_lng']

        kilometers_lat = 55.5*(max_lat - min_lat)
        kilometers_lng = 44.5*(max_lng - min_lng)
        radius = max(1000*kilometers_lng+1000*kilometers_lat, 100)
        center_lng = (max_lng + min_lng)/2
        center_lat = (max_lat + min_lat)/2

        depts = yelp.get_police_departments(center_lat, center_lng, radius)
        self_defense = yelp.get_self_defense(center_lat, center_lng, radius)
        write_log("Police departments", str(depts))
        write_log("Self defense", str(self_defense))

        depts = [x for x in depts if x['lat'] >= min_lat and x['lng'] >= min_lng and x['lat'] <= max_lat and x['lng'] <= max_lng]
        self_defense = [x for x in self_defense if x['lat'] >= min_lat and x['lng'] >= min_lng and x['lat'] <= max_lat and x['lng'] <= max_lng]


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


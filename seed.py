#from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime
from decimal import Decimal

def read_json_file(file_name='simplified_crime_data.json'):
    """Read JSON file for use in creating tables."""

    return json.load(open(file_name, 'r'))


def convert_date(date_string, time_string):
    """Takes the date and time as formatted in the raw data, returns Python datetime object."""

    full_string = date_string + " T " + time_string

    date = datetime.strptime(full_string, "%Y-%m-%d T %H:%M")
    return date


def load_data(file_name):
    """Reads data from a JSON file, loads into database."""

    all_data = read_json_file(file_name)

    for item in all_data:
        crime = Crime(category=item['category'],
            specific=item['specification'],
            date = convert_date(item['date'], item['time'])
            location = item['location'],
            lat = Decimal(item['latitude']),
            lng = Decimal(item['longitude'])
            )
        db.session.add(crime)
    db.session.commit()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        file_name = 'test_data.json'
        db_uri = 'postgresql:///test_crime_data'
    else:
        file_name = 'simplified_crime_data.json'
        db_uri = 'postgresql:///test_crime_data'

    from server import app
    from model import connect_to_db

    connect_to_db(app, db_uri)

    load_data(file_name)

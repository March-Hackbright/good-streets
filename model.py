from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Crime(db.Model):
    """Type, location, and date/time of a crime as provided from SFPD data."""

    __tablename__ = "crimes"

    crime_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Numeric(20, 15))
    lng = db.Column(db.String(20, 15))
    category = db.Column(db.String(128))
    specific = db.Column(db.String(256))
    date = db.Column(db.DateTime)
    location = db.Column(db.String(128))

    def __repr__(self):
        return "Crime %s: %s at %s" % (self.crime_id, self.category, self.location)


def connect_to_db(app, db_uri='postgresql:///crime_data', echo=True):
    """Connect a Flask app to our database."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app)

    db.create_all()

    print "Connected to DB %s" % app.config['SQLALCHEMY_DATABASE_URI']
# Good Streets

## Overview

Good Streets was create as part of [WomenHack - The All-Women Hackathon San Francisco](https://www.eventbrite.com/e/womenhack-the-all-women-hackathon-san-francisco-tickets-27670276542) held March 18, 2017 at [Pivotal Labs](https://pivotal.io/locations/san-francisco). We had 10 hours to code a solution to one of several issues facing women.

## The Team
- [Amanda Crawford](https://github.com/agerista) - Coding
- [Blerina Aliaj](https://github.coerinaAliaj) - Coding
- Elaine Ying - Product Management
- [Elizabeth Goodman](https://github.com/ESQG) - Coding
- [Laurel Kline](https://github.com/geekshe) - Coding
- [Soo Park](https://github.com/soo-park) - Product Management

## The Solution

Good Streets is intended to address the issue of women's safety. We mapped out recent crime data on a map of San Francisco. In keeping with out empowerment focus, we also plotted out Safe Havens that women could use if they were feeling unsafe. To top it all off, we plotted out pro-active resources like self-defense classes that would increase future feelings of safety. And of course, the app can be used by anyone concerned with their safety!

The goal is that someone could open the app, see that the current area is a little unsafe, and choose a safer walking route, or duck into a safe haven and call a Lyft.

## The Tech Stack

The site is built using Python, Flask, and SQLAlchemy. Crime data was provided by the City of San Francisco police reports in CSV format. We imported that into a Posgres DB, then used Python to extract the data and write it in JavaScript format so the Google Maps API could plot it out properly. To overlay the safe havens, we made dynamic queries to the Yelp API to retrieve the hours and locations of businesses categories like police stations or bars (chosen because they keep late hours). Bootstrap was used for the template.

## Forking

You are welcome to fork the project and build on the code base. It would be great to make the world a little safer!

### Seeding the DB

To seed the test database, run:
```
createdb test_crime_data
python seed.py test
```

Otherwise, run:
```
createdb crime_data
python seed.py
```

### Starting the Server

To start the server, run:

```
python server.py
```

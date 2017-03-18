"""Yelp API calls for business ids and reviews. Cap is 25,000 calls per day."""

import os
import requests


# Call limit to yelp api is 25,000/day

SECRET = os.environ["YELP_SECRET"]
Y_ID = os.environ["YELP_ID"]
API_ROOT = "https://api.yelp.com/v3/"


def obtain_bearer_token():
    """Request authorization tokens"""

    endpoint = "https://api.yelp.com/oauth2/token"

    response = requests.post(endpoint, data={"client_secret": SECRET,
                                             "client_id": Y_ID,
                                             "grant_type": "client_credentials"})

    bearer_token = response.json()['access_token']

    return bearer_token


def get_header():
    """get header and token information"""

    token = obtain_bearer_token()
    headers = {"Authorization": 'Bearer {}'.format(token)}

    return headers


def yelp_information(business_id):
    """Returns image, rating, and open hours when given a business_id"""

    endpoint = API_ROOT + "businesses/{}".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    info = response.json()

    yelp_info = {}

    yelp_info["rating"] = info["rating"]

    try:
        yelp_info["open_now"] = info['hours'][0]["is_open_now"]
        yelp_info["opens"] = info['hours'][0]["open"][0]['start']
        yelp_info["closes"] = info['hours'][0]["open"][0]['end']

    except KeyError:
        yelp_info["open_now"] = ''
        yelp_info["opens"] = ''
        yelp_info["closes"] = ''

    ### to-do: key error if hours are not included.

    print yelp_info
    return yelp_info


def get_yelp_reviews(business_id):
    """Given a business_id returns yelp reviews

       yelp_reviews[reviews{user: "Jane Reviewer",
                    text: "This place is awesome!",
                    rating: 5,
                    url: "www.yelp.com/rest_of_url"}]

    """

    endpoint = API_ROOT + "businesses/{}/reviews".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    information = response.json()

    review_list = information['reviews']

    i = 0
    yelp_reviews = []

    while i < len(review_list):

        reviews = {}

        name = review_list[i]['user']['name']
        reviews['name'] = name

        text = review_list[i]['text']
        reviews['text'] = text

        rating = review_list[i]['rating']
        reviews['rating'] = rating

        url = review_list[i]['url']
        reviews['url'] = url

        yelp_reviews.append(reviews)

        i += 1

    return yelp_reviews


def get_police_departments():
    """Get the business id for each business"""

    endpoint = API_ROOT + "businesses/search"

    data = {"categories": "policedepartments",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "limit": 50,
            }

    response = requests.get(endpoint, params=data, headers=get_header())

    business = response.json()

    result_list = []

    for b in business['businesses']:
        police_departments = b['id']

        lat = b['coordinates']['latitude']
        lng = b['coordinates']['longitude']
        data = yelp_information(police_departments)

        data['category'] = "police department"
        data['lat'] = lat
        data['lng'] = lng

        result_list.append(data)

    print result_list
    return result_list


def get_self_defense(center_lat=37.7749, center_lng=-122.4194):
    """Get self-defense studios in the area"""

    endpoint = API_ROOT + "businesses/search"

    data = {"categories": "martialarts",
            "latitude": center_lat,
            "longitude": center_lng,
            "radius": 100
            "limit": 10,
            }

    response = requests.get(endpoint, params=data, headers=get_header())

    business = response.json()

    results = []

    for b in business['businesses']:
        self_defense = b['id']
        lat = b['coordinates']['latitude']
        lng = b['coordinates']['longitude']

        data = yelp_information(self_defense)

        data['lat'] = lat
        data['lng'] = lng
        data['category'] = "self-defense"
        results.append(data)

    return results


################################################################################
if __name__ == "__main__":

    # from server import app
    # connect_to_db(app)
    obtain_bearer_token()
    get_police_departments()
    # get_self_defense()
    # yelp_information(business_id)
    # get_yelp_reviews(business_id)

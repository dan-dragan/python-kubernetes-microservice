from services import root_dir, nice_json
from flask import Flask
from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
import requests
import os
import sys

app = Flask(__name__)

with open("{}/database/users.json".format(root_dir()), "r") as f:
    users = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "users": "/users",
            "user": "/users/<username>",
            "bookings": "/users/<username>/bookings",
            "suggested": "/users/<username>/suggested"
        }
    })


@app.route("/users", methods=['GET'])
def users_list():
    return nice_json(users)    


@app.route("/users/<username>", methods=['GET'])
def user_record(username):
    if username not in users:
        raise NotFound

    return nice_json(users[username])


@app.route("/users/<username>/bookings", methods=['GET'])
def user_bookings(username):
    """
    Gets booking information from the 'Bookings Service' for the user, and
     movie ratings etc. from the 'Movie Service' and returns a list.
    :param username:
    :return: List of Users bookings
    """
    if username not in users:
        raise NotFound("User '{}' not found.".format(username))

    try:
        users_bookings = requests.get("http://127.0.0.1:5003/bookings/{}".format(username))
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The Bookings service is unavailable.")

    if users_bookings.status_code == 404:
        raise NotFound("No bookings were found for {}".format(username))

    users_bookings = users_bookings.json()
     # For each booking, get the rating and the movie title
    result = {}
    moviesByDates= users_bookings["dates"]
    for  date,movies in moviesByDates.items():
        result[date] = []
        for movieid in movies:
            try:
                movies_resp = requests.get("http://127.0.0.1:5001/movies/{}".format(movieid))
            except requests.exceptions.ConnectionError:
                raise ServiceUnavailable("The Movie service is unavailable.")
            movies_resp = movies_resp.json()
            result[date].append({
                "title": movies_resp["title"],
                "rating": movies_resp["rating"],
                "uri": movies_resp["uri"]
            })
    result["uri"]=users_bookings["uri"]
    return nice_json(result)


@app.route("/users/<username>/suggested", methods=['GET'])
def user_suggested(username):
    """
    Returns movie suggestions. The algorithm returns a list of 3 top ranked
    movies that the user has not yet booked.
    :param username:
    :return: Suggested movies
    """
    raise NotImplementedError()


if __name__ == "__main__":
    #if ran in a container with CMD ["flask", "run"] instead of CMD ["python", "services/user.py"] the bellow appear not to to be executed
    #see https://stackoverflow.com/questions/41940663/how-can-i-change-the-host-and-port-that-the-flask-command-uses
    print("FLASK_RUN_HOST: {}".format(os.environ.get("FLASK_RUN_HOST")),file=sys.stdout)
    print("FLASK_SERVER_PORT_USER: {}".format(os.environ.get("FLASK_SERVER_PORT_USER")),file=sys.stdout)
    print("FLASK_RUN_PORT: {}".format(os.environ.get("FLASK_RUN_PORT")),file=sys.stdout)
    sys.stdout.flush()
    app.run(host=os.environ.get("FLASK_RUN_HOST"), port=os.environ.get("FLASK_SERVER_PORT_USER"), debug=True, use_reloader=False)

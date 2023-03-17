from services import root_dir, nice_json
from flask import Flask
import json
from werkzeug.exceptions import NotFound


app = Flask(__name__)

with open("{}/database/bookings.json".format(root_dir()), "r") as f:
    bookings = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<username>"
        }
    })


@app.route("/bookings", methods=['GET'])
def booking_list():
    return nice_json(bookings)


@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound
    result = {}
    result ["dates"] = bookings[username]
    result["uri"] = "/bookings/{}".format(username)
    return nice_json(result)

if __name__ == "__main__":
        app.run(host=os.environ.get("FLASK_RUN_HOST"), port=os.environ.get("FLASK_SERVER_PORT_BOOKINGS"), debug=True, use_reloader=False)


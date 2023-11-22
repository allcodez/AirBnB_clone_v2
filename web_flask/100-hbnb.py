#!/usr/bin/python3
"""
This script starts a Flask web application.

The application is configured to listen on 0.0.0.0, port 5000.
Routes:
    /hbnb: Renders the main HBnB home page.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Renders the main HBnB home page."""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLAlchemyy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

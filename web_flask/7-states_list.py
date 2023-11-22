#!/usr/bin/python3
"""
This script starts a Flask web application.

The application is configured to listen on 0.0.0.0, port 5000.
Routes:
    /states_list: Renders an HTML page displaying a list of all State objects in DBStorage.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Renders an HTML page with a list of all State objects in DBStorage.

    The list is sorted by state name.
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

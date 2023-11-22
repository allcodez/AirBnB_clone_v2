#!/usr/bin/python3
"""
This script starts a Flask web application.

The application is configured to listen on 0.0.0.0, port 5000.
Routes:
    /states: Renders an HTML page displaying a list of all State objects.
    /states/<id>: Renders an HTML page displaying information about the state with the given <id>.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Renders an HTML page with a list of all States.

    The list is sorted by state name.
    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Renders an HTML page with information about the state with the given <id>, if it exists."""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

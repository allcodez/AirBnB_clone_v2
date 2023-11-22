#!/usr/bin/python3
"""
This script starts a Flask web application.

The application is configured to listen on 0.0.0.0, port 5000.

Routes:
    /: Renders a page displaying the greeting 'Hello HBNB!'.
    /hbnb: Renders a page displaying the text 'HBNB'.
    /c/<text>: Renders a page displaying 'C' followed by the value of <text>.
    /python/(<text>): Renders a page displaying 'Python' followed by the value of <text>.
    /number/<n>: Renders a page displaying 'n is a number' only if <n> is an integer.
    /number_template/<n>: Renders an HTML page only if <n> is an integer.
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Renders a page displaying the greeting 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Renders a page displaying the text 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Renders a page displaying 'C' followed by the value of <text>.

    Any underscores in <text> are replaced with spaces.
    """
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """Renders a page displaying 'Python' followed by the value of <text>.

    Any underscores in <text> are replaced with spaces.
    """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Renders a page displaying 'n is a number' only if <n> is an integer."""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Renders an HTML page only if <n> is an integer."""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

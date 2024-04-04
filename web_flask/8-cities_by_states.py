#!/usr/bin/python3
""" HBNB Flask Server """
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def lists_cities():
    """ List all the states """
    states = sorted(list(storage.all(State).values()), key=lambda s: s.name)
    for state in states:
        state.cities.sort(key=lambda c: c.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def app_teardown(exc):
    """ Teardown flask app context """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
""" HBNB Flask Server """
from flask import Flask, render_template

from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def lists_states():
    """ Display the page """
    states = sorted(list(storage.all(State).values()), key=lambda s: s.name)
    amenities = sorted(list(storage.all(Amenity).values()),
                        key=lambda a: a.name)
    return render_template('10-hbnb_filters.html', states=states,
                            amenities=amenities)


@app.teardown_appcontext
def app_teardown(exc):
    """ Teardown flask app context """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

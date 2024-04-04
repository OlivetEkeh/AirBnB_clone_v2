#!/usr/bin/python3
""" HBNB Flask Server """
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def lists_states():
    """ List all the states """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def app_teardown(exc):
    """ Teardown flask app context """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

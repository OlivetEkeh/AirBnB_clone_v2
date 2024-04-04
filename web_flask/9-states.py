#!/usr/bin/python3
""" HBNB Flask Server """
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def lists_states():
    """ List all the states """
    states = sorted(list(storage.all(State).values()), key=lambda s: s.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def lists_states_by_id(id):
    """ List all the states based on the passed id """
    states = sorted(list(storage.all(State).values()), key=lambda s: s.name)
    state_dict = {state.id: state for state in states}
    state = state_dict.get(id)
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def app_teardown(exc):
    """ Teardown flask app context """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

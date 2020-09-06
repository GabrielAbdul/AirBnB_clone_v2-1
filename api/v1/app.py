#!/usr/bin/python3
'''app that starts a flask application'''

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def app_teardown(self):
    '''teardown_method'''
    storage.close()


@app.errorhandler(404)
def app_errorhandle(self):
    '''returns json formmated 404 status'''
    error = {'error': 'Not found'}
    return jsonify(error), 404


if __name__ == '__main__':
    app.run(threaded=True, debug=True)

#!/usr/bin/python3
'''app that starts a flask application'''

from flask import Flask
from models import storage
from api.v1.views import app_views


@app.teardown_appcontext
def teardown_method(self):
    '''teardown_method'''
    storage.close()

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(threaded=True)

import os

from flask import Flask
from flask_cors import CORS



app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_mapping(
    SECRET_KEY='dev',
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/test')
def test():
    return 'test'

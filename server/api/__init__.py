from flask import Flask, jsonify
from flask_cors import CORS
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '84593adec70d3ce156f9eb968a60bebf'

CORS(app)

from api import routes

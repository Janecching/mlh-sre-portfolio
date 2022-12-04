import os
from flask import Flask
from dotenv import load_dotenv
from peewee import *
from .views.myviews import my_view

load_dotenv()
app = Flask(__name__)
app.register_blueprint(my_view)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


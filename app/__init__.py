from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rootuser:abc12345@localhost/rmoney_api_database'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['DEBUG'] = True

db = SQLAlchemy(app)

manager = Manager(app)


from enum import Enum
from app import views
from app import models
from app import get_data
from app import bhav_scrapper
from app import scripts

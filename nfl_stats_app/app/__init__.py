import json
import os
import socket
import string

from flask import Flask, jsonify

from models import db
from api import api_blueprint
from teams.views import teams_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(teams_blueprint, url_prefix='/teams')

if os.environ.get('DATABASE_URL') is None:

  # linkedin laptop
  if socket.gethostname() == 'jizhang-mn2':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/nfl_stats'

  # personal laptop
  elif socket.gethostname() == 'j':  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/nfl_stats'
else:
  # heroku configs
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

def setup_db():
  db.init_app(app)
  db.app = app
  db.create_all()

setup_db()

def normalize_team_name(team_name):
  """
  Converts a team_name from a URL into one that is standardized by the database.
  """
  normal_names = map(string.capitalize, team_name.split('-'))
  return ' '.join(normal_names)

import json
import os
import socket
import string

from flask import Flask, jsonify

from models import db, RushingStat, Team
from api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api')

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

@app.route('/teams/<team_name>')
def render_team_page(team_name):
  """
  For the team given by team_name, renders a top level D3 view containing the total
  passing, rushing, and receiving stats for that team.
  """
  team = normalize_team_name(team_name)
  try:
    team_id = Team.get_or_add_team(team)
  except ValueError as e:
    print e
    #TODO return index page showing all teams
    return 'Index'
 
  rushing_stats = RushingStat.get_rushing_stats_by_team(team_id)
  
  out = []
  for stat in rushing_stats: 
    json_out = stat[0].to_json()
    json_out['player_name'] = stat[1]
    out.append(json_out)
  return json.dumps(out)

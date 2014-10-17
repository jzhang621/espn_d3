import json
import string

from flask import Blueprint

from nfl_stats_app.app.models import ReceivingStat, RushingStat, PassingStat, Team 

teams_blueprint = Blueprint('teams', __name__, template_folder='templates')

def normalize_team_name(team_name):
  """
  Converts a team_name from a URL into one that is standardized by the database.
  """
  normal_names = map(string.capitalize, team_name.split('-'))
  return ' '.join(normal_names)

@teams_blueprint.route('/<team_name>/<stat_type>')
def render_team_page(team_name, stat_type):
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
 
  if stat_type == 'rushing': 
    stats = RushingStat.get_rushing_stats_by_team(team_id)
  elif stat_type == 'passing':
    stats = PassingStat.get_passing_stats_by_team(team_id)
  elif stat_type == 'receiving':
    stats = ReceivingStat.get_receiving_stats_by_team(team_id) 

  out = []
  for stat in stats: 
    json_out = stat[0].to_json()
    json_out['player_name'] = stat[1]
    out.append(json_out)
  return json.dumps(out)

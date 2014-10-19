import json

from flask import Blueprint, jsonify, request

from models import DefensiveStat, ReceivingStat, RushingStat, PassingStat, Player, Team, db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/add-team', methods=['POST', 'GET'])
def get_or_add_team():
  """

  """
  team_name = request.json['team_name']
  team_id = Team.get_or_add_team(team_name)

  return jsonify({'team_id': team_id})

@api_blueprint.route('/add-player-stats', methods=['POST'])
def add_player_stats():
  data = request.json['stats']
  player_name = data['player_name']
  team_name = data['team_name']
  stats_type = request.json['stat_type']

  team_id = Team.get_or_add_team(team_name)
  player_id = Player.get_or_add_player(player_name, team_id)
  data['player_id'] = player_id[0]

  if stats_type == 'Rushing':
    class_type = RushingStat   
  elif stats_type == 'Passing':
    class_type = PassingStat
  elif stats_type == 'Receiving':
    class_type = ReceivingStat
  elif stats_type == 'Defense':
    class_type = DefensiveStat

  class_type.add_stat(**data)
  return jsonify({'player_id': player_id})

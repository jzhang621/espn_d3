import json
import requests

SERVER = 'http://localhost:5000'

class Client():

  def __init__(self):
    self.base_url = SERVER

  def _post_request(self, route, parameters):
    """

    """
    full_route = '{0}/{1}'.format(SERVER, route)
    response = requests.post(full_route, data=json.dumps(parameters), headers={'Content-Type': 'application/json'})
    return response
 
  def get_or_create_team(self, team_name):
    route = 'api/addTeam'
    parameters = {'team_name': team_name}
    return self._post_request(route, parameters)

  def add_player_stats(self, stat_type, stats):
    route = 'api/addPlayerStats'
    parameters = {'stat_type': stat_type, 'stats': stats}
    return self._post_request(route, parameters)

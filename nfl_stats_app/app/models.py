from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
  __tablename__ = 'teams'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  wins = db.Column(db.Integer)
  losses = db.Column(db.Integer)

  def __init__(self, name, wins, losses):
    self.name = name
    self.wins = wins
    self.losses = losses

  @classmethod
  def get_or_add_team(cls, team_name):
    """
    Used by the stats scraper to register new teams to collect stats for.
    
    If the team already has been registered, this function returns the team_id
    """
    team_id = db.session.query(Team.id).filter(Team.name == team_name).first()
    if team_id:
      return int(team_id[0])
    else:
      new_team = Team(team_name, 0, 0)
      db.session.add(new_team)
      db.session.commit()
      return new_team.id

  @classmethod
  def get_team(cls, team_name):
    """
    Returns the team_id for the given team_name.

    If no such team exists, then throws a ValueError
    """
    team_id = db.session.query(Team.id).filter(Team.name == team_name).first()
    if team_id:
      return int(team_id[0])
    else:
      raise ValueError('No such team: %s', team_name)

class Player(db.Model):
  __tablename__ = 'players'
  id = db.Column(db.Integer, primary_key=True)
  team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)
  player_name = db.Column(db.String(50))
  
  def __init__(self, team_id, name):
    self.team_id = team_id
    self.player_name = name

  @classmethod
  def get_or_add_player(cls, player_name, team_id):
    player_key = db.session.query(Player.id, Player.team_id) \
                   .filter(Player.player_name == player_name) \
                   .filter(Player.team_id == team_id).first()
                   
    if player_key:
      return int(player_key[0]), int(player_key[1])
    else:
      new_player = Player(team_id, player_name)
      db.session.add(new_player)
      db.session.commit()
      return new_player.id, new_player.team_id

class RushingStat(db.Model):
  __tablename__ = 'rushing_stats'
  player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
  attempts = db.Column(db.Integer)
  yards = db.Column(db.Integer)
  touchdowns = db.Column(db.Integer)
  first_downs = db.Column(db.Integer)

  def __init__(self, player_id, attempts, yards, touchdowns, first_downs):
    self.player_id = player_id
    self.attempts = attempts
    self.yards = yards
    self.touchdowns = touchdowns
    self.first_downs = first_downs

  @classmethod
  def add_stat(cls, **kwargs):
    player_id = kwargs['player_id']
    attempts = int(kwargs['Att'])
    yards = int(kwargs['Yds'])
    touchdowns = int(kwargs['TD'])
    first_downs = int(kwargs['FD'])

    rushing_stat = RushingStat(player_id, attempts, yards, touchdowns, first_downs) 
    db.session.add(rushing_stat)
    db.session.commit()

  @classmethod
  def get_rushing_stats_by_team(cls, team_id):
    """
    Returns all the RushingStat 
    """
    team_rushing_stats = db.session.query(RushingStat, Player.player_name) \
                                   .filter(RushingStat.player_id == Player.id) \
                                   .filter(Team.id == team_id) \
                                   .filter(Player.team_id == Team.id)
    return team_rushing_stats

  def to_json(self):
    """
    Returns basic json output of a RushingStat
    """
    return {
      'attempts': self.attempts,
      'yards': self.yards,
      'touchdowns': self.touchdowns,
      'first_downs': self.first_downs
    }


class PassingStat(db.Model):
  __tablename__ = 'passing_stats'
  player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
  attempts = db.Column(db.Integer)
  completions = db.Column(db.Integer)
  yards = db.Column(db.Integer)
  touchdowns = db.Column(db.Integer)
  interceptions = db.Column(db.Integer)
  sacks = db.Column(db.Integer)

  def __init__(self, player_id, attempts, completions, yards, touchdowns, interceptions, sacks):
    self.player_id = player_id
    self.attempts = attempts
    self.completions = completions
    self.yards = yards
    self.touchdowns = touchdowns
    self.interceptions = interceptions
    self.sacks = sacks

  @classmethod
  def add_stat(cls, **kwargs):
    player_id = kwargs['player_id']
    attempts = int(kwargs['Att'])
    completions = int(kwargs['Cmp'])
    yards = int(kwargs['Yds'])
    touchdowns = int(kwargs['TD'])
    interceptions = int(kwargs['Int'])
    sacks = int(kwargs['Sack'])

    passing_stat = PassingStat(player_id, attempts, completions, yards, touchdowns, interceptions, sacks)
    db.session.add(passing_stat)
    db.session.commit()

  @classmethod
  def get_passing_stats_by_team(cls, team_id):
    """
    Returns all the RushingStat 
    """
    team_passing_stats = db.session.query(PassingStat, Player.player_name) \
                                   .filter(PassingStat.player_id == Player.id) \
                                   .filter(Team.id == team_id) \
                                   .filter(Player.team_id == Team.id)
    return team_passing_stats

  def to_json(self):
    """
    Returns basic json output of a RushingStat
    """
    return {
      'attempts': self.attempts,
      'completions': self.completions,
      'yards': self.yards,
      'touchdowns': self.touchdowns,
      'interceptions': self.interceptions,
      'sacks': self.sacks
    }

 
class ReceivingStat(db.Model):
  __tablename__ = 'receiving_stats'
  player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
  receptions = db.Column(db.Integer)
  yards = db.Column(db.Integer)
  touchdowns = db.Column(db.Integer)
  first_downs = db.Column(db.Integer)
  targets = db.Column(db.Integer)
  yac = db.Column(db.Integer)

  def __init__(self, player_id, receptions, yards, touchdowns, first_downs, targets, yac):
    self.player_id = player_id
    self.receptions = receptions
    self.yards = yards
    self.touchdowns = touchdowns
    self.first_downs = first_downs
    self.targets = targets
    self.yac = yac

  @classmethod
  def add_stat(cls, **kwargs):
    player_id = kwargs['player_id']
    receptions = int(kwargs['Rec'])
    yards = int(kwargs['Yds'])
    touchdowns = int(kwargs['TD'])
    first_downs = int(kwargs['FD'])
    yac = int(kwargs['YAC'])
    targets = int(kwargs['Tar'])

    receiving_stat = ReceivingStat(player_id, receptions, yards, touchdowns, first_downs, targets, yac)
    db.session.add(receiving_stat)
    db.session.commit()

  @classmethod
  def get_receiving_stats_by_team(cls, team_id):
    """
    Returns all the RushingStat 
    """
    team_receiving_stats = db.session.query(ReceivingStat, Player.player_name) \
                                   .filter(ReceivingStat.player_id == Player.id) \
                                   .filter(Team.id == team_id) \
                                   .filter(Player.team_id == Team.id)
    return team_receiving_stats

  def to_json(self):
    """
    Returns basic json output of a RushingStat
    """
    return {
      'receptions': self.receptions,
      'yards': self.yards,
      'touchdowns': self.touchdowns,
      'first_downs': self.first_downs,
      'yac': self.yac,
      'targets': self.targets
    }


class DefensiveStat(db.Model):
  __tablename__ = 'defensive_stats'
  player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
  tackles = db.Column(db.Integer)
  interceptions = db.Column(db.Integer)
  sacks = db.Column(db.Float)
  touchdowns = db.Column(db.Integer)

  def __init__(self, player_id, tackles, interceptions, sacks, touchdowns):
    self.player_id = player_id
    self.tackles = tackles
    self.interceptions = interceptions
    self.sacks = sacks
    self.touchdowns = touchdowns

  @classmethod
  def add_stat(cls, **kwargs):
    player_id = kwargs['player_id']
    tackles = int(kwargs['Tot'])
    interceptions = int(kwargs['Int'])
    sacks = int(kwargs['Sack'])
    touchdowns = int(kwargs['TD'])

    defensive_stat = DefensiveStat(player_id, tackles, interceptions, sacks, touchdowns)
    db.session.add(defensive_stat)
    db.session.commit()

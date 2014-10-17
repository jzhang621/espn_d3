import os
import socket

from flask import Flask

from models import db
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

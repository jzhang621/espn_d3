import os

from flask import Flask

from models import db
from api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api')

if os.environ.get('DATABASE_URL') is None:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/nfl_stats'
else:
  # heroku configs
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

def setup_db():
  db.init_app(app)
  db.app = app
  db.create_all()

setup_db()

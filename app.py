from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask import render_template
from decouple import config as config_decouple

from models.teams import TeamsModel
from models.match import MatchesModel
from models.competitions import CompetitionsModel
from models.accounts import AccountsModel

############################
# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db3.html
############################
from db import db
from resources.competition import competition
from resources.competitionsList import competitionsList
from resources.match import match
from resources.matchesList import matchesList
from resources.team import team
from resources.teamsList import teamsList
from resources.order import order
from resources.ordersList import orderList
from resources.account import account
from resources.accountsList import accountsList
from resources.login import login

from datetime import datetime
import os
from config import config

app = Flask(__name__)



environment = config['development']
if config_decouple('PRODUCTION', cast=bool ,default=False):
    environment = config['production']

app.config.from_object(environment)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def render_vue():
    return render_template("index.html")

migrate = Migrate(app, db)
db.init_app(app)

api.add_resource(team, '/team/<int:id>', '/team')
api.add_resource(teamsList, '/teams')
api.add_resource(competitionsList, '/competitions')
api.add_resource(matchesList, '/matches')
api.add_resource(competition, '/competition/<int:id>')
api.add_resource(match, '/match/<int:id>')
api.add_resource(order, '/order/<string:username>')
#api.add_resource(orderList, '/orders')
api.add_resource(orderList, '/orders/<string:username>')
api.add_resource(account, '/account/<string:username>', '/account')
api.add_resource(accountsList, '/accounts')
api.add_resource(login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

"""



# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask
from data import teams, competitions, matches

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/python')
def like_python():
    return 'I like Python!'


@app.route('/teams', methods=['GET'])
def get_teams():
    return {'teams': teams}


@app.route('/matches', methods=['GET'])
def get_matches():
    return {'matches': matches}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=5000, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""

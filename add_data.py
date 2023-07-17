from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.teams import TeamsModel
from models.match import MatchesModel
from models.competitions import CompetitionsModel
from models.competitions import teams_in_competitions

import data
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jhzethcohzdmhj:d96ed945d61cc3b9f76006357560c15b3cf64cac98097a347c0ee07b49399a2c@ec2-34-230-153-41.compute-1.amazonaws.com:5432/d6024rs8j7fv5v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

teams = []
matches = []
competitions = []

for team in data.teams:
    teamModel = TeamsModel(name=team["name"], country=team["country"])
    teams.append(teamModel)

for competition in data.competitions:
    competitionModel = CompetitionsModel(name=competition["name"], category=competition["category"],
                                         sport=competition["sport"])
    competitions.append(competitionModel)

for match in data.matches:
    local = random.choice(teams)
    visitor = random.choice(teams)

    while visitor.name != local.name:
        visitor = random.choice(teams)

    random_comp = random.choice(competitions)

    matchModel = MatchesModel(date=datetime.strptime(match["date"], "%Y-%m-%d"), price=match["price"], local=local,
                              visitor=visitor, competition=random_comp, total_available_tickets=2)
    matches.append(matchModel)

db.session.add_all(teams)
db.session.add_all(competitions)
db.session.add_all(matches)

db.session.commit()

# end

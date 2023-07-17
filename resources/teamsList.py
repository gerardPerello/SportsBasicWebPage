from flask_restful import Resource, reqparse  # add reqparse to imports
from models import teams


class teamsList(Resource):
    def get(self):
        teams_list = teams.TeamsModel.query.all()
        if len(teams_list) > 0:
            teams_json = []
            for team in teams_list:
                teams_json.append(team.json())
            return {'teams': teams_json}, 200
        else:
            return {'message': "Not teams founded"}, 404


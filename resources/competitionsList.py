from flask_restful import Resource, reqparse  # add reqparse to imports
from models import competitions


class competitionsList(Resource):
    def get(self):
        competitions_list = competitions.CompetitionsModel.query.all()
        if len(competitions_list) > 0:
            competitions_json = []
            for comp in competitions_list:
                competitions_json.append(comp.json())
            return {'competitions': competitions_json}, 200
        else:
            return {'message': "Not competitions founded"}, 404

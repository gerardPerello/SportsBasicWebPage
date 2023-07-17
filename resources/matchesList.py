from flask_restful import Resource, reqparse  # add reqparse to imports
from models import match


class matchesList(Resource):
    def get(self):
        matches_list = match.MatchesModel.query.all()
        if len(matches_list) > 0:
            matches_json = []
            for m in matches_list:
                matches_json.append(m.json())
            return {'matches': matches_json}, 200
        else:
            return {'message': "Not matches founded"}, 404


from datetime import datetime

from flask_restful import Resource, reqparse  # add reqparse to imports
import models


class match(Resource):

    def get(self, id):

        selected_match = models.match.MatchesModel.get_by_id(id)
        if selected_match:
            return {'team': selected_match.json()}, 200
        else:
            return {'message': "Match with id [{}] does not exists".format(id)}, 404

    def post(self, id=None):

        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        if data["local"] is not None and data["visitor"] is not None and data["competition"] is not None:
            match_by_team = models.match.MatchesModel.get_by_team(data["local"], data["visitor"], data["competition"], datetime.strptime(data["date"], "%Y-%m-%d"))
            if match_by_team is not None and match_by_team.date == datetime.strptime(data["date"], "%Y-%m-%d"):
                return {'message': "Match with teams [{}] and [{}] and competition [{}] already exists".format(match_by_team.local.name, match_by_team.visitor.name, match_by_team.competition.name)}, 404
        if id is None:
            selected_match = None
        else:
            selected_match = models.match.MatchesModel.get_by_id(id)

        if selected_match is None:
            self.addMatch(data)
            return {'message': "Match with id [{}] has been created".format(id)}, 200
        else:
            return {'message': "Match with id [{}] already exists".format(id)}, 404

    def delete(self, id):

        selected_match = models.match.MatchesModel.get_by_id(id)
        if selected_match is not None:
            selected_match.delete_from_db()
            return {'message': "Match with id [{}] have been deleted".format(id)}, 200
        else:
            return {'message': "Match with id [{}] does not exists".format(id)}, 404

    def put(self, id):

        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        if data["local"] is not None and data["visitor"] is not None and data["competition"] is not None:
            match_by_team = models.match.MatchesModel.get_by_team(data["local"], data["visitor"], data["competition"], datetime.strptime(data["date"], "%Y-%m-%d"))
            if match_by_team is not None and match_by_team.date == datetime.strptime(data["date"], "%Y-%m-%d"):
                return {'message': "Match with teams [{}] and [{}] and competition [{}] already exists".format(match_by_team.local.name, match_by_team.visitor.name, match_by_team.competition.name)}, 404 

        selected_match = models.match.MatchesModel.get_by_id(id)
        if selected_match is None:
            self.addMatch(data)
            return {'message': "Match with id [{}] have been created".format(id)}, 200
        else:
            selected_match.delete_from_db()
            self.addMatch(data)
            return {'message': "Competition with id [{}] have been modified".format(id)}, 200

    def addMatch(self, match_params):
        # define all input parameters need and its type
        local = models.teams.TeamsModel.get_by_id(match_params["local"])
        visitor = models.teams.TeamsModel.get_by_id(match_params["visitor"])
        competition = models.competitions.CompetitionsModel.get_by_id(match_params["competition"])
        data = models.match.MatchesModel(date=datetime.strptime(match_params["date"], "%Y-%m-%d"),
                                         price=match_params["price"], local=local, visitor=visitor,
                                         competition=competition, total_available_tickets=match_params["total_available_tickets"])
        data.save_to_db()

    def extract_param(self, parser):
        parser.add_argument('local', type=int)
        parser.add_argument('visitor', type=int)
        parser.add_argument('competition', type=int)
        parser.add_argument('date', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('total_available_tickets', type=int)
        data = parser.parse_args()
        return data

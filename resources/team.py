from flask_restful import Resource, reqparse  # add reqparse to imports
from models import teams


class team(Resource):

    def get(self, id):
        selected_team = teams.TeamsModel.get_by_id(id)
        if selected_team:
            return {'team': selected_team.json()}, 200
        else:
            return {'message': "Team with id [{}] dues not exists".format(id)}, 404

    def post(self, id=None):

        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        team_by_name = teams.TeamsModel.get_by_name(data["name"])
        if team_by_name is not None:
            return {'message': "Team with name [{}] already exists".format(data["name"])}, 404
        if id is None:
            selected_team = None
        else:
            selected_team = teams.TeamsModel.get_by_id(id)

        if selected_team is None:
            self.addTeam(parser)
            return {'message': "Team with id [{}] have been created".format(id)}, 200
        else:
            return {'message': "Team with id [{}] already exists".format(id)}, 404


    def delete(self, id):
        selected_team = teams.TeamsModel.get_by_id(id)
        if selected_team is not None:
            selected_team.delete_from_db()
            return {'message': "Team with id [{}] have been deleted".format(id)}, 200
        else:
            return {'message': "Team with id [{}] does not exists".format(id)}, 404

    def put(self, id):
        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        team_by_name = teams.TeamsModel.get_by_name(data["name"])
        if team_by_name is not None and team_by_name.id != id:
            return {'message': "Team with name [{}] already exists".format(data["name"])}, 404

        selected_team = teams.TeamsModel.get_by_id(id)

        if selected_team is None:
            parser = reqparse.RequestParser()  # create parameters parser from request
            self.addCompetition(parser)
            return {'message': "Team with id [{}] have been created".format(id)}, 200

        else:
            parser = reqparse.RequestParser()  # create parameters parser from request
            team = self.extract_param(parser)
            data = teams.TeamsModel(name=team["name"], country=team["country"])
            selected_team.delete_from_db()
            data.save_to_db()
            return {'message': "Team with id [{}] have been modified".format(id)}, 200

    def addTeam(self, parser):
        # define all input parameters need and its type
        team = self.extract_param(parser)
        data = teams.TeamsModel(name=team["name"], country=team["country"])
        data.save_to_db()

    def extract_param(self, parser):
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        return data

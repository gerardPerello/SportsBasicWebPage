from flask_restful import Resource, reqparse  # add reqparse to imports
from models import competitions


class competition(Resource):

    def get(self, id):

        selected_competition = competitions.CompetitionsModel.get_by_id(id)
        if selected_competition:
            return {'competition': selected_competition.json()}, 200
        else:
            return {'message': "Match with id [{}] dues not exists".format(id)}, 404

    def post(self, id=None):

        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        competition_by_name = competitions.CompetitionsModel.get_by_name(data["name"], data["category"], data["sport"])
        if competition_by_name is not None:
            return {'message': "Competition with name [{}] already exists".format(data["name"])}, 404
        if id is None:
            selected_competition = None
        else:
            selected_competition = competitions.CompetitionsModel.get_by_id(id)

        if selected_competition is None:
            self.addCompetition(parser)
            return {'message': "Competition with id [{}] have been created".format(id)}, 200
        else:
            return {'message': "Competition with id [{}] already exists".format(id)}, 404

    def delete(self, id):
        selected_competition = competitions.CompetitionsModel.get_by_id(id)
        if selected_competition is not None:
            selected_competition.delete_from_db()
            return {'message': "Competition with id [{}] have been deleted".format(id)}, 200
        else:
            return {'message': "Competition with id [{}] does not exists".format(id)}, 404

    def put(self, id):
        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        competition_by_name = competitions.CompetitionsModel.get_by_name(data["name"], data["category"], data["sport"])
        if competition_by_name is not None and competition_by_name.id != id:
            return {'message': "Competition with name [{}] already exists".format(data["name"])}, 404

        selected_competition = competitions.CompetitionsModel.get_by_id(id)

        if selected_competition is None:
            parser = reqparse.RequestParser()  # create parameters parser from request
            self.addCompetition(parser)
            return {'message': "Competition with id [{}] have been created".format(id)}, 200

        else:
            parser = reqparse.RequestParser()  # create parameters parser from request
            competition = self.extract_param(parser)
            data = competitions.CompetitionsModel(name=competition["name"], category=competition["category"],
                                                  sport=competition["sport"])
            selected_competition.delete_from_db()
            data.save_to_db()
            return {'message': "Competition with id [{}] have been modified".format(id)}, 200

    def addCompetition(self, parser):
        # define all input parameters need and its type
        competition = self.extract_param(parser)
        data = competitions.CompetitionsModel(name=competition["name"], category=competition["category"],
                                              sport=competition["sport"])
        data.save_to_db()

    def extract_param(self, parser):
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('category', type=str, choices=competitions.categories_list)
        parser.add_argument('sport', type=str, choices=competitions.sports_list)
        parser.add_argument('teams', type=list)
        data = parser.parse_args()
        return data
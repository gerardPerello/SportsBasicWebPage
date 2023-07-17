import jwt
from flask_restful import Resource, reqparse  # add reqparse to imports
from passlib.hash import pbkdf2_sha256
import models.accounts
from flask import g, current_app

class login(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        username = data["username"]
        password = data["password"]

        selected_account = models.accounts.AccountsModel.get_by_username(username)
        if selected_account:
            if selected_account.verify_password(password):
                token = selected_account.generate_auth_token()
                return {'token': token}, 200
            else:
                return {'message': "This combination of username and password does not exist in our database"}, 400
        else:
            return {'message': "Account with username [{}] dues not exists".format(username)}, 404

    def extract_param(self, parser):
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        return data
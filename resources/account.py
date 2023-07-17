from flask_restful import Resource, reqparse
from sqlalchemy import false, null  # add reqparse to imports

import models.accounts
from passlib.hash import pbkdf2_sha256

class account(Resource):

    def get(self, username):
        selected_account = models.accounts.AccountsModel.get_by_username(username)
        if selected_account:
            return {'account': selected_account.json()}, 200
        else:
            return {'message': "Account with username [{}] dues not exists".format(username)}, 404

    def post(self):
        parser = reqparse.RequestParser()  # create parameters parser from request
        data = self.extract_param(parser)
        
        selected_account = models.accounts.AccountsModel.get_by_username(data["username"])
        if selected_account:
            return {'message': "Username [{}] already exists".format(data["username"])}, 404

        self.addAccount(data)
        actual_account = models.accounts.AccountsModel.get_by_username(data["username"])
        
        actual_account.hash_password(data["password"])

        return {'message': "Account with username [{}] have been created".format(data["username"])}, 200

    def delete(self, username):
        selected_account = models.accounts.AccountsModel.get_by_username(username)
        if selected_account is not None:
            selected_account.delete_from_db()
            return {'message': "Competition with username [{}] have been deleted".format(username)}, 200
        else:
            return {'message': "Competition with username [{}] does not exists".format(username)}, 404

    def addAccount(self, account_info):
        # define all input parameters need and its type
        data = models.accounts.AccountsModel(username=account_info["username"],
                                             is_admin=account_info["is_admin"])

        data.save_to_db()

    def extract_param(self, parser):
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('is_admin', type=int)
        data = parser.parse_args()
        return data
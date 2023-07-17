from flask_restful import Resource, reqparse  # add reqparse to imports
from models import accounts


class accountsList(Resource):
    def get(self):
        accounts_list = accounts.AccountsModel.query.all()
        if len(accounts_list) > 0:
            accounts_json = []
            for account in accounts_list:
                accounts_json.append(account.json())
            return {'accounts': accounts_json}, 200
        else:
            return {'message': "Not competitions founded"}, 404

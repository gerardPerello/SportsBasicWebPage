from datetime import datetime

from flask_restful import Resource, reqparse  # add reqparse to imports
from flask import g
import models
from models.accounts import auth, token_auth
from lock import lock


class order(Resource):

    def get(self, username):

        selected_orders = models.accounts.OrdersModel.get_by_username(username)
        if len(selected_orders) > 0:
            orders_json = []
            for m in selected_orders:
                orders_json.append(m.json())
            return {'orders': orders_json}, 200
        else:
            return {'message': "There are not orders for username [{}].".format(id)}, 404

    @auth.login_required(role='user')
    def post(self, username):
        if username is not None:
            if g.user.username != username:
                return {'message': "Username [{}] does not have an open session".format(username)}, 400
            selected_account = models.accounts.AccountsModel.get_by_username(username)
            if selected_account is None:
                return {'message': "Username [{}] does not exists".format(username)}, 404

            parser = reqparse.RequestParser()  # create parameters parser from request
            data = self.extract_param(parser)
            with lock.lock:
                if data["match_id"] is None or data["tickets_bought"] is None:
                    return {'message': "This field can't left in black"}, 404

                match_selected = models.match.MatchesModel.get_by_id(data["match_id"])

                if match_selected is None:
                    return {'message': "Match with id [{}] does not exists".format(data["match_id"])}, 404

                price_match = match_selected.price
                available_account_money = selected_account.available_money

                if price_match > available_account_money:
                    return {'message': "You have not enought money to buy the ticket for this match"}, 404

                available_tickets_match = match_selected.total_available_tickets

                if available_tickets_match < data["tickets_bought"]:
                    return {'message': "There are not [{}] tickets in stock".format(data["tickets_bought"])}, 404

                match_selected.buy_tickets(data["tickets_bought"])
                selected_account.available_money -= match_selected.price * data["tickets_bought"]
                new_order = models.accounts.OrdersModel(match_id=data["match_id"],
                                                        tickets_bought=data["tickets_bought"])
                selected_account.orders.append(new_order)

                new_order.save_to_db(selected_account,match_selected)

                return new_order.json(),200

    def extract_param(self, parser):
        parser.add_argument('match_id', type=int, required=True)
        parser.add_argument('tickets_bought', type=int, required=True)
        data = parser.parse_args()
        return data

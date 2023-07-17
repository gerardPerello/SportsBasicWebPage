import jwt
from sqlalchemy import and_

from db import db
import time
#import dateutil.parser
from passlib.apps import custom_app_context as pwd_context
from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import g, current_app

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    username = db.Column(db.String(30), primary_key=True)
    hash_pass = db.Column(db.String(200))
    # 0 not admin/ 1 is admin
    is_admin = db.Column(db.Integer, nullable=False)
    available_money = db.Column(db.Integer)
    orders = db.relationship("OrdersModel", back_populates="account", uselist=True)

    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin

    def json(self):
        return {'username': self.username, 'is_admin': self.is_admin,
                'available_money': self.available_money, 'hash':self.hash_pass}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(self, username):
        return db.session.query(AccountsModel).get(username)

    def hash_password(self, password):
        
        self.hash_pass = str(pwd_context.hash(password))
        #self.hash_pass = password
        db.session.commit()

    def verify_password(self, password):
        return pwd_context.verify(password, self.hash_pass)

    def generate_auth_token(self, expiration=600):
        return encode(
            {"username": self.username, "exp": int(time.time()) + expiration},
            current_app.secret_key,
            algorithm="HS256"
        )

    @classmethod
    def verify_auth_token(cls, token):
        try:
            data = decode(token, current_app.secret_key, algorithms=["HS256"])
        except ExpiredSignatureError:
            return None  # expired token
        except InvalidSignatureError:
            return None  # invalid token

        user = cls.query.filter_by(username=data['username']).first()

        return user

@token_auth.verify_token
def verify_token(token):
    user = AccountsModel.verify_auth_token(token)
    if user:
        return user
    else:
        return False

@auth.verify_password
def verify_password(token, password):

    decoded_token = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])

    user = AccountsModel.get_by_username(decoded_token['username'])
    if user:
        g.user = user
        return user
    else:
        return False

@auth.get_user_roles
def get_user_roles(user):
    if user.is_admin:
        return "admin"
    else:
        return "user"

class OrdersModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('accounts.username'))
    match_id = db.Column(db.Integer, nullable=False)
    tickets_bought = db.Column(db.Integer, nullable=False)

    account = db.relationship("AccountsModel", back_populates='orders')

    def __init__(self, match_id, tickets_bought):
        self.match_id = match_id
        self.tickets_bought = tickets_bought

    def json(self):
        return {'id': self.id, 'username': self.username, 'match_id': self.match_id,
                'tickets_bought': self.tickets_bought}

    def save_to_db(self, account, match):
        db.session.add(self)
        db.session.add(match)
        db.session.add(account)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(self, username):
        return db.session.query(OrdersModel).filter_by(username=username).all()

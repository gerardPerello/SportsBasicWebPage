
from passlib.apps import custom_app_context as pwd_context

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lwvmbyftfknsrj:e6d47aecb3ce18bedeb2e88079cc55d936e490e8a3ee942b11fb6418d16cc30e@ec2-34-231-221-151.compute-1.amazonaws.com:5432/daruinjc5e24bh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


from models.accounts import AccountsModel
new_account = AccountsModel(username='admin', is_admin=1)
new_account.hash_pass = pwd_context.encrypt('admin')
db.session.add(new_account)
db.session.commit()


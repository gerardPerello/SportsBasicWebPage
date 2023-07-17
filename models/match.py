from sqlalchemy import and_

from db import db
from datetime import datetime

class MatchesModel(db.Model):
    __tablename__ = 'matches'
    # Serveix per a que no hi hagi dos iguals amb aquests arguments.
    __table_args__ = (db.UniqueConstraint('local_id', 'visitor_id', 'competition_id', 'date'),)

    # Es defineix per defecte com UNIQUE per ser primary key.
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_available_tickets = db.Column(db.Integer, default=0)

    local_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    local = db.relationship("TeamsModel", foreign_keys=[local_id])
    visitor = db.relationship("TeamsModel", foreign_keys=[visitor_id])

    competition_id = db.Column(db.Integer, db.ForeignKey("competitions.id"))
    competition = db.relationship("CompetitionsModel", back_populates="matches")

    def __init__(self, date, price, local, visitor, competition, total_available_tickets):
        self.date = date
        self.price = price
        self.local = local
        self.visitor = visitor
        self.competition = competition
        self.total_available_tickets = total_available_tickets

    def json(self):
        return {'id': self.id, 'date': self.date.isoformat(), 'price': self.price, 'local': self.local.json(),
                'visitor': self.visitor.json(), 'competition': self.competition.name,
                'competition_id': self.competition_id, 'total_available_tickets': self.total_available_tickets}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def buy_tickets(self, n_tickets):
        self.total_available_tickets -= n_tickets

    @classmethod
    def get_by_id(self, id):
        return db.session.query(MatchesModel).get(id)

    @classmethod
    def get_by_date_and_prize(self, team):
        return MatchesModel.query.filter_by(and_(local=team, visitor=team)).first()

    @classmethod
    def get_by_team(self, local, visitor, competition, date):
        return MatchesModel.query.filter(MatchesModel.local_id == local,
                                         MatchesModel.visitor_id == visitor,
                                         MatchesModel.competition_id == competition,
                                         MatchesModel.date == date).first()

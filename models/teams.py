from db import db
from models.competitions import teams_in_competitions


class TeamsModel(db.Model):
    __tablename__ = 'teams'

    # Es defineix per defecte com UNIQUE per ser primary key.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    competitions = db.relationship("CompetitionsModel", secondary=teams_in_competitions, back_populates="teams")

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def json(self):
        return {'id': self.id, 'name': self.name, 'country': self.country,
                'competitions': [competition.name for competition in self.competitions]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return db.session.query.all()

    @classmethod
    def get_by_id(self, id):
        return db.session.query(TeamsModel).get(id)
        # return TeamsModel.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(self, name):
        return TeamsModel.query.filter_by(name=name).first()

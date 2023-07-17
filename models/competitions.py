from db import db

categories_list = ("Senior", "Junior", "Mini", "Infantile", "Iniciacio")
sports_list = ("Volleyball", "Football", "Basketball", "Futsal", "Baseball")

teams_in_competitions = db.Table("teams_in_competitions",
                                 db.Column("id", db.Integer, primary_key=True),
                                 db.Column("team_id", db.Integer, db.ForeignKey("teams.id")),
                                 db.Column("competition_id", db.Integer, db.ForeignKey("competitions.id")))


class CompetitionsModel(db.Model):
    __tablename__ = 'competitions'
    __table_args__ = (db.UniqueConstraint('name', 'category', 'sport'),)

    # Es defineix per defecte com UNIQUE per ser primary key.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    category = db.Column(db.Enum(*categories_list, name='categories_types'), nullable=False)
    sport = db.Column(db.Enum(*sports_list, name='sports_types'), nullable=False)

    teams = db.relationship("TeamsModel", secondary=teams_in_competitions, back_populates="competitions")
    matches = db.relationship("MatchesModel", back_populates="competition", uselist=True)

    def __init__(self, name, category, sport):
        self.name = name
        self.category = category
        self.sport = sport

    def json(self):
        return {'id': self.id, 'name': self.name, 'category': self.category, 'sport': self.sport,
                'teams': [teams.json() for teams in self.teams], 'matches': [match.json() for match in self.matches]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return CompetitionsModel.query.filter_by().all()

    @classmethod
    def get_by_id(self, id):
        return CompetitionsModel.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(self, name, category, sport):
        return CompetitionsModel.query.filter(CompetitionsModel.name == name,
                                              CompetitionsModel.category == category,
                                              CompetitionsModel.sport == sport).first()

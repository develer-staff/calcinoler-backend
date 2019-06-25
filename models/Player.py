from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(30), unique=True, nullable=False)
    nDisonors = db.Column('n_disonors', db.Integer, nullable=False, default=0)


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

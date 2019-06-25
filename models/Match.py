from datetime import datetime
from marshmallow import fields
from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.utcnow)

    sport_id = db.Column(db.Integer,
                         db.ForeignKey('sports.id'),
                         nullable=False)


class MatchSchema(ma.ModelSchema):
    class Meta:
        include_fk = True
        model = Match

    sport_id = fields.Integer(dump_only=True, required=True)


players = db.Table(
    'match_players',
    db.Column('match_id',
              db.Integer,
              db.ForeignKey('matches.id'),
              primary_key=True),
    db.Column('player_id',
              db.Integer,
              db.ForeignKey('players.id'),
              primary_key=True),
)

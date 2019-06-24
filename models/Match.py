from datetime import datetime
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    person_id = db.Column(db.Integer, db.ForeignKey('sports.id'),nullable=False)


class MatchSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    nickname = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


players = db.Table('match_players',
    db.Column('match_id', db.Integer, db.ForeignKey('matches.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.UniqueConstraint('match_id', 'player_id', name='unique_player_in_match')
)
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Sport(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    matches = db.relationship('Match', backref='sport', lazy=True)



class SportSchema(ma.ModelSchema):
    class Meta:
        model = Sport
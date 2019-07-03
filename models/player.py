from marshmallow import fields, validate
from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    slack_id = db.Column(db.String, nullable=False, unique=True)
    dishonors = db.Column(db.Integer,
                          nullable=False,
                          default=0,
                          server_default="0")
    nickname = None
    name = None

    def merge_slack_user(self, slack_user: dict):
        self.nickname = slack_user.get('real_name', "")
        self.name = slack_user.get('display_name', "")


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

    nickname = fields.String(required=True,
                             validate=validate.Length(1),
                             dump_only=True)
    name = fields.String(required=True,
                         validate=validate.Length(1),
                         dump_only=True)

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

    def __init__(self, **kwargs):
        if kwargs.get("dishonors", None) is None:
            kwargs['dishonors'] = self.__table__.c.dishonors.default.arg
        super(Player, self).__init__(**kwargs)

    def merge_slack_user(self, slack_user: dict):
        if self.slack_id is None:
            self.slack_id = slack_user.get('id', "")

        self.nickname = slack_user.get('real_name', "")

        if "display_name" in slack_user:
            self.name = slack_user['display_name']
        elif "display_name" in slack_user.get('profile', {}):
            self.name = slack_user['profile']['display_name']
        else:
            self.name = self.nickname


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

    nickname = fields.String(required=True,
                             validate=validate.Length(1),
                             dump_only=True)
    name = fields.String(required=True,
                         validate=validate.Length(1),
                         dump_only=True)

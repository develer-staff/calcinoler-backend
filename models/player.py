from marshmallow import fields, validate
from flask_marshmallow import Marshmallow

from database import db

ma = Marshmallow()


class Player(db.Model):
    __tablename__ = 'players'
    slack_id = db.Column(db.String, nullable=False, primary_key=True)
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
        """Populates Player instance's name and nickname fields

            slack_user (dict):
                representing Slack user
        """
        if not self.slack_id:
            self.slack_id = slack_user['id']

        self.nickname = slack_user.get('real_name', "")

        if "display_name" in slack_user['profile']:
            self.name = slack_user['profile']['display_name']
        else:
            self.name = self.nickname


class PlayerSchema(ma.ModelSchema):

    slack_id = fields.String(required=True,
                             validate=validate.Length(1),
                             dump_only=True)
    dishonors = fields.Integer(required=True, validate=validate.Range(min=0))
    nickname = fields.String(required=True,
                             validate=validate.Length(1),
                             dump_only=True)
    name = fields.String(required=True,
                         validate=validate.Length(1),
                         dump_only=True)

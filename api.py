from flask import Blueprint
from flask_restful import Api

from resources.players import PlayersResource, PlayerResource

bp = Blueprint('api', __name__)
api = Api(bp)

# Routes
api.add_resource(PlayersResource, "/players/")
api.add_resource(PlayerResource, "/players/<string:slack_id>/")

from flask import request
from flask_restful import Resource
from models.Player import Player, PlayerSchema

from database import db

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


class PlayersResource(Resource):
    def get(self):
        players = Player.query.all()
        res = players_schema.dump(players).data
        return {'data': res}

    def post(self):
        request_data = request.get_json(force=True)
        if not request_data:
            return {'error': 'No data provided'}, 400
        player, errors = player_schema.load(request_data)
        if errors:
            return {"errors": errors}, 422

        db.session.add(player)
        db.session.commit()

        result = player_schema.dump(player).data

        return {'data': result}, 201


class PlayerResource(Resource):
    def get(self, id):
        player = Player.query.get(id)
        if not player:
            return {"error": "Player not found"}, 404
        res = player_schema.dump(player).data
        return {'data': res}

    def put(self, id):
        player = Player.query.get(id)
        if not player:
            return {"error": "Player not found"}, 404
        request_data = request.get_json(force=True)
        if not request_data:
            return {'error': 'No data provided'}, 400
        player, errors = player_schema.load(request_data,
                                            instance=player,
                                            partial=True)
        if errors:
            return {"errors": errors}, 422

        db.session.commit()

        res = player_schema.dump(player).data

        return {'data': res}

    def delete(self, id):
        player = Player.query.get(id)
        if not player:
            return {"error": "Player not found"}, 404
        res = player_schema.dump(player).data
        db.session.delete(player)
        db.session.commit()

        return {'data': res}

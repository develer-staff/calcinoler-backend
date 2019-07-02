from flask import request, current_app
from flask_restful import Resource

from database import db
from models.player import Player, PlayerSchema
from utils.slackhelper import SlackHelper, SlackRequestFailed
from utils.players import enrich_slack_users_with_players

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


class PlayersResource(Resource):
    def get(self):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        players = Player.query.all()
        try:
            slack_users = slack.get_users(search=request.args.get("s"))
        except SlackRequestFailed as e:
            return {'errors': {'general': [str(e)]}}, 503
        players = enrich_slack_users_with_players(slack_users, players)
        res = players_schema.dump(players).data
        return {'data': res}

    def post(self):
        request_data = request.get_json(force=True)
        if not request_data:
            return {'errors': {'general': ['No data provided']}}, 400
        player, errors = player_schema.load(request_data)
        if errors:
            return {"errors": errors}, 422

        db.session.add(player)
        db.session.commit()

        result = player_schema.dump(player).data

        return {'data': result}, 201


class PlayerResource(Resource):
    def get(self, id):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        player = Player.query.get(id)
        if not player:
            return {"errors": {'general': ["Player not found"]}}, 404
        try:
            slack_user = slack.get_user(player.slack_id)
        except SlackRequestFailed:
            return {'errors': {'general': ['Slack request failed']}}, 503
        player.merge_slack_user(slack_user)
        res = player_schema.dump(player).data
        return {'data': res}

    def put(self, id):
        player = Player.query.get(id)
        if not player:
            return {"errors": {'general': ["Player not found"]}}, 404
        request_data = request.get_json(force=True)
        if not request_data:
            return {'errors': {'general': ['No data provided']}}, 400
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
            return {"errors": {'general': ["Player not found"]}}, 404
        res = player_schema.dump(player).data
        db.session.delete(player)
        db.session.commit()

        return {'data': res}

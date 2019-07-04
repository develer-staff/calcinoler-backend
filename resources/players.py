import logging

from flask import request, current_app
from flask_restful import Resource

from database import db
from models.player import Player, PlayerSchema
from utils.slackhelper import SlackHelper, SlackRequestFailed
from utils.players import enrich_slack_users_with_players
from utils.response import Response

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


class PlayersResource(Resource):
    def get(self):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        players = Player.query.all()
        try:
            slack_users = slack.get_users(search=request.args.get("s"))
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)
        players = enrich_slack_users_with_players(slack_users, players)

        return Response.success(players_schema.dump(players).data)

    def post(self):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        request_data = request.get_json(force=True)
        if not request_data:
            return Response.error({'general': [Response.BODY_EMPTY]}, 400)

        player, errors = player_schema.load(request_data)
        if errors:
            return Response.error(errors, 422)

        try:
            slack_user = slack.get_user(player.slack_id)
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)

        if Player.query.filter_by(
                slack_id=player.slack_id).first() is not None:
            return Response.error(
                {"general": [Response.ALREADY_EXISTS.format("Player")]}, 400)

        db.session.add(player)
        db.session.commit()
        player.merge_slack_user(slack_user)

        return Response.success(player_schema.dump(player).data, 201)


class PlayerResource(Resource):
    def get(self, id):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        player = Player.query.get(id)
        if not player:
            return Response.error(
                {'general': [Response.NOT_FOUND.format("Player")]}, 404)
        try:
            slack_user = slack.get_user(player.slack_id)
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)

        player.merge_slack_user(slack_user)

        return Response.success(player_schema.dump(player).data)

    def put(self, id):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        player = Player.query.get(id)
        if not player:
            return Response.error(
                {'general': [Response.NOT_FOUND.format("Player")]}, 404)

        request_data = request.get_json(force=True)
        if not request_data:
            return Response.error({'general': [Response.BODY_EMPTY]}, 400)

        if "slack_id" in request_data:
            del request_data["slack_id"]

        player, errors = player_schema.load(request_data,
                                            instance=player,
                                            partial=True)
        if errors:
            return Response.error(errors, 422)

        try:
            slack_user = slack.get_user(player.slack_id)
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)

        db.session.commit()
        player.merge_slack_user(slack_user)

        return Response.success(player_schema.dump(player).data)

    def delete(self, id):
        player = Player.query.get(id)
        if not player:
            return Response.error(
                {'general': [Response.NOT_FOUND.format("Player")]}, 404)
        db.session.delete(player)
        db.session.commit()

        return Response.success(player_schema.dump(player).data)

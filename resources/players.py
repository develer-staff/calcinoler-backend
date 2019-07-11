import logging

from flask import request, current_app
from flask_restful import Resource

from database import db
from models.player import Player, PlayerSchema
from utils.slackhelper import SlackHelper, SlackRequestFailed, SlackUserNotFound
from utils.players import enrich_slack_users_with_players
from utils.response import Response
from utils.schema import validate_schema_unknown_fields

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


class PlayersResource(Resource):
    def get(self):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        players = Player.query.all()
        try:
            slack_users = slack.get_users(searchTerm=request.args.get("s"))
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)
        players = enrich_slack_users_with_players(slack_users, players)

        return Response.success(players_schema.dump(players).data)


class PlayerResource(Resource):
    def get(self, slack_id):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])
        try:
            slack_user = slack.get_user(slack_id)
        except SlackUserNotFound as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error(
                {'general': [Response.NOT_FOUND.format("Player")]}, 404)
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)

        player = Player.query.get(slack_id)
        if player is None:
            player = Player()

        player.merge_slack_user(slack_user)
        return Response.success(player_schema.dump(player).data)

    def patch(self, slack_id):
        slack = SlackHelper(current_app.config['SLACK_TOKEN'])

        request_data = request.get_json(force=True)
        if not request_data:
            return Response.error({'general': [Response.BODY_EMPTY]}, 400)

        unk = validate_schema_unknown_fields(player_schema, request_data)
        errors = player_schema.validate(request_data)
        errors = dict(**unk, **errors)
        if errors:
            return Response.error(errors, 422)

        try:
            slack_user = slack.get_user(slack_id)
        except SlackUserNotFound as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error(
                {'slack_id': Response.INVALID.format("Slack ID")}, 422)
        except SlackRequestFailed as e:
            logging.error('Slack Api Error: {}'.format(str(e)))
            return Response.error({'general': [Response.REQUEST_FAILED]}, 503)

        player = Player.query.get(slack_id)
        response_code = 200
        if not player:
            player = Player()
            player.slack_id = slack_id
            response_code = 201
            db.session.add(player)

        player_schema.load(request_data, instance=player)

        db.session.commit()
        player.merge_slack_user(slack_user)

        return Response.success(player_schema.dump(player).data, response_code)

from typing import List

from models.player import Player

players_list = List[Player]


def enrich_slack_users_with_players(slack_users: list,
                                    players: players_list) -> players_list:
    """Takes a list of Slack users and a list of players and merge each player with
        the corresponding Slack user by Slack ID.

        slack_users (list(dict)):
            Slack users from Slack Api
        players (list(Player)):
            List of players

        Returns list(Player) with merged data
    """
    players = {p.slack_id: p for p in players}
    res = []
    for su in slack_users:
        player = players.get(su['id'], Player())
        player.merge_slack_user(su)
        res.append(player)
    return res

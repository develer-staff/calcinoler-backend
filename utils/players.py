from models.player import Player


def enrich_slack_users_with_players(slack_users: list, players: list) -> list:
    players = {p.slack_id: p for p in players}
    res = []
    for su in slack_users:
        player = players.get(su['id'], Player())
        player.merge_slack_user(su)
        res.append(player)
    return res

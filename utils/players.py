def enrich_slack_users_with_players(slack_users: list, players: list) -> list:
    res = []
    for su in slack_users:
        try:
            player = next(p for p in players if su["id"] == p.slack_id)
        except StopIteration:
            continue
        player.merge_slack_user(su['profile'])
        res.append(player)
    return res

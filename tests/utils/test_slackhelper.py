from utils.slackhelper import SlackHelper


def test_slack_search_user(app):
    slack_users = [{
        "id": "TEST1",
        "real_name": "ogek",
    }, {
        "id": "TEST2",
        "real_name": "ogal",
    }, {
        "id": "TEST3",
        "real_name": "Slackbot",
    }]

    founded_users = SlackHelper._search_user(slack_users, "og")

    assert len(founded_users) == 2

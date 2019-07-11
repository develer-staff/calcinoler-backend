from utils.slackhelper import SlackHelper


def test_slack_search_user(app):
    slack_users = [{
        "id": "TEST1",
        "profile": {
            "email": "test@test.it",
            "real_name": "Giuseppe",
            "display_name": "ogek"
        }
    }, {
        "id": "TEST2",
        "profile": {
            "email": "ogal@ogal.it",
            "real_name": "Ogal",
            "display_name": "ogal"
        }
    }, {
        "id": "TEST3",
        "profile": {
            "email": "test3@test3.it",
            "real_name": "Slackbot",
            "display_name": "slackbot"
        }
    }]

    found_users = SlackHelper._search_user(slack_users, "og")

    assert len(found_users) == 2


def test_slack_strip_bots(app):
    slack_users = [{
        "id": "TEST1",
        "is_bot": False
    }, {
        "id": "TEST2",
        "is_bot": True
    }, {
        "id": "USLACKBOT",
        "is_bot": False
    }, {
        "id": "TEST3",
        "is_bot": True
    }]

    slack = SlackHelper(app.config['SLACK_TOKEN'])
    users = slack._strip_bots(slack_users)

    assert len(users) == 1

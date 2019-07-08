import mock

from models.player import Player
from utils.slackhelper import SlackHelper


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_empty_player_merge_with_slack(mock_get_user, app):
    p = Player()
    mock_get_user.return_value = {
        'real_name': 'nick',
        'profile': {
            'display_name': 'Test'
        }
    }

    with app.app_context():
        sh = SlackHelper(app.config['SLACK_TOKEN'])
        slack_user = sh.get_user('test')

    p.merge_slack_user(slack_user)

    assert p.name == 'Test'
    assert p.nickname == 'nick'


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_merge_player_with_slack(mock_get_user, app):
    p = Player()
    p.name = 'Giuseppe'
    p.dishonors = 4
    mock_get_user.return_value = {
        'real_name': 'nick',
        'profile': {
            'display_name': 'Test'
        }
    }

    with app.app_context():
        sh = SlackHelper(app.config['SLACK_TOKEN'])
        slack_user = sh.get_user('test')

    p.merge_slack_user(slack_user)

    assert p.name == 'Test'
    assert p.nickname == 'nick'
    assert p.dishonors == 4

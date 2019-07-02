import mock
import json

from models.player import Player
from database import db


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_data_in_get(mock_get_users, app):
    mock_get_users.return_value = [{
        "id": "SLACK_TEST",
        "real_name": "ogek",
        "display_name": "Giuseppe"
    }]
    rv = app.test_client().get('/api/players/')
    json_data = json.loads(rv.data)
    assert 'data' in json_data
    assert isinstance(json_data['data'], list)


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_players_in_data(mock_get_users, app):
    mock_get_users.return_value = [{
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }]
    assert_player_count_x(app, 0)
    player = Player()
    player.slack_id = "TEST1"
    with app.app_context():
        db.session.add(player)
        db.session.flush()
        rv = app.test_client().get('/api/players/')

    json_data = json.loads(rv.data)
    assert len(json_data['data']) == 1


def test_player_post(app):
    assert_player_count_x(app, 0)
    data = dict(slack_id="TEST", dishonors=2)
    with app.test_client() as tc:
        rv = tc.post('/api/players/',
                     data=json.dumps(data),
                     follow_redirects=True)
    json_data = json.loads(rv.data)
    assert_player_count_x(app, 1)
    assert json_data['data']['slack_id'] == data['slack_id']
    with app.app_context():
        p = Player.query.filter_by(slack_id=data['slack_id'])
        assert p is not None


def test_put(app):
    with app.app_context():
        player = Player()
        player.slack_id = "TEST"
        db.session.add(player)
        db.session.flush()
        id = player.id

        data = dict(dishonors=10)
        with app.test_client() as tc:
            _ = tc.put('/api/players/{}/'.format(id),
                       data=json.dumps(data),
                       follow_redirects=True)

        p = Player.query.get(id)
    assert p.dishonors == data['dishonors']


def assert_player_count_x(app, x: int):
    with app.app_context():
        players_number = Player.query.count()
        assert players_number == x

import mock
import json

from models.player import Player
from utils.slackhelper import SlackRequestFailed
from database import db


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_data_in_get(mock_get_users, app):
    mock_get_users.return_value = [{
        "id": "SLACK_TEST",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
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


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_player_post(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

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


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_put(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

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

    assert player.slack_id == p.slack_id
    assert p.dishonors == data['dishonors']


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_get_slack_error(mock_get_users, app):
    mock_get_users.side_effect = SlackRequestFailed()

    rv = app.test_client().get('/api/players/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


def test_post_empty_data_error(app):
    rv = app.test_client().post('/api/players/', data=json.dumps({}))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 400


def test_post_wrong_data_error(app):
    data = dict(dishonors=1)

    rv = app.test_client().post('/api/players/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert 'slack_id' in json_data['errors']
    assert rv.status_code == 422


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_post_slack_error(mock_get_user, app):
    mock_get_user.side_effect = SlackRequestFailed()
    data = dict(slack_id="TEST", dishonors=2)

    rv = app.test_client().post('/api/players/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_post_already_exists_error(mock_get_user, app):
    player = Player()
    player.slack_id = "TEST"

    mock_get_user.return_value = {
        "id": "TEST",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }
    data = dict(slack_id="TEST", dishonors=2)

    with app.app_context():
        db.session.add(player)
        db.session.commit()

    rv = app.test_client().post('/api/players/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 400


def test_get_not_found_error(app):

    rv = app.test_client().get('/api/players/7565/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 404


def test_put_not_found_error(app):

    data = dict(dishonors=2)

    rv = app.test_client().put('/api/players/7565/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 404


def test_put_empty_data_error(app):
    player = Player()
    player.slack_id = "TEST"

    with app.app_context():
        db.session.add(player)
        db.session.commit()
        rv = app.test_client().put('/api/players/{}/'.format(player.id),
                                   data=json.dumps({}))

    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 400


def test_put_wrong_data_error(app):
    data = dict(dishonors=None)
    player = Player()
    player.slack_id = "TEST"

    with app.app_context():
        db.session.add(player)
        db.session.commit()
        rv = app.test_client().put('/api/players/{}/'.format(player.id),
                                   data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert 'dishonors' in json_data['errors']
    assert rv.status_code == 422


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_put_slack_error(mock_get_user, app):
    player = Player()
    player.slack_id = "TEST"
    mock_get_user.side_effect = SlackRequestFailed()
    data = dict(dishonors=3)

    with app.app_context():
        db.session.add(player)
        db.session.commit()
        rv = app.test_client().put('/api/players/{}/'.format(player.id),
                                   data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


def test_delete_not_found_error(app):
    rv = app.test_client().delete('/api/players/7565/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 404


def assert_player_count_x(app, x: int):
    with app.app_context():
        assert Player.query.count() == x

import mock
import json

from models.player import Player
from utils.slackhelper import SlackRequestFailed, SlackUserNotFound
from database import db


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_get_many(mock_get_users, app):
    mock_get_users.return_value = [{
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }]

    player = Player()
    player.slack_id = "TEST1"
    with app.app_context():
        db.session.add(player)
        db.session.flush()

        rv = app.test_client().get('/api/players/', follow_redirects=True)

    json_data = json.loads(rv.data)

    assert isinstance(json_data['data'], list)
    assert len(json_data['data']) == 1


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_get_search(mock_get_users, app):
    mock_get_users.return_value = [{
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }]

    with app.app_context():
        rv = app.test_client().get('/api/players/',
                                   data=json.dumps({'s': 'og'}),
                                   follow_redirects=True)

    json_data = json.loads(rv.data)

    assert isinstance(json_data['data'], list)
    assert len(json_data['data']) == 1


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_get_single_player_exists_in_db(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    player = Player()
    player.slack_id = "TEST1"
    with app.app_context():
        db.session.add(player)
        db.session.flush()

        rv = app.test_client().get('/api/players/{}/'.format(player.slack_id),
                                   follow_redirects=True)

    json_data = json.loads(rv.data)

    assert isinstance(json_data['data'], dict)
    assert json_data['data']['slack_id'] == player.slack_id


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_get_single_player_not_exists_in_db(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    with app.app_context():
        rv = app.test_client().get('/api/players/TEST', follow_redirects=True)

    json_data = json.loads(rv.data)

    assert isinstance(json_data['data'], dict)


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_get_slack_error(mock_get_users, app):
    mock_get_users.side_effect = SlackRequestFailed()

    rv = app.test_client().get('/api/players/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


@mock.patch('utils.slackhelper.SlackHelper.get_users')
def test_get_single_slack_error(mock_get_users, app):
    mock_get_users.side_effect = SlackRequestFailed()

    rv = app.test_client().get('/api/players/TEST/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_get_not_found_error(mock_get_user, app):
    mock_get_user.side_effect = SlackUserNotFound()

    rv = app.test_client().get('/api/players/TEST/')
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 404


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST",
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

        data = {'dishonors': 10}

        with app.test_client() as tc:
            rv = tc.patch('/api/players/{}/'.format(player.slack_id),
                          data=json.dumps(data),
                          follow_redirects=True)
        json_data = json.loads(rv.data)

        p = Player.query.get(player.slack_id)

    assert rv.status_code == 200
    assert player.slack_id == p.slack_id
    assert p.dishonors == data['dishonors']
    assert json_data['data']['dishonors'] == data['dishonors']


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch_create(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    slack_id = "TEST"

    with app.app_context():
        data = {'dishonors': 10}
        with app.test_client() as tc:
            rv = tc.patch('/api/players/{}/'.format(slack_id),
                          data=json.dumps(data),
                          follow_redirects=True)
        json_data = json.loads(rv.data)

        p = Player.query.get(slack_id)

    rv.status_code == 201
    assert slack_id == p.slack_id
    assert p.dishonors == data['dishonors']
    assert json_data['data']['dishonors'] == data['dishonors']


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch_slack_error(mock_get_user, app):
    mock_get_user.side_effect = SlackRequestFailed()

    data = {"dishonors": 1}
    rv = app.test_client().patch('/api/players/TEST/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert rv.status_code == 503


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch_invalid_slack_id_error(mock_get_user, app):
    mock_get_user.side_effect = SlackUserNotFound()

    with app.app_context():
        data = {'dishonors': 10}
        with app.test_client() as tc:
            rv = tc.patch('/api/players/9475/',
                          data=json.dumps(data),
                          follow_redirects=True)
        json_data = json.loads(rv.data)

        assert Player.query.count() == 0
        assert rv.status_code == 422
        assert "errors" in json_data
        assert "slack_id" in json_data['errors']


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch_empty_request(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    rv = app.test_client().patch('/api/players/TEST/',
                                 data=json.dumps({}),
                                 follow_redirects=True)
    json_data = json.loads(rv.data)
    print(json_data)
    assert rv.status_code == 400
    assert 'errors' in json_data


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_patch_negative_dishonors(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    slack_id = "TEST"

    with app.app_context():
        data = {'dishonors': -10}
        with app.test_client() as tc:
            rv = tc.patch('/api/players/{}/'.format(slack_id),
                          data=json.dumps(data),
                          follow_redirects=True)
            json_data = json.loads(rv.data)

            assert Player.query.count() == 0

    assert rv.status_code == 422
    assert "errors" in json_data
    assert "dishonors" in json_data['errors']

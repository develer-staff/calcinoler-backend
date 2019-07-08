import mock
import json

from models.player import Player
from utils.slackhelper import SlackRequestFailed
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


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_get_single(mock_get_user, app):
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

        rv = app.test_client().get('/api/players/{}/'.format(player.id),
                                   follow_redirects=True)

    json_data = json.loads(rv.data)

    assert isinstance(json_data['data'], dict)
    assert json_data['data']['slack_id'] == player.slack_id


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_post(mock_get_user, app):
    mock_get_user.return_value = {
        "id": "TEST1",
        "profile": {
            "real_name": "ogek",
            "display_name": "Giuseppe"
        }
    }

    data = {'slack_id': 'TEST', 'dishonors': 2}

    with app.test_client() as tc:
        rv = tc.post('/api/players/',
                     data=json.dumps(data),
                     follow_redirects=True)
    json_data = json.loads(rv.data)

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

        data = {'dishonors': 10}

        with app.test_client() as tc:
            rv = tc.put('/api/players/{}/'.format(player.id),
                        data=json.dumps(data),
                        follow_redirects=True)
        json_data = json.loads(rv.data)

        p = Player.query.get(player.id)

    assert player.slack_id == p.slack_id
    assert p.dishonors == data['dishonors']
    assert json_data['data']['dishonors'] == data['dishonors']


def test_delete(app):

    with app.app_context():
        player = Player()
        player.slack_id = "TEST"
        db.session.add(player)
        db.session.flush()

        with app.test_client() as tc:
            rv = tc.delete('/api/players/{}/'.format(player.id),
                           follow_redirects=True)
        json_data = json.loads(rv.data)

        p = Player.query.get(player.id)

    assert p is None
    assert json_data['data']['slack_id'] == player.slack_id


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
    data = {'dishonors': 1}

    rv = app.test_client().post('/api/players/', data=json.dumps(data))
    json_data = json.loads(rv.data)

    assert 'errors' in json_data
    assert 'slack_id' in json_data['errors']
    assert rv.status_code == 422


@mock.patch('utils.slackhelper.SlackHelper.get_user')
def test_post_slack_error(mock_get_user, app):
    mock_get_user.side_effect = SlackRequestFailed()
    data = {'slack_id': 'TEST', 'dishonors': 2}

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
    data = {'slack_id': "TEST", 'dishonors': 2}

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

    data = {'dishonors': 2}

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
    data = {'dishonors': None}
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
    data = {'dishonors': 3}

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

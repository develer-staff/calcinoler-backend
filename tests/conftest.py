import pytest
import click

from app import create_app
from database import db


@pytest.fixture(scope='session')
def app():
    app = create_app('config_test.py')
    with app.app_context():
        db.init_app(app)
        db.create_all()
    yield app


@pytest.fixture(autouse=True)
def clear_data(app):
    with app.app_context():
        from database import db
        for table in reversed(db.metadata.sorted_tables):
            click.echo('Clear table {}'.format(table))
            db.session.execute(table.delete())
        db.session.commit()

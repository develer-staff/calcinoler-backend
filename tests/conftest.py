import pytest
import click

from app import create_app


@pytest.fixture
def app():
    app = create_app("config_test.py")
    yield app


@pytest.fixture(autouse=True)
def clear_data(app):
    with app.app_context():
        from database import db
        for table in reversed(db.metadata.sorted_tables):
            click.echo('Clear table {}'.format(table))
            db.session.execute(table.delete())
        db.session.commit()

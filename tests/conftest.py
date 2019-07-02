import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app("config_test.py")
    print(app.config)
    yield app


@pytest.fixture(autouse=True)
def clear_data(app):
    with app.app_context():
        from database import db
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.commit()

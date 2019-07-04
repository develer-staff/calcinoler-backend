"""Renamed column `n_disonors` in `dishonors`

Revision ID: 5540202b6321
Revises: 4bc9c7191c9b
Create Date: 2019-07-01 17:52:06.735857

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5540202b6321'
down_revision = '4bc9c7191c9b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'players',
        sa.Column('dishonors',
                  sa.Integer(),
                  server_default='0',
                  nullable=False))
    op.drop_column('players', 'n_disonors')


def downgrade():
    op.add_column(
        'players',
        sa.Column('n_disonors',
                  sa.INTEGER(),
                  autoincrement=False,
                  nullable=False))
    op.drop_column('players', 'dishonors')

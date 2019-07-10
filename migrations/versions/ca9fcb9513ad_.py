"""Removed `id` field, `slack_id` as primary_key

Revision ID: ca9fcb9513ad
Revises: f7dea6d11e7f
Create Date: 2019-07-09 14:01:44.047539

"""
from alembic import op
import sqlalchemy as sa

revision = 'ca9fcb9513ad'
down_revision = 'f7dea6d11e7f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('players_slack_id_key', 'players', type_='unique')
    op.drop_column('players', 'id')


def downgrade():
    op.add_column(
        'players',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_unique_constraint('players_slack_id_key', 'players',
                                ['slack_id'])

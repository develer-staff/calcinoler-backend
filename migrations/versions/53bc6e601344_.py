"""Edited players table, added slack_id column for Slack integration.
Removed `name` and `nickname` columns because
this data will come from Slack Api

Revision ID: 53bc6e601344
Revises: 
Create Date: 2019-06-26 16:40:04.218205

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '53bc6e601344'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('players', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('slack_id', sa.String(), nullable=False),
                    sa.Column('n_disonors', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('slack_id'))


def downgrade():
    op.drop_table('players')

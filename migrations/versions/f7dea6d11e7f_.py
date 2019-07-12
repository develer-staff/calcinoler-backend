"""Player table creation

Revision ID: f7dea6d11e7f
Revises: 5540202b6321
Create Date: 2019-07-05 12:37:10.115382

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f7dea6d11e7f'
down_revision = '5540202b6321'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'players', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slack_id', sa.String(), nullable=False),
        sa.Column('dishonors',
                  sa.Integer(),
                  server_default='0',
                  nullable=False), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slack_id'))


def downgrade():
    op.drop_table('players')

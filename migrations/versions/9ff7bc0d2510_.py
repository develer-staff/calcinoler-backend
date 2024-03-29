"""Database initialization

Revision ID: 9ff7bc0d2510
Revises: 
Create Date: 2019-06-24 10:40:30.977706

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9ff7bc0d2510'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'players', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('nickname', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('nickname'))
    op.create_table('sports', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=30), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('matches', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), nullable=False),
                    sa.Column('person_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['person_id'],
                        ['sports.id'],
                    ), sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'match_players', sa.Column('match_id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['match_id'],
            ['matches.id'],
        ), sa.ForeignKeyConstraint(
            ['player_id'],
            ['players.id'],
        ), sa.PrimaryKeyConstraint('match_id', 'player_id'),
        sa.UniqueConstraint('match_id',
                            'player_id',
                            name='unique_player_in_match'))


def downgrade():
    op.drop_table('match_players')
    op.drop_table('matches')
    op.drop_table('sports')
    op.drop_table('players')

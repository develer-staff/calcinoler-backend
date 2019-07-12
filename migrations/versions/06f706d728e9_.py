"""Added Sport foreign key in Match

Revision ID: 06f706d728e9
Revises: 9ff7bc0d2510
Create Date: 2019-06-24 16:39:51.475124

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '06f706d728e9'
down_revision = '9ff7bc0d2510'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('matches', sa.Column('sport_id',
                                       sa.Integer(),
                                       nullable=False))
    op.drop_constraint('matches_person_id_fkey', 'matches', type_='foreignkey')
    op.create_foreign_key(None, 'matches', 'sports', ['sport_id'], ['id'])
    op.drop_column('matches', 'person_id')


def downgrade():
    op.add_column(
        'matches',
        sa.Column('sport_id',
                  sa.INTEGER(),
                  autoincrement=False,
                  nullable=False))
    op.drop_constraint(None, 'matches', type_='foreignkey')
    op.create_foreign_key('matches_sport_id_fkey', 'matches', 'sports',
                          ['sport_id'], ['id'])
    op.drop_column('matches', 'sport_id')
    op.drop_constraint('unique_player_in_match',
                       'match_players',
                       type_='unique')

"""Add match table

Revision ID: f870ab84feba
Revises: 1ae95303d00d
Create Date: 2023-06-21 14:01:30.161155

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f870ab84feba'
down_revision = '1ae95303d00d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('match',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('players', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('state', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('start_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_id'), 'match', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_match_id'), table_name='match')
    op.drop_table('match')
    # ### end Alembic commands ###

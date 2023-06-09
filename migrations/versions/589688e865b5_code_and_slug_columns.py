"""Code and slug columns

Revision ID: 589688e865b5
Revises: f870ab84feba
Create Date: 2023-06-21 14:18:44.884634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '589688e865b5'
down_revision = 'f870ab84feba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('slug', sa.String(), nullable=True))
    op.drop_index('ix_game_code', table_name='game')
    op.create_index(op.f('ix_game_slug'), 'game', ['slug'], unique=True)
    op.drop_column('game', 'code')
    op.add_column('match', sa.Column('code', sa.String(), nullable=False))
    op.create_index(op.f('ix_match_code'), 'match', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_match_code'), table_name='match')
    op.drop_column('match', 'code')
    op.add_column('game', sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_game_slug'), table_name='game')
    op.create_index('ix_game_code', 'game', ['code'], unique=False)
    op.drop_column('game', 'slug')
    # ### end Alembic commands ###

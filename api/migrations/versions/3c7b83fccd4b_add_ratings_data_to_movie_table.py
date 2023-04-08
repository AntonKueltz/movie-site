"""add ratings data to movie table

Revision ID: 3c7b83fccd4b
Revises: c852f91c5050
Create Date: 2023-04-08 12:39:49.543665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c7b83fccd4b'
down_revision = 'c852f91c5050'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('review_count', sa.Integer(), nullable=True, server_default="0"))
    op.add_column('movie', sa.Column('avg_rating', sa.Float(), nullable=True))
    op.create_index(op.f('ix_movie_title'), 'movie', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_movie_title'), table_name='movie')
    op.drop_column('movie', 'avg_rating')
    op.drop_column('movie', 'review_count')
    # ### end Alembic commands ###
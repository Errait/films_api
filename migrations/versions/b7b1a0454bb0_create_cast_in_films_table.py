"""Create cast_in_films table

Revision ID: b7b1a0454bb0
Revises: ac5e52cdfa5e
Create Date: 2024-09-25 14:39:34.610632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7b1a0454bb0'
down_revision = 'ac5e52cdfa5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cast_in_films',
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cast_in_films')
    # ### end Alembic commands ###

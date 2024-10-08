"""add film model

Revision ID: ac5e52cdfa5e
Revises: 
Create Date: 2024-09-20 17:59:10.417736

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = 'ac5e52cdfa6e'
down_revision = '20801c48edea'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    now = datetime.now()
    conn.execute(
        text(
            """
                UPDATE films
                SET is_released = true
                WHERE release_date < :now
            """
        ),
        {'now': now}
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                UPDATE films
                SET is_released = NULL
            """
        )
    )

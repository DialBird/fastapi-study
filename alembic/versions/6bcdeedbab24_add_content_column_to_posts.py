"""add content column to posts

Revision ID: 6bcdeedbab24
Revises: bd1e4e33c5d3
Create Date: 2021-11-07 13:39:22.009942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6bcdeedbab24"
down_revision = "bd1e4e33c5d3"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass

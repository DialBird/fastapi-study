"""create posts table

Revision ID: bd1e4e33c5d3
Revises: 
Create Date: 2021-11-07 13:31:08.392184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd1e4e33c5d3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass

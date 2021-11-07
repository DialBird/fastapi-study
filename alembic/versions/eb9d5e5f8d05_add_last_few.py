"""add last few

Revision ID: eb9d5e5f8d05
Revises: 873d0d980715
Create Date: 2021-11-07 13:45:50.822910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb9d5e5f8d05"
down_revision = "873d0d980715"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass

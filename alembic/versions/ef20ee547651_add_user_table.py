"""add user table

Revision ID: ef20ee547651
Revises: 6bcdeedbab24
Create Date: 2021-11-07 13:42:50.214638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ef20ee547651"
down_revision = "6bcdeedbab24"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass

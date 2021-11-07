"""add foreign-key to post table

Revision ID: 873d0d980715
Revises: ef20ee547651
Create Date: 2021-11-07 13:44:29.625681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "873d0d980715"
down_revision = "ef20ee547651"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass

"""Create DB

Revision ID: 60221bf79bdd
Revises: None
Create Date: 2022-06-27 11:43:46.293516

"""
import sqlalchemy as sa
from lvtn_utils import UTCDateTime, get_date

from alembic import op

# revision identifiers, used by Alembic.
revision = "03ecc876dd3e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("meta", sa.LargeBinary, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "seeds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uid", sa.Integer(), nullable=True),
        sa.Column("fingerprint", sa.String(length=32), nullable=True),
        sa.Column("created", UTCDateTime, nullable=True, default=get_date),
        sa.Column("last_accessed", UTCDateTime, nullable=True, default=get_date),
        sa.Column("provider_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String, nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("fingerprint"),
    )

    op.create_table(
        "fruits",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fingerprint", sa.String(length=32), nullable=True),
        sa.Column("created", UTCDateTime, nullable=True, default=get_date),
        sa.Column("last_accessed", UTCDateTime, nullable=True, default=get_date),
        sa.Column("seed_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String, nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("fingerprint"),
    )


def downgrade() -> None:
    op.drop_table("providers")
    op.drop_table("seeds")
    op.drop_table("fruits")

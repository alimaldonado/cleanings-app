"""create_main_tables
Revision ID: b732937fb214
Revises: 
Create Date: 2021-11-23 18:09:17.722455
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'b732937fb214'
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_jobs_table() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("job_type", sa.Text, nullable=False,
                  server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("owner", sa.CHAR(36), sa.ForeignKey(
            "users.id", ondelete="CASCADE")),
        *timestamps(),
    )

    op.execute(
        """
        CREATE TRIGGER update_jobs_modtime
            BEFORE UPDATE
            ON jobs
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("username", sa.Text, unique=True,
                  nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean,
                  nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(),
                  nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(),
                  nullable=False, server_default="False"),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_profiles_table() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("full_name", sa.Text, nullable=True),
        sa.Column("phone_number", sa.Text, nullable=True),
        sa.Column("bio", sa.Text, nullable=True, server_default=""),
        sa.Column("image", sa.Text, nullable=True),
        sa.Column("user_id", sa.CHAR(36), sa.ForeignKey(
            "users.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_profiles_table()
    create_jobs_table()


def downgrade() -> None:
    op.drop_table("jobs")
    op.drop_table("profiles")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")

"""create_main_tables
Revision ID: b732937fb214
Revises: 
Create Date: 2021-11-23 18:09:17.722455
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'b732937fb214'
down_revision = None
branch_labels = None
depends_on = None


def create_jobs_table() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("job_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )


def upgrade() -> None:
    create_jobs_table()


def downgrade() -> None:
    op.drop_table("jobs")

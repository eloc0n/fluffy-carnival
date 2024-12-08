"""initial universities

Revision ID: 84aa25b86685
Revises: 32b5b24d5aac
Create Date: 2024-12-08 12:40:16.040199

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "84aa25b86685"
down_revision: Union[str, None] = "32b5b24d5aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("alpha_two_code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alpha_two_code"),
    )
    op.create_index(op.f("ix_countries_name"), "countries", ["name"], unique=False)
    op.create_table(
        "universities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("web_pages", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("domains", postgresql.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_universities_name"), "universities", ["name"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_universities_name"), table_name="universities")
    op.drop_table("universities")
    op.drop_index(op.f("ix_countries_name"), table_name="countries")
    op.drop_table("countries")
    # ### end Alembic commands ###
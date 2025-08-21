"""Created Task table

Revision ID: 82c84630706c
Revises: 
Create Date: 2025-08-21 11:33:35.779290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82c84630706c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "task",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("text", sa.String(length=2048)),
        sa.Column("completed", sa.Boolean, default=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("task")

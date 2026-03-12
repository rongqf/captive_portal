"""backfill device timestamps

Revision ID: b8b1b8af2c01
Revises: ac1a35d853b7
Create Date: 2026-03-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b1b8af2c01'
down_revision: Union[str, Sequence[str], None] = 'ac1a35d853b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        UPDATE device
        SET create_time = CURRENT_TIMESTAMP
        WHERE create_time IS NULL
    """)
    op.execute("""
        UPDATE device
        SET update_time = COALESCE(update_time, create_time, CURRENT_TIMESTAMP)
        WHERE update_time IS NULL
    """)

    op.alter_column(
        'device',
        'create_time',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        existing_nullable=True,
    )
    op.alter_column(
        'device',
        'update_time',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'device',
        'update_time',
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=True,
    )
    op.alter_column(
        'device',
        'create_time',
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=True,
    )

"""drop_previous_status_from_properties

Revision ID: approval_002
Revises: approval_001
Create Date: 2026-06-23 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'approval_002'
down_revision: Union[str, Sequence[str], None] = 'approval_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('properties', 'previous_status')


def downgrade() -> None:
    op.add_column('properties', sa.Column(
        'previous_status',
        sa.Enum('draft', 'post_pending', 'edit_pending', 'deposit_pending',
                'soldout_pending', 'complete_pending', 'cancel_pending',
                'available', 'deposited', 'soldout', 'expired', 'completed',
                name='propertystatus'),
        nullable=True,
    ))

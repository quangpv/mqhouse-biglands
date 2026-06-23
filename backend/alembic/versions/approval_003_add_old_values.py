"""add_old_values_to_approvals

Revision ID: approval_003
Revises: approval_002
Create Date: 2026-06-23 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'approval_003'
down_revision: Union[str, Sequence[str], None] = 'approval_002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('approvals', sa.Column(
        'old_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True
    ))


def downgrade() -> None:
    op.drop_column('approvals', 'old_values')

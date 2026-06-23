"""add_device_limit_columns

Revision ID: device_limit_001
Revises: abcdef123456
Create Date: 2026-06-23 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'device_limit_001'
down_revision: Union[str, Sequence[str], None] = 'abcdef123456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('device_limit_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('users', sa.Column('device_id', sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'device_id')
    op.drop_column('users', 'device_limit_enabled')

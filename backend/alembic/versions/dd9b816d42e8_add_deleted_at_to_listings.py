"""add deleted_at to listings

Revision ID: dd9b816d42e8
Revises: dbd6afa41724
Create Date: 2026-06-21 05:37:38.588434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd9b816d42e8'
down_revision: Union[str, Sequence[str], None] = 'dbd6afa41724'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('listings', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('listings', 'deleted_at')

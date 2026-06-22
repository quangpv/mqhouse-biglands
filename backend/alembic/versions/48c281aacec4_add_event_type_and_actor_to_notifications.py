"""add event_type actor_name transaction_type to notifications

Revision ID: 48c281aacec4
Revises: a75659a9920b
Create Date: 2026-06-22 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '48c281aacec4'
down_revision: Union[str, Sequence[str], None] = 'a75659a9920b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("notifications", sa.Column("event_type", sa.String(100), nullable=True))
    op.add_column("notifications", sa.Column("actor_name", sa.String(255), nullable=True))
    op.add_column("notifications", sa.Column("transaction_type", sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column("notifications", "transaction_type")
    op.drop_column("notifications", "actor_name")
    op.drop_column("notifications", "event_type")

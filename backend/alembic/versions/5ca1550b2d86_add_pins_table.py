"""add pins table

Revision ID: 5ca1550b2d86
Revises: a6dd421cb721
Create Date: 2026-06-24 00:23:31.354427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5ca1550b2d86'
down_revision: Union[str, Sequence[str], None] = 'a6dd421cb721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('pins',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('property_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'property_id'),
    )


def downgrade() -> None:
    op.drop_table('pins')

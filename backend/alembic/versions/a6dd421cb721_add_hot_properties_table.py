"""add hot_properties table

Revision ID: a6dd421cb721
Revises: 0bc7d3da356b
Create Date: 2026-06-24 00:07:00.281220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a6dd421cb721'
down_revision: Union[str, Sequence[str], None] = '0bc7d3da356b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hot_properties',
        sa.Column('property_id', sa.UUID(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('hot_properties')

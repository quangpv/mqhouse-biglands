"""add_organization_join_tables

Revision ID: 9f207a29b4a7
Revises: 3de2657ebea6
Create Date: 2026-06-23 19:14:04.894453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '9f207a29b4a7'
down_revision: Union[str, Sequence[str], None] = '3de2657ebea6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('organization_property_types',
    sa.Column('organization_id', sa.UUID(), nullable=False),
    sa.Column('property_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['property_type_id'], ['property_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('organization_id', 'property_type_id')
    )
    op.create_table('organization_transaction_types',
    sa.Column('organization_id', sa.UUID(), nullable=False),
    sa.Column('transaction_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['transaction_type_id'], ['transaction_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('organization_id', 'transaction_type_id')
    )


def downgrade() -> None:
    op.drop_table('organization_transaction_types')
    op.drop_table('organization_property_types')

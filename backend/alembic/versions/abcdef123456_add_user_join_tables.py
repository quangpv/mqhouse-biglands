"""add_user_join_tables

Revision ID: abcdef123456
Revises: 9f207a29b4a7
Create Date: 2026-06-23 19:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'abcdef123456'
down_revision: Union[str, Sequence[str], None] = '9f207a29b4a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_property_types',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('property_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['property_type_id'], ['property_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'property_type_id')
    )
    op.create_table('user_transaction_types',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('transaction_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['transaction_type_id'], ['transaction_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'transaction_type_id')
    )


def downgrade() -> None:
    op.drop_table('user_transaction_types')
    op.drop_table('user_property_types')

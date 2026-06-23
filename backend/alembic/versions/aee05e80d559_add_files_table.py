"""add files table

Revision ID: aee05e80d559
Revises: 9f9a8b7c6d5e
Create Date: 2026-06-23 18:47:29.548556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'aee05e80d559'
down_revision: Union[str, Sequence[str], None] = '9f9a8b7c6d5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('files',
        sa.Column('origin_name', sa.String(length=255), nullable=False),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('mimetype', sa.String(length=255), nullable=False),
        sa.Column('size', sa.BigInteger(), nullable=False),
        sa.Column('entity_type', sa.Enum('review', 'property', 'avatar', name='entitytype'), nullable=True),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('files')
    op.execute("DROP TYPE IF EXISTS entitytype")

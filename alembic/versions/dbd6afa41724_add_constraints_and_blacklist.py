"""add_constraints_and_blacklist

Revision ID: dbd6afa41724
Revises: 8c6659e7e625
Create Date: 2026-06-19 02:03:59.695043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbd6afa41724'
down_revision: Union[str, Sequence[str], None] = '8c6659e7e625'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('token_blacklist',
    sa.Column('jti', sa.String(length=500), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_blacklist_jti'), 'token_blacklist', ['jti'], unique=True)

    op.create_index(
        'idx_unique_pending_deposit',
        'deal_events',
        ['listing_id'],
        unique=True,
        postgresql_where=sa.text("event_type = 'DEPOSIT_REPORTED' AND confirmed_by_id IS NULL"),
    )

    op.create_unique_constraint(
        'uq_approval_listing_type',
        'approvals',
        ['listing_id', 'approval_type'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_approval_listing_type', 'approvals', type_='unique')
    op.drop_index('idx_unique_pending_deposit', table_name='deal_events')
    op.drop_index(op.f('ix_token_blacklist_jti'), table_name='token_blacklist')
    op.drop_table('token_blacklist')

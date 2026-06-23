"""create_approvals_table

Revision ID: approval_001
Revises: property_001
Create Date: 2026-06-23 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'approval_001'
down_revision: Union[str, Sequence[str], None] = 'property_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE action ADD VALUE IF NOT EXISTS 'edit'")
    op.execute("ALTER TYPE action ADD VALUE IF NOT EXISTS 'approve'")
    op.execute("ALTER TYPE action ADD VALUE IF NOT EXISTS 'reject'")

    op.create_table('approvals',
        sa.Column('property_id', sa.UUID(), nullable=False),
        sa.Column('transition_id', sa.UUID(), nullable=False),
        sa.Column('transaction_type_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approvalstatus'), nullable=False, server_default=sa.text("'PENDING'")),
        sa.Column('decision_transition_id', sa.UUID(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['transition_id'], ['property_transitions.id'], ),
        sa.ForeignKeyConstraint(['transaction_type_id'], ['transaction_types.id'], ),
        sa.ForeignKeyConstraint(['decision_transition_id'], ['property_transitions.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('approvals')
    op.execute("DROP TYPE IF EXISTS approvalstatus")

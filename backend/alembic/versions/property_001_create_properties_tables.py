"""create_properties_tables

Revision ID: property_001
Revises: device_limit_001
Create Date: 2026-06-23 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'property_001'
down_revision: Union[str, Sequence[str], None] = 'device_limit_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('properties',
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('transaction_type_id', sa.UUID(), nullable=False),
        sa.Column('property_type_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(18, 0), nullable=False),
        sa.Column('commission_type', sa.Enum('PERCENTAGE', 'FLAT', name='commissiontype'), nullable=False),
        sa.Column('commission_value', sa.Numeric(18, 0), nullable=False),
        sa.Column('area_width', sa.Numeric(10, 2), nullable=False),
        sa.Column('area_length', sa.Numeric(10, 2), nullable=False),
        sa.Column('total_area', sa.Numeric(10, 2), nullable=False),
        sa.Column('num_rooms', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('num_bathrooms', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('num_floors', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('street_name', sa.String(255), nullable=False),
        sa.Column('house_number', sa.String(50), nullable=False),
        sa.Column('address', sa.String(500), nullable=False),
        sa.Column('ward', sa.String(100), nullable=False),
        sa.Column('district', sa.String(100), nullable=False),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=True),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=True),
        sa.Column('label', sa.String(100), nullable=True),
        sa.Column('furnishing', sa.String(500), nullable=True),
        sa.Column('frontage_type', sa.String(100), nullable=True),
        sa.Column('legal_status', sa.String(500), nullable=True),
        sa.Column('direction', sa.Enum('EAST', 'WEST', 'SOUTH', 'NORTH', 'NORTHEAST', 'SOUTHEAST', 'NORTHWEST', 'SOUTHWEST', name='directiontype'), nullable=True),
        sa.Column('road_width', sa.String(50), nullable=True),
        sa.Column('owner_phone', sa.String(20), nullable=True),
        sa.Column('video_url', sa.String(500), nullable=True),
        sa.Column('status', sa.Enum('draft', 'post_pending', 'edit_pending', 'deposit_pending', 'soldout_pending', 'complete_pending', 'cancel_pending', 'available', 'deposited', 'soldout', 'expired', 'completed', name='propertystatus'), nullable=False, server_default=sa.text("'draft'")),
        sa.Column('is_hot', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('hot_order', sa.Integer(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('previous_status', sa.Enum('draft', 'post_pending', 'edit_pending', 'deposit_pending', 'soldout_pending', 'complete_pending', 'cancel_pending', 'available', 'deposited', 'soldout', 'expired', 'completed', name='propertystatus'), nullable=True),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['transaction_type_id'], ['transaction_types.id'], ),
        sa.ForeignKeyConstraint(['property_type_id'], ['property_types.id'], ),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
    )

    op.create_table('property_images',
        sa.Column('property_id', sa.UUID(), nullable=False),
        sa.Column('file_id', sa.UUID(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('property_transitions',
        sa.Column('property_id', sa.UUID(), nullable=False),
        sa.Column('from_status', sa.Enum('draft', 'post_pending', 'edit_pending', 'deposit_pending', 'soldout_pending', 'complete_pending', 'cancel_pending', 'available', 'deposited', 'soldout', 'expired', 'completed', name='propertystatus'), nullable=True),
        sa.Column('to_status', sa.Enum('draft', 'post_pending', 'edit_pending', 'deposit_pending', 'soldout_pending', 'complete_pending', 'cancel_pending', 'available', 'deposited', 'soldout', 'expired', 'completed', name='propertystatus'), nullable=False),
        sa.Column('action', sa.Enum('submit', 'withdraw', 'deposit', 'soldout', 'cancel', 'complete', name='action'), nullable=False),
        sa.Column('actor_id', sa.UUID(), nullable=False),
        sa.Column('actor_name', sa.String(255), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('customer_name', sa.String(255), nullable=True),
        sa.Column('customer_phone', sa.String(20), nullable=True),
        sa.Column('contract_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['actor_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('transition_files',
        sa.Column('transition_id', sa.UUID(), nullable=False),
        sa.Column('file_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['transition_id'], ['property_transitions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('transition_files')
    op.drop_table('property_transitions')
    op.drop_table('property_images')
    op.drop_table('properties')
    op.execute("DROP TYPE IF EXISTS propertystatus")
    op.execute("DROP TYPE IF EXISTS commissiontype")
    op.execute("DROP TYPE IF EXISTS directiontype")
    op.execute("DROP TYPE IF EXISTS action")

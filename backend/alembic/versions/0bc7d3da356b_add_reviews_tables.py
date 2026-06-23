"""add reviews tables

Revision ID: 0bc7d3da356b
Revises: approval_003
Create Date: 2026-06-23 23:45:20.421790

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0bc7d3da356b"
down_revision: Union[str, Sequence[str], None] = "approval_003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    dialect = conn.dialect.name
    is_pg = dialect == "postgresql"

    def pg(text: str):
        if is_pg:
            conn.execute(sa.text(text))

    pg("""
        CREATE TABLE IF NOT EXISTS review_files (
            review_id UUID NOT NULL,
            file_id UUID NOT NULL,
            id UUID NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            PRIMARY KEY (id),
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
            FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE
        );
    """)

    pg("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS property_id UUID;")
    pg("UPDATE reviews SET property_id = NULL WHERE property_id IS NULL;")

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews ALTER COLUMN property_id SET NOT NULL;
        EXCEPTION
            WHEN others THEN NULL;
        END $$;
    """)

    pg("""
        CREATE INDEX IF NOT EXISTS ix_reviews_property_id ON reviews(property_id);
    """)

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP CONSTRAINT IF EXISTS uq_review_author_listing;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'uq_review_author_property'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT uq_review_author_property
                    UNIQUE (author_id, property_id);
            END IF;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_listing_id_fkey;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables WHERE table_name = 'properties'
            ) AND NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'reviews_property_id_fkey'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT reviews_property_id_fkey
                    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE;
            END IF;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP COLUMN IF EXISTS listing_id;
        END $$;
    """)

    pg("DROP TABLE IF EXISTS review_images;")


def downgrade() -> None:
    conn = op.get_bind()
    dialect = conn.dialect.name
    is_pg = dialect == "postgresql"

    def pg(text: str):
        if is_pg:
            conn.execute(sa.text(text))

    pg("""
        CREATE TABLE IF NOT EXISTS review_images (
            review_id UUID NOT NULL,
            url VARCHAR(1000) NOT NULL,
            "order" INTEGER NOT NULL,
            id UUID NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE
        );
    """)

    pg("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS listing_id UUID;")

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP CONSTRAINT IF EXISTS uq_review_author_property;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'uq_review_author_listing'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT uq_review_author_listing
                    UNIQUE (author_id, listing_id);
            END IF;
        END $$;
    """)

    pg("DROP INDEX IF EXISTS ix_reviews_property_id;")

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_property_id_fkey;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            ALTER TABLE reviews DROP COLUMN IF EXISTS property_id;
        END $$;
    """)

    pg("""
        DO $$ BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables WHERE table_name = 'listings'
            ) AND NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'reviews_listing_id_fkey'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT reviews_listing_id_fkey
                    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE;
            END IF;
        END $$;
    """)

    pg("DROP TABLE IF EXISTS review_files;")

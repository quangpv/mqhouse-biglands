import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5444/biglands"


async def main():
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as conn:
        rows = await conn.execute(text("""
            SELECT
                n.id,
                n.created_at,
                u.full_name AS recipient,
                n.event_type,
                n.actor_name,
                n.transaction_type,
                n.title,
                n.is_read,
                n.reference_type,
                n.reference_id
            FROM notifications n
            JOIN users u ON u.id = n.user_id
            ORDER BY n.created_at DESC
        """))
        result = rows.fetchall()

        print(f"Total: {len(result)} notifications\n")
        print(f"{'ID':<8} {'Created':<22} {'Recipient':<20} {'Event':<25} {'Actor':<20} {'Title'}")
        print("-" * 120)
        for row in result:
            print(f"{str(row.id)[:8]:<8} {str(row.created_at)[:19]:<22} {row.recipient:<20} {(row.event_type or ''):<25} {(row.actor_name or ''):<20} {row.title[:50]}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

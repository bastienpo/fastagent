"""Database utilities."""

from asyncpg import Pool, create_pool

from fastagent.internal.data.tokens import create_token_table
from fastagent.internal.data.users import create_user_table


async def init_database(dsn: str, max_size: int = 50) -> Pool:
    """Create a new database pool.

    Returns:
        The database pool.
    """
    return await create_pool(dsn, max_size=max_size)


async def setup_postgresql_database(dsn: str) -> None:
    """Setup the database."""
    pool = await init_database(dsn)
    async with pool.acquire() as conn:
        await create_user_table(conn)
        await create_token_table(conn)

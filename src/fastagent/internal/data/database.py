"""Database utilities."""

from asyncpg import Pool, create_pool


async def init_database(dsn: str, max_size: int = 50) -> Pool:
    """Create a new database pool.

    Returns:
        The database pool.
    """
    return await create_pool(dsn, max_size=max_size)

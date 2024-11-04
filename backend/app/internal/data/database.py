"""Database utilities."""

from asyncpg import Pool, create_pool

from app.internal.settings import Settings


async def init_database() -> Pool:
    """Create a new database pool.

    Returns:
        The database pool.
    """
    settings = Settings()
    dsn = settings.database.get_dsn()

    return await create_pool(dsn, max_size=50)

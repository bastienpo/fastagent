"""User data and database CRUD operations."""

from datetime import datetime

from asyncpg.connection import Connection
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretBytes,
    SecretStr,
)

from app.internal.security import hash_password


class UserCreate(BaseModel):
    """User input model with validation."""

    name: str = Field(min_length=1, max_length=256)
    email: EmailStr = Field(max_length=256)
    password: SecretStr = Field(min_length=8, max_length=256)


class UserModel(BaseModel):
    """User model."""

    id: int
    created_at: datetime
    name: str
    email: EmailStr
    password_hash: SecretBytes
    version: int


async def insert_user(conn: Connection, user: UserCreate) -> None:
    """Insert a user into the database.

    Args:
        conn: The database connection.
        user: The user to insert.
    """
    query = """
    INSERT INTO users (name, email, password_hash)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    """

    password_hash = hash_password(user.password.get_secret_value())

    await conn.execute(query, user.name, user.email, password_hash, timeout=3)


async def get_user_by_email(conn: Connection, email: EmailStr) -> UserModel:
    """Get a user by email."""
    query = """
    SELECT id, created_at, name, email, password_hash, version
        FROM users
        WHERE email = $1
    """
    row = await conn.fetchrow(query, email, timeout=3)

    if row is None:
        msg = "User does not exist"
        raise ValueError(msg)

    return UserModel.model_validate(dict(row))

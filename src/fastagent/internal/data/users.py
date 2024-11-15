"""User data and database CRUD operations."""

from datetime import UTC, datetime

from asyncpg.connection import Connection
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretBytes,
    SecretStr,
)

from fastagent.internal.data.tokens import Scope, hash_token
from fastagent.internal.security import hash_password


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


AnnonymousUser = UserModel(
    id=0,
    created_at=datetime.now(UTC),
    name="",
    email="anonymous@example.com",
    password_hash=b"",
    version=0,
)


def is_anonymous(user: UserModel) -> bool:
    """Check if a user is anonymous."""
    return user == AnnonymousUser or user.id == 0


async def create_user_table(conn: Connection) -> None:
    """Create the user table."""
    query = """
        CREATE EXTENSION IF NOT EXISTS citext;

        CREATE TABLE IF NOT EXISTS fastagent_users (
            id bigserial PRIMARY KEY,
            created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
            name text NOT NULL,
            email citext UNIQUE NOT NULL,
            password_hash bytea NOT NULL,
            version integer NOT NULL DEFAULT 1
        );
    """

    await conn.execute(query, timeout=3)


async def insert_user(conn: Connection, user: UserCreate) -> None:
    """Insert a user into the database.

    Args:
        conn: The database connection.
        user: The user to insert.
    """
    query = """
    INSERT INTO fastagent_users (name, email, password_hash)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    """

    password_hash = hash_password(user.password.get_secret_value())

    await conn.execute(query, user.name, user.email, password_hash, timeout=3)


async def get_user_for_token(conn: Connection, scope: Scope, token: str) -> UserModel:
    """Get a user for a token."""
    token_hash = hash_token(token)

    query = """
    SELECT fastagent_users.id,
        fastagent_users.created_at,
        fastagent_users.name,
        fastagent_users.email,
        fastagent_users.password_hash,
        fastagent_users.version
        FROM fastagent_users
        INNER JOIN fastagent_tokens
            ON fastagent_users.id = fastagent_tokens.user_id
        WHERE fastagent_tokens.hash = $1
            AND fastagent_tokens.scope = $2
            AND fastagent_tokens.expiry > $3
    """

    row = await conn.fetchrow(query, token_hash, scope, datetime.now(UTC), timeout=3)

    if row is None:
        msg = "Invalid token"
        raise ValueError(msg)

    return UserModel.model_validate(dict(row))


async def get_user_by_email(conn: Connection, email: EmailStr) -> UserModel:
    """Get a user by email."""
    query = """
    SELECT id, created_at, name, email, password_hash, version
        FROM fastagent_users
        WHERE email = $1
    """
    row = await conn.fetchrow(query, email, timeout=3)

    if row is None:
        msg = "User does not exist"
        raise ValueError(msg)

    return UserModel.model_validate(dict(row))

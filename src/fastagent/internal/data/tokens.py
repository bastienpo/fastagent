"""Token models for activation and authentication."""

import base64
import hashlib
from datetime import UTC, datetime, timedelta
from enum import Enum
from secrets import token_bytes

from asyncpg.connection import Connection
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretBytes,
    SecretStr,
)

TOKEN_LENGTH = 26


class Scope(str, Enum):
    """Token scope."""

    ACTIVATION = "activation"
    AUTHENTICATION = "authentication"


class AuthenticationTokenCreate(BaseModel):
    """Authentication token create model."""

    email: EmailStr = Field(max_length=256)
    password: SecretStr = Field(min_length=8, max_length=256)


class TokenModel(BaseModel):
    """Token model."""

    plain_text: SecretStr = Field(min_length=TOKEN_LENGTH, max_length=TOKEN_LENGTH)
    hash: SecretBytes
    user_id: int
    expiry: datetime
    scope: Scope


async def create_token_table(conn: Connection) -> None:
    """Create the token table."""
    query = """
    CREATE TABLE IF NOT EXISTS tokens (
        hash bytea PRIMARY KEY,
        user_id bigint NOT NULL REFERENCES fastagent_users ON DELETE CASCADE,
        expiry timestamp(0) with time zone NOT NULL,
        scope text NOT NULL
    );
    """
    await conn.execute(query, timeout=3)


def hash_token(token: str) -> SecretBytes:
    """Hash a token using sha3_256."""
    return hashlib.sha3_256(token.encode("utf-8")).digest()


def create_token(user_id: int, ttl: timedelta, scope: Scope) -> TokenModel:
    """Create a token hashed with sha256.

    Args:
        user_id: The user ID to associate with the token.
        ttl: The time-to-live for the token.
        scope: The scope of the token.

    Returns:
        A token model.
    """
    random_bytes = token_bytes(16)

    # Encode to base32 without padding
    token_plain_text = base64.b32encode(random_bytes).decode().rstrip("=")

    # Hash the token using sha3_256
    token_hash = hash_token(token_plain_text)

    expiry = datetime.now(UTC) + ttl

    return TokenModel(
        plain_text=SecretStr(token_plain_text),
        hash=SecretBytes(token_hash),
        user_id=user_id,
        expiry=expiry,
        scope=scope.value,
    )


async def insert_token(conn: Connection, token: TokenModel) -> None:
    """CRUD operation: Insert a token into the database.

    Args:
        conn: The database connection.
        token: The token model.
    """
    query = """
    INSERT INTO tokens (hash, user_id, expiry, scope)
    VALUES ($1, $2, $3, $4)
    """

    await conn.execute(
        query,
        token.hash.get_secret_value(),
        token.user_id,
        token.expiry,
        token.scope,
        timeout=3,
    )


async def new_token(
    conn: Connection, user_id: int, ttl: timedelta, scope: Scope
) -> TokenModel:
    """Generate a new token, insert it into the database, and return the token.

    Args:
        conn: The database connection.
        user_id: The user ID to associate with the token.
        ttl: The time-to-live for the token.
        scope: The scope of the token.

    Returns:
        A token model.
    """
    token = create_token(user_id, ttl, scope)
    await insert_token(conn, token)

    return token


async def delete_all_for_user(conn: Connection, user_id: int, scope: Scope) -> None:
    """CRUD operation: Delete all tokens for a user.

    Args:
        conn: The database connection.
        user_id: The user ID to delete tokens for.
        scope: The scope of the tokens to delete.
    """
    query = """
    DELETE FROM tokens WHERE scope = $1 AND user_id = $2
    """

    await conn.execute(query, scope, user_id, timeout=3)

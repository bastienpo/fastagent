"""Password hashing and verification."""

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

_hasher = PasswordHasher(
    time_cost=4,
)


def verify_password(password: str, password_hash: bytes) -> bool:
    """Verify a password against a hashed password.

    Args:
        password: The password to verify.
        password_hash: The hashed password to verify against.

    Returns:
        True if the password is correct, False otherwise.
    """
    try:
        return _hasher.verify(password_hash, password)
    except VerificationError:
        return False


def hash_password(password: str) -> bytes:
    """Hash a password using Argon2id.

    Args:
        password: The password to hash.

    Returns:
        The hashed password as a bytes object.
    """
    return _hasher.hash(password).encode("utf-8")

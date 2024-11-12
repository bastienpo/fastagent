"""Request context."""

from app.internal.data.users import UserModel
from pydantic import BaseModel


class Context(BaseModel):
    """Context."""

    user: UserModel

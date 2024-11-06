"""Request context."""

from pydantic import BaseModel

from app.internal.data.users import UserModel


class Context(BaseModel):
    """Context."""

    user: UserModel

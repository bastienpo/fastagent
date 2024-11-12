"""Request context."""

from pydantic import BaseModel

from fastagent.internal.data.users import UserModel


class Context(BaseModel):
    """Context."""

    user: UserModel

"""Agent data."""

from pydantic import BaseModel


class AgentInvoke(BaseModel):
    """Agent invoke payload."""

    messages: str

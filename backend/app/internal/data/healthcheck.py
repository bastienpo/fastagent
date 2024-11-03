"""Healthcheck data models."""

from typing import Literal

from pydantic import BaseModel


class SystemInfo(BaseModel):
    """System information."""

    version: str
    environment: Literal["development", "staging", "production"]


class Healthcheck(BaseModel):
    """Healthcheck response."""

    status: Literal["available", "unavailable", "error"]
    system_info: SystemInfo

"""Configuration of the API."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration used by the application."""

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=False,
        validate_default=True,
        extra="ignore",
        frozen=True,
        case_sensitive=False,
    )

    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="The environment."
    )

    granian_port: int = Field(description="The port to use.")

    granian_reload: bool = Field(description="Whether to reload the application.")

    granian_interface: Literal["asgi", "asginl"] = Field(
        description="The interface to use."
    )

    granian_loop: Literal["uvloop", "asyncio"] = Field(
        description="The event loop to use."
    )

    db_database: str = Field(description="The database name.")

    db_user: str = Field(description="The database user.")

    db_host: str = Field(description="The database host.", default="localhost")

    db_password: str = Field(description="The database password.")

    db_port: int = Field(description="The database port.")

    def get_dsn(self: "Settings") -> str:
        """Get the Data Source Name."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the configuration."""
    return Settings()

"""Configuration of the API."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Database settings."""

    user: str = Field(description="The database user.")

    password: str = Field(description="The database password.")

    def get_dsn(self: "DatabaseSettings", name: str, host: str, port: int) -> str:
        """Get the Data Source Name."""
        return f"postgresql://{self.user}:{self.password}@{host}:{port}/{name}"


class Settings(BaseSettings):
    """Configuration used by the application."""

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=False,
        validate_default=True,
        extra="ignore",
        frozen=True,
        case_sensitive=False,
        env_nested_delimiter="_",
    )

    database: DatabaseSettings = Field(description="Database settings.", alias="db")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the configuration."""
    return Settings()


SettingsDependency = Annotated[Settings, Depends(get_settings)]

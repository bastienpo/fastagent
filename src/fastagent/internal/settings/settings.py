"""Configuration of the API."""

from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GranianSettings(BaseModel):
    """Granian settings."""

    port: int = Field(description="The port to use.")

    reload: bool = Field(description="Whether to reload the application.")

    interface: Literal["asgi", "asginl"] = Field(description="The interface to use.")

    loop: Literal["uvloop", "asyncio"] = Field(description="The event loop to use.")

    workers: int = Field(description="The number of workers to use.")


class DatabaseSettings(BaseModel):
    """Database settings."""

    database: str = Field(description="The database name.")

    user: str = Field(description="The database user.")

    host: str = Field(description="The database host.", default="localhost")

    password: str = Field(description="The database password.")

    port: int = Field(description="The database port.")

    def get_dsn(self: "DatabaseSettings") -> str:
        """Get the Data Source Name."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


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

    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="The environment."
    )

    granian: GranianSettings = Field(description="Granian settings.", alias="granian")

    database: DatabaseSettings = Field(description="Database settings.", alias="db")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the configuration."""
    return Settings()


SettingsDependency = Annotated[Settings, Depends(get_settings)]

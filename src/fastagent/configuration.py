"""Configuration for the project."""

import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, Field


class Project(BaseModel):
    """Project configuration.

    User configuration for the project with the project name, framework and app.

    App is the entrypoint to the application in the format `module:attribute`.

    For langchain this is typically `app.main:chain`. where chain is the LangChain Runnable.
    """  # noqa: E501

    name: str = Field(default="fastagent")
    framework: Literal["langchain", "langgraph", "dspy"] = Field(default="langchain")
    app: str = Field(default="app.main:api")


class Storage(BaseModel):
    """Storage configuration."""

    database: Literal["postgresql"] | None = Field(default=None)
    name: str | None = Field(default=None)
    host: str | None = Field(default=None)
    port: int | None = Field(default=None)


class Server(BaseModel):
    """Server configuration.

    Main configuration for granian server.
    """

    port: int = Field(default=8000)
    host: str = Field(default="127.0.0.1")
    workers: int = Field(default=1)
    logging: bool = Field(default=True)
    log_level: Literal["debug", "info", "warning", "error"] = Field(default="info")


class Security(BaseModel):
    """Security configuration.

    Configuration for the authentication and support for HTTPS.

    Choosing a authentication will require a database or backend service.

    Currently only supports Postgresql.
    """

    authentication: Literal["stateful-postgresql"] | None = Field(default=None)
    allowed_origins: list[str] = Field(default=["*"])
    allow_credentials: bool = Field(default=False)
    ssl_cert: str | None = Field(default=None)
    ssl_key: str | None = Field(default=None)


class Config(BaseModel):
    """Configuration for the project.

    Pydantic model for the configuration holding all the configuration options.

    Configuration is read from a TOML file and validated against the Pydantic model.
    """

    project: Project = Field(default=Project())
    security: Security = Field(default=Security())
    storage: Storage = Field(default=Storage())
    server: Server = Field(default=Server())

    @classmethod
    def from_file(cls: type["Config"], path: str = "fastagent.toml") -> "Config":
        """Read the configuration from the given path.

        Args:
            path: The path to read the configuration from.

        Returns:
            The configuration object.
        """
        with Path(path).open("rb") as file:
            config_dict = tomllib.load(file)
            return cls.model_validate(config_dict)

    def write(self: "Config", path: str = "fastagent.toml") -> None:
        """Write the configuration to the given path.

        Args:
            path: The path to write the configuration to.
        """
        config_dict = self.model_dump(
            exclude_none=True,
            exclude=["reload", "logging", "log_level"],
        )

        with Path(path).open("w") as file:
            toml_config = tomli_w.dumps(config_dict)
            file.write(toml_config)

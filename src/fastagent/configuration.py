"""Configuration for the project."""

import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, Field, PrivateAttr


class Project(BaseModel):
    """Project configuration.

    User configuration for the project with the project name, framework and app.

    App is the entrypoint to the application in the format `module:attribute`.

    For langchain this is typically `app.main:chain`. where chain is the LangChain Runnable.
    """  # noqa: E501

    name: str = Field(default="fastagent")
    framework: Literal["langchain", "langgraph", "dspy"] = Field(default="langchain")
    app: str = Field(default="app.main:api")
    database: Literal["postgresql"] | None = Field(default=None)


class Server(BaseModel):
    """Server configuration.

    Main configuration for granian server.
    """

    port: int = Field(default=8000)
    host: str = Field(default="127.0.0.1")
    _reload: bool = PrivateAttr(default=True)
    _logging: bool = PrivateAttr(default=True)
    _log_level: Literal["debug", "info", "warning", "error"] = PrivateAttr(
        default="info"
    )


class Security(BaseModel):
    """Security configuration.

    Configuration for the authentication and support for HTTPS.

    Choosing a authentication will require a database or backend service.

    Currently only supports Postgresql.
    """

    authentication: bool = Field(default=False)
    ssl_cert: str | None = Field(default=None)
    ssl_key: str | None = Field(default=None)


class Config(BaseModel):
    """Configuration for the project.

    Pydantic model for the configuration holding all the configuration options.

    Configuration is read from a TOML file and validated against the Pydantic model.
    """

    _environment: Literal["development", "production"] = PrivateAttr(
        default="development"
    )

    project: Project = Field(default=Project())
    security: Security = Field(default=Security())
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
        config_dict = self.model_dump(exclude_none=True)

        with Path(path).open("w") as file:
            toml_config = tomli_w.dumps(config_dict)
            file.write(toml_config)

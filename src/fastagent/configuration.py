"""Configuration for the project."""

import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, Field, PrivateAttr


class Project(BaseModel):
    """Project configuration."""

    name: str = Field(default="fastagent")
    framework: Literal["langchain", "langgraph", "dspy"] = Field(default="langchain")
    app: str = Field(default="app.main:api")
    database: Literal["postgresql"] | None = Field(default=None)


class Server(BaseModel):
    """Server configuration."""

    port: int = Field(default=8000)
    host: str = Field(default="127.0.0.1")
    _reload: bool = PrivateAttr(default=True)
    _logging: bool = PrivateAttr(default=True)
    _log_level: Literal["debug", "info", "warning", "error"] = PrivateAttr(
        default="info"
    )


class Security(BaseModel):
    """Security configuration."""

    authentication: bool = Field(default=False)
    ssl_cert: str | None = Field(default=None)
    ssl_key: str | None = Field(default=None)


class Config(BaseModel):
    """Configuration for the project."""

    project: Project = Field(default=Project())
    security: Security = Field(default=Security())
    server: Server = Field(default=Server())

    @classmethod
    def from_file(cls: type["Config"], path: str = "fastagent.toml") -> "Config":
        """Read the configuration from the given path.

        Args:
            path: The path to read the configuration from.
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

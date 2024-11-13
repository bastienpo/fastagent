"""Configuration for the project."""

import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, Field


class Project(BaseModel):
    """Project configuration."""

    name: str = Field(default="fastagent")
    database: Literal["postgresql", "none"] = Field(default="none")


class Server(BaseModel):
    """Server configuration."""

    port: int = Field(default=8000)
    host: str = Field(default="127.0.0.1")
    reload: bool = Field(default=True)


class Security(BaseModel):
    """Security configuration."""

    authentication: bool = Field(default=False)


class Tool(BaseModel):
    """Tool configuration."""

    framework: Literal["langchain"] = Field(default="langchain")


class Configuration(BaseModel):
    """Configuration for the project."""

    project: Project = Field(default=Project())
    security: Security = Field(default=Security())
    tool: Tool = Field(default=Tool())
    server: Server = Field(default=Server())

    @classmethod
    def from_file(
        cls: type["Configuration"], path: str = "fastagent.toml"
    ) -> "Configuration":
        """Read the configuration from the given path.

        Args:
            path: The path to read the configuration from.
        """
        with Path(path).open("rb") as file:
            config_dict = tomllib.load(file)
            return cls.model_validate(config_dict)

    def write(self: "Configuration", path: str = "fastagent.toml") -> None:
        """Write the configuration to the given path.

        Args:
            path: The path to write the configuration to.
        """
        config_dict = self.model_dump()

        with Path(path).open("w") as file:
            toml_config = tomli_w.dumps(config_dict)
            file.write(toml_config)

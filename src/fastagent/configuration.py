"""Configuration for the project."""

import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """Configuration for the project."""

    name: str = Field(default="fastagent")
    auth_backend: Literal["postgresql"] | None = Field(default=None)
    agent_framework: Literal["langchain"] | None = Field(default=None)

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

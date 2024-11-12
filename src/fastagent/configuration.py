"""Configuration for the project."""

from pathlib import Path

import toml
from pydantic import BaseModel


class Configuration(BaseModel):
    """Configuration for the project."""

    project_name: str
    auth_backend: str
    agent_backend: str


def read_configuration(path: str) -> Configuration:
    """Read the configuration from the given path."""
    with Path(path).open() as file:
        return Configuration(**toml.load(file))


def write_configuration(path: str, configuration: dict) -> None:
    """Write the configuration to the given path."""
    header = "[tool.fastagent]\n"

    config = Configuration(**configuration)

    with Path(path).open("w") as file:
        file.write(header)
        toml.dump(config.model_dump(), file)

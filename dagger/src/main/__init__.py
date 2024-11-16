from typing import Annotated

import dagger
from dagger import dag, function, object_type


@object_type
class Pipeline:
    """Pipeline class."""

    async def _get_ruff_container(
        self, directory: dagger.Directory, config: dagger.File
    ) -> dagger.Container:
        return (
            dag.container()
            .from_("ghcr.io/astral-sh/uv:python3.12-bookworm-slim")
            .with_env_variable("UV_COMPILE_BYTECODE", "1")
            .with_env_variable("UV_LINK_MODE", "copy")
            .with_mounted_directory("src", directory)
            .with_workdir("src")
            .with_mounted_file(".ruff.toml", config)
            .with_exec(["uv", "tool", "install", "ruff"])
        )

    @function
    async def format(
        self, directory: dagger.Directory, config: dagger.File, output_format: str
    ) -> str:
        """Formats the files in the provided Directory.

        Output format can be found in ruff documentation.
        """
        ruff_container = await self._get_ruff_container(directory, config)

        return await ruff_container.with_exec(
            [
                "uv",
                "tool",
                "run",
                "ruff",
                "format",
                ".",
                "--config",
                ".ruff.toml",
                "--check",
            ]
        ).stdout()

    @function
    async def lint(
        self, directory: dagger.Directory, config: dagger.File, output_format: str
    ) -> str:
        """Returns lines that match a pattern in the files of the provided Directory.

        Output format can be found in ruff documentation.
        """
        ruff_container = await self._get_ruff_container(directory, config)

        return await ruff_container.with_exec(
            [
                "uv",
                "tool",
                "run",
                "ruff",
                "check",
                ".",
                "--config",
                ".ruff.toml",
                "--output-format",
                output_format,
            ]
        ).stdout()

    @function
    async def build_and_push(
        self,
        context: dagger.Directory,
        registry: Annotated[str, "The registry to push the image to."],
        username: Annotated[str, "The username to use for authentication."],
        secret: Annotated[dagger.Secret, "The GitHub token secret."],
        image_name: Annotated[str, "The name of the image to push."],
    ) -> dagger.Container:
        """Builds the Docker image and pushes it to the registry."""
        build = (
            dag.container()
            .build(context)
            .with_registry_auth(
                address=f"{registry}/{image_name}", username=username, secret=secret
            )
        )

        return await build.publish(f"{registry}/{image_name}")

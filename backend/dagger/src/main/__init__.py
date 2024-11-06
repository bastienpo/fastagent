import dagger
from dagger import dag, function, object_type


@object_type
class ContiniousIntegrationPipeline:
    """Continious integration pipeline class."""

    @function
    async def format(self, directory: dagger.Directory) -> str:
        """Formats the files in the provided Directory."""
        return await (
            dag.container()
            .from_("ghcr.io/astral-sh/uv:python3.12-bookworm-slim")
            .with_env_variable("UV_COMPILE_BYTECODE", "1")
            .with_env_variable("UV_LINK_MODE", "copy")
            .with_mounted_directory("src", directory)
            .with_workdir("src")
            .with_exec(["uv", "tool", "install", "ruff"])
            .with_exec(["uv", "tool", "run", "ruff", "format", "."])
            .stdout()
        )

    @function
    async def lint(self, directory: dagger.Directory) -> str:
        """Returns lines that match a pattern in the files of the provided Directory."""
        return await (
            dag.container()
            .from_("ghcr.io/astral-sh/uv:python3.12-bookworm-slim")
            .with_env_variable("UV_COMPILE_BYTECODE", "1")
            .with_env_variable("UV_LINK_MODE", "copy")
            .with_mounted_directory("src", directory)
            .with_workdir("src")
            .with_exec(["uv", "tool", "install", "ruff"])
            .with_exec(["uv", "tool", "run", "ruff", "check", "."])
            .stdout()
        )

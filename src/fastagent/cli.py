"""FastAgent CLI."""

from pathlib import Path

import questionary
import typer
from granian.server import Granian
from rich.console import Console
from rich.panel import Panel

from fastagent.app import api
from fastagent.configuration import Configuration, write_configuration
from fastagent.integrations import create_langchain_router
from fastagent.internal import ModuleLoader
from fastagent.routers import healthcheck

app = typer.Typer(
    name="fastagent",
    help="fastagent is a tool making it easy to ship your agent to production. More information at https://github.com/bastienpo/fastagent.",  # noqa: E501
)


@app.command()
def init() -> None:
    """Initialize the configuration for the project.

    This command will prompt you for the project configuration.

    The configuration is then saved in a fastagent.toml file in your project root.

    Current configuration options: project name, authentication (PostgreSQL or None), agent framework (LangChain).
    """  # noqa: E501
    console = Console()

    configuration = Configuration()

    console.print(Panel.fit("Welcome to FastAgent 🚀", style="bold green"))

    if Path("fastagent.toml").exists() or Path(".fastagent.toml").exists():
        console.print("\n[bold red]❌ Configuration file already exists![/bold red]")
        return

    # Project name
    configuration.project_name = questionary.text(
        message="What is your project name?",
        style=questionary.Style(
            [
                ("qmark", "fg:blue bold"),
                ("question", "bold"),
                ("answer", "fg: cyan bold"),
            ]
        ),
        default=Path.cwd().name,
    ).ask()

    # Authentication choice
    console.print("\n[bold yellow]Authentication Backend Options:[/bold yellow] 🔐")
    configuration.auth_backend = questionary.select(
        message="Choose your authentication backend:",
        choices=[
            {"name": "📦 PostgreSQL", "value": "postgresql"},
            {"name": "🚫 No Authentication", "value": None},
        ],
        style=questionary.Style(
            [
                ("selected", "fg:cyan bold"),
                ("pointer", "fg:green bold"),
            ]
        ),
    ).ask()

    # Agent backend selection
    console.print("\n[bold yellow]Agent Backend Options:[/bold yellow] 🤖")
    configuration.agent_framework = questionary.select(
        message="Choose your agent framework:",
        choices=[
            {"name": "🦜 LangChain", "value": "langchain"},
        ],
        style=questionary.Style(
            [
                ("selected", "fg:cyan bold"),
                ("pointer", "fg:green bold"),
            ]
        ),
    ).ask()

    write_configuration("fastagent.toml", configuration)

    console.print("\n[bold green]✅ Configuration completed successfully![/bold green]")


@app.command()
def dev(
    target: str,
    host: str = "127.0.0.1",
    port: int = 8000,
    *,
    reload: bool = True,
) -> None:
    """Launch a development server for your agent.

    The server will match the configuration you have set in the `fastagent.toml` or `.fastagent.toml` file.

    The server will reload on code changes if the `--reload` flag is set.
    """
    console = Console()

    runnable = ModuleLoader.load_from_string(target)
    api.include_router(create_langchain_router(runnable))
    api.include_router(healthcheck.router)

    granian = Granian(
        target="fastagent.app:api",
        address=host,
        port=port,
        reload=reload,
        interface="asgi",
        loop="uvloop",
        log_enabled=True,
    )

    # Print the running message with the target and port
    console.print(
        Panel.fit(
            f"Running FastAgent CLI in development mode 🚀 \n\n"
            f"The application is available at [bold green]http://{host}:{port}[/bold green]",  # noqa: E501
            style="bold green",
        )
    )

    granian.serve()


@app.command()
def run() -> None:
    """Run the FastAgent CLI."""


@app.command()
def build() -> None:
    """Build the FastAgent CLI."""

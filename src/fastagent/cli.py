"""FastAgent CLI."""

import asyncio
from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from fastagent.configuration import Config
from fastagent.internal.data import setup_postgresql_database
from fastagent.server import FastAgentServer

app = typer.Typer(
    name="fastagent",
    help="fastagent is a tool making it easy to ship your agent to production. More information at https://github.com/bastienpo/fastagent.",  # noqa: E501
)


@app.command()
def init(name: str | None = None, template: str | None = None) -> None:
    """Initialize the configuration for the project.

    This command will prompt you for the project configuration.

    The configuration is then saved in a fastagent.toml file in your project root.

    Current configuration options: project name, authentication (PostgreSQL or None), agent framework (LangChain).
    """  # noqa: E501
    console = Console()

    console.print(Panel.fit("Welcome to FastAgent 🚀", style="bold green"))

    config = Config()

    if Path("fastagent.toml").exists() or Path(".fastagent.toml").exists():
        console.print("\n[bold red]❌ Configuration file already exists![/bold red]")
        return

    if name is None:
        # Project name
        config.project.name = questionary.text(
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
    else:
        config.project.name = name

    if template is None:
        # Agent backend selection
        console.print("\n[bold yellow]Agent Backend Options:[/bold yellow] 🤖")
        config.project.framework = questionary.select(
            message="Choose your agent framework:",
            choices=[
                {"name": "🦜️ LangChain", "value": "langchain"},
                # {"name": "LangGraph", "value": "langgraph"},  # noqa: ERA001
                # {"name": "DsPy", "value": "dspy"},  # noqa: ERA001
            ],
            style=questionary.Style(
                [
                    ("selected", "fg:cyan bold"),
                    ("pointer", "fg:green bold"),
                ]
            ),
        ).ask()
    else:
        config.project.framework = "langchain"

    config.write(path="fastagent.toml")
    console.print("\n[bold green]✅ Configuration completed successfully![/bold green]")


@app.command()
def setup() -> None:
    """Setup the project database. Applies migrations if needed.

    This command will create the user and token tables in the database if they don't exist.
    """  # noqa: E501
    console = Console()

    console.print("[bold green]Setting up the project...[/bold green]")

    try:
        config = Config.from_file(path="fastagent.toml")
    except FileNotFoundError:
        console.print("[bold red]❌ Configuration file not found![/bold red]")
        return

    # TODO: Remove this once we have a proper way to get the DSN from the configuration  # noqa: E501, FIX002, TD002, TD003
    test_dsn = "postgresql://postgres:postgres@localhost:5432/fastagent"

    if (
        config.storage.database
        and config.security.authentication == "stateful-postgresql"
    ):
        console.print(
            f"[bold green]Setting up the user and token tables in the {config.storage.database} database...[/bold green]"  # noqa: E501
        )

        if config.storage.database == "postgresql":
            asyncio.run(setup_postgresql_database(test_dsn))


@app.command()
def dev() -> None:
    """Launch a development server for your agent.

    The server will match the configuration you have set in the `fastagent.toml` or `.fastagent.toml` file.
    """  # noqa: E501
    console = Console()

    config = Config.from_file(path="fastagent.toml")
    server = FastAgentServer(configuration=config, environment="dev")

    # Print the running message with the target and port
    console.print(
        Panel.fit(
            f"Running fastagent server in development mode 🚀 \n\n"
            f"The application is available at [bold green]http://{config.server.host}:{config.server.port}[/bold green]",  # noqa: E501
            style="bold green",
        )
    )

    server.serve()


@app.command()
def run() -> None:
    """Run the FastAgent CLI."""
    console = Console()

    config = Config.from_file(path="fastagent.toml")
    server = FastAgentServer(configuration=config, environment="prod")

    console.print(
        Panel.fit(
            f"Running fastagent server in production mode 🚀 \n\n"
            f"The application is available at [bold green]http://{config.server.host}:{config.server.port}[/bold green]",  # noqa: E501
            style="bold blue",
        )
    )

    server.serve()

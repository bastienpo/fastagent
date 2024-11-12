"""FastAgent CLI."""

from pathlib import Path

import questionary
import typer
from granian.server import Granian
from rich.console import Console
from rich.panel import Panel

from fastagent.configuration import write_configuration

app = typer.Typer()


@app.command()
def init() -> None:
    """Initialize the configuration for the project."""
    console = Console()

    configuration = {}

    console.print(Panel.fit("Welcome to FastAgent CLI 🚀", style="bold green"))

    if Path("./fastagent.toml").exists() or Path("./.fastagent.toml").exists():
        console.print("\n[bold red]❌ Configuration file already exists![/bold red]")
        return

    # Project name
    configuration["project_name"] = questionary.text(
        "What is your project name?",
        style=questionary.Style(
            [
                ("qmark", "fg:blue bold"),
                ("question", "bold"),
                ("answer", "fg:cyan bold"),
            ]
        ),
    ).ask()

    # Authentication choice
    console.print("\n[bold yellow]Authentication Backend Options:[/bold yellow] 🔐")
    configuration["auth_backend"] = questionary.select(
        "Choose your authentication backend:",
        choices=[
            {"name": "📦 PostgreSQL", "value": "postgresql"},
            {"name": "🚫 No Authentication", "value": "none"},
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
    configuration["agent_backend"] = questionary.select(
        "Choose your agent backend:",
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

    write_configuration("./fastagent.toml", configuration)

    console.print("\n[bold green]✅ Configuration completed successfully![/bold green]")


@app.command()
def dev(
    target: str,
    host: str = "127.0.0.1",
    port: int = 8000,
    *,
    reload: bool = False,
) -> None:
    """Run the FastAgent CLI in development mode."""
    console = Console()
    if not Path("./.fastagent.toml").exists():
        console.print(
            Panel.fit(
                "[bold red]❌ Configuration file not found![/bold red]",
                style="bold red",
            )
        )
        return

    granian = Granian(
        target=target,
        address=host,
        port=port,
        reload=reload,
        interface="asgi",
        loop="uvloop",
        log_enabled=False,
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

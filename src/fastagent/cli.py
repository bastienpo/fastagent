"""FastAgent CLI."""

from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from fastagent.configuration import Configuration
from fastagent.internal import ModuleLoader
from fastagent.internal.server import FastAgentServer

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
    configuration.project.name = questionary.text(
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

    console.print("\n[bold yellow] Database Options:[/bold yellow] 🔐")
    configuration.project.database = questionary.select(
        message="Choose your database:",
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
    configuration.tool.framework = questionary.select(
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

    configuration.write(path="fastagent.toml")
    console.print("\n[bold green]✅ Configuration completed successfully![/bold green]")


@app.command()
def dev(
    target: str,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    """Launch a development server for your agent.

    The server will match the configuration you have set in the `fastagent.toml` or `.fastagent.toml` file.

    The server will reload on code changes if the `--reload` flag is set.
    """  # noqa: E501
    console = Console()

    agent_module = ModuleLoader.load_from_string(target)
    if Path("fastagent.toml").exists():
        configuration = Configuration.from_file("fastagent.toml")
    elif Path(".fastagent.toml").exists():
        configuration = Configuration.from_file(".fastagent.toml")
    else:
        console.print(
            "[bold red]❌ No configuration file found![/bold red]\n\n"
            "Please run `fastagent init` to create a configuration file."
        )
        return

    server = FastAgentServer(configuration, agent_module)

    # Print the running message with the target and port
    console.print(
        Panel.fit(
            f"Running FastAgent CLI in development mode 🚀 \n\n"
            f"The application   is available at [bold green]http://{host}:{port}[/bold green]",  # noqa: E501
            style="bold green",
        )
    )

    server.serve()


@app.command()
def run() -> None:
    """Run the FastAgent CLI."""


@app.command()
def build() -> None:
    """Build the FastAgent CLI."""

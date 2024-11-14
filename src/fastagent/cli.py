"""FastAgent CLI."""

from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from fastagent.configuration import Config
from fastagent.internal.server import FastAgentServer

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
                {"name": "LangChain", "value": "langchain"},
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
def dev() -> None:
    """Launch a development server for your agent.

    The server will match the configuration you have set in the `fastagent.toml` or `.fastagent.toml` file.
    """  # noqa: E501
    console = Console()

    config = Config.from_file(path="fastagent.toml")
    server = FastAgentServer(configuration=config)

    # Print the running message with the target and port
    console.print(
        Panel.fit(
            f"Running FastAgent CLI in development mode 🚀 \n\n"
            f"The application is available at [bold green]http://{config.server.host}:{config.server.port}[/bold green]",  # noqa: E501
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

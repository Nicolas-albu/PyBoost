"""This module contains all PyBoost CLI commands."""

from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from typer import Option, Typer

from .core import (
    Generator,
    generate_pyboost_json,
    get_current_path,
    get_path_name,
    get_testing_path,
    processing_directory,
)

console = Console()
app = Typer(pretty_exceptions_show_locals=False)


@app.command(help="Configure PyBoost for python projects.")
def project_settings(
    name_project: str = Option(
        get_path_name(),
        "--name-project",
        "-np",
        help="The name of the project. Defaults to the current directory name.",
    ),
    directory: Path = Option(
        get_current_path(),
        "--directory",
        "-d",
        help="The directory of the project. Defaults to the current directory.",
    ),
    add_python_version: str = Option(
        ...,
        "--python-version",
        "-pv",
        help="Add the .python-version file to the project with the specified Python version.",
    ),
    add_poetry: bool = Option(
        False,
        "--add-poetry",
        "-poetry",
        "-p",
        help="Use Poetry to manage the project dependencies instead of pip and virtualenv",
    ),
    add_dotenv: bool = Option(
        False,
        "--add-dotenv",
        "-dotenv",
        "-env",
        help="Configure and add dotenv file to project.",
    ),
    add_format: bool = Option(
        False,
        "--add-format",
        "-format",
        "-f",
        help="Add the black formatter and isort.",
    ),
    add_makefile: bool = Option(
        False,
        "--add-makefile",
        "-makefile",
        "-make",
        help="Add makefile to project.",
    ),
    with_django: bool = Option(
        False, "--with-django", "-dj", help="Add Django Framework to project."
    ),
    with_tailwind: bool = Option(
        False, "--with_tailwind", "-tw", help="Add TalwindCSS to project."
    ),
) -> None:
    """Configure PyBoost for Python projects.

    Args:
        name_project: The name of the project.
        directory: The directory of the project.
        add_python_version: Add the .python-version file to the project with the specified Python version.
        add_poetry: Use Poetry to manage the project dependencies instead of pip and virtualenv.
        add_dotenv: Configure and add dotenv file to project.
        add_format: Add the black formatter and isort to the project.
        add_makefile: Add a makefile to the project.
        with_django: Add the Django Framework to the project.
        with_tailwind: Add the TailwindCSS to the project.
    """
    directory = processing_directory(directory)
    directory = get_testing_path()

    params: dict[str, str | bool | Path] = {
        "name_project": name_project,
        "directory": directory,
        "add_python_version": add_python_version,
        "add_poetry": add_poetry,
        "add_dotenv": add_dotenv,
        "add_format": add_format,
        "add_makefile": add_makefile,
        "with_django": with_django,
        "with_tailwind": with_tailwind,
    }

    with Progress() as progress:
        task_generate_pyboost_json = progress.add_task(
            "[bold yellow]Generate pyboost.json", total=100
        )
        task_create_files = progress.add_task(
            "[bold red]Creating files[/bold red]", total=100
        )

        while not progress.finished:
            progress.update(task_generate_pyboost_json, advance=0.5)
            progress.update(task_create_files, advance=0.5)

        generate_pyboost_json(**params)
        Generator(**params).run()

    console.print_json((directory / "pyboost.json").read_text())
    console.print(
        f"\n[bold green]{name_project} configured![/bold green] :rocket:"
    )

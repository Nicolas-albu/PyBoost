"""This module contains all PyBoost CLI commands."""

from rich.console import Console
from rich.progress import Progress
from typer import Option, Typer

from .core import generate_pyboost_json, get_current_path, get_path_name

console = Console()
app = Typer(pretty_exceptions_show_locals=False)


@app.command(help="Configure PyBoost for python projects.")
def project_settings(
    name_project: str = Option(
        get_path_name(),
        "--name-project",
        "-np",
        help="The name of the project.",
    ),
    add_python_version: str = Option(
        ...,
        "--python-version",
        "-pv",
        help="Add the .python-version file to the project.",
    ),
    add_poetry: bool = Option(
        False,
        "--add-poetry",
        "-poetry",
        "-p",
        help="Add the poetry to project.",
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
    """Configure PyBoost for python projects.

    Args:
        name_project (str, optional): Option to choose the name of the project.
        add_python_version (float, required): Option needed to add python version file (.python-version).
        add_poetry (bool, optional): Option to add person to project. Otherwise, pip will be used with virtualenv.
        add_dotenv (bool, optional): Option to add the dotenv file to the project.
        add_format (bool, optional): Option to add black formatter and isort.
        add_makefile (bool, optional): Option to add makefile to project.
        with_django (bool, optional): Option to add Django Framework to project.
        with_tailwind (bool, optional): Option to add TailwindCSS to project.
    """
    with Progress() as progress:
        task_generate_pyboost_json = progress.add_task(
            "[bold yellow]Generate pyboost.json", total=100
        )

        while not progress.finished:
            progress.update(task_generate_pyboost_json, advance=0.5)

            generate_pyboost_json(
                name_project=name_project,
                add_python_version=add_python_version,
                add_poetry=add_poetry,
                add_dotenv=add_dotenv,
                add_format=add_format,
                add_makefile=add_makefile,
                with_django=with_django,
                with_tailwind=with_tailwind,
            )

    console.print_json((get_current_path() / "pyboost.json").read_text())
    console.print(
        f"\n[bold green]{name_project} configured![/bold green] :rocket:"
    )

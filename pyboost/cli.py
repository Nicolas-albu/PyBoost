from rich.console import Console
from typer import Option, Typer

from .core import get_path_name

console = Console()
app = Typer()


@app.command(help="Configure PyBoost for python projects.")
def project_settings(
    name_project: str = Option(
        get_path_name(),
        "--name-project",
        "-np",
        help="The name of the project.",
    ),
    add_python_version: float = Option(
        ...,
        "--python-version",
        "-pv",
        help="Add the .python-version file to the project.",
    ),
    add_poetry: bool = Option(
        ..., "--add-poetry", "-poetry", "-p", help="Add the poetry to project."
    ),
    add_dotenv: bool = Option(
        ...,
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
        add_python_version (float, required): Option for python version.
        add_poetry (bool, required): Option needed to add poetry to the project.
        add_dotenv (bool, required): Option needed to add the dotenv file to the project.
        add_format (bool, optional): Option to add black formatter and isort.
        with_django (bool, optional): Option to add Django Framework to project.
        with_tailwind (bool, optional): Option to add TailwindCSS to project.
    """
    ...

"""
This module contains all PyBoot CLI commands.
"""

from pathlib import Path

from typer import Option, Typer

from .core import __CURRENT_PATH__, __PATH_NAME__, BeautifyConsole, PyBoot

beautify = BeautifyConsole()
app = Typer(pretty_exceptions_show_locals=False)


@app.command(help='Configure PyBoot for python projects.')
def pyboot_controller(
    name_project: str = Option(
        __PATH_NAME__,
        '--name-project',
        '-np',
        help=(
            'The name of the project. '
            'Defaults to the current directory name.'
        ),
    ),
    directory: Path = Option(
        __CURRENT_PATH__,
        '--directory',
        '-d',
        help=(
            'The directory of the project. '
            'Defaults to the current directory.'
        ),
    ),
    add_python_version: str = Option(
        ...,
        '--python-version',
        '-pv',
        help=(
            'Add the .python-version file '
            'to the project with the specified Python version.'
        ),
    ),
    add_dotenv: bool = Option(
        False,
        '--add-dotenv',
        '-dotenv',
        '-env',
        help='Configure and add dotenv file to project.',
    ),
    add_format: bool = Option(
        False,
        '--add-format',
        '-format',
        '-f',
        help='Add the black formatter and isort.',
    ),
    add_makefile: bool = Option(
        False,
        '--add-makefile',
        '-makefile',
        '-make',
        help='Add makefile to project.',
    ),
    with_drf: bool = Option(
        False,
        '--with-drf',
        '-drf',
        help='Add Django Rest Framework to project.',
    ),
) -> None:
    """Configure PyBoot for Python projects.

    Args:
        name_project: The name of the project.
        directory: The directory of the project.
        add_python_version: Add the .python-version file to the project with
            the specified Python version.
        add_poetry: Use Poetry to manage the project dependencies instead of
            pip and virtualenv.
        add_dotenv: Configure and add dotenv file to project.
        add_format: Add the black formatter and isort to the project.
        add_makefile: Add a makefile to the project.
        with_drf: Add the Django Rest Framework to the project.
    """

    if not isinstance(directory, Path):
        directory = Path(directory)

    params = {
        'name_project': name_project,
        'directory': directory,
        'add_python_version': add_python_version,
        'add_dotenv': add_dotenv,
        'add_format': add_format,
        'add_makefile': add_makefile,
        'with_drf': with_drf,
    }

    beautify.add_progressbar()
    PyBoot(**params).run()  # building projects with PyBoot configuration

    beautify.final_message_printing(directory, name_project)

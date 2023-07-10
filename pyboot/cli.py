"""
This module contains all PyBoot CLI commands.
"""

from pathlib import Path

from typer import Option, Typer

from .core import (
    __CURRENT_PATH__,
    __PATH_NAME__,
    BeautifyConsole,
    PyBootDirector,
)

beautify = BeautifyConsole()
app = Typer(pretty_exceptions_show_locals=False)


@app.command(help='Configure PyBoot for python projects.')
def pyboot_controller(
    project_name: str = Option(
        __PATH_NAME__,
        '--name-project',
        '-n',
        help=(
            'The name of the project. '
            'Defaults to the current directory name.'
        ),
    ),
    project_path: Path = Option(
        __CURRENT_PATH__,
        '--directory',
        '-d',
        help='The project path. Defaults to the current directory.',
    ),
    add_python_version: str = Option(
        ...,
        '--version',
        '-v',
        help=(
            'Add the .python-version file '
            'to the project with the specified Python version.'
        ),
    ),
    template: str = Option(
        None,
        '--template',
        '-t',
        help='The name of the template to be used.',
    ),
    add_format: bool = Option(
        False,
        '--format',
        '-f',
        help='Add the black formatter and isort.',
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
        project_path: The project path.
        add_python_version: Add the .python-version file to the project with
            the specified Python version.
        add_format: Add the black formatter and isort to the project.
        with_drf: Add the Django Rest Framework to the project.
    """

    if not template:
        template = beautify.ask_template()

    # building projects with PyBoot configuration
    pyboot = PyBootDirector(
        project_path=project_path,
        project_name=project_name,
        template=template,
        with_drf=with_drf,
        format=add_format,
        python_version=add_python_version,
    )

    beautify.add_status(pyboot)
    beautify.final_message(project_path, project_name)

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
    project_path: Path = Option(
        __CURRENT_PATH__,
        '--path',
        '-ph',
        help='The project path. Defaults to the current directory.',
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
    template: str = Option(
        None,
        '--template',
        '-t',
        help='The name of the template to be used.',
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
        project_path: The project path.
        add_python_version: Add the .python-version file to the project with
            the specified Python version.
        add_format: Add the black formatter and isort to the project.
        add_makefile: Add a makefile to the project.
        with_drf: Add the Django Rest Framework to the project.
    """

    if not template:
        template = beautify.ask_template()

    params = {
        'name_project': name_project,
        'project_path': project_path,
        'add_python_version': add_python_version,
        'template': template,
        'add_format': add_format,
        'add_makefile': add_makefile,
        'with_drf': with_drf,
    }

    # building projects with PyBoot configuration
    pyboot_project = PyBoot(**params)

    beautify.add_status(pyboot_project, name_project)
    beautify.final_message(project_path, name_project)

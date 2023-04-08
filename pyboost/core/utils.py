"""This module can contain functions or classes with general utilities that can be used throughout the project.
As functions for:

- get_path_name() -> str: Get the name of the folder where PyBoost is running.
- get_current_path() -> Path: Gets the current path directory.
- generate_pyboost_json(**params_json) -> None: Generate the PyBoost configuration file (pyboost.json).
"""

from json import dump
from pathlib import Path


def get_testing_path() -> Path:
    """Gets the path for testing the PyBoostCLI.

    Returns:
        Path: _description_
    """
    return Path().cwd() / "scripts" / "testing"


def get_path_name() -> str:
    """Gets the name of the folder where PyBoost is running.

    returns:
        str: returns the name of the folder.
    """
    return Path().cwd().name


def get_current_path() -> Path:
    """Gets the current path directory.

    Returns:
        Path: returns the directory of the current path.
    """
    return Path().cwd()


def generate_pyboost_json(**params_json) -> None:
    """Generate the PyBoost configuration file (pyboost.json).

    Args:
        name_project (str, optional): Option to choose the name of the project.
        add_python_version (str, required): Option needed to add python version file (.python-version).
        add_poetry (bool, optional): Option to add person to project. Otherwise, pip will be used with virtualenv.
        add_dotenv (bool, optional): Option to add the dotenv file to the project.
        add_format (bool, optional): Option to add black formatter and isort.
        add_makefile (bool, optional): Option to add makefile to project.
        with_django (bool, optional): Option to add Django Framework to project.
        with_tailwind (bool, optional): Option to add TailwindCSS to project.
    """
    # with open((get_current_path() / "pyboost.json"), "w") as file:
    with open((get_testing_path() / "pyboost.json"), "w") as file:
        dump(params_json, file, indent=4)

"""
This module provides the Builder class for project building operations.
"""

from json import dump
from pathlib import Path

from . import __NAME_CONFIG_FILE__


class Builder:
    """A class for building projects with PyBoost configuration.

    This class provides methods for generating configuration files and
    adding project files.
    """

    __slots__ = ['__directory']

    def __init__(self, *, directory: Path):
        """Initialize the Builder instance.

        Args:
            directory: The directory of the project.
        """
        self.__directory: Path = directory

    def generate_pyboost_json(self, data: dict, /) -> None:
        """Generate the PyBoost configuration file (pyboost.json).

        Args:
            data: The data to be written to the configuration file.
        """
        with open(
            self.__directory / __NAME_CONFIG_FILE__, "w", encoding="utf-8"
        ) as config_file:
            dump(data, config_file, indent=4)

    def add_main_folder(self, name_project: str, /) -> None:
        """Add a main folder to the project.

        Args:
            name_project: The name of the project.
        """
        main_folder: Path = self.__directory / name_project
        main_folder.mkdir(exist_ok=True)

    def add_dotenv_file(self, with_drf=False, /) -> None:
        """Add a .env file to the project.

        Args:
            with_drf: Whether to include Django Rest environment variables in
                the file.
        """
        environments = "" if not with_drf else ""

        with (self.__directory / ".env").open("w") as dotenv_file:
            dotenv_file.write(environments)

    def add_python_version_file(self, python_version: str, /) -> None:
        """Add a .python-version file to the project.

        Args:
            python_version: The Python version to be written in the file.
        """
        with (self.__directory / ".python-version").open(
            "w"
        ) as python_version_file:
            python_version_file.write(python_version)

    def add_makefile(self) -> None:
        """Add a Makefile to the project."""
        with (self.__directory / "Makefile").open("w") as _:
            ...

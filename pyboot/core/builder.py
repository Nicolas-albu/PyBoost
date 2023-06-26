"""
This module provides the Builder class for project building operations.
"""

import secrets
import shutil
from pathlib import Path
from string import printable

import toml
import yaml

from .environment import Environment
from .settings import (
    __GITIGNORE_DJANGO__,
    __NAME_CONFIG_FILE__,
    __SECRETS_CONF_DJANGO__,
    __SETTINGS_CONF_DJANGO__,
    __SETTINGS_DJANGO__,
)


class Builder:
    """
    A class for building projects with PyBoot configuration.

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

    def create_config_file(self, data: dict, /) -> None:
        """Generate the PyBoot configuration file.

        Args:
            data: The data to be written to the configuration file.
        """
        config_file = self.__directory / __NAME_CONFIG_FILE__

        with open(config_file, 'w', encoding='utf-8') as file:
            toml.dump(data, file)

    def add_folder(self, name_folder: str, /) -> None:
        """Add a folder to the project.

        Args:
            name_folder: The name of the folder.
        """
        folder: Path = self.__directory / name_folder
        folder.mkdir(exist_ok=True)

    def add_main_folder(self, venv: Environment, name_project: str, /) -> None:
        """Add a main folder to the project.

        Args:
            name_project: The name of the project.
        """
        command = (
            f'cd {self.__directory} '
            f'&& {venv.django_admin} startproject {name_project} .'
        )

        venv.execute(command)

    def configure_static_folder(self, venv: Environment, /) -> None:
        command = (
            f'cd {self.__directory} '
            f'&& {venv.venv_python} manage.py collectstatic'
        )

        venv.execute(command)

    def add_settings_files(self, name_project: str, /) -> None:
        settings_django_project = (
            self.__directory / name_project / 'settings.py'
        )

        settings_project = self.__directory / 'settings.yaml'
        settings_project.touch()

        secrets_project = self.__directory / '.secrets.yaml'
        secrets_project.touch()

        gitignore_project = self.__directory / '.gitignore'
        gitignore_project.touch()

        shutil.copy2(__SETTINGS_DJANGO__, settings_django_project)
        shutil.copy2(__SETTINGS_CONF_DJANGO__, settings_project)
        shutil.copy2(__SECRETS_CONF_DJANGO__, secrets_project)
        shutil.copy2(__GITIGNORE_DJANGO__, gitignore_project)

        with open(secrets_project, 'r', encoding='utf-8') as file:
            _secrets_config = yaml.safe_load(file)

        for stage in 'development', 'testing', 'production':
            _secrets_config[stage]['SECRET_KEY'] = self._generate_token(
                maxsize=60
            )

        with open(secrets_project, 'w', encoding='utf-8') as file:
            yaml.dump(_secrets_config, file)

    def add_python_version_file(self, python_version: str, /) -> None:
        """Add a .python-version file to the project.

        Args:
            python_version: The Python version to be written in the file.
        """
        python_version_file = self.__directory / '.python-version'

        with open(python_version_file, 'w') as file:
            file.write(python_version)

    def add_makefile(self) -> None:
        """Add a Makefile to the project."""
        makefile = self.__directory / 'Makefile'
        makefile.touch()

    @staticmethod
    def _generate_token(maxsize: int) -> str:
        characters = printable.replace(' ', '')
        _token = ''

        for _ in range(maxsize):
            _token += secrets.choice(characters)

        return _token

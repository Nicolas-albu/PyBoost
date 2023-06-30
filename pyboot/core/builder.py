"""
This module provides the Builder class for project building operations.
"""

import re
import secrets
import shutil
from pathlib import Path
from string import printable
from typing import Generator

import yaml

from .environment import Environment
from .reader import toml_dump
from .settings import (
    __ENVIRONMENT_STAGES__,
    __NAME_CONFIG_FILE__,
    template_django_blank,
)


class Builder:
    """
    A class for building projects with PyBoot configuration.

    This class provides methods for generating configuration files and
    adding project files.
    """

    __slots__ = ['__project_path']

    def __init__(self, *, project_path: Path):
        """Initialize the Builder instance.

        Args:
            project_path: The project path.
        """
        self.__project_path: Path = project_path

    def create_config_file(self, data: dict, /) -> None:
        """Generate the PyBoot configuration file.

        Args:
            data: The data to be written to the configuration file.
        """
        config_file = self.__project_path / __NAME_CONFIG_FILE__

        with open(config_file, 'w', encoding='utf-8') as file:
            toml_dump(data, file)

    def add_folder(self, name_folder: str, /) -> None:
        """Add a folder to the project.

        Args:
            name_folder: The name of the folder.
        """
        folder: Path = self.__project_path / name_folder
        folder.mkdir(exist_ok=True)

    def add_main_folder(
        self,
        venv: Environment,
        name_project: str,
        /,
    ) -> None:
        """Add a main folder to the project.

        Args:
            name_project: The name of the project.
        """
        command = (
            f'cd {self.__project_path} '
            f'&& {venv.django_admin} startproject {name_project} .'
        )

        venv.execute(command)

    def configure_static_folder(self, venv: Environment, /) -> None:
        command = (
            f'cd {self.__project_path} '
            f'&& {venv.venv_python} manage.py collectstatic'
        )

        venv.execute(command)

    def add_settings_files(self, name_project: str, /) -> None:
        settings_django_project = (
            self.__project_path / name_project / 'settings.py'
        )

        secrets_project = self.__project_path / '.secrets.yaml'

        target_files = (
            secrets_project,
            settings_django_project,
            self.__project_path / '.gitignore',
            self.__project_path / 'settings.yaml',
            self.__project_path / 'requirements.txt',
        )

        for source, target in zip(
            template_django_blank,
            target_files,
        ):
            target.touch()
            shutil.copy2(source, target)

        self._configure_dynaconf_secret_file(secrets_project)
        self._configure_settings_django(
            settings_django_project,
            name_project,
        )

    def _configure_dynaconf_secret_file(self, secrets_project: Path) -> None:
        with open(secrets_project, 'r', encoding='utf-8') as file:
            _secrets_config = yaml.safe_load(file)

        for stage in __ENVIRONMENT_STAGES__:
            _token = self._generate_token(maxsize=100)
            _secrets_config[stage]['SECRET_KEY'] = ''.join(tuple(_token))

        with open(secrets_project, 'w', encoding='utf-8') as file:
            yaml.dump(_secrets_config, file)

    @staticmethod
    def _configure_settings_django(
        settings_django: Path,
        name_project: str,
    ) -> None:
        with open(settings_django, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if "PROJECT_NAME = ''" in line:
                    line = f'PROJECT_NAME = {name_project!r}\n'
                file.write(line)

            # Truncates the rest of the file if it is smaller than the original
            file.truncate()

    def add_python_version_file(self, python_version: str, /) -> None:
        """Add a .python-version file to the project.

        Args:
            python_version: The Python version to be written in the file.
        """
        python_version_file = self.__project_path / '.python-version'

        with open(python_version_file, 'w') as file:
            file.write(python_version)

    def add_makefile(self) -> None:
        """Add a Makefile to the project."""
        makefile = self.__project_path / 'Makefile'
        makefile.touch()

    @staticmethod
    def _generate_token(maxsize: int) -> Generator:
        """Generate random tokens using secrets module and given size limit.

        Args:
            maxsize (int): The maximum size of the token.

        Yield:
            Generator: A generator that yields a random token.

        The method generates a token by selecting random characters from the
        printable ASCII characters. It removes any whitespace, backslashes,
        double quotes, and single quotes from the character set.
        """
        characters = re.sub(r'[\s]|[\\]|[\"\']', '', printable)

        yield from (secrets.choice(characters) for _ in range(maxsize))

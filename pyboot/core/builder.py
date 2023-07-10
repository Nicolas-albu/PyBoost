"""
This module provides the Builder class for project building operations.
"""

import re
import secrets
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from string import printable
from typing import Generator

import yaml

from .environment import Environment
from .reader import toml_dump
from .settings import __ENVIRONMENT_STAGES__, __NAME_CONFIG_FILE__
from .templates import django_blank

__all__ = ['AbstractBuilder', 'DjangoBlankBuilder', 'factory_builder']


class AbstractBuilder(ABC):
    def __init__(self, venv: Environment, options: dict):
        self._options = options
        self._project_path: Path = self._options['project_path']
        self._project_name = self._options['project_name']
        self._venv = venv

    @abstractmethod
    def add_main_folder(
        self,
        venv: Environment,
        project_name: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_settings_files(self, project_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> Generator:
        raise NotImplementedError

    @staticmethod
    def _configure_settings_django(
        settings_django: Path,
        project_name: str,
    ) -> None:
        with open(settings_django, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if "PROJECT_NAME = ''" in line:
                    line = f'PROJECT_NAME = {project_name!r}\n'
                file.write(line)

            # Truncates the rest of the file if it is smaller than the original
            file.truncate()

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

    @staticmethod
    def _add_folders(path: Path, *name_of_folders: str) -> None:
        """
        Create folders for the project.

        Args:
            *folders: Variable number of strings representing the names of the
                folders to be created.
        """
        for folder_name in name_of_folders:
            folder: Path = path / folder_name
            folder.mkdir(exist_ok=True)

    @staticmethod
    def _add_file(*, file_name: str, path: Path, content: str) -> None:
        with open(path / file_name, 'w', encoding='utf-8') as file:
            file.write(content)

    def _configure_dynaconf_secret_file(self, secrets_project: Path) -> None:
        with open(secrets_project, 'r', encoding='utf-8') as file:
            _secrets_config = yaml.safe_load(file)

        for stage in __ENVIRONMENT_STAGES__:
            _token = self._generate_token(maxsize=100)
            _secrets_config[stage]['SECRET_KEY'] = ''.join(tuple(_token))

        with open(secrets_project, 'w', encoding='utf-8') as file:
            yaml.dump(_secrets_config, file)

    @staticmethod
    def _create_config_file(*, data: dict, path: Path) -> None:
        """Generate the PyBoot configuration file.

        Args:
            data: The data to be written to the configuration file.
        """
        # remove PosixPath of project_path
        data['project_path'] = str(data['project_path'])

        # remove False values
        pyboot_config = {key: value for key, value in data.items() if value}

        config_file = path / __NAME_CONFIG_FILE__

        with open(config_file, 'w', encoding='utf-8') as file:
            toml_dump(pyboot_config, file)


class DjangoBlankBuilder(AbstractBuilder):
    """
    A class for building projects with PyBoot configuration.

    This class provides methods for generating configuration files and
    adding project files.
    """

    __slots__ = ['_options', '_project_name', '_builder', '_venv']

    def __init__(self, venv: Environment, options):
        """Initialize the Builder instance.

        Args:
            project_path: The project path.
        """
        super().__init__(venv, options)

    def add_main_folder(
        self,
        venv: Environment,
        project_name: str,
        /,
    ) -> None:
        """Add a main folder to the project.

        Args:
            project_name: The name of the project.
        """
        command = (
            f'cd {self._project_path} '
            f'&& {venv.django_admin} startproject {project_name} .'
        )

        venv.execute(command)

    def add_settings_files(self, project_name: str, /) -> None:
        settings_django_project = (
            self._project_path / project_name / 'settings.py'
        )

        secrets_project = self._project_path / '.secrets.yaml'

        target_files = (
            secrets_project,
            settings_django_project,
            self._project_path / '.gitignore',
            self._project_path / 'settings.yaml',
            self._project_path / 'requirements.txt',
        )

        for source, target in zip(django_blank, target_files):
            target.touch()
            shutil.copy2(source, target)

        self._configure_dynaconf_secret_file(secrets_project)
        self._configure_settings_django(
            settings_django_project,
            project_name,
        )

    def configure_static_folder(self, venv: Environment, /) -> None:
        command = (
            f'cd {self._project_path} '
            f'&& {venv.venv_python} manage.py collectstatic'
        )

        venv.execute(command)

    def run(self) -> Generator:
        """
        Run the project building process.

        This method performs the necessary steps for project configuration and
        file generation.
        """
        # general settings
        self._create_config_file(data=self._options, path=self._project_path)
        self._add_folders(
            self._project_path, 'docs', 'apps', 'media', 'static', 'templates'
        )

        super()._add_file(
            file_name='.python-version',
            path=self._project_path,
            content=self._options['python_version'],
        )

        yield 'General settings completed'

        # environment settings
        self._venv.create_venv()
        self._venv.add_dependency('Django', version='4.2.2')
        self._venv.add_dependency('dynaconf', version='3.1.12')
        if self._options['format']:
            self._venv.add_dependency('black')
            self._venv.add_dependency('isort')

        yield 'Environment settings completed'

        # django settings
        self.add_main_folder(self._venv, self._project_name)
        self.add_settings_files(self._project_name)
        self.configure_static_folder(self._venv)

        yield 'Django settings completed'


def factory_builder(*, template_name: str):
    """
    Factory function for creating the Builder instance.

    This function creates the Builder instance based on the specified options.
    """
    match (template_name):
        case 'django4.2-blank':
            return DjangoBlankBuilder
        case _:
            raise ValueError(f'Invalid template name: {template_name!r}')

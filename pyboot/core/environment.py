import os
import platform
import subprocess
import venv
from pathlib import Path


class Environment:
    __slots__ = ['__project_path', 'system', '__venv_path']

    def __init__(self, *, project_path: Path):
        self.__project_path = project_path
        self.__venv_path = self.__project_path / ".venv"
        self.system = platform.system()
        self.__create_venv_path()

    @property
    def venv_pip(self) -> Path:
        if self.system == "Windows":
            return self.__venv_path / "Scripts" / "pip.exe"
        return self.__venv_path / 'bin' / 'pip'

    @property
    def venv_python(self) -> Path:
        if self.system == "Windows":
            return self.__venv_path / "Scripts" / "python.exe"
        return self.__venv_path / "bin" / "python"

    @property
    def django_admin(self) -> Path:
        if self.system == "Windows":
            return self.__venv_path / "Scripts" / "django-admin.exe"
        return self.__venv_path / "bin" / "django-admin"

    def __create_venv_path(self) -> None:
        venv.create(self.__venv_path, with_pip=True)
        subprocess.run(
            [self.venv_pip, "install", "-U", "pip", "setuptools"],
            check=True,
            stdout=open(os.devnull, 'w'),
        )

    def execute(self, command: str, /) -> None:
        # command = command.replace('$PYTHON_VENV', str(self.venv_python))
        # args_command = command.split()

        subprocess.run(
            [command],
            check=True,
            shell=True,
            stdout=open(os.devnull, 'w'),
        )

    def add_dependency(
        self, dependency: str, *, version: str = 'latest'
    ) -> None:
        if version != 'latest':
            dependency += '==' + version

        command = f'{self.venv_pip} install {dependency}'

        self.execute(command)

    def export_django_settings(self, name_project: str, /) -> None:
        # Export Django settings module into environment variables.
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{name_project}.settings'

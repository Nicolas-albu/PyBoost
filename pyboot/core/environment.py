import os
import platform
import subprocess
import venv
from pathlib import Path

from .settings import __DEFAULT_VENV_NAME__, __VENV_NAMES__


class Environment:
    __slots__ = ['__project_path', 'system', '__venv_path', 'venv_name']

    def __init__(self, *, project_path: Path):
        self.__project_path = project_path
        self.system = platform.system()

        self.venv_name: str | None = self.get_venv()
        self.__venv_path = self.__project_path / (
            self.venv_name if self.venv_name else __DEFAULT_VENV_NAME__
        )

    @property
    def venv_pip(self) -> Path:
        if self.system == 'Windows':
            return self.__venv_path / 'Scripts' / 'pip.exe'
        return self.__venv_path / 'bin' / 'pip'

    @property
    def venv_python(self) -> Path:
        if self.system == 'Windows':
            return self.__venv_path / 'Scripts' / 'python.exe'
        return self.__venv_path / 'bin' / 'python'

    @property
    def django_admin(self) -> Path:
        if self.system == 'Windows':
            return self.__venv_path / 'Scripts' / 'django-admin.exe'
        return self.__venv_path / 'bin' / 'django-admin'

    def create_venv(self) -> None:
        if not self.venv_name:
            self.__create_venv_path()
        self.__update_venv()

    def __create_venv_path(self) -> None:
        venv.create(self.__venv_path, with_pip=True)

    def __update_venv(self) -> None:
        subprocess.run(
            [self.venv_pip, 'install', '-U', 'pip', 'setuptools'],
            check=True,
            stdout=open(os.devnull, 'w'),
        )

    def get_venv(self) -> str | None:
        for venv_name in __VENV_NAMES__:
            if (self.__project_path / venv_name).exists():
                return venv_name

        return None

    @staticmethod
    def execute(command: str, /) -> None:
        subprocess.run(
            [command],
            check=True,
            shell=True,
            stdout=open(os.devnull, 'w'),
        )

    @staticmethod
    def export_django_settings(name_project: str, /) -> None:
        # Export Django settings module into environment variables.
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{name_project}.settings'

    def add_dependency(
        self,
        dependency: str,
        *,
        version: str,
    ) -> None:
        _version = list(map(int, version.split('.')))

        _next_version = _version.copy()
        _next_version[1] += 1
        _next_version.pop()

        version = '.'.join(map(str, _version))
        next_version = '.'.join(map(str, _next_version))

        command = (
            f'{self.venv_pip} install'
            f" '{dependency}>={version},<{next_version}' "
        )

        self.execute(command)

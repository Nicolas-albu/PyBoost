"""Esse módulo pode conter funções que geram código ou outros arquivos de forma dinâmica. 

Por exemplo, pode conter funções para gerar arquivos de migração, serializadores, templates ou outros
tipos de arquivos.
"""

import codecs
import subprocess
from pathlib import Path


class Generator:
    def __init__(self, **configurations):
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
        self.config: dict = configurations
        self.directory: Path = self.config["directory"]
        self.config.pop("directory")

    def run(self) -> None:
        generation_cases: dict = {
            "name_project": self.add_main_folder,
            "add_python_version": self.add_python_version_file,
            "add_poetry": self.add_poetry,
            "add_dotenv": self.add_dotenv_file,
            "add_makefile": self.add_makefile,
        }

        for param, value in self.config.items():
            if value:
                generation_cases.get(param)()

    def add_main_folder(self) -> None:
        if not self.config["with_django"]:
            self.main_folder = self.directory / self.config["name_project"]
            self.main_folder.mkdir(exist_ok=True)

    def add_dotenv_file(self) -> None:
        if self.config["add_dotenv"] and not self.config["with_django"]:
            with (self.directory / ".env").open("w") as _:
                ...

    def add_python_version_file(self) -> None:
        if self.config["add_python_version"]:
            with (self.directory / ".python-version").open(
                "w"
            ) as python_version_file:
                python_version_file.write(self.config["add_python_version"])

    def add_makefile(self) -> None:
        if self.config["add_makefile"]:
            with (self.directory / "Makefile").open(
                "w"
            ) as python_version_file:
                ...

    def add_poetry(self) -> None:
        if self.config["add_poetry"]:
            with codecs.open(
                self.directory / "pyproject.toml", "w", encoding="utf-8"
            ) as poetry_file:
                poetry_file.write(
                    "[tool.poetry]\n"
                    + f'name = "{ self.config["name_project"] }"\n'
                    + 'version = "0.1.0"\n'
                    + 'description = ""\n'
                    + 'authors = ["Nícolas Albuquerque Ramos <nicolasalbuquerque581@gmail.com>"]\n'
                    + 'readme = "README.md"\n'
                )

                poetry_file.write(
                    "\n[tool.poetry.dependencies]\n"
                    + f'python = "^{ self.config["add_python_version"] }"\n'
                )

                poetry_file.write(
                    "\n[build-system]\n"
                    + 'requires = ["poetry-core"]\n'
                    + 'build-backend = "poetry.core.masonry.api"\n'
                )

        with (self.directory / ".log").open("w") as poetry_output:
            poetry_output.write('')
            subprocess.run("poetry shell", shell=True, stdout=poetry_output)

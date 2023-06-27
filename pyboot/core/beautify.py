from datetime import datetime
from pathlib import Path

from rich.console import Console

from .pyboot import PyBoot
from .settings import __NAME_CONFIG_FILE__


class BeautifyConsole:
    def __init__(self):
        self.console = Console()

    def final_message(self, directory: Path, name_project: str, /) -> None:
        # get the configurations of project
        pyboot_config = (directory / __NAME_CONFIG_FILE__).read_text()

        # printing results
        self.console.print(pyboot_config)
        self.console.print(
            '[bold green]'
            f'{name_project!r} configured!'
            '[/bold green] :rocket:'
        )

    def add_status(self, pyboot_project: PyBoot, name_project):
        status_message = (
            ':gear:[bold yellow] Creating project...[/bold yellow]'
        )

        with self.console.status(status_message):
            for task in pyboot_project.run():
                actual_hour = f'{datetime.now():%H:%M:%S}'
                self.console.print(
                    f'[bold yellow]{actual_hour} [bold blue]{task}'
                )

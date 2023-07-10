from datetime import datetime
from pathlib import Path

import questionary as question
from rich.console import Console

from .pyboot import PyBootDirector
from .settings import __NAME_CONFIG_FILE__, __TEMPLATES_NAME__


class BeautifyConsole:
    def __init__(self):
        self.console = Console()

    def final_message(self, project_path: Path, project_name: str, /) -> None:
        # get the configurations of project
        pyboot_config = (project_path / __NAME_CONFIG_FILE__).read_text()

        # printing results
        self.console.print(pyboot_config)
        self.console.print(
            '[bold green]'
            f'{project_name!r} configured!'
            '[/bold green] :rocket:'
        )

    def add_status(self, director: PyBootDirector):
        status_message = (
            ':gear:[bold yellow] Creating project...[/bold yellow]'
        )

        with self.console.status(status_message):
            for task in director.run():
                actual_hour = f'{datetime.now():%H:%M:%S}'
                self.console.print(
                    f'[bold yellow]{actual_hour} [bold blue]{task}'
                )

    def ask_template(self) -> str:
        return question.select(
            'What is the template?',
            choices=__TEMPLATES_NAME__,
        ).ask()

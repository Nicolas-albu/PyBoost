from pathlib import Path

from rich.console import Console
from rich.progress import Progress

from . import __NAME_CONFIG_FILE__


class BeautifyConsole:
    def __init__(self):
        self.console = Console()

    def final_message_printing(
        self, directory: Path, name_project: str, /
    ) -> None:
        # get the configurations of project
        pyboost_config = (directory / __NAME_CONFIG_FILE__).read_text()

        # printing results
        self.console.print_json(pyboost_config)
        self.console.print(
            f"\n[bold green]{name_project!r} configured![/bold green] :rocket:"
        )

    def add_progressbar(self) -> None:
        with Progress() as progress:
            task_generate_pyboost_json = progress.add_task(
                "[bold yellow]Generate pyboost.json", total=100
            )
            task_create_files = progress.add_task(
                "[bold red]Creating files[/bold red]", total=100
            )

            while not progress.finished:
                progress.update(task_generate_pyboost_json, advance=0.5)
                progress.update(task_create_files, advance=0.5)

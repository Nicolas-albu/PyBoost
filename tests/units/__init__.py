import shutil
from pathlib import Path
from typing import Optional

fixtures_path = Path().cwd() / 'tests' / 'fixtures'
units_path = Path().cwd() / 'tests' / 'units'
debug_path = units_path / 'debug'


def back_before(
    *,
    folder: Optional[Path] = None,
    file: Optional[Path] = None,
) -> None:
    if folder:
        shutil.rmtree(folder)

    if file:
        file.unlink(missing_ok=True)


def fixtures_to_debug_folder(
    *,
    fixtures_filename: str,
    debug_filename: str,
) -> Path:
    fixture_file = fixtures_path / fixtures_filename
    debug_file = debug_path / debug_filename
    debug_file.touch()

    shutil.copy2(fixture_file, debug_file)

    return debug_file


__all__ = [
    'fixtures_path',
    'units_path',
    'debug_path',
    'back_before',
]

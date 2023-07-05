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


def fixtures_to_debug(
    *,
    fixtures_filename: str,
    debug_filename: str,
    debug_folder: Optional[Path] = None,
) -> Path:
    _debug_folder = debug_folder if debug_folder else debug_path

    fixture_file = fixtures_path / fixtures_filename
    debug_file = _debug_folder / debug_filename

    debug_file.touch()

    shutil.copy2(fixture_file, debug_file)

    return debug_file


__all__ = [
    # paths
    'fixtures_path',
    'units_path',
    'debug_path',
    # functions
    'back_before',
    'fixtures_to_debug',
]

import shutil
from pathlib import Path
from typing import Iterable, Optional

fixtures_path = Path().cwd() / 'tests' / 'fixtures'
units_path = Path().cwd() / 'tests' / 'units'
out_path = units_path / 'out'


def back_before(
    *,
    folder: Optional[Path] = None,
    file: Optional[Path | Iterable[Path]] = None,
) -> None:
    if folder:
        shutil.rmtree(folder)

    if isinstance(file, Path):
        file.unlink(missing_ok=True)

    elif isinstance(file, Iterable):
        for _file in file:
            _file.unlink(missing_ok=True)


def fixtures_to_debug(
    *,
    fixtures_filename: str,
    debug_filename: str,
    debug_folder: Optional[Path] = None,
) -> Path:
    _debug_folder = debug_folder if debug_folder else out_path

    fixture_file = fixtures_path / fixtures_filename
    debug_file = _debug_folder / debug_filename

    debug_file.touch()

    shutil.copy2(fixture_file, debug_file)

    return debug_file


__all__ = [
    # paths
    'fixtures_path',
    'units_path',
    'out_path',
    # functions
    'back_before',
    'fixtures_to_debug',
]

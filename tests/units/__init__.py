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


__all__ = [
    'fixtures_path',
    'units_path',
    'debug_path',
    'back_before',
]

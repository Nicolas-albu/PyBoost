from pathlib import Path

units_path = Path().cwd() / 'tests' / 'units'
debug_path = units_path / 'debug'

__all__ = [
    'units_path',
    'debug_path',
]

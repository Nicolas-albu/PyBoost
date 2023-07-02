import shutil
from pathlib import Path
from typing import Optional

import pytest

from pyboot.core.environment import Environment

units_path = Path().cwd() / 'tests' / 'units'
debug_path = units_path / 'debug'


def back_before(*, venv_path: Optional[Path]):
    if venv_path:
        shutil.rmtree(venv_path)


@pytest.fixture
def test_environment():
    return Environment(project_path=debug_path)


def test_get_venv(test_environment: Environment):
    venv_path = debug_path / '.venv'
    venv_path.mkdir(exist_ok=True)

    assert test_environment.get_venv() == '.venv'
    back_before(venv_path=venv_path)

    venv_path = debug_path / 'venv'
    venv_path.mkdir(exist_ok=True)

    assert test_environment.get_venv() == 'venv'
    back_before(venv_path=venv_path)


def test_create_venv(test_environment: Environment):
    test_environment.create_venv()
    venv_path = debug_path / '.venv'

    assert test_environment.venv_name == '.venv'
    assert venv_path.exists()
    assert test_environment.venv_pip.exists()
    assert test_environment.venv_python.exists()

    back_before(venv_path=venv_path)

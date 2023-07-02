import pytest

from pyboot.core.environment import Environment

from . import back_before, debug_path


@pytest.fixture
def test_environment():
    return Environment(project_path=debug_path)


def test_get_venv(test_environment: Environment):
    venv_path = debug_path / '.venv'
    venv_path.mkdir(exist_ok=True)

    assert test_environment.get_venv_name() == '.venv'
    back_before(folder=venv_path)

    venv_path = debug_path / 'venv'
    venv_path.mkdir(exist_ok=True)

    assert test_environment.get_venv_name() == 'venv'
    back_before(folder=venv_path)


def test_create_venv(test_environment: Environment):
    test_environment.create_venv()
    venv_path = debug_path / '.venv'

    assert test_environment.venv_name == '.venv'
    assert venv_path.exists()
    assert test_environment.venv_pip.exists()
    assert test_environment.venv_python.exists()

    back_before(folder=venv_path)

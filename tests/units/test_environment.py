from pyboot.core.environment import Environment

from . import back_before, debug_path


def test_get_venv(environment: Environment):
    venv_path = debug_path / '.venv'
    venv_path.mkdir(exist_ok=True)

    assert environment.get_venv_name() == '.venv'
    back_before(folder=venv_path)

    venv_path = debug_path / 'venv'
    venv_path.mkdir(exist_ok=True)

    assert environment.get_venv_name() == 'venv'
    back_before(folder=venv_path)


def test_create_venv(environment: Environment):
    environment.create_venv()
    venv_path = debug_path / '.venv'

    assert environment.venv_name == '.venv'
    assert venv_path.exists()
    assert environment.venv_pip.exists()
    assert environment.venv_python.exists()

    back_before(folder=venv_path)

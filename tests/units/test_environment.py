import venv

from pyboot.core.environment import Environment

from . import back_before, out_path


def test_get_venv(environment: Environment):
    # .venv folder
    venv_path = out_path / '.venv'
    venv_path.mkdir(exist_ok=True)

    assert environment.get_venv_name() == '.venv'
    back_before(folder=venv_path)

    # venv folder
    venv_path = out_path / 'venv'
    venv_path.mkdir(exist_ok=True)

    assert environment.get_venv_name() == 'venv'
    back_before(folder=venv_path)

    # env folder
    venv_path = out_path / 'env'
    venv_path.mkdir(exist_ok=True)

    assert environment.get_venv_name() == 'env'
    back_before(folder=venv_path)


def test_create_venv(environment: Environment):
    environment.create_venv()
    venv_path = out_path / '.venv'

    assert environment.venv_name == '.venv'
    assert venv_path.exists()
    assert environment.venv_pip.exists()
    assert environment.venv_python.exists()

    back_before(folder=venv_path)


def test_create_venv_when_venv_path_exists_with_name_dot_venv():
    venv_path = out_path / '.venv'
    venv.create(venv_path, with_pip=True)

    environment = Environment(project_path=out_path)
    environment.create_venv()

    assert environment.venv_name == '.venv'
    assert venv_path.exists()
    assert environment.venv_pip.exists()
    assert environment.venv_python.exists()

    back_before(folder=venv_path)


def test_create_venv_when_venv_path_exists_with_name_venv():
    venv_path = out_path / 'venv'
    venv.create(venv_path, with_pip=True)

    environment = Environment(project_path=out_path)
    environment.create_venv()

    assert environment.venv_name == 'venv'
    assert venv_path.exists()
    assert environment.venv_pip.exists()
    assert environment.venv_python.exists()

    back_before(folder=venv_path)

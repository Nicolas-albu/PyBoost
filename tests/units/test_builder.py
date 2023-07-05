import re
from unittest.mock import MagicMock

import pytest
import yaml
from pytest_mock import MockerFixture

from pyboot.core.builder import Builder
from pyboot.core.environment import Environment
from pyboot.core.settings import __ENVIRONMENT_STAGES__

from . import back_before, debug_path, fixtures_to_debug

TOKEN_PATTERN: str = r'[\s]|[\\]|[\"\']'


@pytest.fixture(
    params={
        'secrets_dynf': debug_path / '.secrets.yaml',
        'settings_django': debug_path / 'settings.py',
        'gitignore': debug_path / '.gitignore',
        'settings_dynf': debug_path / 'settings.yaml',
        'requirements': debug_path / 'requirements.txt',
    }
)
def mock_template_django_blank(request):
    paths = request.param
    mock = MagicMock()

    mock.__iter__.return_value = iter([*paths.values()])

    yield mock
    del mock


def test_token_generation_with_maxsize_of_100(builder: Builder):
    _token = builder._generate_token(maxsize=100)
    token = ''.join(tuple(_token))

    assert re.search(TOKEN_PATTERN, token) is None


def test_python_version_file_creation(builder: Builder):
    python_version: str = '3.9.1'

    builder.add_python_version_file(python_version)

    python_version_file = debug_path / '.python-version'

    assert python_version_file.exists()
    assert python_version_file.read_text() == python_version

    back_before(file=python_version_file)


def test_django_settings_file_configuration(builder: Builder):
    name_project = 'test_project'
    settings_django = fixtures_to_debug(
        fixtures_filename='settings_django_with_name_test_project.py',
        debug_filename='settings.py',
    )

    builder._configure_settings_django(settings_django, name_project)

    assert settings_django.exists()

    with open(settings_django, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if "PROJECT_NAME =" in line:
            assert line == f"PROJECT_NAME = {name_project!r}\n"
            break

    back_before(file=settings_django)


def test_makefile_creation(builder: Builder):
    makefile = debug_path / 'Makefile'
    builder.add_makefile()

    assert makefile.exists()

    back_before(file=makefile)


def test_add_folder(builder: Builder):
    folder = 'test_folder'
    builder.add_folder(folder)

    folder = debug_path / folder

    assert folder.exists()

    back_before(folder=folder)


def test_config_file_creation(builder: Builder):
    pyboot_file = debug_path / 'pyboot.toml'

    data = {
        'project_name': 'test_project',
        'project_path': str(debug_path),
        'add_python_version': '3.9.1',
    }

    builder.create_config_file(data)

    assert pyboot_file.exists()

    with open(pyboot_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line, (key, value) in zip(lines, data.items()):
        if str(key) in line:
            assert line == f'{key} = "{value}"\n'

    back_before(file=pyboot_file)


def test_configure_dynaconf_secret_file(builder: Builder):
    secrets_file = fixtures_to_debug(
        fixtures_filename='secrets_fixture.yaml',
        debug_filename='.secrets.yaml',
    )

    builder._configure_dynaconf_secret_file(secrets_file)

    with open(secrets_file, 'r', encoding='utf-8') as file:
        _secrets_config = yaml.safe_load(file)

    for stage in __ENVIRONMENT_STAGES__:
        token = _secrets_config[stage]['SECRET_KEY']
        assert re.search(TOKEN_PATTERN, token) is None

    back_before(file=secrets_file)


def test_add_settings_files(
    builder: Builder,
    mocker: MockerFixture,
):
    name_project = 'test_project'
    main_path = debug_path / name_project

    main_path.mkdir(exist_ok=True)

    mocker.patch(
        'pyboot.core.settings.template_django_blank',
        return_value=mock_template_django_blank,
    )

    builder.add_settings_files(name_project)

    files = (
        debug_path / '.secrets.yaml',
        main_path / 'settings.py',
        debug_path / '.gitignore',
        debug_path / 'settings.yaml',
        debug_path / 'requirements.txt',
    )

    for file in files:
        assert file.exists()
        assert file.read_text() is not None

    back_before(file=files)
    back_before(folder=main_path)


def test_add_main_folder(builder: Builder, environment: Environment):
    name_project = 'test_project'
    main_path = debug_path / name_project

    environment.create_venv()
    environment.add_dependency('Django', version='4.2.2')

    builder.add_main_folder(environment, name_project)

    assert main_path.exists()
    assert (main_path / 'settings.py').exists()

    back_before(folder=main_path)
    back_before(folder=debug_path / '.venv')
    back_before(file=debug_path / 'manage.py')


def test_configure_static_folder(builder: Builder, environment: Environment):
    name_project = 'test_project'
    main_path = debug_path / name_project

    static_folder = debug_path / 'static'
    static_folder.mkdir(exist_ok=True)

    environment.create_venv()
    environment.add_dependency('Django', version='4.2.2')

    builder.add_main_folder(environment, name_project)

    settings_django = main_path / 'settings.py'
    with open(settings_django, 'a', encoding='utf-8') as file:
        file.write('\nSTATIC_ROOT = BASE_DIR / "static/"\n')

    builder.configure_static_folder(environment)

    assert (debug_path / 'static' / 'admin' / 'img').exists()
    assert (debug_path / 'static' / 'admin' / 'css').exists()
    assert (debug_path / 'static' / 'admin' / 'js').exists()

    back_before(folder=main_path)
    back_before(folder=debug_path / '.venv')
    back_before(folder=debug_path / 'static')
    back_before(file=debug_path / 'manage.py')

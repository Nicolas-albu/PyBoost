import re
from unittest.mock import MagicMock

import pytest
import yaml
from pytest_mock import MockerFixture

from pyboot.core.builder import DjangoBlankBuilder
from pyboot.core.environment import Environment
from pyboot.core.settings import __ENVIRONMENT_STAGES__

from . import back_before, fixtures_to_debug, out_path

TOKEN_PATTERN: str = r'[\s]|[\\]|[\"\']'


@pytest.fixture(
    params={
        'secrets_dynf': out_path / '.secrets.yaml',
        'settings_django': out_path / 'settings.py',
        'gitignore': out_path / '.gitignore',
        'settings_dynf': out_path / 'settings.yaml',
        'requirements': out_path / 'requirements.txt',
    }
)
def mock_django_blank(request):
    paths = request.param
    mock = MagicMock()

    mock.__iter__.return_value = iter([*paths.values()])

    yield mock
    del mock


def test_token_generation_with_maxsize_of_100(
    django_blank_builder: DjangoBlankBuilder,
):
    _token = django_blank_builder._generate_token(maxsize=100)
    token = ''.join(tuple(_token))

    assert re.search(TOKEN_PATTERN, token) is None


def test_python_version_file_creation(
    django_blank_builder: DjangoBlankBuilder,
):
    python_version: str = '3.9.1'

    django_blank_builder._add_file(
        file_name='.python-version',
        path=out_path,
        content=python_version,
    )

    python_version_file = out_path / '.python-version'

    assert python_version_file.exists()
    assert python_version_file.read_text() == python_version

    back_before(file=python_version_file)


def test_django_settings_file_configuration(
    django_blank_builder: DjangoBlankBuilder,
):
    project_name = 'test_project'
    settings_django = fixtures_to_debug(
        fixtures_filename='settings_django_with_name_test_project.py',
        debug_filename='settings.py',
    )

    django_blank_builder._configure_settings_django(
        settings_django, project_name
    )

    assert settings_django.exists()

    with open(settings_django, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if "PROJECT_NAME =" in line:
            assert line == f"PROJECT_NAME = {project_name!r}\n"
            break

    back_before(file=settings_django)


def test_add_folder(django_blank_builder: DjangoBlankBuilder):
    folder = 'test_folder'
    django_blank_builder._add_folders(out_path, folder)

    folder = out_path / folder

    assert folder.exists()

    back_before(folder=folder)


def test_config_file_creation(django_blank_builder: DjangoBlankBuilder):
    pyboot_file = out_path / 'pyboot.toml'

    data = {
        'project_name': 'test_project',
        'project_path': str(out_path),
        'add_python_version': '3.9.1',
    }

    django_blank_builder._create_config_file(data=data, path=out_path)

    assert pyboot_file.exists()

    with open(pyboot_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line, (key, value) in zip(lines, data.items()):
        if str(key) in line:
            assert line == f'{key} = "{value}"\n'

    back_before(file=pyboot_file)


def test_configure_dynaconf_secret_file(
    django_blank_builder: DjangoBlankBuilder,
):
    secrets_file = fixtures_to_debug(
        fixtures_filename='secrets_fixture.yaml',
        debug_filename='.secrets.yaml',
    )

    django_blank_builder._configure_dynaconf_secret_file(secrets_file)

    with open(secrets_file, 'r', encoding='utf-8') as file:
        _secrets_config = yaml.safe_load(file)

    for stage in __ENVIRONMENT_STAGES__:
        token = _secrets_config[stage]['SECRET_KEY']
        assert re.search(TOKEN_PATTERN, token) is None

    back_before(file=secrets_file)


def test_add_settings_files(
    django_blank_builder: DjangoBlankBuilder,
    mocker: MockerFixture,
):
    project_name = 'test_project'
    main_path = out_path / project_name

    main_path.mkdir(exist_ok=True)

    mocker.patch(
        'pyboot.core.templates.django_blank',
        return_value=mock_django_blank,
    )

    django_blank_builder.add_settings_files(project_name)

    files = (
        out_path / '.secrets.yaml',
        main_path / 'settings.py',
        out_path / '.gitignore',
        out_path / 'settings.yaml',
        out_path / 'requirements.txt',
    )

    for file in files:
        assert file.exists()
        assert file.read_text() is not None

    back_before(file=files)
    back_before(folder=main_path)


def test_add_main_folder(
    django_blank_builder: DjangoBlankBuilder, environment: Environment
):
    project_name = 'test_project'
    main_path = out_path / project_name

    environment.create_venv()
    environment.add_dependency('Django', version='4.2.2')

    django_blank_builder.add_main_folder(environment, project_name)

    assert main_path.exists()
    assert (main_path / 'settings.py').exists()

    back_before(folder=main_path)
    back_before(folder=out_path / '.venv')
    back_before(file=out_path / 'manage.py')


def test_configure_static_folder(
    django_blank_builder: DjangoBlankBuilder, environment: Environment
):
    project_name = 'test_project'
    main_path = out_path / project_name

    static_folder = out_path / 'static'
    static_folder.mkdir(exist_ok=True)

    environment.create_venv()
    environment.add_dependency('Django', version='4.2.2')

    django_blank_builder.add_main_folder(environment, project_name)

    settings_django = main_path / 'settings.py'
    with open(settings_django, 'a', encoding='utf-8') as file:
        file.write('\nSTATIC_ROOT = BASE_DIR / "static/"\n')

    django_blank_builder.configure_static_folder(environment)

    assert (out_path / 'static' / 'admin' / 'img').exists()
    assert (out_path / 'static' / 'admin' / 'css').exists()
    assert (out_path / 'static' / 'admin' / 'js').exists()

    back_before(folder=main_path)
    back_before(folder=out_path / '.venv')
    back_before(folder=out_path / 'static')
    back_before(file=out_path / 'manage.py')

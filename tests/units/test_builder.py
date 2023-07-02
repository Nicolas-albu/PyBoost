import re

import pytest

from pyboot.core.builder import Builder

from . import back_before, debug_path, fixtures_to_debug_folder


@pytest.fixture
def test_builder():
    return Builder(project_path=debug_path)


def test_token_generation_with_maxsize_of_100(test_builder: Builder):
    pattern: str = r'[\s]|[\\]|[\"\']'

    _token = test_builder._generate_token(maxsize=100)
    token = ''.join(tuple(_token))

    assert re.search(pattern, token) is None


def test_python_version_file_creation(test_builder: Builder):
    python_version: str = '3.9.1'

    test_builder.add_python_version_file(python_version)

    python_version_file = debug_path / '.python-version'

    assert python_version_file.exists()
    assert python_version_file.read_text() == python_version

    back_before(file=python_version_file)


def test_django_settings_file_configuration(test_builder: Builder):
    name_project = 'test_project'
    settings_django = fixtures_to_debug_folder(
        fixtures_filename='settings_with_name_test_project_.py',
        debug_filename='settings.py',
    )

    test_builder._configure_settings_django(settings_django, name_project)

    assert settings_django.exists()

    with open(settings_django, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if "PROJECT_NAME =" in line:
            assert line == f"PROJECT_NAME = {name_project!r}\n"
            break

    back_before(file=settings_django)


def test_makefile_creation(test_builder: Builder):
    makefile = debug_path / 'Makefile'
    test_builder.add_makefile()

    assert makefile.exists()

    back_before(file=makefile)


def test_add_folder(test_builder: Builder):
    folder = 'test_folder'
    test_builder.add_folder(folder)

    folder = debug_path / folder

    assert folder.exists()

    back_before(folder=folder)


def test_config_file_creation(test_builder: Builder):
    pyboot_file = debug_path / 'pyboot.toml'

    data = {
        'project_name': 'test_project',
        'project_path': str(debug_path),
        'add_python_version': '3.9.1',
    }

    test_builder.create_config_file(data)

    assert pyboot_file.exists()

    with open(pyboot_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line, (key, value) in zip(lines, data.items()):
        if str(key) in line:
            assert line == f'{key} = "{value}"\n'

    back_before(file=pyboot_file)

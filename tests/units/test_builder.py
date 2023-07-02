import re
import shutil

import pytest

from pyboot.core.builder import Builder

from . import back_before, debug_path, fixtures_path


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
    fixture_settings_django = (
        fixtures_path / 'settings_with_name_test_project_.py'
    )

    settings_django = debug_path / 'settings.py'
    settings_django.touch()

    shutil.copy2(fixture_settings_django, settings_django)
    test_builder._configure_settings_django(settings_django, name_project)

    assert settings_django.exists()

    with open(settings_django, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if "PROJECT_NAME =" in line:
            assert line == f"PROJECT_NAME = {name_project!r}\n"
            break

    back_before(file=settings_django)

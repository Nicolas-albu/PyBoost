import re

import pytest

from pyboot.core.builder import Builder

from . import debug_path


@pytest.fixture
def test_builder():
    return Builder(project_path=debug_path)


def test_generation_tokens_with_maxsize_100(test_builder: Builder):
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

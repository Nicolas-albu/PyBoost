import pytest

from pyboot.core.builder import Builder
from pyboot.core.environment import Environment

from . import debug_path


@pytest.fixture
def environment():
    yield Environment(project_path=debug_path)


@pytest.fixture
def builder():
    yield Builder(project_path=debug_path)

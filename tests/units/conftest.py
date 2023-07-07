import pytest

from pyboot.core.builder import Builder
from pyboot.core.environment import Environment

from . import out_path


@pytest.fixture
def environment():
    yield Environment(project_path=out_path)


@pytest.fixture
def builder():
    yield Builder(project_path=out_path)

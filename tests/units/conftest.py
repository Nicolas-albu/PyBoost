import pytest

from pyboot.core.builder import DjangoBlankBuilder
from pyboot.core.environment import Environment

from . import out_path


@pytest.fixture
def environment():
    yield Environment(project_path=out_path)


@pytest.fixture
def django_blank_builder(environment: Environment):
    options = {
        'template': 'django_blank',
        'with_drf': True,
        'format': True,
        'project_name': 'test_project',
        'project_path': out_path,
        'python_version': '3.10.10',
    }

    yield DjangoBlankBuilder(venv=environment, options=options)

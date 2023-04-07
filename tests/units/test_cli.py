import pytest
from typer.testing import CliRunner, Result

from pyboost import app, get_path_name

runner = CliRunner()


class TestProjectSettings:
    OTHER_NAME = "TestPyBoost"

    @pytest.fixture
    def test_with_default_name(self):
        return runner.invoke(app, ["-pv", "3.10"])

    @pytest.fixture
    def test_with_other_name(self):
        return runner.invoke(app, ["-pv", "3.10", "-np", self.OTHER_NAME])

    def test_version(
        self, test_with_default_name: Result, test_with_other_name: Result
    ):
        assert test_with_default_name.exit_code == 0
        assert '"add_python_version": "3.10"' in test_with_default_name.stdout
        assert test_with_other_name.exit_code == 0
        assert '"add_python_version": "3.10"' in test_with_other_name.stdout

    def test_version(
        self, test_with_default_name: Result, test_with_other_name: Result
    ):
        assert test_with_default_name.exit_code == 0
        assert (
            f'"name_project": "{get_path_name()}"'
            in test_with_default_name.stdout
        )
        assert test_with_other_name.exit_code == 0
        assert (
            f'"name_project": "{self.OTHER_NAME}"'
            in test_with_other_name.stdout
        )

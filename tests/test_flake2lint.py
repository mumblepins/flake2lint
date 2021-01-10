import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.testing import check_file_output
from pytest_regressions.file_regression import FileRegressionFixture

from flake2lint import process_file
from flake2lint.__main__ import main


@pytest.fixture()
def example_file(tmp_pathplus):
	example_file = tmp_pathplus / "code.py"

	example_file.write_lines([
			"def foo(  # noqa",
			"	id: int = -1,  # noqa: A002",
			"	dir: PathLike = '.',  # noqa: A002  # pylint: disable=redefined-builtin",
			"	): ...",
			])

	return example_file


def test_flake2lint(example_file, file_regression: FileRegressionFixture):
	assert process_file(example_file)
	check_file_output(example_file, file_regression)


def test_cli(example_file, tmp_pathplus, file_regression: FileRegressionFixture):
	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False, args=str(example_file))
	assert result.exit_code == 1
	check_file_output(example_file, file_regression)


import os

import hypothesis.strategies as strats
from click.testing import CliRunner
from hypothesis import given

from dumbpw.cli import cli
from dumbpw.errors import DumbExitCode


@given(strats.integers(min_value=5, max_value=12))
def test_cli_basic_execution(length):
    """Verify that providing a length returns a password of that length."""
    runner = CliRunner()

    result = runner.invoke(cli, [str(length)])

    assert result.exit_code == 0
    assert len(result.output.strip()) == length


def test_cli_constraints_fail():
    """Verify that invalid constraints trigger an error state."""
    runner = CliRunner()

    result = runner.invoke(cli, ["5", "--min-uppercase", "10"])

    assert result.exit_code == 1
    assert "You cannot request more characters" in result.output


@given(strats.integers(min_value=5, max_value=12))
def test_cli_stdin_specials(length):
    """Verify that passing '--specials -' reads from standard input."""
    runner = CliRunner()
    min_specials = 1

    result = runner.invoke(
        cli,
        [str(length), "--specials", "-", "--min-specials", str(min_specials)],
        input="!",
    )

    assert result.exit_code == 0
    assert result.output.count("!") >= min_specials


def test_cli_no_args_shows_help():
    """Verify that running without arguments displays help text."""
    runner = CliRunner()

    result = runner.invoke(cli, [])

    assert result.exit_code == DumbExitCode.USAGE
    assert result.output.split("\n")[0] == "Usage: dumbpw [OPTIONS] LENGTH"


def test_cli_help_arg_shows_help():
    """Verify that running without arguments displays help text."""
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == DumbExitCode.OK
    assert result.output.split("\n")[0] == "Usage: dumbpw [OPTIONS] LENGTH"


def test_cli_empty_blocklist_allowed():
    """Passing an empty blocklist is allowed."""
    runner = CliRunner()

    result = runner.invoke(cli, ["5", "--blocklist", ""])

    assert result.exit_code == DumbExitCode.OK


def test_cli_env_specials():
    """DUMBPW_SPECIALS env var is read."""
    runner = CliRunner()
    specials = "!"
    os.environ["DUMBPW_SPECIALS"] = specials

    result = runner.invoke(cli, ["5", "--min-specials", "1"])

    assert sum(1 for char in result.output if char in specials) >= 1

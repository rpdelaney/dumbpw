from click.testing import CliRunner

from dumbpw.cli import cli


def test_prints_dumb_valueerror(mocker):
    mock_search = mocker.patch("dumbpw.engine.search")
    runner = CliRunner()

    result = runner.invoke(cli, args=["5"])

    assert result.exception is None
    assert len(result.output) == 5
    assert mock_search.assert_called_once()

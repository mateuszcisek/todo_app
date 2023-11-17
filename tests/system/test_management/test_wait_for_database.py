from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError


@patch("django.db.connection.ensure_connection")
def test_database_connection_available(mock_ensure_connection, capsys):
    """
    Given the database is available
    When we try to connect to the database
    Then the command exits successfully
    And expected message are printed.
    """
    call_command("wait_for_database")

    mock_ensure_connection.assert_called_once()

    stdout, _ = capsys.readouterr()

    assert "Waiting for the database..." in stdout
    assert "Database available!" in stdout


@patch("time.sleep")
@patch("sys.exit")
@patch("django.db.connection.ensure_connection")
def test_database_connection_not_available(
    mock_ensure_connection, mock_exit, _, capsys
):
    """
    Given the database is not available
    When we try to connect to the database
    Then the command exits with status code 1
    And expected message are printed.
    """
    mock_ensure_connection.side_effect = OperationalError

    call_command("wait_for_database", "--timeout", "0.1")

    stdout, stderr = capsys.readouterr()

    mock_exit.assert_called_once_with(1)
    assert "Waiting for the database..." in stdout
    assert "Database connection failed!" in stderr

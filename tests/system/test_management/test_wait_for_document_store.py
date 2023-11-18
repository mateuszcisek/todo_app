from unittest.mock import patch

from django.core.management import call_command
from pymongo.errors import ServerSelectionTimeoutError


@patch("pymongo.MongoClient.server_info")
def test_document_store_connection_available(mock_server_info, capsys):
    """
    Given the document store is available
    When we try to connect to the document store
    Then the command exits successfully
    And expected message are printed.
    """
    call_command("wait_for_document_store")

    mock_server_info.assert_called_once()

    stdout, _ = capsys.readouterr()

    assert "Waiting for the document store..." in stdout
    assert "Document store available!" in stdout


@patch("time.sleep")
@patch("sys.exit")
@patch("mongoengine.connect")
def test_database_connection_not_available(mock_connect, mock_exit, _, capsys):
    """
    Given the document store is not available
    When we try to connect to the document store
    Then the command exits with status code 1
    And expected message are printed.
    """
    mock_connect.side_effect = ServerSelectionTimeoutError

    call_command("wait_for_document_store", "--timeout", "0.1")

    stdout, stderr = capsys.readouterr()

    mock_exit.assert_called_once_with(1)
    assert "Waiting for the document store..." in stdout
    assert "Document store connection failed!" in stderr

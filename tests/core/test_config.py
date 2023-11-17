import os
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch

import pytest
from cybersmart_assessment.core.config import AppConfig
from pydantic import ValidationError


def _get_values(
    database_host: Optional[str] = "localhost",
    database_name: Optional[str] = "db_name",
    database_password: Optional[str] = "db_pass",
    database_port: Optional[int] = "1234",
    database_user: Optional[str] = "db_user",
    debug: Optional[str] = "False",
    logging_level: Optional[str] = "info",
    secret_key: Optional[str] = "very-very-secret-top-secret-key",
    static_files_dir: Optional[str] = "/tmp",
    time_zone: Optional[str] = "Europe/London",
    excluded_fields: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Helper function that returns a dictionary with requested environment variables.
    """
    result = {
        "DATABASE_HOST": database_host,
        "DATABASE_NAME": database_name,
        "DATABASE_PASSWORD": database_password,
        "DATABASE_PORT": database_port,
        "DATABASE_USER": database_user,
        "DEBUG": debug,
        "LOGGING_LEVEL": logging_level,
        "SECRET_KEY": secret_key,
        "STATIC_FILES_DIR": static_files_dir,
        "TIME_ZONE": time_zone,
    }

    if excluded_fields:
        for key in excluded_fields:
            del result[key]

    return {f"TODO_{key}": value for key, value in result.items()}


def test_settings_are_correct():
    """
    Given all environment variables are set
    When we create a new object of AppConfig class
    Then all values in that object are set to correct values.
    """
    expected = {
        "database_host": "localhost",
        "database_name": "db_name",
        "database_password": "db_pass",
        "database_port": 1234,
        "database_user": "db_user",
        "debug": False,
        "logging_level": "INFO",
        "secret_key": "very-very-secret-top-secret-key",
        "static_files_dir": Path("/tmp"),
        "time_zone": "Europe/London",
    }

    with patch.dict(os.environ, _get_values()):
        config = AppConfig()

        assert config.database_host == expected["database_host"]
        assert config.database_name == expected["database_name"]
        assert (
            config.database_password.get_secret_value() == expected["database_password"]
        )
        assert config.database_port == expected["database_port"]
        assert config.database_user == expected["database_user"]
        assert config.debug == expected["debug"]
        assert config.logging_level == expected["logging_level"]
        assert config.secret_key.get_secret_value() == expected["secret_key"]
        assert config.static_files_dir == expected["static_files_dir"]
        assert config.time_zone == expected["time_zone"]


def test_static_files_dir(tmp_path):
    """
    Given an environment variable for TODO_STATIC_FILES_DIR set
    When we create a new object of AppConfig class
    Then the value for data_storage_path is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(static_files_dir=str(tmp_path))):
        config = AppConfig()

    assert config.static_files_dir == tmp_path


@pytest.mark.parametrize("value", ("1", "1.5", "False", "/incorrect/path"))
def test_static_files_dir_incorrect_value(value):
    """
    Given an environment variable for TODO_STATIC_FILES_DIR set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(os.environ, _get_values(static_files_dir=value)), pytest.raises(
        ValidationError
    ):
        AppConfig()


@pytest.mark.parametrize(
    "value, expected_result",
    (
        ("True", True),
        ("true", True),
        ("1", True),
        ("False", False),
        ("false", False),
        ("0", False),
    ),
)
def test_debug(value, expected_result):
    """
    Given an environment variable for DEBUG set
    When we create a new object of AppConfig class
    Then the value for debug is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(debug=value)):
        config = AppConfig()

    assert config.debug is expected_result


@pytest.mark.parametrize("value", ("1.5", "incorrect-value"))
def test_debug_incorrect_value(value):
    """
    Given an environment variable for DEBUG set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(os.environ, _get_values(debug=value)), pytest.raises(
        ValidationError
    ):
        AppConfig()


@pytest.mark.parametrize(
    "value",
    ("debug", "info", "warning", "error", "DEBUG", "INFO", "WARNING", "ERROR"),
)
def test_logging_level(value):
    """
    Given an environment variable for LOGGING_LEVEL set
    When we create a new object of AppConfig class
    Then the value for logging_level is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(logging_level=value)):
        config = AppConfig()

    assert config.logging_level == value.upper()


@pytest.mark.parametrize("value", ("1.0", "1.5", "incorrect-value", "fatal", "FATAL"))
def test_logging_level_incorrect_value(value):
    """
    Given an environment variable for LOGGING_LEVEL set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(os.environ, _get_values(logging_level=value)), pytest.raises(
        ValidationError
    ):
        AppConfig()


def test_time_zone():
    """
    Given an environment variable for TIME_ZONE set
    When we create a new object of AppConfig class
    Then the value for time_zone is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(time_zone="Europe/Warsaw")):
        config = AppConfig()

    assert config.time_zone == "Europe/Warsaw"


def test_time_zone_incorrect_value():
    """
    Given an environment variable for TIME_ZONE set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(
        os.environ, _get_values(time_zone="incorrect-timezone")
    ), pytest.raises(
        ValidationError,
        match="Timezone 'incorrect-timezone' is incorrect.",
    ):
        AppConfig()


def test_secret_key():
    """
    Given an environment variable for SECRET_KEY set
    When we create a new object of AppConfig class
    Then the value for secret_key is set to a correct value.
    """
    value = "1234567890abcdeabcdeabcdeabcdeabcde"
    with patch.dict(os.environ, _get_values(secret_key=value)):
        config = AppConfig()

    assert config.secret_key.get_secret_value() == value


def test_secret_key_too_short():
    """
    Given an environment variable for SECRET_KEY set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(os.environ, _get_values(secret_key="secret-key")), pytest.raises(
        ValidationError, match="The secret key cannot be shorter than 30 characters."
    ):
        AppConfig()


def test_database_host():
    """
    Given an environment variable for DATABASE_HOST set
    When we create a new object of AppConfig class
    Then the value for database_host is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(database_host="sample-host")):
        config = AppConfig()

    assert config.database_host == "sample-host"


def test_database_port():
    """
    Given an environment variable for DATABASE_PORT set
    When we create a new object of AppConfig class
    Then the value for database_port is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(database_port="1234")):
        config = AppConfig()

    assert config.database_port == 1234


def test_database_port_incorrect_value():
    """
    Given an environment variable for DATABASE_PORT set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(
        os.environ, _get_values(database_port="incorrect-value")
    ), pytest.raises(ValidationError):
        AppConfig()


def test_database_user():
    """
    Given an environment variable for DATABASE_USER set
    When we create a new object of AppConfig class
    Then the value for database_user is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(database_user="sample-user")):
        config = AppConfig()

    assert config.database_user == "sample-user"


def test_database_password():
    """
    Given an environment variable for DATABASE_PASSWORD set
    When we create a new object of AppConfig class
    Then the value for database_password is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(database_password="sample-pass")):
        config = AppConfig()

    assert config.database_password.get_secret_value() == "sample-pass"


def test_database_name():
    """
    Given an environment variable for DATABASE_NAME set
    When we create a new object of AppConfig class
    Then the value for database_name is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(database_name="sample-db")):
        config = AppConfig()

    assert config.database_name == "sample-db"


@pytest.mark.parametrize(
    "field_name",
    ("DEBUG", "LOGGING_LEVEL", "TIME_ZONE"),
)
def test_missing_optional_fields(field_name):
    """
    Given an environment variable is missing for an optional settings field
    When we create a new object of AppConfig class
    Then no exceptions are raised.
    """
    with patch.dict(os.environ, _get_values(excluded_fields=[field_name]), clear=True):
        AppConfig(_env_file=None)


@pytest.mark.parametrize(
    "field_name",
    (
        "SECRET_KEY",
        "STATIC_FILES_DIR",
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
        "DATABASE_NAME",
    ),
)
def test_missing_required_fields(field_name, monkeypatch):
    """
    Given an environment variable is missing for a required settings field
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    monkeypatch.delenv(field_name, raising=False)

    with patch.dict(
        os.environ,
        _get_values(excluded_fields=[field_name]),
        clear=True,
    ), pytest.raises(ValidationError):
        AppConfig(_env_file=None)
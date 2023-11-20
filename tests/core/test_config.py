import os
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch

import pytest
from cybersmart_assessment.core.config import AppConfig
from pydantic import ValidationError


def _get_values(
    cache_host: Optional[str] = "localhost",
    cache_port: Optional[str] = "9876",
    database_host: Optional[str] = "localhost",
    database_name: Optional[str] = "db_name",
    database_password: Optional[str] = "db_pass",
    database_port: Optional[int] = "1234",
    database_user: Optional[str] = "db_user",
    debug: Optional[str] = "False",
    document_store_host: Optional[str] = "localhost",
    document_store_name: Optional[str] = "document_db_name",
    document_store_password: Optional[str] = "document_db_pass",
    document_store_port: Optional[int] = "2345",
    document_store_user: Optional[str] = "document_db_user",
    logging_level: Optional[str] = "info",
    public_host: Optional[str] = "localhost",
    secret_key: Optional[str] = "very-very-secret-top-secret-key",
    static_files_dir: Optional[str] = "/tmp",
    time_zone: Optional[str] = "Europe/London",
    weather_api_key: Optional[str] = "sample_api_key",
    excluded_fields: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Helper function that returns a dictionary with requested environment variables.
    """
    result = {
        "CACHE_HOST": cache_host,
        "CACHE_PORT": cache_port,
        "DATABASE_HOST": database_host,
        "DATABASE_NAME": database_name,
        "DATABASE_PASSWORD": database_password,
        "DATABASE_PORT": database_port,
        "DATABASE_USER": database_user,
        "DEBUG": debug,
        "DOCUMENT_STORE_HOST": document_store_host,
        "DOCUMENT_STORE_NAME": document_store_name,
        "DOCUMENT_STORE_PASSWORD": document_store_password,
        "DOCUMENT_STORE_PORT": document_store_port,
        "DOCUMENT_STORE_USER": document_store_user,
        "LOGGING_LEVEL": logging_level,
        "PUBLIC_HOST": public_host,
        "SECRET_KEY": secret_key,
        "STATIC_FILES_DIR": static_files_dir,
        "TIME_ZONE": time_zone,
        "WEATHER_API_KEY": weather_api_key,
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
        "cache_host": "localhost",
        "cache_port": 9876,
        "database_host": "localhost",
        "database_name": "db_name",
        "database_password": "db_pass",
        "database_port": 1234,
        "database_user": "db_user",
        "document_store_host": "localhost",
        "document_store_name": "document_db_name",
        "document_store_password": "document_db_pass",
        "document_store_port": 2345,
        "document_store_user": "document_db_user",
        "debug": False,
        "logging_level": "INFO",
        "public_host": "localhost",
        "secret_key": "very-very-secret-top-secret-key",
        "static_files_dir": Path("/tmp"),
        "time_zone": "Europe/London",
        "weather_api_key": "sample_api_key",
    }

    with patch.dict(os.environ, _get_values()):
        config = AppConfig()

        assert config.cache_host == expected["cache_host"]
        assert config.cache_port == expected["cache_port"]
        assert config.database_host == expected["database_host"]
        assert config.database_name == expected["database_name"]
        assert (
            config.database_password.get_secret_value() == expected["database_password"]
        )
        assert config.database_port == expected["database_port"]
        assert config.database_user == expected["database_user"]
        assert config.document_store_host == expected["document_store_host"]
        assert config.document_store_name == expected["document_store_name"]
        assert (
            config.document_store_password.get_secret_value()
            == expected["document_store_password"]
        )
        assert config.document_store_port == expected["document_store_port"]
        assert config.document_store_user == expected["document_store_user"]
        assert config.debug == expected["debug"]
        assert config.logging_level == expected["logging_level"]
        assert config.public_host == expected["public_host"]
        assert config.secret_key.get_secret_value() == expected["secret_key"]
        assert config.static_files_dir == expected["static_files_dir"]
        assert config.time_zone == expected["time_zone"]
        assert config.weather_api_key == expected["weather_api_key"]


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


def test_public_host():
    """
    Given an environment variable for PUBLIC_HOST set
    When we create a new object of AppConfig class
    Then the value for public_host is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(public_host="sample-host")):
        config = AppConfig()

    assert config.public_host == "sample-host"


def test_weather_api_key():
    """
    Given an environment variable for WEATHER_API_KEY set
    When we create a new object of AppConfig class
    Then the value for weather_api_key is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(weather_api_key="sample-key")):
        config = AppConfig()

    assert config.weather_api_key == "sample-key"


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


def test_document_store_host():
    """
    Given an environment variable for DOCUMENT_STORE_HOST set
    When we create a new object of AppConfig class
    Then the value for document_store_host is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(document_store_host="sample-host")):
        config = AppConfig()

    assert config.document_store_host == "sample-host"


def test_document_store_port():
    """
    Given an environment variable for DOCUMENT_STORE_PORT set
    When we create a new object of AppConfig class
    Then the value for document_store_port is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(document_store_port="1234")):
        config = AppConfig()

    assert config.document_store_port == 1234


def test_document_store_port_incorrect_value():
    """
    Given an environment variable for DOCUMENT_STORE_PORT set to an incorrect value
    When we create a new object of AppConfig class
    Then a ValidationError is raised.
    """
    with patch.dict(
        os.environ, _get_values(document_store_port="incorrect-value")
    ), pytest.raises(ValidationError):
        AppConfig()


def test_document_store_user():
    """
    Given an environment variable for DOCUMENT_STORE_USER set
    When we create a new object of AppConfig class
    Then the value for document_store_user is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(document_store_user="sample-user")):
        config = AppConfig()

    assert config.document_store_user == "sample-user"


def test_document_store_password():
    """
    Given an environment variable for DOCUMENT_STORE_PASSWORD set
    When we create a new object of AppConfig class
    Then the value for document_store_password is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(document_store_password="sample-pass")):
        config = AppConfig()

    assert config.document_store_password.get_secret_value() == "sample-pass"


def test_document_store_name():
    """
    Given an environment variable for DOCUMENT_STORE_NAME set
    When we create a new object of AppConfig class
    Then the value for document_store_name is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(document_store_name="sample-db")):
        config = AppConfig()

    assert config.document_store_name == "sample-db"


def test_cache_host():
    """
    Given an environment variable for CACHE_HOST set
    When we create a new object of AppConfig class
    Then the value for cache_host is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(cache_host="sample-cache")):
        config = AppConfig()

    assert config.cache_host == "sample-cache"


def test_cache_port():
    """
    Given an environment variable for CACHE_PORT set
    When we create a new object of AppConfig class
    Then the value for cache_port is set to a correct value.
    """
    with patch.dict(os.environ, _get_values(cache_port="1234")):
        config = AppConfig()

    assert config.cache_port == 1234


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
        "CACHE_HOST",
        "CACHE_PORT",
        "DATABASE_HOST",
        "DATABASE_NAME",
        "DATABASE_PASSWORD",
        "DATABASE_PORT",
        "DATABASE_USER",
        "DOCUMENT_STORE_HOST",
        "DOCUMENT_STORE_NAME",
        "DOCUMENT_STORE_PASSWORD",
        "DOCUMENT_STORE_PORT",
        "DOCUMENT_STORE_USER",
        "PUBLIC_HOST",
        "SECRET_KEY",
        "STATIC_FILES_DIR",
        "WEATHER_API_KEY",
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

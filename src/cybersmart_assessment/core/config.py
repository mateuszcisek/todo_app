from typing import Literal

from pydantic import DirectoryPath, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytz import all_timezones


class AppConfig(BaseSettings):
    """App configuration.

    The settings' values are fetched from the environment variables.
    """

    debug: bool = Field(False)
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field("INFO")
    public_host: str
    secret_key: SecretStr
    static_files_dir: DirectoryPath
    time_zone: str = Field("Europe/London")

    database_host: str
    database_port: int
    database_user: str
    database_password: SecretStr
    database_name: str

    document_store_host: str
    document_store_port: int
    document_store_user: str
    document_store_password: SecretStr
    document_store_name: str

    weather_api_key: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".env",),
        env_prefix="TODO_",
        extra="ignore",
    )

    @field_validator("logging_level", mode="before")
    @classmethod
    def normalize_logging_level(cls, value: str) -> str:
        """Make sure the value is uppercase."""
        return value.upper()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr) -> SecretStr:
        """Check if the secret key is long enough."""
        value = value.get_secret_value().strip()
        if len(value) < 30:
            raise ValueError("The secret key cannot be shorter than 30 characters.")

        return SecretStr(value)

    @field_validator("time_zone")
    @classmethod
    def validate_time_zone(cls, value: str) -> str:
        """Make sure the timezone is correct."""
        if value not in all_timezones:
            raise ValueError("Timezone '%s' is incorrect." % value)

        return value

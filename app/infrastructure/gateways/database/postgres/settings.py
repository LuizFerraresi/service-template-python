from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL

from .constants import DATABASE_SETTINGS_PREFIX, DatabaseDeploymentMode, DatabasePostgresEcho


class DatabaseDeploymentModeSettings(BaseSettings):
    """Database deployment mode settings."""

    deployment_mode: DatabaseDeploymentMode = Field(..., validation_alias=f'{DATABASE_SETTINGS_PREFIX}_DEPLOYMENT_MODE')


class DatabasePostgresSettings(DatabaseDeploymentModeSettings):
    """Database PostgreSQL settings."""

    driver: str = Field(
        default='asyncpg', description='Database driver', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_DRIVER'
    )
    dialect: str = Field(
        default='postgresql', description='Database dialect', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_DIALECT'
    )
    username: str = Field(
        default=..., description='Database username', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_USERNAME'
    )
    password: str = Field(
        default=..., description='Database password', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_PASSWORD'
    )
    host: str = Field(default=..., description='Database host', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_HOST')
    port: int = Field(default=5432, description='Database port', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_PORT')
    name: str = Field(
        default='postgres', description='Database name', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_NAME'
    )
    pool_size: int = Field(
        default=10, description='Database pool size', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_POOL_SIZE'
    )
    max_overflow: int = Field(
        default=20, description='Database max overflow', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_MAX_OVERFLOW'
    )
    pool_recycle_seconds: int = Field(
        default=300,
        description='Database pool recycle seconds',
        validation_alias=f'{DATABASE_SETTINGS_PREFIX}_POOL_RECYCLE_SECONDS',
    )
    pool_timeout_seconds: int = Field(
        default=30,
        description='Database pool timeout seconds',
        validation_alias=f'{DATABASE_SETTINGS_PREFIX}_POOL_TIMEOUT_SECONDS',
    )
    pool_pre_ping: bool = Field(
        default=True, description='Database pool pre ping', validation_alias=f'{DATABASE_SETTINGS_PREFIX}_POOL_PRE_PING'
    )
    echo_sql: str | DatabasePostgresEcho = Field(
        default=DatabasePostgresEcho.DISABLED,
        description='Database echo SQL',
        validation_alias=f'{DATABASE_SETTINGS_PREFIX}_ECHO_SQL',
    )
    echo_pool: str | DatabasePostgresEcho = Field(
        default=DatabasePostgresEcho.DISABLED,
        description='Database echo pool',
        validation_alias=f'{DATABASE_SETTINGS_PREFIX}_ECHO_POOL',
    )
    # connection_timeout_seconds: int = Field(
    #    default=10,
    #    description='Database connection timeout seconds',
    #    validation_alias=f'{DATABASE_SETTINGS_PREFIX}_CONNECTION_TIMEOUT_SECONDS',
    # )
    # statement_timeout_ms: int = Field(
    #     default=30,
    #     description="Database statement timeout seconds",
    #     validation_alias=f"{DATABASE_SETTINGS_PREFIX}_STATEMENT_TIMEOUT_MS"
    # )

    def build_uri(self) -> URL:
        """Build the database URI."""
        return URL.create(
            drivername=f'{self.dialect}+{self.driver}',
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )

    def __init_subclass__(cls, host_alias: str | None, **kwargs) -> None:  # type: ignore  # noqa: ANN003
        """Initialize subclass with custom validation prefix."""
        if host_alias is not None:
            prefix = f'{DATABASE_SETTINGS_PREFIX}_{host_alias.upper()}'

            for field_name, field_info in cls.model_fields.items():
                if hasattr(field_info, 'validation_alias'):
                    field_info.validation_alias = f'{prefix}_{field_name.upper()}'

        super().__init_subclass__(**kwargs)

    @field_validator('echo_sql', 'echo_pool', mode='before')
    @classmethod
    def validate_echo(cls, value: str | DatabasePostgresEcho) -> DatabasePostgresEcho:
        """Validate echo."""
        if isinstance(value, DatabasePostgresEcho):
            return value

        value = value.lower()
        values = {
            'true': DatabasePostgresEcho.ENABLED,
            'false': DatabasePostgresEcho.DISABLED,
            'debug': DatabasePostgresEcho.DEBUG,
        }
        if value not in values:
            raise ValueError('Invalid echo')
        return values[value]


def create_database_postgres_settings(host_alias: str | None) -> type[DatabasePostgresSettings]:
    """Factory function to create database settings with custom prefix."""

    class CustomDatabasePostgresSettings(DatabasePostgresSettings, host_alias=host_alias):
        pass

    return CustomDatabasePostgresSettings

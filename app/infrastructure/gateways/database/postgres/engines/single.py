import logging
from asyncio import current_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.sql import text

from ..constants import DATABASE_HEALTHCHECK_QUERY
from ..settings import DatabasePostgresSettings

logger = logging.getLogger(__name__)


class DatabasePostgresSingleGateway:
    """Database PostgreSQL Gateway."""

    def __init__(self, settings: DatabasePostgresSettings, application_alias: str) -> None:
        """Initialize the database adapter."""
        self._application = application_alias
        self._settings = settings
        self._async_engine: AsyncEngine

    @property
    def _async_engine_config(self) -> dict:
        return {
            'pool_size': self._settings.pool_size,
            'max_overflow': self._settings.max_overflow,
            'pool_timeout': self._settings.pool_timeout_seconds,
            'pool_pre_ping': self._settings.pool_pre_ping,
            'pool_recycle': self._settings.pool_recycle_seconds,
            'echo': self._settings.echo_sql,
        }

    @property
    def _connection_args(self) -> dict[str, dict]:
        return {
            'server_settings': {
                'application_name': self._application,
                # 'timeout': str(self._settings.connection_timeout_seconds),
                # "statement_timeout": str(self._settings.statement_timeout_seconds),
            }
        }

    def _async_session_facrory(self, async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
            future=True,
        )

    async def connect(self) -> None:
        """Connect to the database."""
        # logger.info(f'[ADAPTER][DATABASE][CONNECTION MODE: {connection_mode.value.upper()}]')
        logger.info(f'[ADAPTER][DATABASE][CONNECTION URI: {self._settings.build_uri().render_as_string()}]')
        self._async_engine = create_async_engine(
            url=self._settings.build_uri(), **self._async_engine_config, connect_args=self._connection_args
        )
        await self.healthcheck()

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        """Get a connection from the database."""
        async with self._async_engine as connection, connection.begin():  # pyright: ignore[reportGeneralTypeIssues]
            yield connection

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a session from the database."""
        current_session = async_scoped_session(self._async_session_facrory(self._async_engine), current_task)
        try:
            yield current_session()
            await current_session.commit()
        except Exception as err:
            logger.error(f'[ADAPTER][DATABASE][SESSION ROLLBACK][ERROR]: {err}')
            await current_session.rollback()
            raise
        finally:
            await current_session.close()

    async def disconnect(self) -> None:
        """Disconnect from the database."""
        await self._async_engine.dispose()
        del self._async_engine
        logger.info('[ADAPTER][DATABASE][RW DISCONNECTED]')

    async def healthcheck(self) -> bool:
        """Test the engine connection with the connection pool and with the database host.

        The engine.connect() validate if the pool is active.
        The connection.execute() validate if the connection is active.
        """
        async with self.get_connection() as connection:
            result = await connection.execute(text(DATABASE_HEALTHCHECK_QUERY))
            result = result.scalar()

        healthy: bool = result == 1
        logger.info(f'[ADAPTER][DATABASE][CONNECTION ACTIVE: {healthy}]')

        return healthy

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from ..settings import CacheRedisSettings

logger = logging.getLogger(__name__)


class CacheRedisSingleGateway:
    """Redis Single Instance Gateway."""

    def __init__(self, settings: CacheRedisSettings, application_alias: str) -> None:
        """Redis Instance Gateway Implementation."""
        self._application_alias = application_alias
        self._settings = settings
        self._connection_pool: ConnectionPool | None = None

    @property
    def _common_config(self) -> dict[str, Any]:
        return {
            'host': self._settings.host,
            'port': self._settings.port,
            'db': self._settings.db,
            'socket_timeout': self._settings.socket_timeout,
            'socket_keepalive': self._settings.socket_keepalive,
            'socket_connect_timeout': self._settings.socket_connect_timeout,
            'max_connections': self._settings.max_connections,
            'health_check_interval': self._settings.health_check_interval,
            'client_name': self._application_alias,
        }

    @property
    def _config(self) -> dict[str, Any]:
        return {
            **self._common_config,
            'retry_on_timeout': self._settings.retry_on_timeout,  # type: ignore
        }

    async def connect(self) -> None:
        """Create the connection pool with Redis."""
        logger.info(f'[GATEWAY][CACHE][CONNECTION URI: {self._settings.build_uri_hidden_password}]')
        logger.info(f'[GATEWAY][CACHE][CONNECTION MODE: {self._settings.deployment_mode.value.upper()}]')
        self._connection_pool = ConnectionPool(**self._config)
        logger.info(f'[GATEWAY][CACHE][CONNECTION POOL ACTIVE: {self._connection_pool.can_get_connection()}]')
        logger.info(f'[GATEWAY][CACHE][CONNECTION ACTIVE: {await self.healthcheck()}]')

    async def disconnect(self) -> None:
        """Close connection pool."""
        if self._connection_pool:
            await self._connection_pool.aclose()
            del self._connection_pool
        logger.info('[GATEWAY][CACHE][DISCONNECTED]')

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[Redis, None]:
        """Get Session from Redis Pool using context manager."""
        async with Redis(connection_pool=self._connection_pool) as session:
            yield session

    async def healthcheck(self) -> tuple[bool, str | None]:
        """Check the health of the cache."""
        try:
            async with self.get_session() as session:
                session.ping()
            return True, None
        except Exception as err:
            return False, str(err)

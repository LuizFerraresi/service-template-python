import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff

from ..settings import CacheRedisClusterSettings

logger = logging.getLogger(__name__)


class CacheRedisClusterGateway:
    """Redis Cluster Gateway."""

    def __init__(self, settings: CacheRedisClusterSettings, application_alias: str) -> None:
        """Redis Cluster Gateway Implementation."""
        self._application_alias = application_alias
        self._settings = settings
        self._connection: RedisCluster

    @property
    def _retry_config(self) -> dict[str, Any]:
        retry_config = {
            'retry': Retry(ExponentialBackoff(), retries=self._settings.retry_max_attempts),
            'retry_on_error': [ConnectionError, TimeoutError],
        }
        return retry_config

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
            **self._retry_config,
            'load_balancing_strategy': self._settings.load_balancing_strategy,
            'require_full_coverage': self._settings.require_full_coverage,
        }

    async def connect(self) -> None:
        """Connect to the cache."""
        logger.info(f'[GATEWAY][CACHE][CONNECTION URI: {self._settings.build_uri_hidden_password}]')
        logger.info(f'[GATEWAY][CACHE][CONNECTION MODE: {self._settings.deployment_mode.value.upper()}]')
        self._connection = RedisCluster(**self._config)
        logger.info(f'[GATEWAY][CACHE][CONNECTION ACTIVE: {await self.healthcheck()}]')
        logger.info(f'[GATEWAY][CACHE][CLUSTER NODES: {self._connection.get_nodes()}]')

    async def disconnect(self) -> None:
        """Disconnect from REdis Cluster."""
        if self._connection:
            await self._connection.aclose()
            del self._connection
        logger.info('[GATEWAY][CACHE][DISCONNECTED]')

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[RedisCluster, None]:
        """Get a session to connect to Redis Cluster."""
        async with self._connection as session:
            yield session

    async def healthcheck(self) -> tuple[bool, str | None]:
        """Check the health of the cache."""
        try:
            async with self.get_session() as session:
                session.ping()
            return True, None
        except Exception as err:
            return False, str(err)

from unittest.mock import MagicMock, AsyncMock

from src.infrastructure.repositories import CacheRepository, DatabaseRepository, BrokerRepository


async def http_gateway_stub():
    return


async def cache_repository_mock() -> MagicMock:
    mock = MagicMock(spec=CacheRepository)
    return mock


async def database_repository_mock() -> MagicMock:
    mock = MagicMock(spec=DatabaseRepository)
    return mock


async def broker_repository_mock() -> MagicMock:
    mock = MagicMock(spec=BrokerRepository)
    return mock

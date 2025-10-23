from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, ThreadSafeSingleton

from app.infrastructure.gateways import CacheRedisGateway, DatabasePostgresGateway


class ApplicationContainer(DeclarativeContainer):
    """Applications Dependency Injections."""

    # Database Gateway
    database_pool = ThreadSafeSingleton(DatabasePostgresGateway)
    database_session = Factory(lambda database: database.inject_session, database=database_pool)

    # Cache Gateway
    cache_adapter = ThreadSafeSingleton(CacheRedisGateway)
    cache_session = Factory(lambda cache: cache.inject_session, cache=cache_adapter)

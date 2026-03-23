from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware import Middleware

from app.containers import ApplicationContainer
from app.entrypoints.routes import healthcheck, index, metrics, v1, who
from app.infrastructure.gateways import PrometheusMiddleware
from app.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """A FastAPI lifespan is a context manager that defines actions to run when the application starts and stops."""
    # Startup

    yield

    # Post Stop


def application() -> FastAPI:
    """Build FastAPI Application."""
    containers = ApplicationContainer()
    middlewares = [Middleware(PrometheusMiddleware, settings.application.name)]

    app = FastAPI(
        title=settings.application.name,
        version=settings.application.version,
        middleware=middlewares,
        containers=containers,
    )

    app.include_router(index)
    app.include_router(healthcheck)
    app.include_router(who)
    app.include_router(metrics)
    app.include_router(v1)

    return app


app = application()

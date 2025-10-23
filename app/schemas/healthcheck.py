from pydantic import BaseModel

from app.constants import HealthStatus


class GatewaySchema(BaseModel):
    """Schema for gateway healthcheck response."""

    status: HealthStatus
    error: str | None = None


class HealthcheckResponseSchema(BaseModel):
    """Healthcheck response contract."""

    status: HealthStatus
    dependencies: dict[str, GatewaySchema | None]

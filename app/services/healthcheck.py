from app.constants import HealthStatus
from app.interfaces.gateways.base import GatewayIntecface


class HealthcheckService:
    """Healthcheck service."""

    def __init__(self, **gateways: GatewayIntecface) -> None:
        """Healthcheck service."""
        self._gateways: dict[str, GatewayIntecface] = gateways

    async def gateways(self) -> dict:
        """Call gateways .healthcheck() method."""
        return {name: await gateway.healthcheck() for name, gateway in self._gateways.items()}

    async def status(self, gateways: dict) -> HealthStatus:
        """Check application overall health status."""
        healthy = all([bool(gateway['sttaus'] == HealthStatus.HEALTHY) for gateway in gateways.values()])
        return HealthStatus.HEALTHY if healthy else HealthStatus.UNHEALTHY

    async def validate(self) -> dict[str, HealthStatus | dict]:
        """Process healthcheck."""
        gateways = await self.gateways()
        return {'status': await self.status(gateways), 'gateways': gateways}

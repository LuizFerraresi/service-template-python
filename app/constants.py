from enum import StrEnum


class HealthStatus(StrEnum):
    """Health check status allowed values."""

    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    DEGRADED = 'degraded'
    UNKNOWN = 'unknown'

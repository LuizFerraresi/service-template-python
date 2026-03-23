from pydantic import Field
from pydantic_settings import BaseSettings

from .constants import METRICS_SETTING_PREFIX


class PrometheusSettings(BaseSettings):
    """Metrics Prometheus Settings."""

    metrics_path: str = Field(..., validation_alias=f'{METRICS_SETTING_PREFIX}_PATH')
    metrics_exclude_paths: list[str] = Field(..., validation_alias=f'{METRICS_SETTING_PREFIX}_EXCLUDE_PATHS')

    @classmethod
    def validate_metrics_excluded_paths(cls, values: dict) -> dict:
        """Parse metrics excluded paths from string to list of strings."""
        values['metrics_exclude_paths'] = values['metrics_exclude_paths'].split(',')
        return values

from enum import StrEnum

METRICS_SETTING_PREFIX = 'METRICS'

METRIC_PREFIX = 'fastapi'


class MetricLabels(StrEnum):
    """Prometheus Metrics Labels."""

    APPLICATION_ALIAS = 'application_alias'
    METHOD = 'method'
    PATH = 'path'
    STATUS_CODE = 'status_code'
    EXCEPTION_TYPE = 'execption_type'

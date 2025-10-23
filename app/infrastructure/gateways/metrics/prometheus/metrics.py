from prometheus_client.metrics import Counter, Gauge, Histogram

from .constants import METRIC_PREFIX, MetricLabels

METRICS_DEFAULT_LABELS: list[str] = [
    str(MetricLabels.APPLICATION_ALIAS),
    str(MetricLabels.METHOD),
    str(MetricLabels.PATH),
]

REQUESTS = Counter(
    f'{METRIC_PREFIX}_requests_total', 'Total count of requests by method and path.', METRICS_DEFAULT_LABELS
)

RESPONSES = Counter(
    f'{METRIC_PREFIX}_responses_total',
    'Total count of responses by method, path and status codes.',
    METRICS_DEFAULT_LABELS + [str(MetricLabels.STATUS_CODE)],
)

REQUESTS_PROCESSING_TIME = Histogram(
    f'{METRIC_PREFIX}_requests_duration_seconds',
    'Histogram of requests processing time by path (in seconds)',
    METRICS_DEFAULT_LABELS,
)

EXCEPTIONS = Counter(
    f'{METRIC_PREFIX}_exceptions_total',
    'Total count of exceptions raised by path and exception type',
    METRICS_DEFAULT_LABELS + [str(MetricLabels.EXCEPTION_TYPE)],
)

REQUESTS_IN_PROGRESS = Gauge(
    f'{METRIC_PREFIX}_requests_in_progress',
    'Gauge of requests by method and path currently being processed',
    METRICS_DEFAULT_LABELS,
)

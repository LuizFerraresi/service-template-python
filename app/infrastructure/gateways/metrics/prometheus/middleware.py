import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

from .metrics import EXCEPTIONS, REQUESTS, REQUESTS_IN_PROGRESS, REQUESTS_PROCESSING_TIME, RESPONSES

_logger = logging.getLogger(__name__)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Prometheus Middleware."""

    def __init__(self, app: ASGIApp, application_alias: str) -> None:
        """Metrics Middleware."""
        super().__init__(app)
        self._application_alias = application_alias

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Request Dispatch method."""
        status_code = None
        metric_labels = {
            'method': request.method,
            'path': request.url.path,
            'application_alias': self._application_alias,
        }

        REQUESTS_IN_PROGRESS.labels(**metric_labels).inc()
        REQUESTS.labels(**metric_labels).inc()
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except BaseException as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(**metric_labels, status_code=status_code, exception_type=type(e).__name__).inc()
            raise e from None
        else:
            status_code = response.status_code
        finally:
            RESPONSES.labels(**metric_labels, status_code=status_code).inc()
            REQUESTS_IN_PROGRESS.labels(**metric_labels).dec()
            REQUESTS_PROCESSING_TIME.labels(**metric_labels, status_code=status_code).observe(
                time.perf_counter() - start_time
            )
        return response

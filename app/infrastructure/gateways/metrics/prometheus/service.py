from prometheus_client import REGISTRY
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST, generate_latest
from starlette.requests import Request
from starlette.responses import Response


async def prometheus_service(request: Request) -> Response:
    """Prometheus Service to scrape metrics."""
    return Response(generate_latest(REGISTRY), headers={'Content-Type': CONTENT_TYPE_LATEST})

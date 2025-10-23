from fastapi import APIRouter, Request, Response

from app.infrastructure.gateways import prometheus_service_metrics

router = APIRouter(tags=['observability'])


@router.get('/metrics')
async def metrics_route(request: Request) -> Response:
    """Expose metrics endpoint."""
    return await prometheus_service_metrics(request)

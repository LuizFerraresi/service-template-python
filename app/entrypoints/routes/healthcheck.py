from typing import Any

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.schemas.healthcheck import HealthcheckResponseSchema
from app.services.healthcheck import HealthcheckService

router = APIRouter()


@router.get(path='/healthcheck', status_code=HTTP_200_OK, response_model=HealthcheckResponseSchema)
async def healthcheck_route() -> dict[str, Any]:
    """Expose health check route."""
    service = HealthcheckService()
    return await service.validate()

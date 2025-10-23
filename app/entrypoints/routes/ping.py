from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.schemas.ping import PingResponseSchema

router = APIRouter()


@router.get(path='/ping', status_code=HTTP_200_OK, response_model=PingResponseSchema)
async def ping_route() -> dict[str, str]:
    """Expose ping endpoint."""
    return {'message': 'pong'}

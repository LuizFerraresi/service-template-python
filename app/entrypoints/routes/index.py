from fastapi import APIRouter

from app.schemas.index import IndexResponseSchema
from app.settings import get_settings

settings = get_settings()
router = APIRouter()


@router.get(
    path='/',
    tags=['Index'],
    response_model=IndexResponseSchema,
)
async def index_route() -> dict[str, str]:
    """Expose index route."""
    return {'application': settings.application.name, 'version': settings.application.version}

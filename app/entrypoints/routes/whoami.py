from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/who')
async def whoami_route(request: Request) -> dict:
    """Expose whoami endpoint."""
    client_host = request.client
    forwarded_for = request.headers.get('x-forwarded-for')
    real_ip = forwarded_for.split(',')[0].strip() if forwarded_for else client_host
    user_agent = request.headers.get('user-agent', 'unknown')

    return {
        'ip': real_ip,
        'client': client_host,
        'user_agent': user_agent,
        'headers': dict(request.headers),
    }

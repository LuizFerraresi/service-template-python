from pydantic import BaseModel


class PingResponseSchema(BaseModel):
    """Ping response contract."""

    message: str

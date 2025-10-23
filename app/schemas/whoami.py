from pydantic import BaseModel


class WhoAmIResonseSchema(BaseModel):
    """Who Am I Endpoint response contract."""

    ip: str
    client: str
    user_agent: str
    headers: dict

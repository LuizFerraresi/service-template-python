from pydantic import BaseModel


class IndexResponseSchema(BaseModel):
    """Index response contract."""

    application: str
    version: str

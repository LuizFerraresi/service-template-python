from typing import Protocol


class GatewayIntecface(Protocol):
    """Gateway interface."""

    def __init__(self) -> None:
        """Gateway instance."""
        ...

    async def healthcheck(self) -> tuple[bool, str | None]:
        """Check Gateway connection health."""
        ...

from .constants import DatabaseDeploymentMode
from .engines.single import DatabasePostgresSingleGateway
from .settings import DatabaseDeploymentModeSettings, create_database_postgres_settings


class DatabasePostgresGateway:
    """PostgreSQL Single Instance Gateway."""

    def __init__(
        self, application_alias: str, host_alias: str, deployment_mode: DatabaseDeploymentMode | None = None
    ) -> None:
        """Instance and Configure PostgreSQL Adapter."""
        self._deployment_mode = deployment_mode or self.get_deployment_mode()
        self._application_alias = application_alias
        self._host_alias = host_alias

    @staticmethod
    def get_deployment_mode() -> DatabaseDeploymentMode:
        """Get deployment_mode using env vars by Pydantic Model."""
        settings = DatabaseDeploymentModeSettings()  # pyright: ignore[reportCallIssue]
        return settings.deployment_mode

    def single_config(self) -> DatabasePostgresSingleGateway:
        """Congifure PostgreSQL Gateway to Single Instance."""
        CustomSettings = create_database_postgres_settings(self._host_alias)
        return DatabasePostgresSingleGateway(CustomSettings(), self._application_alias)  # pyright: ignore[reportCallIssue]

    # def cluster_config(self):
    #     return

    def config(self) -> DatabasePostgresSingleGateway:
        """Config gateway based on DEPLOYMENT_MODE env var."""
        deploy = {
            str(DatabaseDeploymentMode.SINGLE): self.single_config,
            # str(DatabaseDeploymentMode.CLUSTER): self.cluster_config,
        }
        return deploy[self._deployment_mode]()

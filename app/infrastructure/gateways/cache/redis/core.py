from .constants import CacheDeploymentMode
from .engines.cluster import CacheRedisClusterGateway
from .engines.single import CacheRedisSingleGateway
from .settings import CacheDeploymentModeSettings, CacheRedisClusterSettings, CacheRedisSettings


class CacheRedisGateway:
    """Cache Redis Gateway."""

    def __init__(self, application_alias: str, deployment_mode: CacheDeploymentMode | None = None) -> None:
        """Instance and Configure Cache Redis."""
        self._deployment_mode = deployment_mode or self.get_deployment_mode()
        self._application_alias = application_alias

    @staticmethod
    def get_deployment_mode() -> CacheDeploymentMode:
        """Get deployment_mode using env vars by Pydantic Model."""
        settings = CacheDeploymentModeSettings()
        return settings.deployment_mode

    def single_config(self) -> CacheRedisSingleGateway:
        """Configure Redis Gateway to Single Instance."""
        return CacheRedisSingleGateway(CacheRedisSettings(), self._application_alias)

    def cluster_config(self) -> CacheRedisClusterGateway:
        """Configure Redis Gateway to Cluster Instance."""
        return CacheRedisClusterGateway(CacheRedisClusterSettings(), self._application_alias)

    def config(self) -> CacheRedisSingleGateway | CacheRedisClusterGateway:
        """Config gateway based on DEPLOYMENT_MODE env var."""
        deploy = {
            str(CacheDeploymentMode.SINGLE): self.single_config,
            str(CacheDeploymentMode.CLUSTER): self.cluster_config,
        }
        return deploy[self._deployment_mode]()

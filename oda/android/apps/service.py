from oda.android.apps.models import InstalledApp
from oda.android.apps.provider import AppProvider
from oda.android.apps.registry import AppRegistry


class AppService:
    def __init__(
        self,
        provider: AppProvider,
        registry: AppRegistry | None = None,
    ):
        self.provider = provider
        self.registry = registry or AppRegistry()

    def refresh(self) -> list[InstalledApp]:
        apps = self.provider.list_apps()

        for app in apps:
            self.registry.add(app)

        return apps

    def find(self, name: str) -> InstalledApp | None:
        return self.registry.find_partial(name)

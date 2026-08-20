from oda.android.apps.models import InstalledApp


class AppRegistry:
    def __init__(self):
        self._apps: dict[str, InstalledApp] = {}

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(
            text.strip().lower().split()
        )

    def add(self, app: InstalledApp) -> None:
        self._apps[self._normalize(app.name)] = app

    def all(self) -> list[InstalledApp]:
        return list(self._apps.values())

    def find(self, name: str) -> InstalledApp | None:
        return self._apps.get(self._normalize(name))

    def find_partial(self, name: str) -> InstalledApp | None:
        target = self._normalize(name)

        for app in self._apps.values():
            app_name = self._normalize(app.name)

            if target in app_name or app_name in target:
                return app

        return None

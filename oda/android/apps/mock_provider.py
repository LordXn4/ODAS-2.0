from oda.android.apps.models import InstalledApp
from oda.android.apps.provider import AppProvider


class MockAppProvider(AppProvider):
    def list_apps(self) -> list[InstalledApp]:
        return [
            InstalledApp(
                name="YouTube",
                package_name="com.google.android.youtube",
            ),
            InstalledApp(
                name="Google Chrome",
                package_name="com.android.chrome",
            ),
            InstalledApp(
                name="Configurações",
                package_name="com.android.settings",
            ),
        ]

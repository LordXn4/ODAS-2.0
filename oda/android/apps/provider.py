from abc import ABC, abstractmethod

from oda.android.apps.models import InstalledApp


class AppProvider(ABC):
    """
    Interface para descobrir aplicativos instalados.

    A implementação Android real usará o PackageManager.
    """

    @abstractmethod
    def list_apps(self) -> list[InstalledApp]:
        raise NotImplementedError

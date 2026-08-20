from abc import ABC, abstractmethod

from oda.android.accessibility.actions import AccessibilityAction
from oda.android.accessibility.ui import UISnapshot


class AccessibilityBridge(ABC):
    """
    Contrato entre o núcleo da ODA e a implementação Android.

    O núcleo não conhece ADB, Termux ou detalhes da interface Android.
    """

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def screen(self) -> UISnapshot:
        raise NotImplementedError

    @abstractmethod
    def execute(self, action: AccessibilityAction) -> bool:
        raise NotImplementedError

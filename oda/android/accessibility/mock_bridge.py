from oda.android.accessibility.actions import AccessibilityAction
from oda.android.accessibility.bridge import AccessibilityBridge
from oda.android.accessibility.ui import UISnapshot


class MockAccessibilityBridge(AccessibilityBridge):
    """Ponte usada somente nos testes do núcleo da ODA."""

    def __init__(self):
        self._screen = UISnapshot()
        self.executed_actions: list[AccessibilityAction] = []

    def is_available(self) -> bool:
        return True

    def screen(self) -> UISnapshot:
        return self._screen

    def execute(self, action: AccessibilityAction) -> bool:
        self.executed_actions.append(action)
        return True

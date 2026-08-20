from oda.android.accessibility.actions import (
    AccessibilityAction,
    ActionType,
)


class AccessibilityManager:
    def __init__(self):
        self.enabled = False

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def is_enabled(self) -> bool:
        return self.enabled

    def validate(self, action: AccessibilityAction) -> bool:
        if not self.enabled:
            return False

        if action.type == ActionType.TAP:
            return action.x is not None and action.y is not None

        if action.type == ActionType.OPEN_APP:
            return bool(action.app)

        if action.type == ActionType.SEARCH:
            return bool(action.text)

        return True

    def describe(self, action: AccessibilityAction) -> str:
        if not self.validate(action):
            return "Ação não disponível."

        return action.description

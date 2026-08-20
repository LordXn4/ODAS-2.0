from oda.android.accessibility.actions import (
    AccessibilityAction,
    ActionType,
)
from oda.android.accessibility.bridge import AccessibilityBridge
from oda.android.apps.service import AppService


class AccessibilityController:
    def __init__(
        self,
        bridge: AccessibilityBridge,
        apps: AppService,
    ):
        self.bridge = bridge
        self.apps = apps

    def open_app(self, name: str) -> bool:
        app = self.apps.find(name)

        if app is None or not app.launchable:
            return False

        action = AccessibilityAction(
            type=ActionType.OPEN_APP,
            description=f"Abrir {app.name}",
            app=app.package_name,
        )

        return self._execute(action)

    def back(self) -> bool:
        return self._execute(
            AccessibilityAction(
                type=ActionType.BACK,
                description="Voltar",
            )
        )

    def home(self) -> bool:
        return self._execute(
            AccessibilityAction(
                type=ActionType.HOME,
                description="Tela inicial",
            )
        )

    def tap(self, x: int, y: int) -> bool:
        return self._execute(
            AccessibilityAction(
                type=ActionType.TAP,
                description=f"Toque em {x},{y}",
                x=x,
                y=y,
            )
        )

    def _execute(self, action: AccessibilityAction) -> bool:
        if not self.bridge.is_available():
            return False

        return self.bridge.execute(action)

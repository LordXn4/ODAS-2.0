from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):
    TAP = "tap"
    SWIPE = "swipe"
    BACK = "back"
    HOME = "home"
    OPEN_APP = "open_app"
    SEARCH = "search"


@dataclass
class AccessibilityAction:
    type: ActionType
    description: str
    x: int | None = None
    y: int | None = None
    text: str | None = None
    app: str | None = None

from typing import Callable


class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Callable] = {}

    def register(self, name: str, handler: Callable) -> None:
        self._commands[name] = handler

    def execute(self, name: str, *args, **kwargs):
        handler = self._commands.get(name)

        if handler is None:
            return None

        return handler(*args, **kwargs)

    def has(self, name: str) -> bool:
        return name in self._commands

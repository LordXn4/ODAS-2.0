from typing import Callable


class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Callable] = {}

    @staticmethod
    def _normalize(name: str) -> str:
        return " ".join(
            name.strip().lower().rstrip("!?.,;:")
            .split()
        )

    def register(self, name: str, handler: Callable) -> None:
        self._commands[self._normalize(name)] = handler

    def execute(self, name: str, *args, **kwargs):
        handler = self._commands.get(self._normalize(name))

        if handler is None:
            return None

        return handler(*args, **kwargs)

    def has(self, name: str) -> bool:
        return self._normalize(name) in self._commands

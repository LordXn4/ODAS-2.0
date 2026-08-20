from dataclasses import dataclass
from typing import Literal


Route = Literal["command", "llm"]


@dataclass
class RouteResult:
    route: Route
    text: str


class Router:
    COMMAND_PREFIXES = (
        "abra ",
        "feche ",
        "inicie ",
        "pare ",
        "aumente ",
        "diminua ",
        "mude ",
        "ative ",
        "desative ",
    )

    COMMAND_PHRASES = {
        "diagnóstico do sistema",
        "diagnostico do sistema",
        "status da ram",
        "status da memória",
        "status da memoria",
    }

    def route(self, text: str) -> RouteResult:
        normalized = " ".join(
            text.strip().lower().split()
        ).rstrip("!?.,;:")

        if (
            normalized.startswith(self.COMMAND_PREFIXES)
            or normalized in self.COMMAND_PHRASES
        ):
            return RouteResult("command", text)

        return RouteResult("llm", text)

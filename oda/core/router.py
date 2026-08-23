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

        # Volume
        "aumente o volume",
        "aumentar o volume",
        "aumente volume",
        "aumentar volume",
        "diminua o volume",
        "diminuir o volume",
        "diminua volume",
        "diminuir volume",
        "volume máximo",
        "volume maximo",
        "volume mínimo",
        "volume minimo",

        # Assistente
        "olá oda",
        "ola oda",
        "oi oda",
        "oi",
        "que horas são",
        "que horas sao",

        # Mídia
        "pausar música",
        "pausar musica",
        "pause a música",
        "pause a musica",
        "continuar música",
        "continuar musica",
        "continue a música",
        "continue a musica",
        "próxima música",
        "proxima musica",
        "próxima faixa",
        "proxima faixa",
        "música anterior",
        "musica anterior",
        "voltar a música",
        "voltar a musica",
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


import asyncio
import threading

from oda.hud_bridge import HudBridge


class HudState:
    """
    Controle simples do estado visual do HUD.

    Pode ser usado pelo pipeline de voz sem bloquear
    a execução principal do ODA.
    """

    def __init__(self):
        self.bridge = HudBridge()
        self.loop = None
        self.thread = None
        self.started = threading.Event()

    def start(self):
        if self.thread and self.thread.is_alive():
            return

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )
        self.thread.start()

        self.started.wait(timeout=3)

    def _run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        async def boot():
            await self.bridge.start()
            self.started.set()

        self.loop.run_until_complete(boot())
        self.loop.run_forever()

    def set(self, state):
        if self.loop is None:
            return

        asyncio.run_coroutine_threadsafe(
            self.bridge.set_state(state),
            self.loop,
        )

    def idle(self):
        self.set("idle")

    def listening(self):
        self.set("listening")

    def processing(self):
        self.set("processing")


hud = HudState()

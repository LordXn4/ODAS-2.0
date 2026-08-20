
import asyncio
import json

try:
    import websockets
except ImportError:
    websockets = None


class HudBridge:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.state = "idle"
        self.audio_level = 0.0
        self.server = None

    async def _handler(self, websocket):
        self.clients.add(websocket)

        try:
            await websocket.send(json.dumps({
                "type": "state",
                "state": self.state,
                "audio_level": self.audio_level,
            }))

            async for _ in websocket:
                pass

        finally:
            self.clients.discard(websocket)

    async def set_state(self, state):
        if state not in {"idle", "listening", "processing"}:
            raise ValueError(f"Estado inválido: {state}")

        self.state = state

        if not self.clients:
            return

        message = json.dumps({
            "type": "state",
            "state": state,
            "audio_level": self.audio_level,
        })

        disconnected = set()

        for client in self.clients:
            try:
                await client.send(message)
            except Exception:
                disconnected.add(client)

        self.clients.difference_update(disconnected)

    async def set_audio_level(self, level):
        level = max(0.0, min(1.0, float(level)))
        self.audio_level = level

        if not self.clients:
            return

        message = json.dumps({
            "type": "audio",
            "audio_level": level,
        })

        disconnected = set()

        for client in self.clients:
            try:
                await client.send(message)
            except Exception:
                disconnected.add(client)

        self.clients.difference_update(disconnected)

    async def start(self):
        if websockets is None:
            raise RuntimeError(
                "Dependência ausente: pip install websockets"
            )

        self.server = await websockets.serve(
            self._handler,
            self.host,
            self.port,
        )

        print(f"[HUD] WebSocket ativo em ws://{self.host}:{self.port}")

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None


async def demo():
    bridge = HudBridge()

    await bridge.start()

    print("[HUD] TESTE")
    await asyncio.sleep(2)

    print("[HUD] listening")
    await bridge.set_state("listening")
    await asyncio.sleep(3)

    print("[HUD] processing")
    await bridge.set_state("processing")
    await asyncio.sleep(3)

    print("[HUD] idle")
    await bridge.set_state("idle")
    await asyncio.sleep(2)

    await bridge.stop()


if __name__ == "__main__":
    asyncio.run(demo())

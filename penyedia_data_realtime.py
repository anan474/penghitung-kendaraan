import asyncio
import websockets
import json
import logging
import threading


class PenyediaDataRealtime():
    def __init__(self):
        self.users = set()
        self.state = {"value": 0}

        self.start_server = websockets.serve(self.counter, "localhost", 6789)
        asyncio.get_event_loop().run_until_complete(self.start_server)

        loop = asyncio.get_event_loop()

        def run_forever(loop):
            loop.run_forever()

        # because run_forever() will block the current thread, we spawn
        # a subthread to issue that call in.
        thread = threading.Thread(target=run_forever, args=(loop,))
        thread.start()

    def state_event(self):
        return json.dumps({"type": "state", **self.state})

    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.users)})

    async def notify_state(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.users])

    async def notify_users(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.users])

    async def register(self, websocket):
        self.users.add(websocket)
        await self.notify_users()

    async def unregister(self, websocket):
        self.users.remove(websocket)
        await self.notify_users()

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "minus":
                    self.state["value"] -= 1
                    await self.notify_state()
                elif data["action"] == "plus":
                    self.state["value"] += 1
                    await self.notify_state()
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

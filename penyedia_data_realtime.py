import asyncio
import websockets
import json
import logging
import threading

from pengelola_basisdata import PengelolaBasisdata

pengelola_basisdata = PengelolaBasisdata()


class PenyediaDataRealtime():
    def __init__(self):
        self.users = set()
        self.loop = None

    def start(self):
        self.start_server = websockets.serve(
            self.server_websocket, "localhost", 6789)

        self.loop = asyncio.get_event_loop()

        self.loop.run_until_complete(self.start_server)

        def run_forever(loop):
            loop.run_forever()

        thread = threading.Thread(target=run_forever, args=(self.loop,))
        thread.start()

    def stop(self):
        self.loop.stop()

    def konversi_ke_json(self, data):
        return json.dumps({"type": "users", "count": len(self.users)})

    async def repeat(self, interval, func, *args, **kwargs):
        """Run func every interval seconds.

        If func has not finished before *interval*, will run again
        immediately when the previous iteration finished.

        *args and **kwargs are passed as the arguments to func.
        """
        while True:
            await asyncio.gather(
                func(*args, **kwargs),
                asyncio.sleep(interval),
            )

    async def kirim_data(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            data = pengelola_basisdata.get_status_sekarang()
            message = self.konversi_ke_json(data)
            await asyncio.wait([user.send(message) for user in self.users])

    async def register(self, websocket):
        self.users.add(websocket)
        await self.kirim_data()

    async def server_websocket(self, websocket, path):
        # await asyncio.ensure_future(self.repeat(5, self.kirim_data))
        await self.register(websocket)
        # await websocket.send(self.kirim_data())

import asyncio
import websockets
import threading
import logging
import json

from pengelola_basisdata import PengelolaBasisdata


class PenyediaDataRealtime():
    def __init__(self):
        self.loop = None
        self.pengelola_basisdata = PengelolaBasisdata()

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
        return json.dumps({
            "kanan": {
                "keduanya": data[0][2],
                "mobil": data[1][2],
                "motor": data[2][2],
                "tidakdiketahui": data[3][2],
            },
            "kiri": {
                "keduanya": data[4][2],
                "mobil": data[5][2],
                "motor": data[6][2],
                "tidakdiketahui": data[7][2],
            }
        })

    async def server_websocket(self, websocket, path):
        while True:
            data = self.pengelola_basisdata.get_status_sekarang()
            message = self.konversi_ke_json(data)
            await websocket.send(message)
            await asyncio.sleep(5)

import asyncio
import websockets
import threading
import json
import os

from pengelola_basisdata import PengelolaBasisdata

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config-dev.json')


class PenyediaDataRealtime():
    def __init__(self):
        with open(CONFIG_PATH) as json_data_file:
            self.config = json.load(json_data_file)

        self.loop = None
        self.pengelola_basisdata = PengelolaBasisdata()

    def start(self):
        print("starting websocket")
        self.start_server = websockets.serve(
            self.server_websocket, "localhost", 8010)

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_server)

        def run_forever(loop):
            loop.run_forever()

        thread = threading.Thread(target=run_forever, args=(self.loop,))
        thread.start()

    def stop(self):
        self.loop.stop()

    def konversi_ke_json(self, data):
        return json.dumps(data)

    async def server_websocket(self, websocket, path):
        while True:
            data = self.pengelola_basisdata.get_status_sekarang()
            message = self.konversi_ke_json(data)
            await websocket.send(message)
            await asyncio.sleep(self.config["sediadata"]["websocketdelay"])

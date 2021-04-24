
import threading
import json
from flask import Flask, Response
from flask_classful import FlaskView
from pengelola_basisdata import PengelolaBasisdata

pengelola_basis_data = PengelolaBasisdata()


class DataView(FlaskView):
    def index(self):

        print("index dipanggil")
        data = pengelola_basis_data.get_status_sekarang()
        print(data)

        data_json = json.dumps({
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
        respon = Response(response=data_json, status=200,
                          mimetype="application/json")
        respon.headers["Content-Type"] = "application/json; charset=utf-8"
        return respon

    def statussekarang(self):
        data = pengelola_basis_data.get_status_sekarang()
        data_json = json.dumps({
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
        respon = Response(response=data_json, status=200,
                          mimetype="application/json")
        respon.headers["Content-Type"] = "application/json; charset=utf-8"
        return respon

    def semuadatabytanggal(self, tanggal):
        data = pengelola_basis_data.get_semua_data_by_tanggal(tanggal)
        data_json = json.dumps(data)
        respon = Response(response=data_json, status=200,
                          mimetype="application/json")
        respon.headers["Content-Type"] = "application/json; charset=utf-8"
        return respon

    def statusbytanggal(self, tanggal):
        data = pengelola_basis_data.get_status_by_tanggal(tanggal)
        data_json = json.dumps({
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
        respon = Response(response=data_json, status=200,
                          mimetype="application/json")
        respon.headers["Content-Type"] = "application/json; charset=utf-8"
        return respon


class PenyediaDataStatistik():
    def __init__(self):
        self.app = Flask(__name__)

    def start(self):

        DataView.register(self.app)

        def run_forever():
            self.app.run()

        thread = threading.Thread(target=run_forever)
        thread.start()

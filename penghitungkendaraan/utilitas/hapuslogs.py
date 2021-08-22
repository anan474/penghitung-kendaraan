# hapus gambar dan teks logs agar bisa dari awal lagi

import json
from pathlib import Path

config = False

with open("../config-dev.json") as json_data_file:
    config = json.load(json_data_file)

if config:
    path_gambar = "../"+config['simpangambar_klasifikasi']['direktori']
    path_logs = "../"+config['logs']["direktori"] + \
        config['logs']['klasifikasi']["direktori"]

    for f in Path(path_gambar).rglob('*.png'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    for f in Path(path_logs).rglob('*.csv'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
else:
    print("tidak ada file config di suppsly")

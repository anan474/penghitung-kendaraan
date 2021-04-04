import json
import time
import sys
import datetime

import cv2 as cv

from pendeteksi_objek import PendeteksiObjek
from tracker_kendaraan import TrackerKendaraan

from penyedia_data_realtime import PenyediaDataRealtime
from penyedia_data_statistik import PenyediaDataStatistik

from gambar_objek import GambarObjek

from logger import Logger

# ============================================================================

VIDEO = "vid.mp4"

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360
# ============================================================================


def main():

    with open("config-dev.json") as json_data_file:
        config = json.load(json_data_file)
    print(config)

    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))

    pendeteksi_objek = PendeteksiObjek()
    tracker_kendaraan = TrackerKendaraan()
    gambar_objek = GambarObjek(config)

    if (config['sediadata']['realtime']):
        penyedia_data_realtime = PenyediaDataRealtime()
        penyedia_data_realtime.start()

    if (config['sediadata']['statistik']):
        penyedia_data_statistik = PenyediaDataStatistik()
        penyedia_data_statistik.start()

    logger = Logger()

    video = cv.VideoCapture(VIDEO)
    frame_counter = -1

    while True:

        frame_counter += 1

        ret, frame = video.read()

        if not ret:
            print("Tidak dapat membuka video. Stop.")
            break

        frame = cv.resize(frame, (RESIZE_LEBAR, RESIZE_TINGGI))

        daftar_objek = pendeteksi_objek.deteksi_objek(frame)

        daftar_kendaraan = tracker_kendaraan.perbarui_tracker(
            daftar_objek, frame)

        gambar_objek.tampilkan_frame(frame, daftar_objek, daftar_kendaraan)
        # cv.imshow('asli', frame)

        ###
        c = cv.waitKey(1)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

    print("Menutup video ...")
    video.release()
    cv.destroyAllWindows()
    # penyedia_data_realtime.stop()
    print("Selesai .")


# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()

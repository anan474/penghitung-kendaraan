from penyedia_data_statistik import PenyediaDataStatistik
from penyedia_data_realtime import PenyediaDataRealtime
from penghitung_kendaraan import PenghitungKendaraan
from pendeteksi_objek import PendeteksiObjek
import json

import cv2 as cv

# ============================================================================

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

# ============================================================================


def main():

    with open("config-dev.json") as json_data_file:
        config = json.load(json_data_file)

    pendeteksi_objek = PendeteksiObjek(config)
    penghitung_kendaraan = PenghitungKendaraan(config)

    if (config['sediadata']['realtime']):
        penyedia_data_realtime = PenyediaDataRealtime()
        penyedia_data_realtime.start()

    if (config['sediadata']['statistik']):
        penyedia_data_statistik = PenyediaDataStatistik()
        penyedia_data_statistik.start()

    video = cv.VideoCapture(config["input"]["video"])
    frame_counter = -1

    while True:

        ret, frame = video.read()

        if not ret:
            print("Tidak dapat membuka video. Stop.")
            break

        frame = cv.resize(frame, (RESIZE_LEBAR, RESIZE_TINGGI))

        daftar_objek = pendeteksi_objek.deteksi_objek(frame)

        penghitung_kendaraan.hitung_kendaraan(
            daftar_objek, frame, frame_counter)

        ###
        c = cv.waitKey(config["input"]["speed"])
        if c == ord('p'):
            cv.waitKey(-1)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

    print("Menutup video ...")
    video.release()
    cv.destroyAllWindows()
    penyedia_data_realtime.stop()
    print("Selesai .")


# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()

import time
import sys
import datetime

import cv2 as cv

from pendeteksi_objek import PendeteksiObjek
from tracker_kendaraan import TrackerKendaraan

from gambar_objek import GambarObjek

from logger import Logger

# ============================================================================

VIDEO = "vid.mp4"

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360
# ============================================================================


def main():

    pendeteksi_objek = PendeteksiObjek()
    tracker_kendaraan = TrackerKendaraan()
    gambar_objek = GambarObjek()

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

        ###
        c = cv.waitKey(100)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

    print("Menutup video ...")
    video.release()
    cv.destroyAllWindows()
    print("Selesai .")


# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()

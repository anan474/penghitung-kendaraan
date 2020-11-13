import time
import sys
import datetime

import cv2 as cv

from penghitung_kendaraan import Penghitung
from pendeteksi_objek import PendeteksiObjek

from gambar_objek import GambarObjek

from logger import Logger

# ============================================================================

VIDEO = "vid.mp4"

# ============================================================================


def main():

    video = cv.VideoCapture(VIDEO)

    penghitung_lajur_kiri = Penghitung(
        GARIS_PEMBATAS_KIRI_MASUK, GARIS_PEMBATAS_KIRI_KELUAR, "kiri")
    penghitung_lajur_kanan = Penghitung(
        GARIS_PEMBATAS_KANAN_MASUK, GARIS_PEMBATAS_KANAN_KELUAR, "kanan")

    pendeteksi_objek = PendeteksiObjek()
    gambar_objek = GambarObjek()
    logger = Logger()

    frame_counter = -1

    while True:

        frame_counter += 1

        ret, frame = video.read()
        if not ret:
            print("Tidak dapat membuka video. Stop.")
            break

        daftar_objek = pendeteksi_objek.deteksi_objek(frame)

        ####
        # hubungkan dengan modul penghitung
        penghitung_lajur_kiri.perbarui_penghitung(
            objek_ditemukan_lajur_kiri, frame)
        penghitung_lajur_kanan.perbarui_penghitung(
            objek_ditemukan_lajur_kanan, frame)

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

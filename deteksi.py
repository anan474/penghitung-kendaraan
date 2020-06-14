import os
import time
import sys
import datetime

import cv2 as cv
import numpy as np

from penghitung import Penghitung

# ============================================================================

GARIS_PEMBATAS_KIRI_MASUK = 240
GARIS_PEMBATAS_KIRI_KELUAR = 60

GARIS_PEMBATAS_KANAN_MASUK = 40
GARIS_PEMBATAS_KANAN_KELUAR = 120


RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

# ============================================================================

GAMBAR_BACKGROUND = "bg.png"
VIDEO = "vid.mp4"

# ============================================================================


# Warna untuk digambar di gambar nanti
WARNA_GARIS_PEMBATAS_MASUK = (255, 255, 0)
WARNA_GARIS_PEMBATAS_KELUAR = (0, 255, 255)
WARNA_GARIS_PEMBATAS_TENGAH = (0, 0, 0)

WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_BOUNDING_BOX_HIJAU = (0, 255, 0)

WARNA_CENTROID = (0, 0, 255)
WARNA_GARIS = [(0, 0, 255), (0, 106, 255), (0, 216, 255), (0, 255, 182), (0, 255, 76),
               (144, 255, 0), (255, 255, 0), (255, 148, 0), (255, 0, 178), (220, 0, 255)]

# ============================================================================


def hitung_centroid(x, y, w, h):
    # centroid adalah titik tengah dari objek terdeteksi
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

# ============================================================================


def main():

    gambar_background = cv.imread(GAMBAR_BACKGROUND)

    background_subtractor = cv.createBackgroundSubtractorMOG2()
    background_subtractor.setShadowValue(0)
    background_subtractor.apply(gambar_background, 1)

    video = cv.VideoCapture(VIDEO)
    lebar_frame = RESIZE_LEBAR
    tinggi_frame = RESIZE_TINGGI

    ###
    penghitung_lajur_kiri = Penghitung(
        GARIS_PEMBATAS_KIRI_MASUK, GARIS_PEMBATAS_KIRI_KELUAR, "kiri")
    penghitung_lajur_kanan = Penghitung(
        GARIS_PEMBATAS_KANAN_MASUK, GARIS_PEMBATAS_KANAN_KELUAR, "kanan")

    frame_counter = -1

    while True:

        frame_counter += 1

        ret, frame = video.read()
        if not ret:
            print("Tidak dapat membuka video. Stop.")
            break

        ####
        # resize frame ke 640 x 360
        frame = cv.resize(frame, (RESIZE_LEBAR, RESIZE_TINGGI))

        ####
        frame_foreground = background_subtractor.apply(frame, 1)
        cv.imshow('foreground 1', frame_foreground)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

        frame_foreground = cv.bilateralFilter(frame_foreground, 9, 75, 75)
        frame_foreground = cv.morphologyEx(
            frame_foreground, cv.MORPH_CLOSE, kernel)
        frame_foreground = cv.morphologyEx(
            frame_foreground, cv.MORPH_OPEN, kernel)
        frame_foreground = cv.dilate(frame_foreground, kernel, iterations=5)
        frame_foreground = cv.erode(frame_foreground, kernel, iterations=3)
        frame_foreground = cv.morphologyEx(
            frame_foreground, cv.MORPH_CLOSE, kernel)

        ####
        LEBAR_MINIMAL = 21
        TINGGI_MINIMAL = 21

        contours, _ = cv.findContours(
            frame_foreground, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        objek_ditemukan_lajur_kiri = []
        objek_ditemukan_lajur_kanan = []
        for (i, contour) in enumerate(contours):

            (x, y, w, h) = cv.boundingRect(contour)
            objek_valid = (w >= LEBAR_MINIMAL) and (h >= TINGGI_MINIMAL)

            if not objek_valid:
                continue

            centroid = hitung_centroid(x, y, w, h)

            if centroid[0] < (lebar_frame/2):
                objek_ditemukan_lajur_kiri.append(((x, y, w, h), centroid))
            else:
                objek_ditemukan_lajur_kanan.append(((x, y, w, h), centroid))

        ####
        # hubungkan dengan modul penghitung
        penghitung_lajur_kiri.perbarui_penghitung(objek_ditemukan_lajur_kiri, frame)
        penghitung_lajur_kanan.perbarui_penghitung(objek_ditemukan_lajur_kanan, frame)

        ####
        # print jumlah kendaraan terdeteksi
        os.system("clear")
        print("frame ke: ", frame_counter)
        print("lajur kiri: ", penghitung_lajur_kiri.jumlah_kendaraan)
        print("lajur kanan:", penghitung_lajur_kanan.jumlah_kendaraan)

        ####
        # gambar objek terdeteksi dan centroid nya
        for (i, objek) in enumerate(objek_ditemukan_lajur_kanan + objek_ditemukan_lajur_kiri):
            posisi, centroid = objek
            x, y, w, h = posisi

            # gambar bounding box pada frame
            cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1),
                         WARNA_BOUNDING_BOX, 1)

            # gambar centroid pada frame
            cv.circle(frame, centroid, 2, WARNA_CENTROID, -1)

        ####
        # gambar kedaraan terdeteksi, centroid nya dan garis pergerakan kendaraan tersebut, dari penghitung kendaraan

        for (i, kendaraan) in enumerate(penghitung_lajur_kanan.kendaraan + penghitung_lajur_kiri.kendaraan):
            x, y, w, h = kendaraan.posisi
            warna = WARNA_GARIS[kendaraan.id % len(WARNA_GARIS)]

            # gambar bounding box pada frame
            cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1),
                         WARNA_BOUNDING_BOX_HIJAU if kendaraan.telah_dihitung else WARNA_BOUNDING_BOX, 1)

            teks = 'id:{}\ncentroid:{}\nmuncul:{} frame'.format(

                kendaraan.id, kendaraan.centroid[-1], len(kendaraan.centroid))

            for i, baris in enumerate(teks.split('\n')):
                cv.putText(frame, baris, (x+5, y+10 + (10*i)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.3,
                           warna,
                           1)
            # gambar garis pergerakan
            for point in kendaraan.centroid:
                cv.circle(frame, point, 2, warna, -1)
                cv.polylines(frame, [np.int32(
                    kendaraan.centroid)], False, warna, 1)

            # gambar centroid pada frame
            cv.circle(frame, centroid, 2, WARNA_CENTROID, -1)

        ####
        # gambar garis pembatas kiri, kanan, dan tengah

        # kiri
        cv.line(frame, (0, GARIS_PEMBATAS_KIRI_MASUK), (int(lebar_frame/2), GARIS_PEMBATAS_KIRI_MASUK),
                WARNA_GARIS_PEMBATAS_MASUK, 1)
        cv.line(frame, (0, GARIS_PEMBATAS_KIRI_KELUAR), (int(lebar_frame/2), GARIS_PEMBATAS_KIRI_KELUAR),
                WARNA_GARIS_PEMBATAS_KELUAR, 1)

        # kanan
        cv.line(frame, (int(lebar_frame/2), GARIS_PEMBATAS_KANAN_MASUK), (int(lebar_frame), GARIS_PEMBATAS_KANAN_MASUK),
                WARNA_GARIS_PEMBATAS_MASUK, 1)
        cv.line(frame, (int(lebar_frame/2), GARIS_PEMBATAS_KANAN_KELUAR), (int(lebar_frame), GARIS_PEMBATAS_KANAN_KELUAR),
                WARNA_GARIS_PEMBATAS_KELUAR, 1)

        # tengah
        cv.line(frame, (int(lebar_frame/2), 0), (int(lebar_frame/2), tinggi_frame),
                WARNA_GARIS_PEMBATAS_TENGAH, 1)

        ####
        cv.imshow('asli', frame)
        cv.imshow('foreground', frame_foreground)

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

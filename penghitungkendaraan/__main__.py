from utilitas import Utilitas
from gambar_objek import GambarObjek
from penyedia_data_statistik import PenyediaDataStatistik
from penyedia_data_realtime import PenyediaDataRealtime
from penghitung_kendaraan import PenghitungKendaraan
from pendeteksi_objek import PendeteksiObjek
from picamera.array import PiRGBArray
from picamera import PiCamera
import json
import time
import sys
import datetime

import cv2 as cv
import logging
logging.basicConfig(level=logging.INFO)


# ============================================================================

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360
# ============================================================================

# ============================================================================
time.sleep(0.1)


def main():
    with open("config-dev.json") as json_data_file:
        config = json.load(json_data_file)

    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))

    pendeteksi_objek = PendeteksiObjek(config)
    penghitung_kendaraan = PenghitungKendaraan(config)
    gambar_objek = GambarObjek(config)
    utilitas = Utilitas()

    utilitas.empty_output()

    if (config['sediadata']['realtime']):
        penyedia_data_realtime = PenyediaDataRealtime()
        penyedia_data_realtime.start()

    if (config['sediadata']['statistik']):
        penyedia_data_statistik = PenyediaDataStatistik()
        penyedia_data_statistik.start()

    video = cv.VideoCapture(config["input"]["video"])

    camera = PiCamera()
    camera.resolution = (RESIZE_LEBAR, RESIZE_TINGGI)
    camera.framerate = 15
    rawCapture = PiRGBArray(camera, size=(RESIZE_LEBAR, RESIZE_TINGGI))

    frame_counter = -1

    # while True:
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame_counter += 1
        # print("frame ke : " + str(frame_counter))

        frame = image.array

        # frame = cv.resize(frame, (RESIZE_LEBAR, RESIZE_TINGGI))

        daftar_objek, foreground = pendeteksi_objek.deteksi_objek(frame)

        daftar_kendaraan = penghitung_kendaraan.hitung_kendaraan(
            daftar_objek, frame, frame_counter)

        gambar_objek.tampilkan_frame(
            frame, foreground, frame_counter, daftar_objek, daftar_kendaraan)

        ###
        c = cv.waitKey(config["input"]["speed"])
        if c == ord('p'):
            cv.waitKey(-1)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    print("Menutup video ...")
    video.release()
    cv.destroyAllWindows()
    penyedia_data_realtime.stop()
    print("Selesai .")


# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()

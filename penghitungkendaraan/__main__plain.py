from penyedia_data_statistik import PenyediaDataStatistik
from penyedia_data_realtime import PenyediaDataRealtime
from tracker_kendaraan import PenghitungKendaraan
from pendeteksi_objek import PendeteksiObjek
from picamera.array import PiRGBArray
from picamera import PiCamera
import json
import time
import cv2 as cv


# ============================================================================

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

# ============================================================================
time.sleep(0.1)


def main():
    with open("config-dev.json") as json_data_file:
        config = json.load(json_data_file)

    pendeteksi_objek = PendeteksiObjek(config)
    tracker_kendaraan = PenghitungKendaraan(config)

    penyedia_data_realtime = PenyediaDataRealtime()
    penyedia_data_realtime.start()

    penyedia_data_statistik = PenyediaDataStatistik()
    penyedia_data_statistik.start()

    camera = PiCamera()
    camera.resolution = (RESIZE_LEBAR, RESIZE_TINGGI)
    camera.framerate = 15
    rawCapture = PiRGBArray(camera, size=(RESIZE_LEBAR, RESIZE_TINGGI))

    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = image.array
        daftar_objek = pendeteksi_objek.deteksi_objek(frame)
        tracker_kendaraan.hitung_kendaraan(
            daftar_objek, frame)

        c = cv.waitKey(config["input"]["speed"])
        if c == ord('p'):
            cv.waitKey(-1)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    cv.destroyAllWindows()
    penyedia_data_realtime.stop()
    print("Selesai .")

# ============================================================================


if __name__ == "__main__":
    print("Mulai .")
    main()

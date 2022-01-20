import cv2 as cv
import logging

logger = logging.getLogger(__name__)

GAMBAR_BACKGROUND = "bg.png"

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

LEBAR_MINIMAL = 21
TINGGI_MINIMAL = 21


class PendeteksiObjek():
    """Kelas ini melakukan proses terhadap citra asli untuk mengekstrak daftar objek kendaraan yang ada dengan melakukan Background Subtraction dan proses morfologi.
    """

    def __init__(self, config):

        self.config = config

        gambar_background = cv.imread(GAMBAR_BACKGROUND)

        self.background_subtractor = cv.createBackgroundSubtractorMOG2()
        self.background_subtractor.setShadowValue(0)
        self.background_subtractor.apply(gambar_background, 1)

        self.lebar_frame = RESIZE_LEBAR

        self.kernel3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        self.kernel7 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
        self.kernel9 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))

        logger.info("init module")

    def __get_foreground(self, frame):
        frame_foreground = self.background_subtractor.apply(frame, 1)

        return frame_foreground

    def __proses_morfologi(self, frame):

        frame = cv.bilateralFilter(
            frame, 9, 75, 75)

        # frame_foreground = cv.morphologyEx(
        #     frame, cv.MORPH_OPEN, self.kernel9)

        # frame = cv.erode(frame, self.kernel3, iterations=3)
        frame = cv.erode(frame, self.kernel3, iterations=1)
        frame = cv.dilate(frame, self.kernel3, iterations=1)
        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, self.kernel7)

        # frame = cv.morphologyEx(
        #     frame, cv.MORPH_CLOSE, self.kernel3)

        if (self.config['cetakgambar']['morfologi']):
            cv.imshow('morfologi', frame)

        return frame

    def __hitung_centroid(self, x, y, w, h):
        # centroid adalah titik tengah dari objek terdeteksi
        x1 = int(w / 2)
        y1 = int(h / 2)

        cx = x + x1
        cy = y + y1

        return (cx, cy)

    def __dapatkan_objek(self, frame):
        contours, _ = cv.findContours(
            frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        objek_ditemukan = []
        for (i, contour) in enumerate(contours):

            (x, y, w, h) = cv.boundingRect(contour)
            objek_valid = (w >= LEBAR_MINIMAL) and (h >= TINGGI_MINIMAL)

            if not objek_valid:
                continue

            centroid = self.__hitung_centroid(x, y, w, h)

            lajur = "kiri" if centroid[0] < (self.lebar_frame/2) else "kanan"

            objek_ditemukan.append(
                ((x, y, w, h), centroid, lajur))

        return objek_ditemukan

    def deteksi_objek(self, frame):

        foreground = self.__get_foreground(frame)
        foreground = self.__proses_morfologi(foreground)
        daftar_objek = self.__dapatkan_objek(foreground)

        return daftar_objek, foreground

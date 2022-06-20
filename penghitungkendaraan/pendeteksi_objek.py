import cv2 as cv
import logging
import os

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GAMBAR_BACKGROUND = os.path.join(ROOT_DIR, "bg.png")

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

LEBAR_MINIMAL = 25
TINGGI_MINIMAL = 25


class PendeteksiObjek():
    """Kelas ini melakukan proses terhadap citra asli untuk mengekstrak daftar objek kendaraan yang ada dengan melakukan Background Subtraction dan proses morfologi.
    """

    def __init__(self, config):

        self.config = config

        gambar_background = cv.imread(GAMBAR_BACKGROUND)

        self.background_subtractor = cv.createBackgroundSubtractorMOG2()
        self.background_subtractor.setShadowValue(0)
        self.background_subtractor.apply(gambar_background)

        self.lebar_frame = RESIZE_LEBAR

        self.kernel3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        self.kernel7 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
        self.kernel9 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))

        logger.info("init module")

    def __get_foreground(self, frame):
        frame_foreground = self.background_subtractor.apply(frame)

        return frame_foreground

    def __proses_morfologi(self, frame, frame_counter):

        # cv.imshow("Background Subtraction", frame)
        if(self.config['simpangambar']["morfologi_detail"]):
            cv.imwrite((self.config['simpangambar']['direktori'] +
                        "morfologi_detail" + "/%04d_1_backsubract.png") % frame_counter, frame)

        # frame = cv.bilateralFilter(
        #     frame, 9, 75, 75)

        # cv.imwrite((self.config['simpangambar']['direktori'] +
        #             "morfologi_detail" + "/%04d_2_bilateralfilter.png") % frame_counter, frame)

        frame = cv.erode(frame, self.kernel3, iterations=1)
        # cv.imshow("Morfologi Erode", frame)
        if(self.config['simpangambar']["morfologi_detail"]):
            cv.imwrite((self.config['simpangambar']['direktori'] +
                        "morfologi_detail" + "/%04d_2_erode.png") % frame_counter, frame)

        frame = cv.dilate(frame, self.kernel7, iterations=2)
        # cv.imshow("Morfologi Dilate", frame)
        if(self.config['simpangambar']["morfologi_detail"]):
            cv.imwrite((self.config['simpangambar']['direktori'] +
                        "morfologi_detail" + "/%04d_3_dilate.png") % frame_counter, frame)

        frame = cv.erode(frame, self.kernel7, iterations=1)
        # cv.imshow("Morfologi Erode", frame)
        if(self.config['simpangambar']["morfologi_detail"]):
            cv.imwrite((self.config['simpangambar']['direktori'] +
                        "morfologi_detail" + "/%04d_4_erode.png") % frame_counter, frame)

        # frame = cv.morphologyEx(
        #     frame, cv.MORPH_OPEN, self.kernel3)
        # # cv.imshow("Morfologi Opening", frame)
        # cv.imwrite((self.config['simpangambar']['direktori'] +
        #             "morfologi_detail" + "/%04d_4_opening.png") % frame_counter, frame)

        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, self.kernel9)
        # cv.imshow("Morfologi Close", frame)
        if(self.config['simpangambar']["morfologi_detail"]):
            cv.imwrite((self.config['simpangambar']['direktori'] +
                        "morfologi_detail" + "/%04d_5_closing.png") % frame_counter, frame)

        # cv.imshow('morfologi', frame)

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

    def deteksi_objek(self, frame, frame_counter):

        foreground = self.__get_foreground(frame)
        foreground = self.__proses_morfologi(foreground, frame_counter)
        daftar_objek = self.__dapatkan_objek(foreground)

        return daftar_objek, foreground

import cv2 as cv


GAMBAR_BACKGROUND = "bg.png"

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360

LEBAR_MINIMAL = 21
TINGGI_MINIMAL = 21


class PendeteksiObjek():
    def __init__(self):
        self.gambar_background = cv.imread(GAMBAR_BACKGROUND)
        self.background_subtractor = cv.createBackgroundSubtractorMOG2()
        self.background_subtractor.setShadowValue(0)
        self.background_subtractor.apply(gambar_background, 1)

        self.lebar_frame = RESIZE_LEBAR
        self.tinggi_frame = RESIZE_TINGGI

        self.kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        self.kernel2 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

    def resize(self, frame):
        frame_resized = cv.resize(frame, (self.lebar_frame, self.tinggi_frame))
        return frame_resized

    def get_foreground(self, frame):
        frame_foreground = self.background_subtractor.apply(frame, 1)
        return frame_foreground

    def proses_morfologi(self, frame):
        frame = cv.bilateralFilter(
            frame, 9, 75, 75)

        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, self.kernel)

        frame_foreground = cv.morphologyEx(
            frame, cv.MORPH_OPEN, self.kernel2)

        frame = cv.dilate(frame, self.kernel, iterations=5)

        frame = cv.erode(frame, self.kernel, iterations=3)

        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, self.kernel)

        return frame

    def hitung_centroid(self, x, y, w, h):
        # centroid adalah titik tengah dari objek terdeteksi
        x1 = int(w / 2)
        y1 = int(h / 2)

        cx = x + x1
        cy = y + y1

        return (cx, cy)

    def dapatkan_objek(self, frame):
        contours, _ = cv.findContours(
            frame_foreground, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        objek_ditemukan = []
        for (i, contour) in enumerate(contours):

            (x, y, w, h) = cv.boundingRect(contour)
            objek_valid = (w >= LEBAR_MINIMAL) and (h >= TINGGI_MINIMAL)

            if not objek_valid:
                continue

            centroid = hitung_centroid(x, y, w, h)
            objek_ditemukan.append(((x, y, w, h), centroid))
        return objek_ditemukan

    def deteksi_objek(self, frame):
        frame = resize(frame)
        foreground = get_foreground(frame)
        foreground = proses_morfologi(foreground)

        daftar_objek = dapatkan_objek(foreground)

        return daftar_objek

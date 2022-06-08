import unittest
import collections.abc
import cv2 as cv
from pendeteksi_objek import PendeteksiObjek
from penghitung_kendaraan import PenghitungKendaraan


class PendeteksiObjekTestCase(unittest.TestCase):
    def setUp(self):
        self.pendeteksi_objek = PendeteksiObjek()
        self.penghitung_kendaraan = PenghitungKendaraan()

        self.citra_jalan = cv.imread("./test_assets/citra_jalan.png")

    def test_background_subtraction(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)

        self.assertTrue(foreground.any() and len(foreground) > 0,
                        "Gagal ambil foreground")

    def test_proses_morfologi(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)

        print(morfologi)

        self.assertTrue(len(morfologi) > 0,
                        "Gagal ambil citra morfologi")

    def test_dapatkan_blob_objek(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        daftar_objek = self.pendeteksi_objek.dapatkan_blob_objek(morfologi)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_deteksi_objek(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

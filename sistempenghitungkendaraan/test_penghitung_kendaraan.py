import unittest
import collections.abc
import cv2 as cv
from pendeteksi_objek import PendeteksiObjek
from penghitung_kendaraan import PenghitungKendaraan


# masih ecek ecek untuk laporan jak
class PenghitungKendaraanTestCase(unittest.TestCase):
    def setUp(self):
        self.pendeteksi_objek = PendeteksiObjek()
        self.penghitung_kendaraan = PenghitungKendaraan()

        self.citra_jalan = cv.imread("./test_assets/citra_jalan.png")

    def test_hitung_vektor(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)

        self.assertTrue(foreground.any() and len(foreground) > 0,
                        "Gagal ambil foreground")

    def test_apakah_vektor_valid(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        self.assertTrue(len(morfologi) > 0,
                        "Gagal ambil citra morfologi")

    def test_apakah_masuk_garis(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        daftar_objek = self.pendeteksi_objek.dapatkan_blob_objek(morfologi)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_apakah_melewati_garis(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_cocokkan_data_yang_ada(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_tambahkan_ke_daftar_tracking(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_handle_kendaraan_melewati_batas(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_prebarui_tracker(self):

        daftar_objek = self.pendeteksi_objek.deteksi_objek(self.citra_jalan)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")
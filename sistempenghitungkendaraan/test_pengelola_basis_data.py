import unittest
import collections.abc
import cv2 as cv
from pendeteksi_objek import PendeteksiObjek
from penghitung_kendaraan import PenghitungKendaraan


# masih ecek ecek untuk laporan jak
class PengelolaBasisdataTestCase(unittest.TestCase):
    def setUp(self):
        self.pendeteksi_objek = PendeteksiObjek()
        self.penghitung_kendaraan = PenghitungKendaraan()

        self.citra_jalan = cv.imread("./test_assets/citra_jalan.png")

    def test_get_semua_data_by_tanggal(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)

        self.assertTrue(foreground.any() and len(foreground) > 0,
                        "Gagal ambil foreground")

    def test_get_status_sekarang(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        self.assertTrue(len(morfologi) > 0,
                        "Gagal ambil citra morfologi")

    def test_get_status_by_tanggal(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        daftar_objek = self.pendeteksi_objek.dapatkan_blob_objek(morfologi)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_get_jumlah_data(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        daftar_objek = self.pendeteksi_objek.dapatkan_blob_objek(morfologi)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

    def test_simpan_ke_db(self):

        foreground = self.pendeteksi_objek.background_subtraction(
            self.citra_jalan)
        morfologi = self.pendeteksi_objek.proses_morfologi(
            foreground)
        daftar_objek = self.pendeteksi_objek.dapatkan_blob_objek(morfologi)

        self.assertIsInstance(daftar_objek, collections.abc.Sequence,
                              "Gagal mengambi daftar objek")

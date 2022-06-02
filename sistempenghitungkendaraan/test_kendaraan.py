import unittest

import cv2 as cv
from kendaraan import Kendaraan


class KendaraanTestCase(unittest.TestCase):
    def setUp(self):
        self.kendaraan = Kendaraan(1, (506, 45), (492, 11, 29, 68), 'kanan')

    def test_perbarui_centroid(self):
        # setup
        centroid_baru = (512, 72)
        jumlah_centroid = len(self.kendaraan.centroid)

        # operation
        self.kendaraan.perbarui_centroid(centroid_baru)

        # assert
        self.assertEqual(len(self.kendaraan.centroid), jumlah_centroid+1,
                         "Jumlah centroid tidak sesuai")

        self.assertEqual(self.kendaraan.centroid[jumlah_centroid], centroid_baru,
                         "Nilai centroid tidak sama")

    def test_ambil_nilai_centroid_terakhir(self):
        centroid_baru = (15, 15)
        self.kendaraan.perbarui_centroid(centroid_baru)

        # operation
        centroid_terakhir = self.kendaraan.centroid_terakhir

        # assert
        self.assertTrue(centroid_terakhir,
                        "Tidak dapat mengambil nilai centroid")
        self.assertEqual(centroid_terakhir, centroid_baru,
                         "Tidak sesuai nilai centroid dengan yang terbaru")

    def test_perbarui_posisi(self):
        # setup
        posisi_baru = (10, 10, 10, 10)

        # operation
        self.kendaraan.perbarui_posisi(posisi_baru)

        # assert
        self.assertEqual(self.kendaraan.posisi, posisi_baru,
                         "Nilai posisi tidak sesuai")

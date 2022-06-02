import unittest

import cv2 as cv
from kendaraan import Kendaraan


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.kendaraan = Kendaraan(1, 10, 10, "kiri")

        self.video = cv.VideoCapture("vid.mp4")
        self.frame = False
        self.frame_counter = 0

    def test_read_video(self):

        while self.frame_counter < 5:

            print(self.video)
            print(self.video.read())
            ret, self.frame = self.video.read()
            print(self.frame)
            self.frame_counter += 1
            if not ret:
                print("Tidak dapat membuka video. Stop.")
                break

            cv.waitKey(100)
            if self.frame_counter > 5:
                cv.waitKey(-1)

        self.assertTrue(self.frame.any() and len(self.frame) > 0,
                        "image frame not read")

    def test_widget_resize(self):

        while self.frame_counter < 5:

            ret, self.frame = self.video.read()
            self.frame_counter += 1
            if not ret:
                print("Tidak dapat membuka video. Stop.")
                break

            cv.waitKey(100)
            if self.frame_counter > 5:
                cv.waitKey(-1)

        resized = cv.resize(self.frame, (640, 320))
        a, b, _ = self.frame.shape
        aa, bb, _ = resized.shape

        self.assertFalse(a == aa and b == bb,
                         'wrong size after resize')

import cv2 as cv
import logging

logger = logging.getLogger(__name__)

CASCADE_MOTOR_KIRI = "./classifier/motorkiri.xml"
CASCADE_MOTOR_KANAN = "./classifier/motorkanan.xml"
CASCADE_MOBIL_KIRI = "./classifier/download/cars.xml"
CASCADE_MOBIL_KANAN = "./classifier/download/cars.xml"


class Klasifier():
    def __init__(self):
        self.klasifier_cascade_motor_kiri = cv.CascadeClassifier(
            CASCADE_MOTOR_KIRI)
        self.klasifier_cascade_motor_kanan = cv.CascadeClassifier(
            CASCADE_MOTOR_KANAN)

        self.klasifier_cascade_mobil_kiri = cv.CascadeClassifier(
            CASCADE_MOBIL_KIRI)
        self.klasifier_cascade_mobil_kanan = cv.CascadeClassifier(
            CASCADE_MOBIL_KANAN)
    logger.debug('init modul')

    def klasifikasi_kendaraan(self, gambar, lajur):
        logger.debug('kendaraan lajur %s',lajur)
        if lajur == "kiri":
            klasifikasi_motor = self.klasifier_cascade_motor_kiri.detectMultiScale(
            gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kiri.detectMultiScale(
                gambar)
        elif lajur == "kanan":
            klasifikasi_motor = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kanan.detectMultiScale(
                gambar)

        klasifikasi = "tidakdiketahui"
        jumlah = 0

        if((len(klasifikasi_motor) >= 1) and (len(klasifikasi_mobil) >= 1)):
            klasifikasi = "keduanya"
            jumlah = len(klasifikasi_motor) + len(klasifikasi_mobil)
        elif(len(klasifikasi_motor) >= 1):
            klasifikasi = "motor"
            jumlah = len(klasifikasi_motor)

        elif(len(klasifikasi_mobil) >= 1):
            klasifikasi = "mobil"
            jumlah = len(klasifikasi_mobil)

        logger.debug('klasifikasi %s',klasifikasi, jumlah)

        return klasifikasi, jumlah

import cv2 as cv

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

    def klasifikasi_kendaraan_lajur_kiri(self, gambar):
        klasifikasi_motor = self.klasifier_cascade_motor_kiri.detectMultiScale(
            gambar)

        klasifikasi_mobil = self.klasifier_cascade_mobil_kiri.detectMultiScale(
            gambar)

        klasifikasi = "tidakdiketahui"

        if((len(klasifikasi_motor) >= 1) and (len(klasifikasi_mobil) >= 1)):
            klasifikasi = "keduanya"
        elif(len(klasifikasi_motor) >= 1):
            klasifikasi = "motor"
        elif(len(klasifikasi_mobil) >= 1):
            klasifikasi = "mobil"

        return klasifikasi

    def klasifikasi_kendaraan_lajur_kanan(self, gambar):
        klasifikasi_motor = self.klasifier_cascade_motor_kanan.detectMultiScale(
            gambar)

        klasifikasi_mobil = self.klasifier_cascade_mobil_kanan.detectMultiScale(
            gambar)

        klasifikasi = "tidakdiketahui"

        if((len(klasifikasi_motor) >= 1) and (len(klasifikasi_mobil) >= 1)):
            klasifikasi = "keduanya"
        elif(len(klasifikasi_motor) >= 1):
            klasifikasi = "motor"
        elif(len(klasifikasi_mobil) >= 1):
            klasifikasi = "mobil"

        return klasifikasi

    def klasifikasi_kendaraan(self, gambar, lajur):
        if lajur == "kiri":
            return self.klasifikasi_kendaraan_lajur_kiri(
                gambar)
        elif lajur == "kanan":
            return self.klasifikasi_kendaraan_lajur_kanan(
                gambar)

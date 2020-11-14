import cv2 as cv

CASCADE_MOTOR_KIRI = "./classifier/motorkiri.xml"
CASCADE_MOTOR_KANAN = "./classifier/motorkanan.xml"
# CASCADE_MOBIL_KIRI = ""
# CASCADE_MOBIL_KANAN = ""


class Klasifier():
    def __init__(self):
        self.klasifier_cascade_motor_kiri = cv.CascadeClassifier(
            CASCADE_MOTOR_KIRI)
        self.klasifier_cascade_motor_kanan = cv.CascadeClassifier(
            CASCADE_MOTOR_KANAN)

    def klasifikasi_kendaraan(self, gambar, lajur):
        klasifikasi = ""
        if lajur == "kiri":
            klasifikasi = self.klasifier_cascade_motor_kiri.detectMultiScale(
                gambar)
        elif lajur == "kanan":
            klasifikasi = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambar)
        return klasifikasi

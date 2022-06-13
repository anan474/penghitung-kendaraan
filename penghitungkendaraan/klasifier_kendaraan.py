import cv2 as cv
import logging
import uuid

logger = logging.getLogger(__name__)

CASCADE_MOTOR_KIRI = "./classifier/motorkiri.xml"
CASCADE_MOTOR_KANAN = "./classifier/motorkanan.xml"
CASCADE_MOBIL_KIRI = "./classifier/download/cars.xml"
CASCADE_MOBIL_KANAN = "./classifier/download/cars.xml"

WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_BOUNDING_BOX_HIJAU = (0, 255, 0)


class Klasifier():
    def __init__(self, config):
        self.config = config

        self.klasifier_cascade_motor_kiri = cv.CascadeClassifier(
            CASCADE_MOTOR_KIRI)
        self.klasifier_cascade_motor_kanan = cv.CascadeClassifier(
            CASCADE_MOTOR_KANAN)

        self.klasifier_cascade_mobil_kiri = cv.CascadeClassifier(
            CASCADE_MOBIL_KIRI)
        self.klasifier_cascade_mobil_kanan = cv.CascadeClassifier(
            CASCADE_MOBIL_KANAN)
    logger.info('init modul')

    def klasifikasi_kendaraan(self, gambar, gambarfull, lajur, frame_counter):
        # logger.info('kendaraan lajur %s', lajur)
        base_name = str(frame_counter)+"_" + str(uuid.uuid4())[:8]

        if lajur == "kiri":
            klasifikasi_motor = self.klasifier_cascade_motor_kiri.detectMultiScale(
                gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kiri.detectMultiScale(
                gambar)

            for klasifikasi in klasifikasi_motor:
                # print(klasifikasi)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/motor/" + base_name+".png"), gambar)

                x, y, w, h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/motor/" + base_name+"_rec.png"), gambar)

            for klasifikasi in klasifikasi_mobil:
                # print(klasifikasi)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/mobil/" + base_name+"_rec.png"), gambar)
                x, y, w, h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX_HIJAU, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/mobil/" + base_name+".png"), gambar)

            if len(klasifikasi_mobil) == 0 and len(klasifikasi_motor) == 0 and self.config['simpangambar']['debug']:
                cv.imwrite(
                    ("debug/" + lajur + "/tidakdiketahui/" + base_name+".png"), gambar)

            # ~~ DEBUG FULL PIC
            klasifikasi_motor_full = self.klasifier_cascade_motor_kiri.detectMultiScale(
                gambarfull)

            klasifikasi_mobil_full = self.klasifier_cascade_mobil_kiri.detectMultiScale(
                gambarfull)

            for klasifikasi in klasifikasi_motor_full:
                # print(klasifikasi)
                x, y, w, h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" +
                                base_name+"_full.png"), gambarfull)

            for klasifikasi in klasifikasi_mobil_full:
                # print(klasifikasi)
                x, y, w, h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX_HIJAU, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" +
                                base_name+"_full.png"), gambarfull)

            if len(klasifikasi_mobil_full) == 0 and len(klasifikasi_motor_full) == 0 and self.config['simpangambar']['debug']:
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" +
                            base_name+"_full.png"), gambarfull)

        elif lajur == "kanan":
            klasifikasi_motor = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kanan.detectMultiScale(
                gambar)

            for klasifikasi in klasifikasi_motor:
                # print(klasifikasi)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/motor/" + base_name+".png"), gambar)
                x, y, w, h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/motor/" + base_name+"_rec.png"), gambar)

            for klasifikasi in klasifikasi_mobil:
                # print(klasifikasi)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/mobil/" + base_name+".png"), gambar)
                x, y, w, h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX_HIJAU, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(
                        ("debug/" + lajur + "/mobil/" + base_name+"_rec.png"), gambar)

            if len(klasifikasi_mobil) == 0 and len(klasifikasi_motor) == 0 and self.config['simpangambar']['debug']:
                cv.imwrite(
                    ("debug/" + lajur + "/tidakdiketahui/" + base_name+".png"), gambar)

            # ~~ DEBUG FULL PIC

            klasifikasi_motor_full = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambarfull)

            klasifikasi_mobil_full = self.klasifier_cascade_mobil_kanan.detectMultiScale(
                gambarfull)

            for klasifikasi in klasifikasi_motor_full:
                # print(klasifikasi)

                x, y, w, h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" +
                                base_name+"_full.png"), gambarfull)

            for klasifikasi in klasifikasi_mobil_full:
                # print(klasifikasi)

                x, y, w, h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                             WARNA_BOUNDING_BOX_HIJAU, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" +
                                base_name+"_full.png"), gambarfull)

            if len(klasifikasi_mobil_full) == 0 and len(klasifikasi_motor_full) == 0 and self.config['simpangambar']['debug']:
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" +
                            base_name+"_full.png"), gambarfull)

        klasifikasi = "tidakdiketahui"

        jumlah_mobil = 0
        jumlah_motor = 0

        if(len(klasifikasi_motor) >= 1):
            klasifikasi = "motor"
            jumlah_motor = len(klasifikasi_motor)

        if(len(klasifikasi_mobil) >= 1):
            klasifikasi = "mobil"
            jumlah_mobil = len(klasifikasi_mobil)

        # logger.info('klasifikasi %s, mobil %d, motor %d', klasifikasi,
        #             jumlah_mobil, jumlah_motor)

        return klasifikasi, jumlah_mobil, jumlah_motor

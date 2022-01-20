import cv2 as cv
import logging
import uuid

logger = logging.getLogger(__name__)

CASCADE_MOTOR_KIRI = "./classifier/motorkiri.xml"
CASCADE_MOTOR_KANAN = "./classifier/motorkanan.xml"
CASCADE_MOBIL_KIRI = "./classifier/mobil_kiri/classifier/cascade.xml"
CASCADE_MOBIL_KANAN = "./classifier/download/cars.xml"

WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_BOUNDING_BOX_HIJAU = (0, 255, 0)


class Klasifier():
    def __init__(self,config):
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

    def klasifikasi_kendaraan(self, gambar, gambarfull, lajur,frame_counter):
        logger.info('kendaraan lajur %s', lajur)

        identifier = str(uuid.uuid4())[:8]

        filename = str(frame_counter)+ "_"+identifier+".png" 
        filename_full = str(frame_counter)+ "_"+identifier+"_"+"full.png" 

        if lajur == "kiri":
            klasifikasi_motor = self.klasifier_cascade_motor_kiri.detectMultiScale(
                gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kiri.detectMultiScale(
                gambar)



            for klasifikasi in klasifikasi_motor:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX, 1)
   
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" + filename), gambar)

            for klasifikasi in klasifikasi_mobil:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX_HIJAU, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" + filename), gambar)

            if len(klasifikasi_mobil) == 0 and len(klasifikasi_motor) ==0 and self.config['simpangambar']['debug'] :
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" + filename), gambar)

            ## ~~ DEBUG FULL PIC
            klasifikasi_motor_full = self.klasifier_cascade_motor_kiri.detectMultiScale(
                gambarfull)

            klasifikasi_mobil_full = self.klasifier_cascade_mobil_kiri.detectMultiScale(
                gambarfull)

            for klasifikasi in klasifikasi_motor_full:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" + filename_full), gambarfull)

            for klasifikasi in klasifikasi_mobil_full:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX_HIJAU, 1)

                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" + filename_full), gambarfull)

            if len(klasifikasi_mobil_full) == 0 and len(klasifikasi_motor_full) ==0 and self.config['simpangambar']['debug']:
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" + filename_full), gambarfull)


        elif lajur == "kanan":
            klasifikasi_motor = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambar)

            klasifikasi_mobil = self.klasifier_cascade_mobil_kanan.detectMultiScale(
                gambar)

            for klasifikasi in klasifikasi_motor:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" + filename), gambar)

            for klasifikasi in klasifikasi_mobil:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambar, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX_HIJAU, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" + filename), gambar)

            if len(klasifikasi_mobil) == 0 and len(klasifikasi_motor) ==0 and self.config['simpangambar']['debug'] :
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" + filename), gambar)


            ## ~~ DEBUG FULL PIC
            
            klasifikasi_motor_full = self.klasifier_cascade_motor_kanan.detectMultiScale(
                gambarfull)

            klasifikasi_mobil_full = self.klasifier_cascade_mobil_kanan.detectMultiScale(
                gambarfull)

            for klasifikasi in klasifikasi_motor_full:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/motor/" + filename_full), gambarfull)

            for klasifikasi in klasifikasi_mobil_full:
                # print(klasifikasi)

                x,y,w,h = klasifikasi
                cv.rectangle(gambarfull, (x, y), (x + w, y + h),
                            WARNA_BOUNDING_BOX_HIJAU, 1)
                if(self.config['simpangambar']['debug']):
                    cv.imwrite(("debug/" + lajur + "/mobil/" + filename_full), gambarfull)

            if len(klasifikasi_mobil_full) == 0 and len(klasifikasi_motor_full) ==0 and self.config['simpangambar']['debug'] :
                cv.imwrite(("debug/" + lajur + "/tidakdiketahui/" + filename_full), gambarfull)





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


        logger.info('klasifikasi %s %d', klasifikasi, jumlah)

        return klasifikasi, jumlah

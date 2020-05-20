from __future__ import print_function
import cv2 as cv
import argparse

SIMPAN_GAMBAR_POSITIF = True
DIREKTORI_GAMBAR_TEST = "training/images/test/"


filenamekiri = "logklasifikasikiri.csv"
filenamekanan = "logklasifikasikanan.csv"
filelogkiri = open(filenamekiri,'w')
filelogkanan = open(filenamekanan,'w')

# filelogkanan.write("motor1000,motor2000,motor3000,motor4000,motor5000,filename")
# filelogkiri.write("motor1000,motor2000,motor3000,motor4000,motor5000,filename")


class DeteksiKendaraan():
    def __init__(self):
        # self.mobilkanan_file = "./classifier/mobilkanan/classifier/cascade.xml"
        # self.mobilkiri_file = "./classifier/mobilkiri/classifier/cascade.xml"

        self.motorkanan_file = "./classifier/motorkanan.xml"
        self.motorkiri_file = "./classifier/motorkiri.xml"

        self.motorkanan_file1000 = "./classifier/motorkanan1000.xml"
        self.motorkiri_file1000 = "./classifier/motorkiri1000.xml"

        self.motorkanan_file2000 = "./classifier/motorkanan2000.xml"
        self.motorkiri_file2000 = "./classifier/motorkiri2000.xml"

        self.motorkanan_file3000 = "./classifier/motorkanan3000.xml"
        self.motorkiri_file3000 = "./classifier/motorkiri3000.xml"

        self.motorkanan_file4000 = "./classifier/motorkanan4000.xml"
        self.motorkiri_file4000 = "./classifier/motorkiri4000.xml"

        # self.mobilkanan_classifier = cv.CascadeClassifier(self.mobilkanan_file)
        # self.mobilkiri_classifier = cv.CascadeClassifier(self.mobilkiri_file)
        self.motorkanan_classifier = cv.CascadeClassifier(self.motorkanan_file)
        self.motorkiri_classifier = cv.CascadeClassifier(self.motorkiri_file)


        self.motorkanan_classifier1000 = cv.CascadeClassifier(self.motorkanan_file1000)
        self.motorkiri_classifier1000 = cv.CascadeClassifier(self.motorkiri_file1000)


        self.motorkanan_classifier2000 = cv.CascadeClassifier(self.motorkanan_file2000)
        self.motorkiri_classifier2000 = cv.CascadeClassifier(self.motorkiri_file2000)


        self.motorkanan_classifier3000 = cv.CascadeClassifier(self.motorkanan_file3000)
        self.motorkiri_classifier3000 = cv.CascadeClassifier(self.motorkiri_file3000)


        self.motorkanan_classifier4000 = cv.CascadeClassifier(self.motorkanan_file4000)
        self.motorkiri_classifier4000 = cv.CascadeClassifier(self.motorkiri_file4000)

    def klasifikasi_kendaraan_masuk(self, frame, id):
        frame_gray = frame
        # frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # frame_gray = cv.equalizeHist(frame_gray)

        # mobil = self.mobilkanan_classifier.detectMultiScale(frame_gray)
        file_name = (DIREKTORI_GAMBAR_TEST +"/kanan/motor_{}.jpg".format(id)) 
        file_name1 = "/kanan/motor_{}.jpg".format(id)
        cv.imwrite(file_name, frame_gray)

        motor = self.motorkanan_classifier.detectMultiScale(frame_gray)
        motor1000 = self.motorkanan_classifier1000.detectMultiScale(frame_gray)
        motor2000 = self.motorkanan_classifier2000.detectMultiScale(frame_gray)
        motor3000 = self.motorkanan_classifier3000.detectMultiScale(frame_gray)
        motor4000 = self.motorkanan_classifier4000.detectMultiScale(frame_gray)
        # print("masuk 1000")
        # print(motor1000)

        # print("masuk 2000")
        # print(motor2000)

        # print("masuk 3000")
        # print(motor3000)

        # print("masuk 4000")
        # print(motor4000)

        # print("masuk 7000")
        # print(motor)

        filelogkanan.write("\n{},{},{},{},{},{}".format(len(motor1000),len(motor2000),len(motor3000),len(motor4000),len(motor), file_name1))

        # for (x,y,w,h) in mobil:
        #     frame = cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1), (255, 0, 255), 1)

        for (x,y,w,h) in motor:
            frame = cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1), (255, 255, 255), 1)

        # cv.imshow('kendaraan masuk kanan', frame)

    def klasifikasi_kendaraan_keluar(self, frame,id):
        frame_gray = frame
        # frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # frame_gray = cv.equalizeHist(frame_gray)

        # mobil = self.mobilkiri_classifier.detectMultiScale(frame_gray)
        file_name = (DIREKTORI_GAMBAR_TEST +"/kiri/motor_{}.jpg".format(id)) 
        file_name1 = "/kiri/motor_{}.jpg".format(id)

        cv.imwrite(file_name, frame_gray)

        motor = self.motorkiri_classifier.detectMultiScale(frame_gray)
        motor1000 = self.motorkiri_classifier1000.detectMultiScale(frame_gray)
        motor2000 = self.motorkiri_classifier2000.detectMultiScale(frame_gray)
        motor3000 = self.motorkiri_classifier3000.detectMultiScale(frame_gray)
        motor4000 = self.motorkiri_classifier4000.detectMultiScale(frame_gray)
        # print("keluar 1000")
        # print(motor1000)

        # print("keluar 2000")
        # print(motor2000)

        # print("keluar 3000")
        # print(motor3000)

        # print("keluar 4000")
        # print(motor4000)

        # print("keluar 7000")
        # print(motor)
        
        # print(motor)o
        
        filelogkiri.write("\n{},{},{},{},{},{}".format(len(motor1000),len(motor2000),len(motor3000),len(motor4000),len(motor), file_name1))

        # for (x,y,w,h) in mobil:
        #     frame = cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1), (255, 0, 255), 1)

        for (x,y,w,h) in motor:
            frame = cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1), (255, 255, 255), 1)

        # cv.imshow('kendaraan masuk kiri', frame)








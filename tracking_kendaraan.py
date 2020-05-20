import os
import time
import sys
import datetime

import cv2
import numpy as np

from hitung_kendaraan import PenghitungKendaraan

# ============================================================================

NAMA_GAMBAR_BACKGROUND = "bg.png"
SUMBER = "vid.mp4" 

# kecepatan program, tunggu berapa waktu untuk pindah ke frame selanjutnya , 0=forever
WAKTU_TUNGGU = 1 # ms

TULIS_KE_FILE = False

# Warna untuk digambar di gambar nanti    
WARNA_GARIS_PEMBELAH = (255, 255, 0)
WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_CENTROID = (0, 0, 255)

# ============================================================================

def dapatkan_centroid(x, y, w, h):
    # centroid adalah titik tengah dari objek terdeteksi
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

# ============================================================================

def deteksi_objek(frame_foreground):

    LEBAR_MINIMAL = 21
    TINGGI_MINIMAL = 21

    # Temukan objek pada gambar
    _ , contours, _ = cv2.findContours(frame_foreground
        , cv2.RETR_EXTERNAL
        , cv2.CHAIN_APPROX_SIMPLE)

    objek_ditemukan = []
    for (i, contour) in enumerate(contours):

        (x, y, w, h) = cv2.boundingRect(contour)
        objek_valid = (w >= LEBAR_MINIMAL) and (h >= TINGGI_MINIMAL)

        if not objek_valid:
            continue

        centroid = dapatkan_centroid(x, y, w, h)

        objek_ditemukan.append(((x, y, w, h), centroid,contour))

    return objek_ditemukan

# ============================================================================

def transformasi_morfologi(frame_foreground):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    # kernel = np.ones((3,3), np.uint8)

    frame_foreground = cv2.bilateralFilter(frame_foreground,9,75,75)

    # isi bolong bolong
    frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_CLOSE, kernel)

    # hilangkan noise
    frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_OPEN, kernel)

    # gabung dengan objek terdekat
    frame_foreground = cv2.dilate(frame_foreground, kernel, iterations = 5)
    frame_foreground = cv2.erode(frame_foreground, kernel, iterations = 3)

    # isi bolong bolong
    frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_CLOSE, kernel2)

    return frame_foreground

# ============================================================================

def proses_frame(nomor_frame, frame, background_subtractor, penghitung_kendaraan, sebelah):

    ### copy frame asli 
    frame_diproses = frame.copy()

    ### gambar garis batas pertama.
    cv2.line(frame_diproses, (0, penghitung_kendaraan.garis_horizontal_pertama), (frame.shape[1], penghitung_kendaraan.garis_horizontal_pertama), WARNA_GARIS_PEMBELAH, 1)
    ### gambar garis batas kedua
    cv2.line(frame_diproses, (0, penghitung_kendaraan.garis_horizontal_kedua), (frame.shape[1], penghitung_kendaraan.garis_horizontal_kedua), WARNA_GARIS_PEMBELAH, 1)

    ### hilangkan backgroud menghasilkan gambar foreground
    frame_foreground = background_subtractor.apply(frame, 1)

    ### gambar garis pertama di frame hitam putih 
    # cv2.line(frame_foreground, (0, penghitung_kendaraan.garis_horizontal_pertama), (frame.shape[1], penghitung_kendaraan.garis_horizontal_pertama), WARNA_GARIS_PEMBELAH, 1)
    ### gambar garis kedua di frame hitam putih 
    # cv2.line(frame_foreground, (0, penghitung_kendaraan.garis_horizontal_kedua), (frame.shape[1], penghitung_kendaraan.garis_horizontal_kedua), WARNA_GARIS_PEMBELAH, 1)
    
    # cv2.imshow('foreground awal '+sebelah, frame_foreground)

    ### lakukan transformasi morfologi pada gambar foreground
    frame_foreground = transformasi_morfologi(frame_foreground)
    # cv2.imshow('foreground akhir '+sebelah, frame_foreground)

    objek_ditemukan = deteksi_objek(frame_foreground)

    for (i, objek) in enumerate(objek_ditemukan):
        posisi, centroid, _ = objek
        x, y, w, h = posisi

        # gambar bounding box pada gambar 
        cv2.rectangle(frame_diproses, (x, y), (x + w - 1, y + h - 1), WARNA_BOUNDING_BOX, 1)
        # cv2.rectangle(frame_foreground, (x, y), (x + w - 1, y + h - 1), WARNA_BOUNDING_BOX, 1)
       
        # gambar centroid pada gambar 
        cv2.circle(frame_diproses, centroid, 2, WARNA_CENTROID, -1)
        # cv2.circle(frame_foreground, centroid, 2, WARNA_CENTROID, -1)
        

    penghitung_kendaraan.update_jumlah_kendaraan(sebelah, objek_ditemukan, frame_diproses,frame, frame_foreground)

    return frame_diproses, frame_foreground

# ============================================================================

def kanan(rame,penghitung_kendaraan_kanan,nomor_frame,background_subtractor_kanan):
    frame_diproses, frame_foreground = proses_frame(nomor_frame, frame, background_subtractor_kanan, penghitung_kendaraan_kanan, "kanan")

    # cv2.imshow('Sebelah kanan asli', frame)
    # cv2.imshow('Sebelah kanan proses', frame_diproses)i

# ============================================================================

def kiri(frame,penghitung_kendaraan_kiri,nomor_frame,background_subtractor_kiri):
    frame_diproses, frame_foreground = proses_frame(nomor_frame, frame, background_subtractor_kiri, penghitung_kendaraan_kiri, "kiri")

    # cv2.imshow('Sebelah kiri asli', frame)
    # cv2.imshow('Sebelah kiri proses', frame_diproses)

# ============================================================================


def main():

    ## definisi background subtractor
    gambar_background = cv2.imread(NAMA_GAMBAR_BACKGROUND)

    # mogSubtractor = cv2.bgsegm.createBackgroundSubtractorMOG(300)
    # mog2Subtractor = cv2.createBackgroundSubtractorMOG2(300, 400, True)
    # gmgSubtractor = cv2.bgsegm.createBackgroundSubtractorGMG(10, .2)
    # knnSubtractor = cv2.createBackgroundSubtractorKNN(100, 400, True)
    # cntSubtractor = cv2.bgsegm.createBackgroundSubtractorCNT(5, True)

    # background_subtractor_kanan = mog2Subtractor
    # background_subtractor_kiri = mog2Subtractor

    background_subtractor_kanan = cv2.createBackgroundSubtractorMOG2(100, 0, True)
    background_subtractor_kiri = cv2.createBackgroundSubtractorMOG2(100, 0, True)

    background_subtractor_kanan.setShadowValue(0)
    background_subtractor_kiri.setShadowValue(0)

    gambar_backgroundkanan = gambar_background[0:gambar_background.shape[1], int(gambar_background.shape[1]/2):gambar_background.shape[1]]
    gambar_backgroundkiri = gambar_background[0:gambar_background.shape[1], 0:int(gambar_background.shape[1]/2)]
    
    background_subtractor_kanan.apply(gambar_backgroundkanan, 1)
    background_subtractor_kiri.apply(gambar_backgroundkiri, 1)

    ## definisi penghitung kendaran. Akan di tentukan saat frame pertama di load
    penghitung_kendaraan_kanan = None
    penghitung_kendaraan_kiri = None

    # Setup sumber gambar
    sumber_gambar = cv2.VideoCapture(SUMBER)

    lebar_frame = sumber_gambar.get(cv2.CAP_PROP_FRAME_WIDTH)
    tinggi_gambar = sumber_gambar.get(cv2.CAP_PROP_FRAME_HEIGHT)

    nomor_frame = -1

    while True:
        nomor_frame += 1

        ret, frame = sumber_gambar.read()
        if not ret:
            print("Mengambil gambar gagal, menghentikan program...")
            break

        print(nomor_frame)

        #belah gambar jadi dua
        sebelah_kiri  = frame[0:frame.shape[1], 0:int(frame.shape[1]/2)]
        sebelah_kanan  = frame[0:frame.shape[1], int(frame.shape[1]/2):frame.shape[1]]

        #inisialisasi kounter. dilakukan saat ini agar tau ukuran gambar nya
        if penghitung_kendaraan_kanan is None:
            penghitung_kendaraan_kanan = PenghitungKendaraan(sebelah_kanan.shape[:2], 80,"kanan")
        if penghitung_kendaraan_kiri is None:
            penghitung_kendaraan_kiri = PenghitungKendaraan(sebelah_kiri.shape[:2], 40,"kiri")

        # lakukan komputasi
        kanan(sebelah_kanan,penghitung_kendaraan_kanan,nomor_frame,background_subtractor_kanan)
        kiri(sebelah_kiri,penghitung_kendaraan_kiri,nomor_frame,background_subtractor_kiri)
        
        c = cv2.waitKey(WAKTU_TUNGGU)
        if c == 27:
            print("ESC ditekan, menghentikan program ...")
            break

    print("Menutup video ...")
    sumber_gambar.release()
    cv2.destroyAllWindows()
    print("Selesai .")

# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()

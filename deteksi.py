import os
import time
import sys
import datetime

import cv2
import numpy as np

# ============================================================================

GAMBAR_BACKGROUND = "bg.png"
VIDEO = "vid.mp4" 

# Warna untuk digambar di gambar nanti    
WARNA_GARIS_PEMBELAH = (255, 255, 0)
WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_CENTROID = (0, 0, 255)

# ============================================================================

def hitung_centroid(x, y, w, h):
    # centroid adalah titik tengah dari objek terdeteksi
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

# ============================================================================


def main():

    gambar_background = cv2.imread(GAMBAR_BACKGROUND)
    
    background_subtractor = cv2.createBackgroundSubtractorMOG2(100, 0, True)
    background_subtractor.setShadowValue(0)
    background_subtractor.apply(gambar_background, 1)

    video = cv2.VideoCapture(VIDEO)
    lebar_frame = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    tinggi_gambar = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frame_counter = -1

    while True:
        frame_counter += 1

        ret, frame = video.read()
        if not ret:
            print("Tidak dapat membuka video. Stop.")
            break
        
        ####
        frame_foreground = background_subtractor.apply(frame, 1)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

        frame_foreground = cv2.bilateralFilter(frame_foreground,9,75,75)
        frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_CLOSE, kernel)
        frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_OPEN, kernel)
        frame_foreground = cv2.dilate(frame_foreground, kernel, iterations = 5)
        frame_foreground = cv2.erode(frame_foreground, kernel, iterations = 3)
        frame_foreground = cv2.morphologyEx(frame_foreground, cv2.MORPH_CLOSE, kernel)

        ####
        LEBAR_MINIMAL = 21
        TINGGI_MINIMAL = 21

        _ , contours, _ = cv2.findContours(frame_foreground
            , cv2.RETR_EXTERNAL
            , cv2.CHAIN_APPROX_SIMPLE)

        objek_ditemukan = []
        for (i, contour) in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contour)
            objek_valid = (w >= LEBAR_MINIMAL) and (h >= TINGGI_MINIMAL)

            if not objek_valid:
                continue

            centroid = hitung_centroid(x, y, w, h)

            objek_ditemukan.append(((x, y, w, h), centroid,contour))

        ####
        for (i, objek) in enumerate(objek_ditemukan):
            posisi, centroid, _ = objek
            x, y, w, h = posisi

            # gambar bounding box pada gambar 
            cv2.rectangle(frame, (x, y), (x + w - 1, y + h - 1), WARNA_BOUNDING_BOX, 1)
        
            # gambar centroid pada gambar 
            cv2.circle(frame, centroid, 2, WARNA_CENTROID, -1)
            

        ####
        cv2.imshow('asli', frame)
        cv2.imshow('foreground', frame_foreground)

        c = cv2.waitKey(250)
        if c == 27:
            print("ESC ditekan, menghentikan program.")
            break

    print("Menutup video ...")
    video.release()
    cv2.destroyAllWindows()
    print("Selesai .")


# ============================================================================

if __name__ == "__main__":
    print("Mulai .")
    main()
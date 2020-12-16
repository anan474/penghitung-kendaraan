#!/usr/bin/python3
import cv2 as cv
import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(
            argv, "i:b:o:w:h:", ["help", "ifile=", "bfile=", "odir=", "width=", "height="])
    except getopt.GetoptError:
        print('resize_image.py -i <inputfile> -b <backgroundimagefile> -o <outdirectory> -w <width> -h <height>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--help":
            print(
                'resize_image.py -i <inputfile> -b <backgroundimagefile> -o <outdirectory> -w <width> -h <height>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-b", "--bfile"):
            backgroundimgfile = arg
        elif opt in ("-o", "--odir"):
            outdirectory = arg
        elif opt in ("-w", "--width"):
            width = int(arg)
        elif opt in ("-h", "--height"):
            height = int(arg)

    lebar_frame = width
    tinggi_frame = height
    print('Input file is :', inputfile)
    print('Background image file is :', backgroundimgfile)
    print('Output directory is :', outdirectory)

    gambar_background = cv.imread(backgroundimgfile)
    background_subtractor = cv.createBackgroundSubtractorMOG2()
    background_subtractor.setShadowValue(0)
    background_subtractor.apply(gambar_background, 1)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    kernel2 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

    gambar = cv.imread(inputfile)

    def get_foreground(frame):
        frame_foreground = background_subtractor.apply(frame, 1)
        return frame_foreground

    def proses_morfologi(frame):
        frame = cv.bilateralFilter(
            frame, 9, 75, 75)

        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, kernel)

        frame_foreground = cv.morphologyEx(
            frame, cv.MORPH_OPEN, kernel2)

        frame = cv.dilate(frame, kernel, iterations=5)

        frame = cv.erode(frame, kernel, iterations=3)

        frame = cv.morphologyEx(
            frame, cv.MORPH_CLOSE, kernel)

        return frame

    def hitung_centroid(x, y, w, h):
        # centroid adalah titik tengah dari objek terdeteksi
        x1 = int(w / 2)
        y1 = int(h / 2)

        cx = x + x1
        cy = y + y1

        return (cx, cy)

    def dapatkan_objek(frame):
        contours, _ = cv.findContours(
            frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        objek_ditemukan = []
        for (i, contour) in enumerate(contours):

            (x, y, w, h) = cv.boundingRect(contour)
            objek_valid = (w >= width) and (h >= height)

            if not objek_valid:
                continue

            centroid = hitung_centroid(x, y, w, h)

            lajur = "kiri" if centroid[0] < (lebar_frame/2) else "kanan"

            objek_ditemukan.append(
                ((x, y, w, h), centroid, lajur))

        return objek_ditemukan

    def deteksi_objek(frame):

        foreground = get_foreground(frame)
        cv.imwrite(outdirectory + "/foreground1.jpg", foreground)
        foreground = proses_morfologi(foreground)
        cv.imwrite(outdirectory + "/foreground2.jpg", foreground)

        daftar_objek = dapatkan_objek(foreground)

        return daftar_objek

    objek = deteksi_objek(gambar)
    for idx, obj in enumerate(objek):
        posisi, _, lajur = obj
        x, y, w, h = posisi
        crop_img = gambar[y:y+h, x:x+w]
        cv.imwrite(outdirectory + "/" + lajur + "/" + idx + ".jpg", gambar)


if __name__ == "__main__":
    main(sys.argv[1:])

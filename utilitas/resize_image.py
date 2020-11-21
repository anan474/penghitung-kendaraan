#!/usr/bin/python3
import cv2 as cv
import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(
            argv, "i:o:w:h:", ["ifile=", "ofile=", "width=", "height="])
    except getopt.GetoptError:
        print('resize_image.py -i <inputfile> -o <outputfile> -w <width> -h <height>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--help':
            print('resize_image.py -i <inputfile> -o <outputfile> -w <width> -h <height>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-w", "--width"):
            width = int(arg)
        elif opt in ("-h", "--height"):
            height = int(arg)

    print('Input file is :', inputfile)
    print('Output file is :', outputfile)
    print('Resized to width : ', width, ' and height : ', height)
    gambar = cv.imread(inputfile)
    gambar = cv.resize(gambar, (width, height))
    cv.imwrite(outputfile, gambar)


if __name__ == "__main__":
    main(sys.argv[1:])

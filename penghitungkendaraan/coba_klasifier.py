
import cv2 as cv
from klasifier_kendaraan import Klasifier

# ============================================================================

klasifier = Klasifier()

gambar_background = cv.imread(GAMBAR_BACKGROUND)

klasifikasi, jumlah, jumlah_mobil, jumlah_motor = klasifier.klasifikasi_kendaraan(
    gambar_kendaraan, frame, lajur, frame_counter)

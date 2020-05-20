import math

import cv2
import numpy as np

from classifier import DeteksiKendaraan

# ============================================================================

WARNA_GARIS = [ (0,0,255), (0,106,255), (0,216,255), (0,255,182), (0,255,76)
    , (144,255,0), (255,255,0), (255,148,0), (255,0,178), (220,0,255) ]

WARNA_BOUNDING_BOX = (255, 0, 0)

DIREKTORI_GAMBAR_POSITIF = "training/images/positif/"
SIMPAN_GAMBAR_POSITIF = False

# ============================================================================

class Kendaraan(object):
    def __init__(self, id, centroid, posisi, contour):
        self.id = id
        self.posisi = posisi
        self.posisi_kendaraan = [centroid]
        self.sejak_ditemukan = 0 # berapa frame sejak pertama kali ditemukan
        self.telah_dihitung = False
        self.contour_kendaraan = contour

    @property
    def posisi_terakhir(self):
        return self.posisi_kendaraan[-1]

    def tambah_posisi(self, posisi_baru):
        self.posisi_kendaraan.append(posisi_baru)
        self.sejak_ditemukan = 0

    def draw_track(self, gambar_hasil):
        warna_track = WARNA_GARIS[self.id % len(WARNA_GARIS)]
        for point in self.posisi_kendaraan:
            cv2.circle(gambar_hasil, point, 2, warna_track, -1)
            cv2.polylines(gambar_hasil, [np.int32(self.posisi_kendaraan)]
                , False, warna_track, 1)

    def update_posisi(self, posisi):
        self.posisi = posisi

    def update_contour(self, contour):
        self.contour_kendaraan = contour
# ============================================================================

class PenghitungKendaraan(object):
    def __init__(self, shape, garis_horizontal_pertama, namafolder):

        self.height, self.width = shape
        self.garis_horizontal_pertama = garis_horizontal_pertama
        self.garis_horizontal_kedua = garis_horizontal_pertama+20

        self.namafolder = namafolder

        self.semua_kendaraan = []
        self.id_kendaraan_selanjutnya = 0
        self.jumlah_kendaraan = 0
        self.maks_tidak_terlihat = 7 # berapa frame kendaraannya tidak terlihat, dihapus dari daftar

    @staticmethod
    def get_vector(a, b):
        """Calculate vector (distance, angle in degrees) from point a to point b.

        Angle ranges from -180 to 180 degrees.
        Vector with angle 0 points straight down on the image.
        Values increase in clockwise direction.
        """
        dx = float(b[0] - a[0])
        dy = float(b[1] - a[1])

        distance = math.sqrt(dx**2 + dy**2)

        if dy > 0:
            angle = math.degrees(math.atan(-dx/dy))
        elif dy == 0:
            if dx < 0:
                angle = 90.0
            elif dx > 0:
                angle = -90.0
            else:
                angle = 0.0
        else:
            if dx < 0:
                angle = 180 - math.degrees(math.atan(dx/dy))
            elif dx > 0:
                angle = -180 - math.degrees(math.atan(dx/dy))
            else:
                angle = 180.0        

        return distance, angle 


    @staticmethod
    def apakah_vector_valid(a):
        distance, angle = a
        threshold_distance = max(40.0, -0.008 * angle**2 + 0.4 * angle + 25.0)
        return (distance <= threshold_distance)


    def update_kendaraan(self, kendaraan, objek_ditemukan):
        # Cari tau apakah objek yand ditemuan merupakan kendaraan ini
        for i, objek in enumerate(objek_ditemukan):
            posisi, centroid, contour = objek

            vector = self.get_vector(kendaraan.posisi_terakhir, centroid)
            if self.apakah_vector_valid(vector):
                kendaraan.tambah_posisi(centroid)
                kendaraan.update_posisi(posisi)
                kendaraan.update_contour(contour)
                return i

        # Tidak ada objek ditemukan yang sesuai...        
        kendaraan.sejak_ditemukan += 1
        return None


    def update_jumlah_kendaraan(self, sebelah, objek_ditemukan, gambar_hasil = None, frame_asli = None, frame_foreground = None):

        klasifier = DeteksiKendaraan()

        # Update semua kendaraan
        for kendaraan in self.semua_kendaraan:
            i = self.update_kendaraan(kendaraan, objek_ditemukan)
            if i is not None:
                del objek_ditemukan[i]

        # tambahkan kendaraan baru dari blob yang belum di asosiasi dengan kendaraan yang udah ada
        for objek in objek_ditemukan:
            posisi, centroid, contour = objek


            if self.namafolder is "kiri" and not (centroid[1] < self.garis_horizontal_pertama):
                kendaraan_baru = Kendaraan(self.id_kendaraan_selanjutnya, centroid, posisi, contour)
                self.id_kendaraan_selanjutnya += 1
                self.semua_kendaraan.append(kendaraan_baru)

            if self.namafolder is "kanan" and not (centroid[1] > self.garis_horizontal_kedua):
                kendaraan_baru = Kendaraan(self.id_kendaraan_selanjutnya, centroid, posisi, contour)
                self.id_kendaraan_selanjutnya += 1
                self.semua_kendaraan.append(kendaraan_baru)
            

        # Hitung kendaraan yang melewati garis horizotal pertama dan belum melewati garis horizontal kedua. 
        # Hal ini agar meminimalisir salah hitung
        #nomor = 0
        for kendaraan in self.semua_kendaraan:
            if not kendaraan.telah_dihitung and (kendaraan.posisi_terakhir[1] > self.garis_horizontal_pertama) and (kendaraan.posisi_terakhir[1] < self.garis_horizontal_kedua):
                self.jumlah_kendaraan += 1
                kendaraan.telah_dihitung = True
                
                x, y, w, h = kendaraan.posisi
                crop_img = frame_asli[y:y+h, x:x+w]
                # cv2.imshow("step 1 "+sebelah, crop_img)

                # crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2BGRA)

                crop_img1 = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                # cv2.imshow("step 2 "+sebelah, crop_img1)

                # crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                # _, crop_img1 = cv2.threshold(
                #     crop_img1, 100, 101, cv2.THRESH_TOZERO)

                crop_img1[crop_img1 < 10] = 10

                crop_img_foreground = frame_foreground[y:y+h, x:x+w]
                # cv2.imshow("step 3 "+sebelah, crop_img_foreground)

                
                # hasil = np.zeros_like(crop_img)
                # hasil = cv2.bitwise_and(
                #     crop_img, crop_img, mask=crop_img_foreground)

                hasil1 = cv2.bitwise_and(
                    crop_img1, crop_img1, mask=crop_img_foreground)
                # cv2.imshow("step4 "+sebelah, hasil1)

                # hasil[crop_img ==
                #       0] = 1

                # hasil[crop_img_foreground ==
                #       255] = crop_img[crop_img_foreground == 255]

                # ret, mask = cv2.threshold(crop_img_foreground, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                # kernel = np.ones((9,9), np.uint8)
                # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

                # hasil = crop_img.copy()
                # crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2BGRA)
                # hasil[:, :, 3] = crop_img_foreground
                # crop_img[:, :, 3] = crop_img_foreground

                # cv2.imshow("hasil1 "+sebelah, hasil1)
                # cv2.imshow("crop_img "+sebelah, crop_img)
                # cv2.imshow("kendaraan terdeteksi "+sebelah, crop_img)
                # cv2.imshow("kendaraan terdeteksi foreground"+sebelah, crop_img_foreground)
                # cv2.imshow("hasil"+sebelah, hasil)
                # cv2.imshow("mask"+sebelah, mask)
                # cv2.imshow("gambar hasil "+sebelah, gambar_hasil)
                # cv2.imshow("frame asli "+sebelah, frame_asli)

                if sebelah is "kiri":
                    klasifier.klasifikasi_kendaraan_keluar(crop_img1,kendaraan.id)
                if sebelah is "kanan":
                    klasifier.klasifikasi_kendaraan_masuk(crop_img1,kendaraan.id)

                # cv2.rectangle(frame_asli, (x, y), (x + w - 1, y + h - 1), WARNA_BOUNDING_BOX, 1)
                # cv2.imshow("kendaraan "+sebelah, frame_asli)
                
                # file_name = (DIREKTORI_GAMBAR_POSITIF +self.namafolder+ "/gabungan_%07d.jpg") % self.jumlah_kendaraan
                # cv2.imwrite(file_name, hasil1)
                
                

        # gambar centroid dan garis track kendaraan antar frame
        if gambar_hasil is not None:
            for kendaraan in self.semua_kendaraan:
                kendaraan.draw_track(gambar_hasil)

            cv2.putText(gambar_hasil, ("%02d" % self.jumlah_kendaraan), (142, 10)
                , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)

        # Hapus kendaraan yang tidak dilihat setelah beberapa frame
        yang_dihapus = [ kendaraan.id for kendaraan in self.semua_kendaraan
            if kendaraan.sejak_ditemukan >= self.maks_tidak_terlihat ]

        self.semua_kendaraan[:] = [ kendaraan for kendaraan in self.semua_kendaraan
            if not kendaraan.sejak_ditemukan >= self.maks_tidak_terlihat ]
        

        if sebelah is "kiri":
            yang_dihapus = [ kendaraan.id for kendaraan in self.semua_kendaraan
                if not (kendaraan.telah_dihitung and kendaraan.posisi_terakhir[1] < self.garis_horizontal_pertama) ]

            self.semua_kendaraan[:] = [ kendaraan for kendaraan in self.semua_kendaraan
                if not (kendaraan.telah_dihitung and kendaraan.posisi_terakhir[1] < self.garis_horizontal_pertama) ]
            

        if sebelah is "kanan":
            yang_dihapus = [ kendaraan.id for kendaraan in self.semua_kendaraan
                if not (kendaraan.telah_dihitung and kendaraan.posisi_terakhir[1] > self.garis_horizontal_kedua) ]

            self.semua_kendaraan[:] = [ kendaraan for kendaraan in self.semua_kendaraan
                if not (kendaraan.telah_dihitung and kendaraan.posisi_terakhir[1] > self.garis_horizontal_kedua) ]
            

# ============================================================================

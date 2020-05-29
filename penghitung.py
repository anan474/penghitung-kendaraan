import math

import cv2
import numpy as np

# ============================================================================

WARNA_GARIS = [ (0,0,255), (0,106,255), (0,216,255), (0,255,182), (0,255,76)
    , (144,255,0), (255,255,0), (255,148,0), (255,0,178), (220,0,255) ]

WARNA_BOUNDING_BOX = (255, 0, 0)

# ============================================================================

class Kendaraan(object):
    def __init__(self, id, centroid)
        self.id = id

        self.posisi = [centroid]
        self.tidak_terlihat = 0
        self.telah_dihitung = False
        
    @property
    def posisi_terakhir(self):
        return self.posisi[-1]

    def perbarui_posisi(self, posisi_terbaru):
        self.posisi.append(posisi_terbaru)
        self.tidak_terlihat = 0

# ============================================================================

class Penghitung (object):
    def __init__(self, tinggi_frame, lebar_frame , garis_masuk, garis_keluar, lajur):
        self.tinggi_frame = tinggi_frame
        self.lebar_frame = lebar_frame
        self.garis_masuk = garis_masuk
        self.garis_keluar = garis_keluar

        self.lajur = lajur

        self.kendaraan = []
        self.id_kendaraan_selanjutnya = 0
        self.jumlah_kendaraan = 0
        self.limit_tidak_terlihat = 10 # jika pada @limit frame tidak terlihat maka kendaraan dihilangkan

    @staticmethod
    def hitung_vektor(a,b):
        # Hitung vektor antara titik satu ke titik lainnya. Sudut 0 merupakan tegak lurus dari atas ke bawah, sudut bergerak searah jarum jam
        dx = float(b[0] - a[0])
        dy = float(b[1] - a[1])

        jarak = math.sqrt(dx**2 + dy**2)

        if dy > 0:
            sudut = math.degrees(math.atan(-dx/dy))
        elif dy == 0:
            if dx < 0:
                sudut = 90.0
            elif dx > 0:
                sudut = -90.0
            else:
                sudut = 0.0
        else:
            if dx < 0:
                sudut = 180 - math.degrees(math.atan(dx/dy))
            elif dx > 0:
                sudut = -180 - math.degrees(math.atan(dx/dy))
            else:
                sudut = 180.0        

        return jarak, sudut 

    def apakah_masuk_garis(self, centroid):
        # jika centroid berada dalam garis sesuai dengan lajur nya maka kembalikan nilai True
        if self.lajur is "kiri" and (centroid[1] < self.garis_masuk) and (centroid[1] > self.garis_keluar):
            return True
        elif self.lajur is "kanan" and (centroid[1] > self.garis_masuk) and (centroid[1] > self.garis_keluar):
            return True
        else:
            return False

    def apakah_melewati_garis_keluar(self, kendaraan):
        # jika kendararan telah melewati garis keluar sesuai jalurnya maka kembalikan nilai True
        if self.jalur is "kiri" and (kendaraan.posisi_terakhir[1] < self.garis_keluar):
            return True
        elif self.jalur is "kanan" and (kendaraan.posisi_terakhir[1] > self.garis_keluar):
            return True
        else:
            return False


    def perbarui_penghitung(self, objek, potongan_gambar):
        
        # dari data kendaraan yang telah di-tracking, cek satu persatu mana yang merupakan kendaraan tersebut        
        for indek_kendaraan, kendaraan in enumerate(self.kendaraan):

            ### update status kendaraan
            #  jika cocok update status kendaraan nya,
            #  jika tidak ada cocok dengan kendaraan yang sudah ada maka tambahkan jadi kendaraan baru
            ada_objek_yg_cocok = False
            for indek_objek_ini, objek_ini in enumerate(objek):
                posisi_objek_ini, centroid_objek_ini = objek_ini

                vektor = self.hitung_vektor(kendaraan.posisi_terakhir, centroid_objek_ini)

                if self.apakah_vektor_valid(vektor):
                    # update status kendaraan
                    kendaraan.perbarui_posisi(centroid_objek_ini)
                    # hilangkan dari daftar objek
                    del objek[indek_objek_ini]
                    # set bahwa ada objek yang cocok untuk kendaraan ini
                    ada_objek_yg_cocok = True

                    ## sampai disini sebenarnya bisa di hentikan perulangan nya tapi coba biarkan untuk cek apakah bisa terdeteksi menjadi lebih dari dua kendaraan untuk objek yang sama
            
            # kalau tidak ada ketemu tambahkan hitungan jumlah frame tidak terlihat untuk kendaraan ini
            if ada_objek_yg_cocok is False:
                kendaraan.tidak_terlihat += 1

            ### hitung kendaraan yang belum dihitung dan melewati garis batas keluar 
            if not kendaraan.telah_dihitung and apakah_melewati_garis_keluar(kendaraan):
                self.jumlah_kendaraan += 1
                kendaraan.telah_dihitung = True

            ### hapus kendaraan yang telah melewati limit batas nilai tidak terlihat di frame
            if kendaraan.tidak_terlihat > self.limit_tidak_terlihat:
                del self.kendaraan[indek_kendaraan]

        # dari objek yang tersisa dari operasi sebelumnya, tambahkan menjadi kendaraan baru
        for objek_ini in objek:
            posisi_objek_ini, centroid_objek_ini = objek_ini

            # cek apakah objek berada dalam area yang dibatasi garis
            if apakah_masuk_garis(centroid_objek_ini):
                kendaraan_baru = Kendaraan(self.id_kendaraan_selanjutnya, centroid_objek_ini, posisi_objek_ini)
                self.id_kendaraan_selanjutnya += 1
                self.kendaraan.append(kendaraan_baru)


        
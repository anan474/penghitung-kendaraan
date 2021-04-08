
import math
import copy
import numpy as np
import cv2 as cv

from klasifier_kendaraan import Klasifier
from kendaraan import Kendaraan
from pengelola_basisdata import PengelolaBasisdata
from gambar_objek import GambarObjek

klasifier = Klasifier()
pengelola_basisdata = PengelolaBasisdata()

# ============================================================================

GARIS_PEMBATAS_KIRI_MASUK = 240
GARIS_PEMBATAS_KIRI_KELUAR = 60

GARIS_PEMBATAS_KANAN_MASUK = 40
GARIS_PEMBATAS_KANAN_KELUAR = 120


BATAS_FRAME_KENDARAAN_TIDAK_TERLIHAT = 10

# =======================================================


class TrackerKendaraan ():
    """Kelas ini mencatat dan memanajemen daftar kendaraan yang sedang di tracking
    """

    def __init__(self):
        self.garis_masuk_kiri = GARIS_PEMBATAS_KIRI_MASUK
        self.garis_keluar_kiri = GARIS_PEMBATAS_KIRI_KELUAR
        self.garis_masuk_kanan = GARIS_PEMBATAS_KANAN_MASUK
        self.garis_keluar_kanan = GARIS_PEMBATAS_KANAN_KELUAR

        self.kendaraan = []
        self.id_kendaraan_selanjutnya = 0

        self.kendaraan_untuk_diklasifikasi = []

        self.jumlah_kendaraan = 0
        self.jumlah_kendaraan_terklasifikasi = 0

        # jika pada @limit frame tidak terlihat maka kendaraan dihilangkan
        self.limit_tidak_terlihat = BATAS_FRAME_KENDARAAN_TIDAK_TERLIHAT

    @staticmethod
    def hitung_vektor(a, b):
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

    @staticmethod
    def apakah_vektor_valid(a):
        jarak, sudut = a
        batas_jarak = max(40.0, -0.008 * sudut**2 + 0.4 * sudut + 25.0)
        return (jarak <= batas_jarak)

    def apakah_masuk_garis(self, centroid, lajur):
        # jika centroid berada dalam garis sesuai dengan lajur nya maka kembalikan nilai True
        if lajur == "kiri" and (centroid[1] < self.garis_masuk_kiri) and (centroid[1] > self.garis_keluar_kiri):
            return True
        elif lajur == "kanan" and (centroid[1] > self.garis_masuk_kanan) and (centroid[1] < self.garis_keluar_kanan):
            return True
        else:
            return False

    def apakah_melewati_garis_keluar(self, kendaraan):
        # jika kendararan telah melewati garis keluar sesuai lajur nya maka kembalikan nilai True
        if kendaraan.lajur == "kiri" and (kendaraan.centroid_terakhir[1] < self.garis_keluar_kiri):
            return True
        elif kendaraan.lajur == "kanan" and (kendaraan.centroid_terakhir[1] > self.garis_keluar_kanan):
            return True
        else:
            return False

    def cocokkan_dengan_data_yg_ada(self, objek):
        # dari data kendaraan yang telah di-tracking, cek satu persatu mana yang merupakan kendaraan tersebut

        # return sisa objek yang tidak ada kecocokan

        for indek_kendaraan, kendaraan in enumerate(self.kendaraan):

            # update status kendaraan
            #  jika cocok update status kendaraan nya,
            #  jika tidak ada cocok dengan kendaraan yang sudah ada maka tambahkan jadi kendaraan baru
            ada_objek_yg_cocok = False
            for indek_objek_ini, objek_ini in enumerate(objek):
                posisi_objek_ini, centroid_objek_ini, lajur = objek_ini

                vektor = self.hitung_vektor(
                    kendaraan.centroid_terakhir, centroid_objek_ini)

                if self.apakah_vektor_valid(vektor):
                    # update status kendaraan
                    kendaraan.perbarui_centroid(centroid_objek_ini)
                    kendaraan.perbarui_posisi(posisi_objek_ini)
                    # hilangkan dari daftar objek
                    del objek[indek_objek_ini]
                    # set bahwa ada objek yang cocok untuk kendaraan ini
                    ada_objek_yg_cocok = True

                    # sampai disini sebenarnya bisa di hentikan perulangan nya tapi coba biarkan untuk cek apakah bisa terdeteksi menjadi lebih dari dua kendaraan untuk objek yang sama

            # kalau tidak ada ketemu tambahkan hitungan jumlah frame tidak terlihat untuk kendaraan ini
            if ada_objek_yg_cocok is False:
                kendaraan.tidak_terlihat += 1

            # hitung kendaraan yang belum dihitung dan melewati garis batas keluar
            if not kendaraan.telah_dihitung and self.apakah_melewati_garis_keluar(kendaraan):
                self.jumlah_kendaraan += 1
                kendaraan.telah_dihitung = True

            # jika kendaraan telah dihitung maka pindahkan ke kendaraan_untuk_diklasifikasi
            if kendaraan.telah_dihitung:
                self.kendaraan_untuk_diklasifikasi.append(
                    self.kendaraan[indek_kendaraan])
                del self.kendaraan[indek_kendaraan]

            # hapus kendaraan yang telah melewati limit batas nilai tidak terlihat di frame
            if kendaraan.tidak_terlihat > self.limit_tidak_terlihat:
                del self.kendaraan[indek_kendaraan]

        return objek

    def tambahkan_ke_daftar_tracking(self, objek):

        # dari objek yang tersisa dari operasi sebelumnya, tambahkan menjadi kendaraan baru
        for objek_ini in objek:
            posisi_objek_ini, centroid_objek_ini, lajur = objek_ini

            # cek apakah objek berada dalam area yang dibatasi garis
            if self.apakah_masuk_garis(centroid_objek_ini, lajur):
                kendaraan_baru = Kendaraan(
                    self.id_kendaraan_selanjutnya, centroid_objek_ini, posisi_objek_ini, lajur)
                self.id_kendaraan_selanjutnya += 1
                self.kendaraan.append(kendaraan_baru)

    def handle_kendaraan_melewati_batas(self, frame):
        # dari kendaraan_untuk_diklasifikasi lakukan klasifikasi, lalu masukkan nilai nya ke variabel
        for indek_kendaraan, kendaraan in enumerate(self.kendaraan_untuk_diklasifikasi):
            x, y, w, h = kendaraan.posisi
            lajur = kendaraan.lajur

            # crop gambar jadi hanya kendaraan | ambil snapshot kendaraan
            gambar_kendaraan = frame[y:y+h, x:x+w]
            gambar_kendaraan_gray = cv.cvtColor(
                gambar_kendaraan, cv.COLOR_BGR2GRAY)  # convert ke grayscale

            # kalo ada pixel di bawah 10 (hitam pekat), jadikan abu abu
            gambar_kendaraan_gray[gambar_kendaraan_gray < 10] = 10

            klasifikasi = klasifier.klasifikasi_kendaraan(
                gambar_kendaraan_gray, lajur)

            GambarObjek.print_simpan_kendaraan(gambar_kendaraan,lajur,klasifikasi)
            # tambahkan ke basis data
            pengelola_basisdata.simpan_ke_db(klasifikasi, lajur)

            # tambah nilai ke kounter
            if klasifikasi:
                self.jumlah_kendaraan_terklasifikasi += 1

            # hapus dari daftar
            del self.kendaraan_untuk_diklasifikasi[indek_kendaraan]

    def perbarui_tracker(self, objek, frame):
        objek_sisa = self.cocokkan_dengan_data_yg_ada(objek)

        self.tambahkan_ke_daftar_tracking(objek_sisa)

        self.handle_kendaraan_melewati_batas(frame)

        return self.kendaraan

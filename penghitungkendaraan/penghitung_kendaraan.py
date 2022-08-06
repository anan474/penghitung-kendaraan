
import math
import time
import uuid
import copy
import numpy as np
import cv2 as cv

from klasifier_kendaraan import Klasifier
from kendaraan import Kendaraan
from pengelola_basisdata import PengelolaBasisdata
from gambar_objek import GambarObjek


# ============================================================================

# GARIS_PEMBATAS_KIRI_MASUK = 240
GARIS_PEMBATAS_KIRI_MASUK = 120

GARIS_PEMBATAS_KIRI_KELUAR = 60

# GARIS_PEMBATAS_KANAN_MASUK = 10
GARIS_PEMBATAS_KANAN_MASUK = 40
# GARIS_PEMBATAS_KANAN_KELUAR = 50
GARIS_PEMBATAS_KANAN_KELUAR = 80
# GARIS_PEMBATAS_KANAN_KELUAR = 100
# GARIS_PEMBATAS_KANAN_KELUAR = 120


BATAS_FRAME_KENDARAAN_TIDAK_TERLIHAT = 10

# =======================================================


LEBAR = 640
TINGGI = 360


class PenghitungKendaraan ():
    """Kelas ini mencatat dan memanajemen daftar kendaraan yang sedang di tracking
    """

    def __init__(self, config):
        self.config = config
        self.garis_masuk_kiri = GARIS_PEMBATAS_KIRI_MASUK
        self.garis_keluar_kiri = GARIS_PEMBATAS_KIRI_KELUAR
        self.garis_masuk_kanan = GARIS_PEMBATAS_KANAN_MASUK
        self.garis_keluar_kanan = GARIS_PEMBATAS_KANAN_KELUAR

        self.kendaraan = []
        self.id_kendaraan_selanjutnya = 0

        self.kendaraan_untuk_diklasifikasi = []

        self.jumlah_kendaraan = 0

        # jika pada @limit frame tidak terlihat maka kendaraan dihilangkan
        self.limit_tidak_terlihat = BATAS_FRAME_KENDARAAN_TIDAK_TERLIHAT

        self.klasifier = Klasifier(config)
        self.pengelola_basisdata = PengelolaBasisdata()

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

    def cocokkan_dengan_data_yg_ada(self, objek, foreground):
        # dari data kendaraan yang telah di-tracking, cek satu persatu mana yang merupakan kendaraan tersebut

        # return sisa objek yang tidak ada kecocokan

        for indek_kendaraan, kendaraan in enumerate(self.kendaraan):

            # update status kendaraan
            #  jika cocok update status kendaraan nya,
            #  jika tidak ada cocok dengan kendaraan yang sudah ada maka tambahkan jadi kendaraan baru
            ada_objek_yg_cocok = False

            for indek_objek_ini, objek_ini in enumerate(objek):
                # looping data objek yang diberikan
                posisi_objek_ini, centroid_objek_ini, lajur = objek_ini

                vektor = self.hitung_vektor(
                    kendaraan.centroid_terakhir, centroid_objek_ini)

                # print(lajur, kendaraan.centroid_terakhir, centroid_objek_ini)
                # print(lajur, "turun:", kendaraan.centroid_terakhir[
                #     1] < centroid_objek_ini[1])
                # print(lajur, "naik:",
                #       kendaraan.centroid_terakhir[1] > centroid_objek_ini[1])

                # benar_di_kanan = kendaraan.centroid_terakhir[
                #     1] < centroid_objek_ini[1] and lajur == "kanan"
                # benar_di_kiri = kendaraan.centroid_terakhir[1] > centroid_objek_ini[1] and lajur == "kiri"

                if self.apakah_vektor_valid(vektor):
                    # update status kendaraan
                    kendaraan.perbarui_centroid(centroid_objek_ini)
                    kendaraan.perbarui_posisi(posisi_objek_ini)
                    # hilangkan dari daftar objek
                    # set bahwa ada objek yang cocok untuk kendaraan ini
                    ada_objek_yg_cocok = True
                    del objek[indek_objek_ini]

            # kalau tidak ada ketemu tambahkan hitungan jumlah frame tidak terlihat untuk kendaraan ini
            if ada_objek_yg_cocok is False:
                self.kendaraan[indek_kendaraan].tidak_terlihat += 1

            # hitung kendaraan yang belum dihitung dan melewati garis batas keluar
            # jika kendaraan telah dihitung maka pindahkan ke kendaraan_untuk_diklasifikasi
            if self.apakah_melewati_garis_keluar(kendaraan):
                self.jumlah_kendaraan += 1
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

    def handle_kendaraan_melewati_batas(self, frame, frame_counter, foreground):

        # dari kendaraan_untuk_diklasifikasi lakukan klasifikasi, lalu masukkan nilai nya ke variabel
        for indek_kendaraan, kendaraan in enumerate(self.kendaraan_untuk_diklasifikasi):
            x, y, w, h = kendaraan.posisi
            lajur = kendaraan.lajur

            lebihkan = 10

            ya = y-lebihkan
            yb = y+h+lebihkan

            xa = x-lebihkan
            xb = x+w+lebihkan

            if ya < 0:
                ya = 0
            if yb > 360:
                yb = 360

            if xa < 0:
                xa = 0
            if xb > 640:
                xb = 640

            # crop gambar jadi hanya kendaraan | ambil snapshot kendaraan
            gambar_kendaraan_awal = frame[y:y+h, x:x+w]
            gambar_kendaraan = frame[ya:yb, xa:xb]
            gambar_kendaraan_gray = cv.cvtColor(
                gambar_kendaraan, cv.COLOR_BGR2GRAY)  # convert ke grayscale

            gambar_kendaraan_gray_awal = gambar_kendaraan_gray
            # kalo ada pixel di bawah 10 (hitam pekat), jadikan abu abu

            gambar_kendaraan_gray[gambar_kendaraan_gray < 10] = 10
            # cv.imshow("frame 1", frame)

            frame_klasifikasi = frame.copy()
            gambar_kendaraan_gray_klasifikasi = gambar_kendaraan_gray.copy()
            klasifikasi, jumlah_mobil, jumlah_motor = self.klasifier.klasifikasi_kendaraan(
                gambar_kendaraan_gray_klasifikasi, frame_klasifikasi, lajur, frame_counter)
            # cv.imshow("frame 2", frame_klasifikasi)
            # print("menerima hasil klasifikasi di lajur %s dengan klasifikasi %s dengan jumlah motor %d dan jumlah mobil %d" % (
            #       lajur, klasifikasi, jumlah_motor, jumlah_mobil))

            gambar_kendaraan_klasifikasi = frame_klasifikasi[ya:yb, xa:xb]

            base_name = str(frame_counter)+"_" + str(uuid.uuid4())[:8]
            filename = base_name+("_%04d.png") % kendaraan.id
            filename_awal = base_name+("_%04d_awal.png") % kendaraan.id
            filename_resized_ori = base_name + \
                ("_%04d_resized_ori.png") % kendaraan.id
            filename_resized_gray = base_name + \
                ("_%04d_resized_gray.png") % kendaraan.id
            filename_klasifikasi = base_name + \
                ("_%04d_klasifikasi.png") % kendaraan.id
            filename_klasifikasi_gray = base_name + \
                ("_%04d_klasifikasi_gray.png") % kendaraan.id

            # gambar bounding box output klasifikasi, simpan

            # CEK KLASIFIKASI ~ END

            jumlah_motor_print = jumlah_motor
            jumlah_mobil_print = jumlah_mobil
            if(jumlah_motor_print):
                if(self.config['logs']['klasifikasi'][lajur][klasifikasi]):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+lajur+"/"+klasifikasi+"/logs.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')
                if(self.config['logs']['klasifikasi']['gabungan']):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+"/gabungan/logs_gabungan.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";" + \
                            str(int(jumlah_motor))+";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')

                while jumlah_motor_print:
                    if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename), gambar_kendaraan)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_awal), gambar_kendaraan_awal)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_resized_ori), gambar_kendaraan_gray_awal)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_resized_gray), gambar_kendaraan_gray)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_klasifikasi), gambar_kendaraan_klasifikasi)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_klasifikasi_gray), gambar_kendaraan_gray_klasifikasi)
                    jumlah_motor_print = jumlah_motor_print-1

            if(jumlah_mobil_print):
                if(self.config['logs']['klasifikasi'][lajur][klasifikasi]):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+lajur+"/"+klasifikasi+"/logs.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')
                if(self.config['logs']['klasifikasi']['gabungan']):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+"/gabungan/logs_gabungan.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";" + \
                            str(int(jumlah_mobil)) + \
                            ";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')

                while jumlah_mobil_print:
                    if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename), gambar_kendaraan)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_awal), gambar_kendaraan_awal)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_resized_ori), gambar_kendaraan_gray_awal)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_resized_gray), gambar_kendaraan_gray)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_klasifikasi), gambar_kendaraan_klasifikasi)
                        cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                    lajur + "/" + klasifikasi + "/" + filename_klasifikasi_gray), gambar_kendaraan_gray_klasifikasi)
                    jumlah_mobil_print = jumlah_mobil_print - 1

            if(not jumlah_motor and not jumlah_mobil):
                if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename), gambar_kendaraan)
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename_awal), gambar_kendaraan_awal)
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename_resized_ori), gambar_kendaraan_gray_awal)
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename_resized_gray), gambar_kendaraan_gray)
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename_klasifikasi), gambar_kendaraan_klasifikasi)
                    cv.imwrite((self.config['simpangambar_klasifikasi']['direktori'] +
                                lajur + "/" + klasifikasi + "/" + filename_klasifikasi_gray), gambar_kendaraan_gray_klasifikasi)

                if(self.config['logs']['klasifikasi'][lajur][klasifikasi]):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+lajur+"/"+klasifikasi+"/logs.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')
                if(self.config['logs']['klasifikasi']['gabungan']):
                    with open(self.config['logs']["direktori"]+self.config['logs']['klasifikasi']["direktori"]+"/gabungan/logs_gabungan.csv", 'a') as f:
                        ts = time.time()
                        teks = (("%04d") % frame_counter) + ";"
                        teks += str(int(ts))+";"+lajur+";" + \
                            klasifikasi + ";" + \
                            str(int(jumlah_mobil)+int(jumlah_motor))+";"+filename
                        if(self.config['simpangambar_klasifikasi'][lajur][klasifikasi]):
                            teks += ";simpan"
                        else:
                            teks += ";tidaksimpan"

                        f.write(teks)
                        f.write('\n')

            # tambahkan ke basis data
            self.pengelola_basisdata.simpan_ke_db(
                klasifikasi, lajur, jumlah_mobil, jumlah_motor)

            # hapus dari daftar
            del self.kendaraan_untuk_diklasifikasi[indek_kendaraan]

    def hitung_kendaraan(self, objek, frame, frame_counter, foreground):

        objek_sisa = self.cocokkan_dengan_data_yg_ada(objek, foreground)

        # print("frame_counter", frame_counter)

        self.tambahkan_ke_daftar_tracking(objek_sisa)

        self.handle_kendaraan_melewati_batas(frame, frame_counter, foreground)

        return self.kendaraan

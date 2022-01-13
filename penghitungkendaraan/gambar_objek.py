import cv2 as cv
import numpy as np

WARNA_GARIS_PEMBATAS_MASUK = (255, 255, 0)
WARNA_GARIS_PEMBATAS_KELUAR = (0, 255, 255)
WARNA_GARIS_PEMBATAS_TENGAH = (0, 0, 0)

WARNA_BOUNDING_BOX = (255, 0, 0)
WARNA_BOUNDING_BOX_HIJAU = (0, 255, 0)

WARNA_CENTROID = (0, 0, 255)
WARNA_GARIS = [(0, 0, 255), (0, 106, 255), (0, 216, 255), (0, 255, 182), (0, 255, 76),
               (144, 255, 0), (255, 255, 0), (255, 148, 0), (255, 0, 178), (220, 0, 255)]

RESIZE_LEBAR = 640
RESIZE_TINGGI = 360


GARIS_PEMBATAS_KIRI_MASUK = 240
GARIS_PEMBATAS_KIRI_KELUAR = 60

GARIS_PEMBATAS_KANAN_MASUK = 40
GARIS_PEMBATAS_KANAN_KELUAR = 120


class GambarObjek():
    def __init__(self, config):
        self.config = config
        self.lebar_frame = RESIZE_LEBAR
        self.tinggi_frame = RESIZE_TINGGI

    def gambar_box_n_centroid(self, frame, daftar_objek):
        ####
        # gambar objek terdeteksi dan centroid nya

        for (i, objek) in enumerate(daftar_objek):
            posisi, centroid, _ = objek
            x, y, w, h = posisi

            # gambar bounding box pada frame
            cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1),
                         WARNA_BOUNDING_BOX, 1)

            # gambar centroid pada frame
            cv.circle(frame, centroid, 2, WARNA_CENTROID, -1)

        return frame

    def gambar_garis_tracking(self, frame, daftar_kendaraan):
        ####
        # gambar kedaraan terdeteksi, centroid nya dan garis pergerakan kendaraan tersebut, dari penghitung kendaraan

        for (i, kendaraan) in enumerate(daftar_kendaraan):
            x, y, w, h = kendaraan.posisi
            warna = WARNA_GARIS[kendaraan.id % len(WARNA_GARIS)]

            # gambar bounding box pada frame
            cv.rectangle(frame, (x, y), (x + w - 1, y + h - 1),
                         WARNA_BOUNDING_BOX_HIJAU if kendaraan.telah_dihitung else WARNA_BOUNDING_BOX, 1)

            teks = 'id:{}\ncentroid:{}\nmuncul:{} frame'.format(

                kendaraan.id, kendaraan.centroid[-1], len(kendaraan.centroid))

            for i, baris in enumerate(teks.split('\n')):
                cv.putText(frame, baris, (x+5, y+10 + (10*i)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.3,
                           warna,
                           1)
            # gambar garis pergerakan
            for point in kendaraan.centroid:
                cv.circle(frame, point, 2, warna, -1)
                cv.polylines(frame, [np.int32(
                    kendaraan.centroid)], False, warna, 1)

            # gambar centroid pada frame
            cv.circle(frame, kendaraan.centroid[-1], 2, WARNA_CENTROID, -1)

        return frame

    def gambar_garis_batas(self, frame):
        ####
        # gambar garis pembatas kiri, kanan, dan tengah

        # kiri
        cv.line(frame, (0, GARIS_PEMBATAS_KIRI_MASUK), (int(self.lebar_frame/2), GARIS_PEMBATAS_KIRI_MASUK),
                WARNA_GARIS_PEMBATAS_MASUK, 1)
        cv.line(frame, (0, GARIS_PEMBATAS_KIRI_KELUAR), (int(self.lebar_frame/2), GARIS_PEMBATAS_KIRI_KELUAR),
                WARNA_GARIS_PEMBATAS_KELUAR, 1)

        # kanan
        cv.line(frame, (int(self.lebar_frame/2), GARIS_PEMBATAS_KANAN_MASUK), (int(self.lebar_frame), GARIS_PEMBATAS_KANAN_MASUK),
                WARNA_GARIS_PEMBATAS_MASUK, 1)
        cv.line(frame, (int(self.lebar_frame/2), GARIS_PEMBATAS_KANAN_KELUAR), (int(self.lebar_frame), GARIS_PEMBATAS_KANAN_KELUAR),
                WARNA_GARIS_PEMBATAS_KELUAR, 1)

        # tengah
        cv.line(frame, (int(self.lebar_frame/2), 0), (int(self.lebar_frame/2), self.tinggi_frame),
                WARNA_GARIS_PEMBATAS_TENGAH, 1)

        return frame


    def tampilkan_simpan_jalan(self, tipe, frame, frame_counter):
        if (self.config['cetakgambar'][tipe]):
            cv.imshow(tipe, frame)

        if (self.config['simpangambar'][tipe]):
            cv.imwrite((self.config['simpangambar']['direktori'] + tipe + "/%04d.png") % frame_counter, frame)


    def tampilkan_frame(self, frame, foreground, frame_counter, daftar_objek, daftar_kendaraan):
        # print(cv.utils.dumpInputArray(frame))

        self.tampilkan_simpan_jalan('asli',frame,frame_counter)

        frame_hasil = frame.copy()
        frame_hasil = self.gambar_garis_batas(frame_hasil)
        frame_hasil = self.gambar_box_n_centroid(frame_hasil, daftar_objek)
        frame_hasil = self.gambar_garis_tracking(frame_hasil, daftar_kendaraan)

        self.tampilkan_simpan_jalan('hasil',frame_hasil,frame_counter)
        self.tampilkan_simpan_jalan('morfologi',foreground,frame_counter)

        lebar = self.config['input']['dimensi']['lebar']
        tinggi = self.config['input']['dimensi']['tinggi']

        foreground_rgb = cv.cvtColor(foreground,cv.COLOR_GRAY2RGB)
        gabungan = cv.hconcat([frame,foreground_rgb,frame_hasil])

        self.tampilkan_simpan_jalan('gabungan',gabungan,frame_counter)

    @staticmethod
    def print_simpan_kendaraan(gbr_kendaraan, lajur, klasifikasi, jumlah):
        cv.imshow("kendaraan",gbr_kendaraan)
        # print(lajur)
        # print(klasifikasi)
        # print(jumlah)

        
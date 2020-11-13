
class Kendaraan(object):
    def __init__(self, id, centroid, posisi):
        self.id = id

        self.centroid = [centroid]
        self.tidak_terlihat = 0
        self.telah_dihitung = False
        self.posisi = posisi

        self.klasifikasi = ""
        self.sudah_klasifikasi = False

    @property
    def centroid_terakhir(self):
        return self.centroid[-1]

    def perbarui_centroid(self, centroid_terbaru):
        self.centroid.append(centroid_terbaru)
        self.tidak_terlihat = 0

    def perbarui_posisi(self, posisi_terbaru):
        self.posisi = posisi_terbaru
        self.tidak_terlihat = 0

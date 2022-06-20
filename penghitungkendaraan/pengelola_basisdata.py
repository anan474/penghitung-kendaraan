import sqlite3
import datetime
import time


class PengelolaBasisdata(object):
    def __init__(self):

        self.nama_db = 'trafikkendaraan.db'
        self.nama_tabel = 'trafik_kendaraan'

        self.sqliteConnection = sqlite3.connect(
            self.nama_db, check_same_thread=False)

    def _formatdatastat(self, records):
        pagiini = datetime.datetime.now()
        pagiini = pagiini.replace(hour=0, minute=0, second=1)

        hariini = datetime.datetime.now()
        timediff = hariini-pagiini

        hourdiff = timediff.total_seconds()/(60*60)

        data = {
            "requesttimestamp": hariini.timestamp(),
            "hariini": time.strftime("%d-%m-%Y"),
            "hariberjalan": hariini.hour < 17,
            "statkendperjam": {
                "masuk": {
                    "semua": 0,
                    "motor": 0,
                    "mobil": 0
                },
                "keluar": {
                    "semua": 0,
                    "motor": 0,
                    "mobil": 0
                }
            },
            "kiri": {
                "motor": 0,
                "mobil": 0,
                "tidakdiketahui": 0
            },
            "kanan": {
                "motor": 0,
                "mobil": 0,
                "tidakdiketahui": 0
            }
        }

        for (i, record) in enumerate(records):
            data[record[1]][record[0]] = record[2]

        data["statkendperjam"]["masuk"]["motor"] = data["kanan"]["motor"] / hourdiff
        data["statkendperjam"]["masuk"]["mobil"] = data["kanan"]["mobil"] / hourdiff
        data["statkendperjam"]["masuk"]["semua"] = (
            data["kanan"]["mobil"]+data["kanan"]["motor"]) / hourdiff
        data["statkendperjam"]["keluar"]["motor"] = data["kiri"]["motor"] / hourdiff
        data["statkendperjam"]["keluar"]["mobil"] = data["kiri"]["mobil"] / hourdiff
        data["statkendperjam"]["keluar"]["semua"] = (
            data["kiri"]["mobil"]+data["kiri"]["motor"]) / hourdiff

        return data

    def _formatdatalist(self, records):
        data = []

        for (i, record) in enumerate(records):
            data.append(
                dict(zip(("id", "klasifikasi", "lajur", "timestamp"), record)))

        return data

    def empty_table(self):
        try:
            cursor = self.sqliteConnection.cursor()
            query1 = """DROP TABLE trafik_kendaraan;"""
            cursor.execute(query1)
            self.sqliteConnection.commit()

            query2 = '''CREATE TABLE trafik_kendaraan (
                        id INTEGER PRIMARY KEY,
                        klasifikasi TEXT NOT NULL,
                        lajur TEXT NOT NULL,
                        waktu datetime);'''
            cursor.execute(query2)
            self.sqliteConnection.commit()

            cursor.close()

            return "done"

        except sqlite3.Error as error:
            print("gagal mengosongkan tabel:", error)

        return self

    def get_semua_data_by_tanggal(self, tanggal):
        try:
            cursor = self.sqliteConnection.cursor()

            tanggal = tanggal.split("-")
            hari = datetime.datetime(
                int(tanggal[2]), int(tanggal[1]), int(tanggal[0]))
            hari_plus = hari + datetime.timedelta(days=1)
            query = """SELECT 
                            * 
                        FROM 
                            trafik_kendaraan 
                        WHERE 
                            waktu 
                        BETWEEN 
                            ?
                        AND 
                            ?
                    ;"""

            params = (hari, hari_plus)
            print(params)
            cursor.execute(query, params)
            records = cursor.fetchall()
            data = self._formatdatalist(records)
            cursor.close()

            return data

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def get_semua_hari_ini(self):
        try:
            cursor = self.sqliteConnection.cursor()
            query = """SELECT 
                            * 
                        FROM 
                            trafik_kendaraan
                        WHERE
                            waktu
                        BETWEEN
                            datetime('now','start of day')
                        AND
                            datetime('now')
                    ;"""

            params = ()
            cursor.execute(query, params)
            records = cursor.fetchall()
            data = self._formatdatalist(records)

            cursor.close()

            return data

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def get_status_sekarang(self):
        try:
            cursor = self.sqliteConnection.cursor()

            query = """SELECT 
                            klasifikasi,
                            lajur, 
                            COUNT(*)
                        FROM 
                            trafik_kendaraan
                        WHERE
                            waktu
                        BETWEEN
                            datetime('now','start of day')
                        AND
                            datetime('now')
                        GROUP BY 
                            lajur,
                            klasifikasi
                    ;"""

            params = ()
            cursor.execute(query, params)
            records = cursor.fetchall()

            data = self._formatdatastat(records)
            cursor.close()

            return data

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def get_status_by_tanggal(self, tanggal):
        try:
            cursor = self.sqliteConnection.cursor()
            tanggal = tanggal.split("-")
            hari = datetime.datetime(
                int(tanggal[2]), int(tanggal[1]), int(tanggal[0]), hour=0, minute=0, second=1)
            hari_plus = datetime.datetime(
                int(tanggal[2]), int(tanggal[1]), int(tanggal[0]), hour=23, minute=59, second=59)
            query = """SELECT 
                            klasifikasi,
                            lajur, 
                            COUNT(*)
                        FROM 
                            trafik_kendaraan
                        WHERE 
                            waktu 
                        BETWEEN 
                            ?
                        AND 
                            ?
                        GROUP BY 
                            lajur,
                            klasifikasi
                    ;"""

            params = (hari, hari_plus)
            cursor.execute(query, params)
            records = cursor.fetchall()
            data = self._formatdatastat(records)
            del data["hariini"]
            del data["hariberjalan"]
            cursor.close()

            return data

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def jumlah_data(self):
        try:
            cursor = self.sqliteConnection.cursor()

            query = """SELECT 
                            COUNT(*) 
                        FROM 
                            trafik_kendaraan
                            ;"""
            params = ()
            cursor.execute(query, params)
            records = cursor.fetchall()

            cursor.close()

            return records

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def simpan_ke_db(self, klasifikasi, lajur, jumlah_mobil, jumlah_motor):
        try:
            # print("mau simpan kendaraan di lajur %s dengan klasifikasi %s dengan jumlah motor %d dan jumlah mobil %d" % (
            #       lajur, klasifikasi, jumlah_motor, jumlah_mobil))

            if(klasifikasi == "tidakdiketahui"):
                cursor = self.sqliteConnection.cursor()
                query = """INSERT INTO trafik_kendaraan (klasifikasi, lajur, waktu) VALUES (? ,?, datetime('now') );"""
                params = (klasifikasi, lajur)
                cursor.execute(query, params)
                self.sqliteConnection.commit()

                cursor.close()

            while jumlah_mobil:
                cursor = self.sqliteConnection.cursor()

                query = """INSERT INTO trafik_kendaraan (klasifikasi, lajur, waktu) VALUES (? ,?, datetime('now') );"""

                params = ("mobil", lajur)

                cursor.execute(query, params)
                self.sqliteConnection.commit()

                cursor.close()

                jumlah_mobil -= 1

            while jumlah_motor:
                cursor = self.sqliteConnection.cursor()

                query = """INSERT INTO trafik_kendaraan (klasifikasi, lajur, waktu) VALUES (? ,?, datetime('now') );"""

                params = ("motor", lajur)

                cursor.execute(query, params)
                self.sqliteConnection.commit()

                cursor.close()

                jumlah_motor -= 1

        except sqlite3.Error as error:
            print("Gagal menulis ke tabel:", error)
            return False

        return True

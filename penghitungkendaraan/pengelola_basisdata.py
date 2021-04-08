import sqlite3
import logging
from datetime import datetime, time, timedelta


class PengelolaBasisdata(object):
    def __init__(self):

        self.nama_db = 'trafikkendaraan.db'
        self.nama_tabel = 'trafik_kendaraan'

        self.sqliteConnection = sqlite3.connect(
            self.nama_db, check_same_thread=False)

    def get_semua_data_by_tanggal(self, tanggal):
        try:
            cursor = self.sqliteConnection.cursor()

            tanggal = tanggal.split("-")
            hari = datetime(int(tanggal[2]), int(tanggal[1]), int(tanggal[0]))
            hari_plus = hari + timedelta(days=1)
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

            cursor.close()

            return records

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
                        GROUP BY 
                            lajur,
                            klasifikasi
                    ;"""

            params = ()
            cursor.execute(query, params)
            records = cursor.fetchall()

            cursor.close()

            return records

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def get_status_by_tanggal(self, tanggal):
        try:
            cursor = self.sqliteConnection.cursor()
            tanggal = tanggal.split("-")
            hari = datetime(int(tanggal[2]), int(tanggal[1]), int(tanggal[0]))
            hari_plus = hari + timedelta(days=1)
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

            cursor.close()

            return records

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

    def simpan_ke_db(self, klasifikasi, lajur):
        try:
            waktu = datetime.now()

            cursor = self.sqliteConnection.cursor()

            query = """INSERT INTO trafik_kendaraan (klasifikasi, lajur, waktu) VALUES (? ,?, ? );"""

            params = (klasifikasi, lajur, waktu)

            cursor.execute(query, params)
            self.sqliteConnection.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Gagal menulis ke tabel:", error)
            return False

        return True

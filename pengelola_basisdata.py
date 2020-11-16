import sqlite3
import logging
import datetime


class PengelolaBasisdata(object):
    def __init__(self):

        self.nama_db = 'trafikkendaraan.db'
        self.nama_tabel = 'trafik_kendaraan'

        self.sqliteConnection = sqlite3.connect(
            self.nama_db, check_same_thread=False)

    def get_data_hari_ini(self):
        try:
            cursor = self.sqliteConnection.cursor()

            query = """SELECT * from trafik_kendaraan"""
            params = ()
            cursor.execute(query, params)
            records = cursor.fetchall()

            # print("Jumlah kendaraan:  ", len(records))
            # print("Data:")
            # for row in records:
            #     print("id: ", row[0])
            #     print("klasifikasi: ", row[1])
            #     print("lajur: ", row[2])
            #     print("waktu: ", row[3])
            #     print("\n")

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
            # print("Jumlah kendaraan:  ", len(records))
            # print("Data:")
            # for row in records:
            #     print("klasifikasi: ", row[0])
            #     print("lajur: ", row[1])
            #     print("jumlah: ", row[2])

            print(records[0])

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
            # print("Jumlah kendaraan:  ", len(records))
            # print("Data:")
            for row in records:
                print("jumlah: ", row[0])

            # print(records[0])

            cursor.close()

            return records

        except sqlite3.Error as error:
            print("gagal membaca tabel:", error)

        return self

    def simpan_ke_db(self, klasifikasi, lajur):
        try:
            waktu = datetime.datetime.now()

            cursor = self.sqliteConnection.cursor()

            query = """INSERT INTO trafik_kendaraan (klasifikasi, lajur, waktu) VALUES (? ,?, ? );"""

            params = (klasifikasi, lajur, waktu)
            # print(params)
            cursor.execute(query, params)
            self.sqliteConnection.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Gagal menulis ke tabel:", error)
            return False

        return True

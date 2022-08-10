import sqlite3
import logging
from datetime import datetime, time, timedelta
import os
import shutil
import glob

# delete folders
dirarr = [
    "./gambar_output/citra/asli",
    "./gambar_output/citra/elapsed",
    "./gambar_output/citra/hasil",
    "./gambar_output/citra/morfologi",
    "./gambar_output/citra/morfologi_detail",
    "./gambar_output/citra/morfologi_hasil",
    "./gambar_output/citra/morfologi_hasil_garis",
    "./gambar_output/citra/gabungan",
    "./gambar_output/klasifikasi/kiri/mobil",
    "./gambar_output/klasifikasi/kiri/motor",
    "./gambar_output/klasifikasi/kiri/keduanya",
    "./gambar_output/klasifikasi/kiri/tidakdiketahui",
    "./gambar_output/klasifikasi/kanan/mobil",
    "./gambar_output/klasifikasi/kanan/motor",
    "./gambar_output/klasifikasi/kanan/keduanya",
    "./gambar_output/klasifikasi/kanan/tidakdiketahui",
    "./logs/klasifikasi/gabungan",
    "./logs/klasifikasi/kiri/mobil",
    "./logs/klasifikasi/kiri/motor",
    "./logs/klasifikasi/kiri/keduanya",
    "./logs/klasifikasi/kiri/tidakdiketahui",
    "./logs/klasifikasi/kanan/mobil",
    "./logs/klasifikasi/kanan/motor",
    "./logs/klasifikasi/kanan/keduanya",
    "./logs/klasifikasi/kanan/tidakdiketahui",
    "./debug/kiri/mobil",
    "./debug/kiri/motor",
    "./debug/kiri/keduanya",
    "./debug/kiri/tidakdiketahui",
    "./debug/kanan/mobil",
    "./debug/kanan/motor",
    "./debug/kanan/keduanya",
    "./debug/kanan/tidakdiketahui",
]


class Utilitas():
    def __init__(self):

        self.nama_db = 'trafikkendaraan.db'
        self.nama_tabel = 'trafik_kendaraan'

        self.sqliteConnection = sqlite3.connect(
            self.nama_db, check_same_thread=False)

    def empty_output(self):
        print("menghapus output sebelumnya...\n")
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

            for dir in dirarr:
                for file in os.scandir(dir):
                    os.remove(file.path)

            return "done"

        except sqlite3.Error as error:
            print("gagal mengosongkan tabel:", error)

        return self

    def empty_output_content(self, resetdb=False):
        print("menghapus output sebelumnya...\n")
        try:
            if resetdb is True:
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

            for dir in dirarr:
                for file in os.scandir(dir):
                    files = glob.glob(file.path)
                    for f in files:
                        os.remove(f)

            return "done"

        except sqlite3.Error as error:
            print("gagal mengosongkan tabel:", error)

        return self

    def create_output_folders(self, resetdb=False):
        print("create output folders...\n")
        try:
            for dir in dirarr:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            if resetdb is True:
                sqliteConnection = sqlite3.connect('trafikkendaraan.db')
                sqlite_create_table_query = '''CREATE TABLE trafik_kendaraan (
                                            id INTEGER PRIMARY KEY,
                                            klasifikasi TEXT NOT NULL,
                                            lajur TEXT NOT NULL,
                                            waktu datetime);'''

                cursor = sqliteConnection.cursor()
                print("Berhasil terhubung ke SQLite")
                cursor.execute(sqlite_create_table_query)
                sqliteConnection.commit()
                print("Tabel berhasil dibuat")

                cursor.close()

            return "done"

        except:
            print("ada error create_output_folders")

        return self

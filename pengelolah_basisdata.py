import sqlite3
import logging
import datetime
class Storage(object):
    def __init__(self, nama_db):

        self.nama_db = nama_db
        self.nama_tabel = 'trafik_kendaraan'

        self.sqliteConnection = sqlite3.connect(nama_db)
  
    def get_data_hari_ini(self):
        try:
            cursor = self.sqliteConnection.cursor()

            query = """SELECT * from ?"""
            params = (self.nama_tabel,)
            cursor.execute(query, params)
            records = cursor.fetchall()
            print("Jumlah kendaraan:  ", len(records))
            print("Data:")
            for row in records:
                print("id: ", row[0])
                print("jenis: ", row[1]) 
                print("sebelah: ", row[2])
                print("waktu: ", row[3])
                print("\n")

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
 
        return self

    def simpan_ke_db(self, sebelah, jenis):
        try:
            waktu = datetime.datetime.now()

            cursor = self.sqliteConnection.cursor()

            query = """INSERT INTO ? ('jenis', 'sebelah', waktu)  VALUES (?, ?, ?);"""
            params = (self.nama_tabel, jenis, sebelah, waktu)
            cursor.execute(query, params)
            self.sqliteConnection.commit()
            
            print("data berhasil ditambahkan \n")

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return False

 
        return True

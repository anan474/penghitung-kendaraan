import sqlite3

try:
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

except sqlite3.Error as error:
    print("Gagal membuat tabel", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("Koneksi ke SQLite ditutup")

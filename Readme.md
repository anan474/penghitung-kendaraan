# Sistem perhitungan kendaraan

Bagian dari tugas akhir oleh Agung Tuah Ananda pada program studi Teknik Informatika Universitas Tanjungpura. Informasi lebih lengkap hubungi __anan474@myself.com__.

Tediri dari 3 branch:
- master : kode paling lengkap dan update, termasuk dengan logging dan cetak foto dan debug.
- clean : kode rapi tanpa ada logging dan lainnya, biar mudah di baca dan tulis ke dokumentasi.
- testing : kode dari branch clean, dengan kode untuk pengujian unit testing.

Requirement:

- opencv
- flask & flask-classful
- asyncio
- websockets
- pytest

cara install:
```python3 -m pip install flask flask-classful asyncio websockets pytest opencv-python```


cara menjalankan : 
masuk ke folder penghitung kendaraan, lalu jalankan ```python3 __main__.py```

Catatan: anda mesti install requirements di perangkat anda. perhatikan konfigurasi di ```config-dev.json```

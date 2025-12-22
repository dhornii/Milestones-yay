# Milestone 1, 22 Desember 2025
Bahas-bahas sensor jarak yang lebih optimal dari HC-SR04 dan aktuator Servo

## Pertanyaan Target Pencapaian Hari Ini
### `1. Ada pin apa saja di servo yang digunakan?`

Ground, Vin/VCC, dan pin input (penggerak servo).

### `2. Apa itu baudrate?, penggunaannya di program python gimana?`

Baudrate bisa dibilang **laju pertukaran informasi** dengan satuan **simbol per detik**. Digunakan
simbol karena ada konversi protokol informasi dari 
*Universal Asynchronous Receiver/Transmitter* (UART) milik mikrokontroler ke USB agar informasi bisa diterima oleh laptop.

Di program python, dipakai saat membuka Serial. Nilai baudrate harus sama dengan program di Arduino IDE agar komunikasi bisa sinkron dan informasi tersampaikan.

### `3. Gimana alur programnya?`

**1) Kode Arduino IDE**

Kode di sketch diupload dulu ke ESP32, di mana poin programnya adalah

- Siapkan objek servo serta pin `baris 3-4`
- Setup serial dengan baudrate 115200 dan attach pin untuk servo `baris 7-9`
- Cek pada setiap loopnya apakah ada informasi yang diupload ke serial `baris 13`
- Jika ada maka ambil infonya sebagai tipe integer lalu cek apakah nilai tersebut berada pada rentang 0 - 180, jika iya maka putar servo sesuai derajat yang diberikan `baris 14-18`
- Selanjutnya baca Serial (tanpa gunakan infonya) sampai habis jika ada informasi sisa, ini biar misal ada `\n` di kode nggak bakal diproses program `baris 20-22`

**2) Kode Python di VS Code**

Dijalankan setelah kode Arduino IDE selesai upload (matikan Serial Monitor jika nyala sebelumnya). Poin programnya adalah

- Buka Serial dengan port usb serta baud rate yang sama `baris 7`
- Buat fungsi untuk menerima masukan angka lalu dirubah ke string. String ini akan dikodekan melalui `.encode()` agar bisa menjadi simbol sebelum dikirimkan ke Serial milik mikrokontroler `baris 10-12`
- Loop terus sambil minta ke user buat nulis ke terminal mau putar sudut servo berapa derajat `baris 14-18`

  Tambahan informasi kalau kodenya adalah unicode serta kalau dibalik kiriman dari mikon ke program python itu bisa didecode pakai utf-8.

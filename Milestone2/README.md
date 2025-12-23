# Milestone 2, 23 Desember 2025
Bahas-bahas Python dan ROS2 sekalian sampe coba turtlesimnya ros2.

Hasil hari ini ada package python sama sudah buat virtual environtment.

## Pertanyaan Target Pencapaian Hari Ini
### `1. Apa Itu Virtual Environtment dan Kenapa Diperlukan Buat Package Python?`

Dalam konteks python, virtual environtment itu seperti satu paket khusus berisi *dependency* python yang memang didedikasikan buat satu proyek,
yang artinya juga versi dari module atau file package lainnya `khusus/konsisten di versi tertentu aja`.

Package python suatu proyek kalau *dependecies*-nya banyak atau rumit bisa aja `konflik` sama module lainnya (dari global) kalau tidak pakai virtual environtment,
bisa bikin program menimbulkan error misal jadi ada 2 module dengan versi beda atau sekedar ada format fungsi yang dipakai ternyata sudah *outdated*.

### `2. Jelaskan Fungsi Package Python?`

Sebagai tempat dikumpulkannya beberapa module yang khusus untuk sebuah proyek atau karena module-module tersebut memang saling berkaitan fungsinya. Dengan
adanya package, bisa ditata lebih rapi module-module yang digunakan serta fungsi buatan sendiri yang bisa diadopsi ke program lain atau
bisa juga buat mengeksekusi langsung sebuah program dari packagenya.

### `3. Apa Itu Node, Topic, dan Service di ROS2?`

**1) Node**

Individu yang bisa ikut berkomunikasi dalam sebuah jaringan ROS2 sebagai penerima data atau sebagai pemberinya. Bisa dari misal laptop berbeda atau program berbeda dalam satu laptop yang jalan bersamaan.

**2) Topic**

Salah satu tipe interaksi yang terjadi di jaringan ROS2 di mana dalam suatu topic ada nodes yang bertindak sebagai pemberi informasi sementara nodes lainnya bakal ngambil informasi
itu secara bebas. Jadi kayak ada yang setor informasi terus ke topic, terus informasi ini mau digunakan oleh node siapapun itu bebas tanpa batasan.

**3) Service**

Tipe lain yang bisa terjadi dalam komunikasi jaringan ROS2 di mana akan ada 2 node, satu bertindak sebagai pengirim dan satunya sebagai klien. Klien akan minta (*request*) informasi tertentu dan akan
menunggu respon dari pihak satunya di service tersebut. Bisa kayak request hasil programnya misal ada input tertentu, nah nanti akan dikirimkan outputnya ke klien tersebut.

### `4. Kenapa ROS2, Apa Keunggulannya?`

Dengan pakai *framework* dari ROS2 ini, sekumpulan program yang saling bergantung datanya bisa **`diintegrasikan serta berjalan bersamaan`**. Kalau beberapa program misal kayak pengambil data lewat sensor, pengolah 
data tersebut, terus fungsi buat ngasih respon semuanya berada di satu program sama itu akal dieksekusi secara sekuensial (urut), hasilnya adalah robot bisa jadi kurang responsif pada pengambilan keputusan
geraknya maupun pengolahan datanya.

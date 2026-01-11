# Milestone 9, 7-9 Januari 2026

Simulasi gerakin kakinya loky yang total sendinya ada 18. Langkah yang udah dicoba selama hari-hari tersebut:
## `Publish dengan ros2_control`
Sama kayak pas `Bézier Curve` di mana gerakan sudutnya dipublish ke **`/joint_trajectory_controller/joint_trajectory`**.
### Hasil
- Gerakan `Bézier Curve` bisa dilakukan, tapi hasilnya kayak rotasi terhadap pusat `base_link` loky, jadinya bukan
  gerakan lurus ada menyamping, cuman gerakan untuk memutar badan saja. Selain itu, penentuan titik tujuan untuk menggerakkan loky dengan
  sudut pandang `base_link` juga belum bisa.

## `Forward Kinematic`
Yap, FK lagi buat kaki loky yang spesial ini. Mirip banget dengan FK buat program sebelumnya yang `leg.urdf`. Fungsi Fk yang baru ada di bagian
program python berisi fungsi FK buat **`py_pubsub`**
### Hasil
- Hasil perhitungan benar semua untuk seluruh kaki, selain itu logika + urutan komputasinya sudah jelas. Yang dimanfaatkan
  untuk perhitungan adalah matriks transformasi homogeneous `(berisi rotasi sumbu yang ditentukan + bisa translasi sekalian jika perlu)`.
- Catatan aja buat pelajari ulang transformasi ruang 3 dimensi lagi jika diperlukan. 3Blue1Brown mungkin membantu.

## `Inverse Kinematic`
Lanjutan dari FK, IK dilakukan dengan perkalian matriks inverse dulu buat eliminasi istilahnya 'relativitas' setiap kaki terhadap
`base_link`. Jadi perhitungannya bisa dilakukan dengan perspektif kita adalah masing-masing *coxa* kaki yang mau dikalkulasi IK-nya
### Hasil
- Perhitungan bisa baru buat `satu kaki`, jadi kedepannya harus bisa hitung juga buat keenam kaki bersamaan terlepas dari sudut inputnya yang beda
  semua. Masih memanfaatkan translasi serta rotasi dari *`homogeneous transformation matrix`*. Yang menarik di bagian ini adalah kita awalnya cuma
  masukin rotasi `0 radian` buat *coxa* dalam rumus, tapi akhirnya bisa dapet juga nilai rotasi coxanya berapa buat mencapai titik tersebut.
- *Keep in mind* kalau seperti program IK untuk `leg.urdf` sebelumnya, input sudut yang agak 'meledak' atau 'ngawur' juga bakal hasilin
  perhitungan yang tidak sesuai sama simulasi `RViz`. Mungkin butuh dikembangkan dengan penerapan logika if-else di beberapa bagian fungsi IK.

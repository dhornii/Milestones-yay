# Milestone 3, 25 Desember 2025
Bahas-bahas Python dan ROS2 sampe ke cobain servo `Dynamixel` dan simulasi visual robot pakai `Vriz`.

Dynamixel disimulasikan lewat `Dynamixel Wizard 2.0` (software open source), simulasi robot dengan package `Arm_Kinematics` di repo ini.

## Pertanyaan Target Pencapaian Hari Ini
### `1. Apa itu servo Dynamixel?`

Servo dengan protokol komunikasi `RS-485` serta arsitektur lebih canggih dari servo biasa yang pernah digunakan (referensi milestone 1), di mana kondisi gerakan yang dihasilkan dapat
diatur langsung dari komputer lewat software *dedicated*-nya yang artinya pasti bisa diintegrasi dengan program Python juga.

### `2. Selain itu apa lagi yang membedakan servo dynamixel ini dengan servo biasa?`

Selain bisa diatur manual lewat software, opsi buat inputnya juga macem-macem. Ada dari posisi sudutnya mau berapa derajat dari kondisi *rest* `(goal position mode)`, mode mutar dengan
aturan kecepatan berapa *revolution per second* `(velocity mode)`, dan mode putaran tapi berdasarkan *Pulse Width Modulation* (PWM) `(PWM mode)`. Satu hal lagi yang membedakan dari servo biasa
adalah kebutuhan komponen tambahan berupa `U2D2` sebelum bisa digunakan bersama komputer.

### `3. Apa fungsinya U2D2?`

Komponen kecil itu berguna untuk konversi komunikasi USB ke protokol komunikasi lainnya yang digunakan komponen dynamixel, kalau kasus ini adalah ke RS-485. Tanpa adanya U2D2, dynamixel nggak
bisa nerima input dari komputer sehingga software juga meskipun mungkin nge-*detect* servonya pun ndak bakal bisa digerakkan.

---

### `4. Jelaskan apa itu URDF?`

*Unified Robotic Description Format* (URDF) bisa dibilang merupakan salah satu program ros2 berbasis XML yang berkontribusi sebagai penyedia sebuah tampilan visual model robot.
Hal keren lainnya juga meliputi sifat `kolisi` antar komponen yang bisa diaktifkan dan juga simulasi `kinematik` yang bisa dijalankan pada simulasi tersebut.

### `5. Package apa aja yang diperlukan untuk memvisualisasikan URDF di RViz2?`

- 1. RViz2 : Package utama tempat window simulasi
- 2. Joint State Publisher : Memublikasikan model robot bagian joint
- 3. Robot State Publisher : Memublikasikan model komponen robot
- 4. URDF : Membaca file urdf yang berisi komponen robot dan sebagainya yang akan tampil di simulasi
- 5. xacro : Membantu simulasi kinematik atau sekedar tampilan RViz

### `6. Selain RViz, URDF bisa digunakan untuk simulasi lewat sofware apa lagi?`

Contoh lainnya yang mungkin adalah program:
- Pybullet
- Gazebo (agak berat *requirement* spesifikasi komputernya kalau buat satu ini)

## Dokumentasi Singkat Hari Ini 
![Documentasi Singkat Hasil](Docum.png)

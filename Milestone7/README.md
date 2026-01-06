# Milestone 7, 31 Desember 2025 - 2 Januari 2026

## `1) urdf raw to xacro`
Edit file urdf jadi `xacro-macro` biar bisa digabung sama `ros2_control`, jadinya ekstensi file di **urdf/** jadi .xacro semua belakangnya. Ros2_control dipakai
buat gerakin robotnya, secara simulasi ataupun komponen real.

Baca-baca lagi mengenai penggunaan [xacro](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html) di ros2 tutorial:
- Bisa buat operasi `matematis/numerik`
- Deklarasi dan penggunaan `variabel`
- Integrasi file `description.urdf` (komponen simulasi) dengan file `ros2_control.xacro` yang bersifat seperti plugin

### Mock Components di file `leg.ros2_control.xacro` bisa dibilang kayak komponen palsu buat simulasi aja.

## `2) Package baru; arm_bringup`
### 1. controller.yaml 
Berisi semua node yang diperlukan ros2_control serta ada *`ros__parameters`*-nya masing-masing
### 2. leg.rviz
Pengaturan buat window rviz-nya, bisa didapat dari `save-as` habis buka simulasi rviz. Info yang dituliskan di file ini cuma bagian penting
dari file `save_rviz.rviz` hasil `save-as` tadi karena emang yang bakal muncul itu banyak banget tetapan parameternya walaupun cuma dari 1 simulasi rviz aja.
### 3. setup.py
Sangat-sangat mirip kayak setup.py di sebelumnya, cuma butuh ditambahin `os` dan `glob` lagi seperti di package `arm_kinematic`
### 4. bringup.ros2_control.launch.py
Program akan subscribe ke topic `/joint_trajectory_controller/joint_trajectory` buat dapat informasi deskripsi gerakannya gimana. Buat lihat informasi apa aja yang
dibutuhkan buat publish suatu gerakan ke topic itu, bisa dengan launch dulu rviznya lewat `bringup.ros2_control.launch.py`.
- Buka terminal baru
- `ros2 topic list`
- Harusnya ada `/joint_trajectory_controller/joint_trajectory`
- `ros2 topic info /joint_trajectory_controller/joint_trajectory`, harusnya di sini subscribernya ada 1 dengan 0 publisher
- `ros2 interface show trajectory_msgs/msg/JointTrajectory` buat lihat apa aja yang dibutuhkan sama publisher info gerakan joints
- ada juga `trajectory_msgs/msg/JointTrajectoryPoint` buat nentuin gerakan (FK) dengan masukan putaran radian
Selanjutnya ada package buat ngirim informasi gerakan dengan memanfaatkan JointTrajectory + JointTrajectoryPoint

## `3) leg_point_pub`
Bikin `entry_point` dulu di setup terus sisanya fokus aja ke bagian `point_publisher.py` di dalam directory `leg_point_pub`.

Program publisher point (FK) di bagian `point_publisher.py` sudah dijelaskan pada kode dengan comments :D

# Milestone 6, 30 Desember 2025
Bikin file urdf baru buat check rechek hasil hitung-hitung FK IK `Arm_Kinematics` yang ada di bagian ini sudah update dari milestone sebelumnya. Bagian
urdf udah ada tambahan `leg.urdf`, perwakilan anatomi salah satu kaki yang akan digerakkan + coba (lagi) IK dengan program python baru.

Program pythonnya ada di bagian `py_pubsub` lagi, dengan catatan hadirnya fungsi `IK_3dofspec` (IK 3 dof special case) di file `FK_for_RViz2.py` yang khusus 
digunakan untuk kasus simulasi `leg.urdf`.

### Buat referensi IK bentuk lainnya ada di milestone sebelumnya

## Sekilas hasil coba program spesial IK :
![sekilas hasil nyoba IK](docum_6.png)

# Milestone 8, 5 Januari 2026

## `1) Bézier Curve`
Buat fungsi untuk membentuk sampel path dari `Bézier Curve`, path hasil interpolasi linear berbagai titik yang disebut titik `anchor` untuk **awal-akhir** serta 
`control` untuk pembentuk **lengkungan path-nya**. Kurva ini berguna untuk trajectory gerak kaki robot agar hasilnya mulus sekaligus efektif untuk perpindahan posisi.

Referensi belajar `Bézier Curve`: 
- `Youtube` --- [The Beauty of Bézier Curves ](https://www.youtube.com/watch?v=aVwxzDHniEw) by **Freya Holmér**
- `Youtube` --- [How Computers Draw Curves - Bézier Curves Explained](https://www.youtube.com/watch?v=ABBknLY1L4o) by **Alex K.**
- `Youtube` --- [Bezier Curves Explained ](https://www.youtube.com/watch?v=pnYccz1Ha34) by **Guidev**
- `pdf paper` --- [A new approach based on Bezier curves to solve path planning problems for mobile robots](https://www.sciencedirect.com/science/article/pii/S1877750321001988) **(Duraklı & Nabiyev, 2022)**
- `wiki` --- [Bézier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)

## `2) Penerapan ke arm_bringup`
Seperti pada milestone sebelumnya, prosedur program untuk menggerakkan simulasi rviz dari `arm_bringup` adalah program harus mengirim sudut gerakan ke topic `/joint_trajectory_controller/joint_trajectory`
melalui publish. Nah di sini bisa sekalian dilakukan `inverse kinematic` untuk setiap titik sampel hasil `Bézier Curve` sehingga `end_effector` kakinya bisa melewati semua titik tersebut, menghasilkan
gerakan mulus.

Di repo ini, package `leg_point_pub` sudah dimodifikasi untuk merealisasikan gerakan sepanjang `Bézier Curve`. Operasi *throughout* kodenya dilakukan melalui perhitungan vektor karena melibatkan
3 titik di setiap kalkulasinya `[x,y,z]` meskipun rumus yang sama cuma diulang-ulang.

### kata kunci milestone kali ini:
#### > linear interpolation (lerp)
#### > numpy (matrix, array)
#### > IK
#### > waktu (per gerakan)

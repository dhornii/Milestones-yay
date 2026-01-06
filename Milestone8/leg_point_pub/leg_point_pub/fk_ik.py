import numpy as np              #Untuk perhitungan matriks

# Kode mulai

# ========================================================
# Matriks dan Fungsi untuk Forward Kinematics
# ==2 DoF bidang X-Y==""
def FK_2dof(l1, l2, theta1, theta2):
    theta1 = theta1+np.deg2rad(90)

    # R untuk rotasi dan P untuk point di sepanjang sumbu x
    R1 = np.array([ # Array R1 atau rotasi pertama yang akan merotasikan l1
        [np.cos(theta1), -np.sin(theta1), 0],
        [np.sin(theta1), np.cos(theta1), 0],
        [0, 0, 1]
    ])
    P1 = np.array([ # Array P1 berupa panjang lengan atas (yang akan sambung dengan origin)
        [1, 0, l1],
        [0, 1, 0],
        [0, 0, 1]
    ])
    P1 = np.matrix(P1) # Bentuk array R1 dan P1 dirubah ke matriks
    R1 = np.matrix(R1) 

    """Pengubahan ke matriks dilakukan pada baris ini soalnya butuh 
    menjalankan fungsi np.sin dan np.cos, di mana selama saya coding,
    tidak bisa dipanggil jika langsung membentuk dengan np.matrix([])"""
    
    # Pembentukan matriks seperti pada rotasi pertama dan panjang lengan atas (l1)
    R2 = np.array([
        [np.cos(theta2), -np.sin(theta2), 0],
        [np.sin(theta2), np.cos(theta2), 0],
        [0, 0, 1]
    ])
    P2 = np.array([
        [1, 0, l2],
        [0, 1, 0],
        [0, 0, 1]
    ])
    R2 = np.matrix(R2)
    P2 = np.matrix(P2)

    # Hasil rotasi berupa perkalian matriks dengan urutan R1*P1*R2*P2
    # Untuk lebih jelas pada hasilnya terdapat di foto kertas pengerjaan rumus

    hasil = (R1*P1) * (R2*P2)
    return hasil

# ==3 DoF bidang X-Y==
def FK_3dof(l1, l2, l3, theta1, theta2, theta3):
    # Memanggil fungsi sebelumnya untuk menghitung matriks transformasi l1 dengan l2 = T1
    T1 = FK_2dof(l1, l2, theta1, theta2)

    """Konsep perhitungan sama seperti DoF berjumlah 2 karena semua sendi 
    pada kasus ini adalah engsel (2 arah saja) sehingga bagian ke-3 bisa
    dianggap perhitungan 2 DoF antara lengan 2 dengan lengan 3. Hasilnya 
    adalah perhitungan matriks yang mirip, bertambah di bagian akhir saja"""

    theta3 = theta3
    R2 = np.array([
        [np.cos(theta3), -np.sin(theta3), 0],
        [np.sin(theta3), np.cos(theta3), 0],
        [0,0,1]
    ])
    P2 = np.array([
        [1,0,l3],
        [0,1,0],
        [0,0,1]
    ])
    P2 = np.matrix(P2)
    R2 = np.matrix(R2)

    # Perhitungan matrix bertambah sehingga bentuknya menjadi R1*P1*R2*P2*R3*P3 jika dijabarkan
    hasil = T1*(R2*P2)
    return hasil

# ========================================================
# Fungsi untuk Inverse Kinematics
# ==2 DoF bidang X-Y==
def IK_2dof(l1,l2,x,y):
    # Karena bagian sudut dari cos inverse pada kedua rumus (di kertas pengerjaan) didapat sama, yaitu:
    sudut_arccos = (x*x + y*y - l1*l1 - l2*l2)/(2*l1*l2)

    # Misal hasil absolutnya di luar 1, artinya tidak dapat terjangkau fungsi trigonometri, 
    # sehingga pasti titik target di luar jangkauan lengan
    if(abs(sudut_arccos) > 1):
        raise ValueError("Titik berada di luar jangkauan robot, tolong input ulang titik tujuan")

    """Terdapat 2 kasus untuk membentuk pertambahan 2 vektor agar mencapai titik yang sama,
    aturan tersebut disebut paralellogram rule atau aturan jajar genjang (jika pernah dengar)"""

    # Untuk kasus lower-elbow, saat lengan 1 menjadi sisi bawah jajar genjang lalu lengan 2 menunjuk titik target
    theta2_lower = np.arccos(sudut_arccos)
    theta1_lower = np.arctan2(y,x) - np.arctan2(l2*np.sin(theta2_lower), l1 + l2*np.cos(theta2_lower))

    # Untuk kasus upper-elbow, saat lengan 2 menjadi sisi kiri jajar genjang lalu lengan 2 menunjuk titik target
    # Perlu diperhatikan di sini sudut dari sin negatif karena lengan 2 harus berputar ke kanan (clockwise) untuk menunjuk titik target
    theta2_upper = -np.arccos(sudut_arccos) 
    theta1_upper = np.arctan2(y,x) - np.arctan2(l2*np.sin(theta2_upper), l1 + l2*np.cos(theta2_upper))

    hasil = np.array([
        [theta1_lower, theta1_upper],
        [theta2_lower, theta2_upper]
    ])
    return hasil

# == khusus buat Rviz arm.urdf == versi lama pas pakai arm.urdf di arm_kinematic ==
# def IK_3dofspec(l1, l2, l3, x_target, y_target, z_target):

#     # sudut bagian coxa
#     z_translated = z_target - 0.9
#     theta_c = -np.arctan2(y_target, z_translated)

#     # sudut bagian femur
#     x_0 = np.sqrt(z_translated**2 + y_target**2)
#     theta_f1 = np.arctan2(x_target, x_0 - l1)

#     a_length = np.sqrt((x_0 - l1)**2 + x_target**2)
#     arccos_in = (l2**2 + a_length**2 - l3**2) / (2 * a_length * l2)
#     theta_f2 = np.arccos(arccos_in)
#     theta_f = -(theta_f1 + theta_f2)

#     # sudut bagian tibia
#     arccos_in_t =  (l2**2 + l3**2 - a_length**2) / (2 * l2 * l3) 
#     theta_t = -(np.arccos(arccos_in_t) - np.deg2rad(180))

#     hasil = np.array(
#         [theta_c, theta_f, theta_t] # coxa, femur, tibia
#         )
    
#     return hasil

# versi baru buat coba gerakkan satu kaki dari file leg.urdf arm_kinematic
def IK_3dofspec(l1, l2, l3, x_target, y_target, z_target):

    # sudut bagian coxa
    z_translated = z_target + 0.45
    theta_c = np.arctan2(y_target, x_target)

    # sudut bagian femur
    x_0 = np.sqrt(x_target**2 + y_target**2)
    theta_f1 = np.arctan2(z_translated, x_0 - l1)

    a_length = np.sqrt((x_0 - l1)**2 + z_translated**2)
    arccos_in = (l2**2 + a_length**2 - l3**2) / (2 * a_length * l2)
    theta_f2 = np.arccos(arccos_in)
    theta_f = (theta_f1 + theta_f2)

    # sudut bagian tibia
    arccos_in_t =  (l2**2 + l3**2 - a_length**2) / (2 * l2 * l3) 
    theta_t = (np.arccos(arccos_in_t) - np.deg2rad(90))

    hasil = np.array(
        [theta_c, theta_f, theta_t] # coxa, femur, tibia
        )
    
    return hasil


# Kode selesai
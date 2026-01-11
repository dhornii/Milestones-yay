"""
Gerak satu arah aja sesuai bezier curvenya. Belum ada perhitungan perpindahan terhadap
'base_link' dan setiap sendi bergerak dengan magnitude sudut sama besar, belum ditentukan
arah gerak yang bisa itu ke arah sumbu apa aja.
"""

import rclpy
from builtin_interfaces.msg import Duration
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import numpy as np
from leg_point_pub.bezier_func import cubic_bezier
from leg_point_pub.fk_ik import IK_3dofspec

class Movement_Pub(Node):

    def __init__(self):
        super().__init__('movement_publisher')

        # panjang parts
        self.l1 = 0.025
        self.l2 = 0.055
        self.l3 = 0.071429

        # jumlah titik bezier curve yang akan jadi target gerakan
        self.sample_t = np.linspace(0, 1, 30)

        # seberapa jauh gerakan target masing-masing sumbu
        self.sumbu_x = 0.01
        self.sumbu_y = 0.00
        self.sumbu_z = 0.00

        # posisi end_effector tes dan translasi
        self.cur_x = 0
        self.cur_y = 0.1666603
        self.cur_z = -0.047929 - 0.08694 # sekarang harusnya coxa sudah sejajar Z-nya dengan base link
        
        # rotasi terhadap sumbu z agar kaki di sepanjang sumbu x
        self.rot_x = np.cos( (3 / 6) * np.pi) * self.cur_x + np.sin( (3 / 6) * np.pi) * self.cur_y - 0.08663
        self.rot_y = -np.sin( (3 / 6) * np.pi) * self.cur_x + np.cos( (3 / 6) * np.pi) * self.cur_y

        # publish ke /joint_trajectory_controller/joint_trajectory
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        # tunggu 1 detik baru baru jalankan send_point
        self.timer = self.create_timer(1, self.send_point)

    def send_point(self):
        # cancel timer biar jalan sekali aja (tanpa ngirim ulang tiap beberapa detik)
        self.timer.cancel()

        # titik awal, akhir, dan control pergerakan [x,y,z]
        # self.start = np.array([self.rot_x - self.sumbu_y, -0.05 - self.sumbu_x, self.cur_z])
        # self.ctrl1 = np.array([self.rot_x - self.sumbu_y, -0.025 - self.sumbu_x, self.cur_z + self.sumbu_z + 0.05])
        # self.ctrl2 = np.array([self.rot_x + self.sumbu_y, 0.025 + self.sumbu_x, self.cur_z + self.sumbu_z + 0.05])
        # self.end   = np.array([self.rot_x + self.sumbu_y, 0.05 + self.sumbu_x, self.cur_z])

        self.start = np.array([0.08, 0.04, -0.1])
        self.ctrl1 = np.array([0.08, 0.02, -0.055])
        self.ctrl2 = np.array([0.08, -0.02, -0.055])
        self.end = np.array([0.08, -0.04, -0.1])

        self.sample_t = self.sample_t.reshape((-1, 1)) # parameter (-1): jumlah baris langsung menyesuaikan agar terbentuk vector sementara jumlah kolom adalah 1

        # bikin JointTrajectory buat nyatakan sendi yang digerakkan, namanya harus persis di file urdf atau urdf.xacro
        message = JointTrajectory()
        message.joint_names = [
            'leg1_coxa_joint', 'leg1_femur_joint', 'leg1_tibia_joint',
            'leg2_coxa_joint', 'leg2_femur_joint', 'leg2_tibia_joint',
            'leg3_coxa_joint', 'leg3_femur_joint', 'leg3_tibia_joint',
            'leg4_coxa_joint', 'leg4_femur_joint', 'leg4_tibia_joint',
            'leg5_coxa_joint', 'leg5_femur_joint', 'leg5_tibia_joint',
            'leg6_coxa_joint', 'leg6_femur_joint', 'leg6_tibia_joint'
            ]
        message.header.stamp = self.get_clock().now().to_msg()

        # membentuk kumpulan titik-titik [x,y,z] dalam sebuah array
        trajectory_points = [cubic_bezier(self.start, self.end, self.ctrl1, self.ctrl2, time) for time in self.sample_t]

        # dibuat menjadi matrix agar komponennya lebih mudah direferensi (dipakai dalam perhitungan)
        traject_matrix = np.matrix(trajectory_points)

        # total waktu seluruh pergerakan dan jeda setiap sub-pergerakan agar gerakan mulus
        total_time = 3
        time_increment = (total_time-1) / len(trajectory_points)

        last1 = 0.0
        last2 = 0.0
        last3 = 0.0

        for t in range(traject_matrix.shape[0]):          

            ik_result = IK_3dofspec( # hitung IK dari titik yang direferensi saat ini dari sampel hasil bezier curve
                self.l1, 
                self.l2, 
                self.l3, 
                traject_matrix[t,0], 
                traject_matrix[t,1], 
                traject_matrix[t,2])
            
            movement = JointTrajectoryPoint() # bikin JointTrajectoryPoint
            movement.positions = [
                0.0, 0.0, 0.0,
                float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                0.0, 0.0, 0.0,
                -float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                0.0, 0.0, 0.0,
                -float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                ]    # dalam radian, gerakan setiap sendinya (sesuai urutan joint_names)
            
            # time_from_start hanya menerima parameter waktu ---> sec: int32 ; nanosec: uint32 
            new_time = (t+1) * time_increment
            new_sec = int(new_time)
            new_nanosec = int((new_time - new_sec) * 10**9)

            last1 = float(ik_result[0])
            last2 = float(ik_result[1])
            last3 = float(ik_result[2])

            movement.time_from_start = Duration(sec = new_sec + 1, nanosec = new_nanosec)           # durasi gerakan (diset ke 2 detik)
            message.points.append(movement)                                                         # append ke JointTrajectory buat dipublish

        # publish ke topic
        self.publisher_.publish(message)

        for t in range(traject_matrix.shape[0]):          

            ik_result = IK_3dofspec(
                self.l1, 
                self.l2, 
                self.l3, 
                traject_matrix[t,0], 
                traject_matrix[t,1], 
                traject_matrix[t,2])
            
            movement = JointTrajectoryPoint()                                                     
            movement.positions = [
                float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                last1, last2, last3,
                -float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                -last1, last2, last3,
                -float(ik_result[0]), float(ik_result[1]), float(ik_result[2]),
                -last1, last2, last3,
                ]  
            
            new_time = (t+1) * time_increment 
            new_sec = int(new_time)
            new_nanosec = int((new_time - new_sec) * 10**9)

            movement.time_from_start = Duration(sec = new_sec + 4, nanosec = new_nanosec)          
            message.points.append(movement)                                                        

        # publish ke topic
        self.publisher_.publish(message)

def main(args=None):
    rclpy.init(args=args)
    movement_publisher = Movement_Pub()

    rclpy.spin(movement_publisher)

    movement_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
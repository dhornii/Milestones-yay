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
        self.l1 = 0.25
        self.l2 = 0.55
        self.l3 = 0.7149

        # jumlah titik bezier curve yang akan jadi target gerakan
        self.sample_t = np.linspace(0, 1, 20)

        # titik awal, akhir, dan control pergerakan [x,y,z]
        self.start = np.array([0.8, -0.4, -1])
        self.ctrl1 = np.array([0.8, -0.2, -0.55])
        self.ctrl2 = np.array([0.8, 0.2, -0.55])
        self.end = np.array([0.8, 0.4, -1])

        # publish ke /joint_trajectory_controller/joint_trajectory
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        # tunggu 1 detik baru baru jalankan send_point
        self.timer = self.create_timer(1, self.send_point)

    def send_point(self):
        # cancel timer biar jalan sekali aja (tanpa ngirim ulang tiap beberapa detik)
        self.timer.cancel()

        self.sample_t = self.sample_t.reshape((-1, 1)) # parameter (-1): jumlah baris langsung menyesuaikan agar terbentuk vector sementara jumlah kolom adalah 1

        # membentuk kumpulan titik-titik [x,y,z] dalam sebuah array
        trajectory_points = [cubic_bezier(self.start, self.end, self.ctrl1, self.ctrl2, time) for time in self.sample_t]

        # dibuat menjadi matrix agar komponennya lebih mudah direferensi (dipakai dalam perhitungan)
        traject_matrix = np.matrix(trajectory_points)

        # bikin JointTrajectory buat nyatakan sendi yang digerakkan, namanya harus persis di file urdf atau urdf.xacro
        message = JointTrajectory()
        message.joint_names = ['Base_Coxa', 'Coxa_Femur', 'Femur_Tibia']
        message.header.stamp = self.get_clock().now().to_msg()

        # total waktu seluruh pergerakan dan jeda setiap sub-pergerakan agar gerakan mulus
        total_time = 3
        time_increment = (total_time-1) / len(trajectory_points)

        for t in range(traject_matrix.shape[0]):          

            ik_result = IK_3dofspec( # hitung IK dari titik yang direferensi saat ini dari sampel hasil bezier curve
                self.l1, 
                self.l2, 
                self.l3, 
                traject_matrix[t,0], 
                traject_matrix[t,1], 
                traject_matrix[t,2])
            
            movement = JointTrajectoryPoint()                                                       # bikin JointTrajectoryPoint
            movement.positions = [float(ik_result[0]), float(ik_result[1]), float(ik_result[2])]    # dalam radian, gerakan setiap sendinya (sesuai urutan joint_names)
            
            # time_from_start hanya menerima parameter waktu ---> sec: int32 ; nanosec: uint32 
            new_time = (t+1) * time_increment
            new_sec = int(new_time)
            new_nanosec = int((new_time - new_sec) * 10**9)

            movement.time_from_start = Duration(sec = new_sec + 1, nanosec = new_nanosec)               # durasi gerakan (diset ke 2 detik)
            message.points.append(movement)                                                         # append ke JointTrajectory buat dipublish

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
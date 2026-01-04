import rclpy
from builtin_interfaces.msg import Duration
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class Point_Pub(Node):

    def __init__(self):
        super().__init__('point_publisher')

        # publish ke /joint_trajectory_controller/joint_trajectory
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        # tunggu 1.5 detik baru baru jalankan send_point
        self.timer = self.create_timer(1.5, self.send_point)

    def send_point(self):
        # cancel timer biar jalan sekali aja (tanpa ngirim ulang tiap beberapa detik)
        self.timer.cancel()

        # bikin JointTrajectory buat nyatakan sendi yang digerakkan, namanya harus persis di file urdf atau urdf.xacro
        point_message = JointTrajectory()
        point_message.joint_names = ['Base_Coxa', 'Coxa_Femur', 'Femur_Tibia']
        point_message.header.stamp = self.get_clock().now().to_msg()

        # ==== bagian ini dan seterusnya sampe point3 berfungsi sama: ====

        point1 = JointTrajectoryPoint()                         # bikin JointTrajectoryPoint
        point1.positions = [0.0, -0.8, 1.5]                     # dalam radian, gerakan setiap sendinya (sesuai urutan joint_names)
        point1.time_from_start = Duration(sec = 2, nanosec = 0) # durasi gerakan (diset ke 2 detik)
        point_message.points.append(point1)                     # append ke JointTrajectory buat dipublish

        point2 = JointTrajectoryPoint()
        point2.positions = [0.8, 0.3, -0.4]
        point2.time_from_start = Duration(sec = 5, nanosec = 0)
        point_message.points.append(point2)

        point3 = JointTrajectoryPoint()
        point3.positions = [-1.3, -0.5, 1.4]
        point3.time_from_start = Duration(sec = 6, nanosec = 0)
        point_message.points.append(point3)

        # sebagai catatan di sini setiap duration gaboleh start dari waktu yang sama 

        # publish ke topic
        self.publisher_.publish(point_message)

def main(args=None):
    rclpy.init(args=args)
    point_publisher = Point_Pub()

    rclpy.spin(point_publisher)

    point_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()